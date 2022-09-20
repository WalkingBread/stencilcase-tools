from PIL import Image as PillowImage
from PIL import ImageFilter, ImageOps
from color import Color, colors

DEFAULT_IMAGE_SIZE = (600, 600)

class Image:
    def __init__(self, path=None, size=None, pillow_image=None):
        self.path = path
        if path != None:
            self.raw_image = PillowImage.open(path)
            self.raw_image = self.raw_image.convert('RGBA')
        else:
            self.raw_image = PillowImage.new('RGBA', DEFAULT_IMAGE_SIZE, colors.BLANK)
        if size != None:
            self.raw_image = self.raw_image.resize(size)
        if pillow_image != None:
            self.raw_image = pillow_image
        
    def resize(self, new_size):
        resized = self.raw_image.resize(new_size)
        return Image(pillow_image=resized)

    def resize_with_prop(self, height):
        w, h = self.get_size()
        prop = height / h
        width = int(prop * w)
        return self.resize((width, height))

    def paste_image(self, image, position=(0, 0)):
        return Image(pillow_image=self.raw_image.paste(image, position))

    def get_size(self):
        return self.raw_image.size

    def get_pixel_color(self, position):
        return Color(self.raw_image.getpixel(position))

    def set_pixel_color(self, position, color):
        self.raw_image.putpixel(position, color.get_values())

    def copy(self):
        copy = Image(size=self.get_size())
        copy.paste_image(self.raw_image)
        return copy

    def convert_to_grayscale(self):
        return Image(pillow_image=self.raw_image.convert('L'))

    def convert_to_rgb(self):
        return Image(pillow_image=self.raw_image.convert('RGB'))

    def invert_colors(self):
        return Image(pillow_image=ImageOps.invert(self.raw_image))

    def get_edges(self):
        return Image(pillow_image=self.raw_image.filter(ImageFilter.FIND_EDGES))

    def smoothen(self):
        smoothened = self.raw_image.filter(ImageFilter.SMOOTH)
        smoothened = self.raw_image.filter(ImageFilter.SMOOTH_MORE)
        return Image(pillow_image=smoothened)

    def save(self, path):
        ext = path.rsplit('.', 1)[1].lower()
        if ext == 'png':
            self.raw_image.save(path)
        elif ext == 'jpg':
            jpg = PillowImage.new('RGB', self.raw_image.size)
            jpg.paste(self.raw_image)
            jpg.save(path)
    