class TSNodo:
    """description of class"""
    def __init__(self, lexsema, valor, tipo):
        self.lexsema = lexsema
        self.valor = valor
        self.tipo = tipo
        self.next = None
        self.prev = None

    def PrintTable(self):
        TSNode = self  # start from the head node
        print(" lexema | valor |  tipo/token ")
        while TSNode != None:
            print(TSNode.lexsema,"|", TSNode.valor,"|", TSNode.tipo)
            TSNode = TSNode.next  # move on to the next nod


