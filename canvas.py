from enum import Enum
from PIL import Image, ImageFilter, ImageOps

BLANK_COLOR = (0, 0, 0, 0)
WHITE_COLOR = (255, 255, 255, 255)
BLACK_COLOR = (0, 0, 0, 255)

DEFAULT_LAYER_SIZE = (600, 600)

class Format(Enum):
    A0 = (14043, 9933),
    A1 = (9933, 7016),
    A2 = (7016, 4961),
    A3 = (4961, 3508),
    A4 = (3508, 2480),
    A5 = (2480, 1748),
    A6 = (1748, 1240),
    HD = (1280, 720),
    FULL_HD = (1920, 1080)

def reinforce_edge(image_with_edges):
    pass

def get_color_brightness(color):
    r = color[0]
    g = color[1]
    b = color[2]
    return (r + g + b) / 3

def get_shade(color, value):
    r = color[0] + value
    if r < 0:
        r = 0
    elif r > 255:
        r = 255
    g = color[1] + value
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    b = color[2] + value
    if b < 0:
        b = 0
    elif b > 255:
        b = 255
    if len(color) == 3:
        return (r, g, b)
    return (r, g, b, color[3])

def create_blank_image(size):
    return Image.new('RGBA', size, BLANK_COLOR)

def modify_pixels(image, new_image, operation, operation_args):
    img = image.load()
    width, height = image.size
    for x in range(width):
        for y in range(height):
            position = (x, y)
            operation(image, new_image, position, operation_args)
    return new_image

def extract_color(image, new_image, position, operation_args):
    color = operation_args['color']
    if image.getpixel(position) == color:
        new_image.putpixel(position, color)

def remove_datails(image, new_image, position, operation_args):
    colors = []
    x, y = position
    w, h = image.size
    for _x in range(x - 1, x + 2):
        if _x > 0 and _x < w - 1:
            for _y in range(y - 1, y + 2):
                if (_y > 0 and _y < h - 1) and (x != _x or y != _y):
                    colors.append(image.getpixel((_x, _y)))
    dominant_color = max(set(colors), key=colors.count)
    new_image.putpixel(position, dominant_color)

def limit_colors(image, new_image, position, operation_args):
    palette = operation_args['palette']
    color_number = len(palette)
    color_threshold = int(255 / color_number)
    color = image.getpixel(position)
    brightness = get_color_brightness(color)
    color_level = int(brightness / color_threshold)
    new_color = palette[color_level]
    new_image.putpixel(position, new_color)

class Layer:
    def __init__(self, size=None, image=None):
        if image == None:
            if size == None:
                size = DEFAULT_LAYER_SIZE

            self.layer_image = create_blank_image(size)
        else:
            if size != None:
                image = image.resize(size)
            self.layer_image = image

    def get_size(self):
        return self.layer_image.size

    def paste_image(self, image, position):
        self.layer_image.paste(image, position)

    def get_pixel_color(self, position):
        return self.layer_image.getpixel(position)

    def set_pixel_color(self, position, color):
        self.layer_image.putpixel(position, color)

    def extract_color(self, color):
        new_img = create_blank_image(self.layer_image.size)
        img = modify_pixels(self.layer_image, new_img, extract_color, {'color': color})
        return Layer(image=img)

    def get_grayscale(self):
        grayscale_image = self.layer_image.convert('L')
        return Layer(image=grayscale_image)

    def get_edges(self):
        grayscale_image = self.layer_image.convert('L')
        image_with_edges = grayscale_image.filter(ImageFilter.FIND_EDGES)
        image_with_edges = ImageOps.invert(image_with_edges)
        image_with_edges = image_with_edges.convert('RGB')
        return Layer(image=image_with_edges)

    def divide(self):
        pass

    def limit_colors(self, palette):
        new_img = create_blank_image(self.layer_image.size)
        limited = modify_pixels(self.layer_image, new_img, limit_colors, {'palette': palette})
        new_img = limited.copy()
        limited = modify_pixels(limited, new_img, remove_datails, {})
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
        ext = path.rsplit('.', 1)[1].lower()
        print(ext)
        if ext == 'png':
            self.layer_image.save(path)
        elif ext == 'jpg':
            jpg = Image.new('RGB', self.layer_image.size)
            jpg.paste(self.layer_image)
            jpg.save(path)