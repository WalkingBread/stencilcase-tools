from enum import Enum
from PIL import Image, ImageFilter, ImageOps

BLANK_COLOR = (0, 0, 0, 0)
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

class Layer:
    def __init__(self, size=None, image=None):
        if image == None:
            if size == None:
                size = DEFAULT_LAYER_SIZE

            self.layer_image = Image.new('RGBA', size, BLANK_COLOR)
        else:
            if size != None:
                image = image.resize(size)
            self.layer_image = image

    def get_size(self):
        return self.layer_image.size

    def paste_image(self, image, position):
        self.layer_image.paste(image, position)

    def get_pixel_color(self, position):
        pixels = self.layer_image.load()
        return pixels[position]

    def set_pixel_color(self, position, color):
        pixels = self.layer_image.load()
        pixels[position] = color

    def extract_color_to_layer(self, color):
        new_layer = Layer(size=self.get_size())
        width, height = self.get_size()
        for x in range(width):
            for y in range(height):
                position = (x, y)
                if self.get_pixel_color(position) == color:
                    new_layer.set_pixel_color(position, color)
        return new_layer

    def get_grayscale_to_layer(self):
        grayscale_image = self.layer_image.convert('L')
        return Layer(image=grayscale_image)

    def get_edges_to_layer(self):
        grayscale_image = self.layer_image.convert('L')
        image_with_edges = grayscale_image.filter(ImageFilter.FIND_EDGES)
        image_with_edges = ImageOps.invert(image_with_edges)
        return Layer(image=image_with_edges)

    def divide(self):
        pass

    def save(self, path):
        self.layer_image.save(path)