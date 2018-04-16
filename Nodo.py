

class Nodo:
    """description of class"""    
    def __init__(self, token, lexsema, linea):
        self.token = token
        self.lexsema = lexsema
        self.linea = linea
        self.next = None
        self.prev = None

    def PrintLista(self):
        node = self  # start from the head node
        while node != None:
            print("token: ", node.token)
            print("lexema: ", node.lexsema)
            print("linea: ", node.linea)
            print("--------")
            node = node.next  # move on to the next nod



