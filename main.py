from canvas import Layer
from image import Image
from color import Color

if __name__ == '__main__':
    img = Image('../pig.png')
    layer = Layer(image=img)
    layer = layer.extract_color(Color((0, 0, 0, 255)))
    layer.save('samples/sea1.png')
