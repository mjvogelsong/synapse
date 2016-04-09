class Unit(object):
    def __init__(self, value, grad):
        self.value = value
        self.grad = grad

    def __str__(self):
        return str(self.__dict__)
