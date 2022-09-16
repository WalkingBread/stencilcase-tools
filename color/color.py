class Color:
    def __init__(self, color):
        self.r = color[0]
        self.g = color[1]
        self.b = color[2]
        self.a = None
        if len(color) == 4:
            self.a = color[3]

    def get_brightness(self):
        return (self.r + self.g + self.b) / 3

    def get_values(self):
        return(self.r, self.g, self.b, self.a)
    
    def get_shade(self, value):
        r = self.r + value
        if r < 0:
            r = 0
        elif r > 255:
            r = 255
        g = self.g + value
        if g < 0:
            g = 0
        elif g > 255:
            g = 255
        b = self.b + value
        if b < 0:
            b = 0
        elif b > 255:
            b = 255
        if self.a == None:
            return (r, g, b)
        return Color((r, g, b, self.a))