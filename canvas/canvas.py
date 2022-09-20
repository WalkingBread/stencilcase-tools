from image import Image
from canvas.format import Format
from color import Color

DEFAULT_LAYER_SIZE = (600, 600)

def reinforce_edge(image_with_edges):
    pass

def get_neighbour_pixel_colors(image, position):
    neighbour_colors = []
    x, y = position
    w, h = image.get_size()
    for _x in range(x - 1, x + 2):
        if _x > 0 and _x < w - 1:
            for _y in range(y - 1, y + 2):
                if (_y > 0 and _y < h - 1) and (x != _x or y != _y):
                    neighbour_colors.append(image.get_pixel_color((_x, _y)))
    return neighbour_colors

def modify_pixels(image, new_image, operation, operation_args):
    width, height = image.get_size()
    for x in range(width):
        for y in range(height):
            position = (x, y)
            operation(image, new_image, position, operation_args)
    return new_image

def extract_color(image, new_image, position, operation_args):
    color = operation_args['color']
    if image.get_pixel_color(position) == color:
        new_image.set_pixel_color(position, color)

def remove_artifacts(image, new_image, position, operation_args):
    neighbour_colors = get_neighbour_pixel_colors(image, position)
    dominant_color = max(set(neighbour_colors), key=neighbour_colors.count)
    new_image.set_pixel_color(position, dominant_color)

def limit_colors(image, new_image, position, operation_args):
    palette = operation_args['palette']
    color_number = len(palette)
    color_threshold = int(255 / color_number)
    color = image.get_pixel_color(position)
    brightness = color.get_brightness()
    color_level = int(brightness / color_threshold) - 1
    new_color = palette[color_level]
    new_image.set_pixel_color(position, new_color)

class Layer:
    def __init__(self, size=None, image=None):
        if image == None:
            if size == None:
                size = DEFAULT_LAYER_SIZE

            self.layer_image = Image(size=size)
        else:
            if size != None:
                image = image.resize(size)
            self.layer_image = image

    def get_size(self):
        return self.layer_image.get_size()

    def paste_image(self, image, position):
        self.layer_image.paste_image(image, position)

    def get_pixel_color(self, position):
        return self.layer_image.get_pixel_color(position)

    def set_pixel_color(self, position, color):
        self.layer_image.set_pixel_color(position, color)

    def extract_color(self, color):
        new_img = Image(size=self.layer_image.get_size())
        img = modify_pixels(self.layer_image, new_img, extract_color, {'color': color})
        return Layer(image=img)

    def get_grayscale(self):
        grayscale_image = self.layer_image.convert_to_grayscale()
        return Layer(image=grayscale_image)

    def get_edges(self):
        grayscale_image = self.layer_image.convert_to_grayscale()
        image_with_edges = grayscale_image.get_edges()
        image_with_edges = image_with_edges.invert_colors()
        image_with_edges = image_with_edges.convert_to_rgb()
        return Layer(image=image_with_edges)

    def divide(self):
        pass

    def limit_colors(self, palette):
        limited = self.layer_image.smoothen()
        new_img = Image(size=self.layer_image.get_size())
        limited = modify_pixels(limited, new_img, limit_colors, {'palette': palette})
        new_img = limited.copy()
        limited = modify_pixels(limited, new_img, remove_artifacts, {})
        return Layer(image=limited)
    
    def resize(self, new_size):
        return Layer(image=self.layer_image.resize(new_size))

    def resize_with_prop(self, height):
        w, h = self.get_size()
        prop = height / h
        width = int(prop * w)
        return self.resize((width, height))

    def copy(self):
        return Layer(image=self.layer_image)

    def save(self, path):
        self.layer_image.save(path)