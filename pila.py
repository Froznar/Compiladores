class pila(object):
    """description of class"""
    def __init__(self):
        self.items = []
    def estaVacia(self):
        return self.items == []

    def xpush(self, item):
        self.items.insert(0,item)

    def xpop(self):
        return self.items.pop(0)

    def last(self):
        return self.items[0]

    def xlen(self):
        return len(self.items)


