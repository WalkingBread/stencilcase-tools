from canvas import Layer
from image import Image
from color import Color

if __name__ == '__main__':
    img = Image('samples/walter.jpg')
    layer = Layer(image=img)
    layer = layer.limit_colors([Color((222, 122, 204, 255)), Color((108, 96, 171, 255)), Color((96, 66, 245, 255)), Color((26, 18, 66, 255))])
    layer.save('samples/walter1.png')
    layer = layer.get_edges()
