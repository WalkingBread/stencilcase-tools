from canvas import Layer
from image import Image
from color import Color

if __name__ == '__main__':
    img = Image('samples/sea.png')
    layer = Layer(image=img)
    layer = layer.get_edges()
    layer.save('samples/seaedge.png')
