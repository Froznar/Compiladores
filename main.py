import re
from Nodo import Nodo
from TSNodo import TSNodo

TOKENS = (
    ('P_SELECT', re.compile('SELECT|select')),
    ('P_INSER', re.compile('INSERT|insert')),
    ('P_UPDATE', re.compile('UPDATE|update')),
    ('P_DELETE', re.compile('DELETE|delete')),
    ('P_FROM', re.compile('FROM|from')),
    ('P_WHERE', re.compile('WHERE|where')),
    ('P_INTO', re.compile('INTO|into')),
    ('P_VALUES', re.compile('VALUES|values')),
    ('P_ON', re.compile('ON|on')),
    ('P_IN', re.compile('IN|in')),
    ('P_INER', re.compile('INER|iner')),
    ('P_LEFT', re.compile('LEFT|left')),
    ('P_RIGHT', re.compile('RIGHT|right')),
    ('T_INT', re.compile('INTEGER|integer')),
    ('S_ASTER', re.compile('\*')),
    ('S_COMA', re.compile(',')),
    ('S_PUNTO', re.compile('\.')),
    ('OP_RELA', re.compile('=|<|>|<=|>=|<>')),
    ('OP_ARIT', re.compile('\+|-|/|%')),
    ('NUMB', re.compile('[0-9]+')),
    ('VAR', re.compile('[a-zA-Z0-9]+$'))
)

def main():

    # Simbolos que separar
    hay_coma = re.compile('.*,')
    hay_punto = re.compile('.*\.')
    hay_igual = re.compile('.*=|.*<|.*>|.*<=|.*>=|.*<>')



    data = open('D:\Francisco\python proyects\Compiladores\Archivos\Refined.txt')
    palabras = []
    linea = []

    #tokenisador quitando espacios y colocando lineas
    l = 1;
    for line in data:
        for word in line.split():
            palabras.append(word)
            linea.append(l)
            print(word)
        l = l+1

    palabras2 = []
    linea2 = []
    for i in range(0,len(palabras)):
        l = linea[i];
        if hay_coma.match(palabras[i]):
            cont = 0
            single = 0
            for j in palabras[i].split(","):
                if j != '':
                    palabras2.append(j)
                    linea2.append(l)
                    cont +=1
                    if cont < len(palabras[i].split(",")):
                        palabras2.append(",")
                        linea2.append(l)
                elif single == 0:
                    single = single + 1
                    palabras2.append(",")
                    linea2.append(l)
        else:
            palabras2.append(palabras[i])
            linea2.append(l)


    palabras3 = []
    linea3 = []
    for i in range(0, len(palabras2)):
        l = linea2[i];
        if hay_punto.match(palabras2[i]):
            cont = 0
            for j in palabras2[i].split("."):
                palabras3.append(j)
                linea3.append(l)
                cont += 1
                if cont < len(palabras2[i].split(".")):
                    palabras3.append(".")
                    linea3.append(l)
        else:
            palabras3.append(palabras2[i])
            linea3.append(l)

    palabras4 = palabras3
    linea4 = linea3
    op_relacionales = ("=","<",">","<=",">=","<>")

    for op in op_relacionales:
        p4=[]
        l4=[]
        for i in range(0, len(palabras4)):
            l = linea4[i];
            if hay_igual.match(palabras4[i]):
                cont = 0
                single = 0
                for j in palabras4[i].split(op):
                    if j != '':
                        p4.append(j)
                        l4.append(l)
                        cont += 1
                        if cont < len(palabras4[i].split(op)):
                            p4.append(op)
                            l4.append(l)
                    elif single == 0:
                        single = single + 1
                        p4.append(op)
                        l4.append(l)

            else:
                p4.append(palabras4[i])
                l4.append(l)
        palabras4 = p4
        linea4 = l4

    iterador = Nodo("inicio","inicio",0)
    tnode = TSNodo("inicio", "inicio", 0)
    TablaSimbolos = tnode
    Lista = iterador
    #only one in varialbles
    variables = []
    #creador de la lista y TS
    for lex in range(0,len(palabras4)):
        lexema = palabras4[lex]
        linea = linea4[lex]
        error = False
        for exp in TOKENS:
            patron = exp[1]
            if patron.match(lexema):
                iter = Nodo(exp[0], lexema, linea)
                if exp[0] == "VAR" and lexema not in variables:
                    variables.append(lexema)
                    tsiter = TSNodo(lexema," ",exp[0])
                    tnode.next = tsiter
                    tnode = tsiter
                iterador.next = iter
                iterador = iter
                error = False
                break
            else:
                error = True
        if error == True:
            print("ERROR: valor >> ", lexema, " << no encontrado")


    Lista.PrintLista()
    TablaSimbolos.PrintTable()

    stest = "="
    print( stest.split("="))


if __name__ == '__main__':

    # PREPROSESAMINETO
    refined = open('D:\Francisco\python proyects\Compiladores\Archivos\Refined.txt', "w")

    with open('D:\Francisco\python proyects\Compiladores\Archivos\Sentencias.txt') as fileobj:
        bigcomment = False
        bc = 0
        lastline = False
        for line in fileobj:
            comment = False
            endoffile = False
            for ch in range(0, len(line)-1):
                a = line[ch]
                b = line[ch + 1]
                bc = bc + 1
                if a == '/' and b == '*':
                    bigcomment = True
                if a == '*' and b == '/':
                    bigcomment = False
                    bc = -2
                if a == '-' and b == '-':
                    break
                if comment == False and bigcomment == False and bc >= 0:
                    refined.write(a)
                if ch == len(line)-2:
                    refined.write(b)
                    endoffile = True
            if not endoffile:
                refined.write('\n')

    refined.close()

    main()