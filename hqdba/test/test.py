class Box1():
    def __init__(self, lenght1, width1, height1):
        self.length = lenght1
        self.width = width1
        self.height = height1

    def volume(self):
        return self.length * self.width * self.height

mybox = Box1(10, 10, 10)
print(mybox.volume())