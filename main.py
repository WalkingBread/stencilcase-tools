from canvas import Layer
from PIL import Image


if __name__ == '__main__':
    img = Image.open('samples/walter.jpg')
    pixels = img.load()
    layer = Layer(image=img)
    layer = layer.limit_colors([(0, 0, 0, 255), (100, 100, 100, 255), (255, 255, 255, 255)])
    layer1 = layer.extract_color((0, 0, 0, 255))
    layer2 = layer.extract_color((100, 100, 100, 255))
    layer3 = layer.extract_color((255, 255, 255, 255))
    #layer = layer.get_edges()
    layer1.save('samples/woman1.png')
    layer2.save('samples/woman2.png')
    layer3.save('samples/woman3.png')