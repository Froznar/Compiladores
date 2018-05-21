import re
from Nodo import Nodo
from TSNodo import TSNodo
from pila import pila

TOKENS = (
    ('P_SELECT', re.compile('SELECT|select')),
    ('P_INSERT', re.compile('INSERT|insert')),
    ('P_UPDATE', re.compile('UPDATE|update')),
    ('P_DELETE', re.compile('DELETE|delete')),
    ('P_FROM', re.compile('FROM|from')),
    ('P_WHERE', re.compile('WHERE|where')),
    ('P_INTO', re.compile('INTO|into')),
    ('P_VALUES', re.compile('VALUES|values')),
    ('P_SET', re.compile('SET|set')),
    ('P_ON', re.compile('ON|on')),
    ('P_IN', re.compile('IN|in')),
    ('P_JOIN', re.compile('JOIN|join')),
    ('P_INNER', re.compile('INER|iner')),
##    ('P_LEFT', re.compile('LEFT|left')),
##    ('P_RIGHT', re.compile('RIGHT|right')),
##    ('P_HAVING', re.compile('HAVING|having')),
##    ('P_GROUP_BY', re.compile('GROUP BY|group by')),
    ('S_ASTER', re.compile('\*')),
    ('S_COMA', re.compile(',')),
    ('S_PUNTO', re.compile('\.')),
    ('S_P_AB', re.compile('\(')),
    ('S_P_CE', re.compile('\)')),
    ('OP_AND', re.compile('AND|and')),
    ('OP_OR', re.compile('OR|or')),
    ('OP_NOT', re.compile('NOT|not')),
    ('OP_RELA', re.compile('=|<|>|<=|>=|<>')),
    ('OP_ARIT', re.compile('\+|-|/|%')),
    ('NUMB_FLOAT', re.compile('[0-9]+.[0-9]+')),
    ('NUMB_INT', re.compile('[0-9]+')),
    ('CHAR', re.compile('"[a-zA-Z0-9]+"')),
    ('VAR', re.compile('[a-zA-Z0-9]+$'))
)
## count average and sum

TABLA_SINTACTICA = (
    ('@'    , 'P_SELECT'   , 'P_INSERT'                                   , 'P_UPDATE'             , 'P_DELETE'           , 'P_WHERE'  , 'P_FROM'     , 'P_INTO'    , 'VALUES'   , 'P_SET'  , 'P_ON'    , 'P_JOIN'     , 'P_INNER'                 , 'OP_RELA' , 'OP_NOT'      , 'OP_AND'     , 'OP_OR'     , 'S_COMA'    , 'S_ASTER'         ,'S_PUNTO'          ,'S_P_AB'      ,'S_P_CE'            ,   'VAR'            , 'NUMB_FLOAT'      ,'NUMB_INT'          ,'CHAR'              , '$'),
    ('S'    , 'A'          ,'P'                                           ,'U'                     ,'T'                   ,''          ,''            ,''           ,''          ,''        ,''         ,''            ,''                         ,''         ,''             ,''            ,''           ,''           ,''                 ,''                 ,''            ,''                  ,''                  ,''                 ,''                  ,''                  ,''  ),
    ('A'    , 'C B'        ,''                                            ,''                      ,''                    ,''          ,''            ,''           ,''          ,''        ,''         ,''            ,''                         ,''         ,''             ,''            ,''           ,''           ,''                 ,''                 ,''            ,''                  ,''                  ,''                 ,''                  ,''                  ,''  ),
    ('B'    , ''           ,''                                            ,''                      ,''                    ,     'E'    ,''            ,''           ,''          ,''        ,''         ,''            ,'X'                        ,''         ,''             ,''            ,''           ,''           ,''                 ,''                 ,''            ,''                  ,''                  ,''                 ,''                  ,''                  ,''  ),
    ('C'    , 'P_SELECT D' ,''                                            ,''                      ,''                    ,''          ,''            ,''           ,''          ,''        ,''         ,''            ,''                         ,''         ,''             ,''            ,''           ,''           ,''                 ,''                 ,''            ,''                  ,''                  ,''                 ,''                  ,''                  ,''  ),
    ('D'    , ''           ,''                                            ,''                      ,''                    ,''          ,''            ,''           ,''          ,''        ,''         ,''            ,''                         ,''         ,''             ,''            ,''           ,''           ,'S_ASTER P_FROM I' ,''                 ,''            ,''                  ,'J P_FROM I'        ,''                 ,''                  ,''                  ,''  ),
    ('E'    , ''           ,''                                            ,''                      ,''                    ,'P_WHERE F' ,''            ,''           ,''          ,''        ,''         ,''            ,''                         ,''         ,''             ,''            ,''           ,''           ,''                 ,''                 ,''            ,''                  ,''                  ,''                 ,''                  ,''                  ,''  ),
    ('F'    , ''           ,''                                            ,''                      ,''                    ,''          ,''            ,''           ,''          ,''        ,''         ,''            ,''                         ,''         ,'OP_NOT F H'   ,''            ,''           ,''           ,''                 ,''                 ,''            ,''                  ,'J OP_RELA G H'     ,'G OP_RELA J H'    ,'G OP_RELA J H'     ,'G OP_RELA J H'     ,''  ),
    ('G'    , ''           ,''                                            ,''                      ,''                    ,''          ,''            ,''           ,''          ,''        ,''         ,''            ,''                         ,''         ,''             ,''            ,''           ,''           ,''                 ,''                 ,''            ,''                  ,''                  ,'N'                ,'N'                 ,'CHAR'              ,''  ),
    ('H'    , ''           ,''                                            ,''                      ,''                    ,''          ,''            ,''           ,''          ,''        ,''         , ''           ,''                         ,''         ,''             ,'AND F'       ,'OR F'       ,''           ,''                 ,''                 ,''            ,''                  ,''                  ,''                 ,''                  ,''                  ,'vacio'  ),
    ('I'    , ''           ,''                                            ,''                      ,''                    ,''          ,''            ,''           ,''          ,''        ,''         , ''           , ''                        ,''         ,''             ,''            ,''           ,''           ,''                 ,''                 ,''            ,''                  ,'VAR'               ,''                 ,''                  ,''                  ,'vacio'  ),
    ('J'    , ''           ,''                                            ,''                      ,''                    ,''          ,''            ,''           ,''          ,''        ,''         , ''           ,''                         ,''         ,''             ,''            ,''           ,''           ,''                 ,''                 ,''            ,''                  ,'VAR K'            ,''                 ,''                  ,''                  ,''  ),
    ('K'    , ''           ,''                                            ,''                      ,''                    ,''          ,'vacio'       ,''           ,''          ,''        ,''         , ''           ,''                         ,'vacio'    ,''             ,''            ,''           ,'vacio'      ,''                 ,'S_PUNTO VAR'      ,''            ,''                  ,''                  ,''                 ,''                  ,''                  ,'vacio'  ),
    ('L'    , ''           ,''                                            ,''                      ,''                    ,''          ,''            ,''           ,''          ,''        ,''         , ''           ,''                         ,''         ,''             ,''            ,''           ,''           ,''                 ,''                 ,''            ,''                  ,'J M  '             ,''                 ,''                  ,''                  ,''  ),
    ('M'    , ''           ,''                                            ,''                      ,''                    ,''          ,''            ,''           ,''          ,''        ,''         , ''           ,''                         ,''         ,''             ,''            ,''           ,'S_COMA L'   ,''                 ,''                 ,''            ,''                  ,''                  ,''                 ,''                  ,''                  ,''  ),
    ('N'    , ''           ,''                                            ,''                      ,''                    ,''          ,''            ,''           ,''          ,''        ,''         ,''            ,''                         ,''         ,''             ,''            ,''           ,''           ,''                 ,''                 ,''            ,''                  ,''                  ,'NUM_FLOAT'        ,'NUM_INT'           ,''                  ,''  ),
    ('O'    , ''           ,''                                            ,''                      ,''                    ,''          ,''            ,''           ,''          ,''        ,''         ,''            ,''                         ,''         ,''             ,''            ,''           ,''           ,''                 ,''                 ,''            ,''                  ,''                  ,'NUM_FLOAT'        ,'NUM_INT'           ,'CHAR'              ,''  ),
    ('P'    , ''           ,'P_INSERT P_INTO I P_VALUES S_P_AB Q S_P_CE'  ,''                      ,''                    ,''          ,''            ,''           ,''          ,''        ,''         ,''            ,''                         ,''         ,''             ,''            ,''           ,''           ,''                 ,''                 ,''            ,''                  ,''                  ,'O R'              ,'O R'               ,'O R'               ,''  ),
    ('Q'    , ''           ,''                                            ,''                      ,''                    ,''          ,''            ,''           ,''          ,''        ,''         ,''            ,''                         ,''         ,''             ,''            ,''           ,''           ,''                 ,''                 ,''            ,''                  ,''                  ,''                 ,''                  ,''                  ,''  ),
    ('R'    , ''           ,''                                            ,''                      ,''                    ,''          ,''            ,''           ,''          ,''        ,''         ,''            ,''                         ,''         ,''             ,''            ,''           ,'S_COMA Q'   ,''                 ,''                 ,''            ,''                  ,''                  ,''                 ,''                  ,''                  ,''  ),
    ('T'    , ''           ,''                                            ,''                      ,'P_DELETE P_FROM I E' ,''          ,''            ,''           ,''          ,''        ,''         ,''            ,''                         ,''         ,''             ,''            ,''           ,''           ,''                 ,''                 ,''            ,''                  ,''                  ,''                 ,''                  ,''                  ,''  ),
    ('U'    , ''           ,''                                            ,'P_UPDATE I P_SET V E'  ,''                    ,''          ,''            ,''           ,''          ,''        ,''         ,''            ,''                         ,''         ,''             ,''            ,''           ,''           ,''                 ,''                 ,''            ,''                  ,''                  ,''                 ,''                  ,''                  ,''  ),
    ('V'    , ''           ,''                                            ,''                      ,''                    ,''          ,''            ,''           ,''          ,''        ,''         ,''            ,''                         ,''         ,''             ,''            ,''           ,''           ,''                 ,''                 ,''            ,''                  ,'VT OP_RELA O W'    ,''                 ,''                  ,''                  ,''  ),
    ('W'    , ''           ,''                                            ,''                      ,''                    ,''          ,''            ,''           ,''          ,''        ,''         ,''            ,''                         ,''         ,''             ,''            ,''           ,'S_COMA V'   ,''                 ,''                 ,''            ,''                  ,''                  ,''                 ,''                  ,''                  ,''  ),
    ('X'    , ''           ,''                                            ,''                      ,''                    ,''          ,''            ,''           ,''          ,''        ,''         ,''            ,'P_INNER P_JOIN I P_ON F'  ,''         ,''             ,''            ,''           ,''           ,''                 ,''                 ,''            ,''                  ,''                  ,''                 ,''                  ,''                  ,''  ),
)

end = False

def locate_in_table(nt,t):    
    posx=0
    posy=0
    k=0
    for x in TABLA_SINTACTICA[0]:
        if t == x:            
            posx=k
            break
        k=k+1
    k=0
    for i in TABLA_SINTACTICA:
        if nt == i[0]:
            posy=k
        k=k+1

    if TABLA_SINTACTICA[posy][posx] == '':
        return 'ERROR'
    else:
        return TABLA_SINTACTICA[posy][posx]

id = 0
acceptar = False
def add_in_pila(express, mistokens, xpila, noterminal):    
    global id
    if id < len(mistokens) :
        print('ELEMENTO ',express)
        for s in express.split(' '):
            xpila.xpush(s)
            if not xpila.estaVacia():
                if (s=='ERROR'):
                    print('Error de sintaxis en el token: ', mistokens[id])
                    id = id + 1
                elif len(s) == 1:
                    express = locate_in_table(s,mistokens[id])
                    xpila.xpop()
                    add_in_pila(express, mistokens, xpila, s)
                elif xpila.last() == 'vacio':
                    if(s== '$'):
                        acceptar = True
                        print('Finalizar')
                    print('correcto: ',xpila.xpop())
                elif xpila.last() == mistokens[id]:
                    print('correcto: ',xpila.xpop())
                    id = id+1                            
                else:
                    print('Error de sintaxis en el token: ', mistokens[id])
                    id = id+1

    


def main():

    # Simbolos que separar
    hay_coma = re.compile('.*,')
    hay_punto = re.compile('.*\.')
    hay_igual = re.compile('.*=|.*<|.*>|.*<=|.*>=|.*<>')



    data = open('Archivos/Refined.txt')
    palabras = []
    linea = []

    #tokenisador quitando espacios y colocando lineas
    l = 1;
    for line in data:
        for word in line.split():
            palabras.append(word)
            linea.append(l)
        l = l+1

    for l in palabras:
        print(l)

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
            for j in palabras2[i].split("."):#Agregar exepcion para numeros decimales
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
    for l in palabras4:
        print(l)
    #juntar elemento separados
    numbcheck = re.compile('[0-9]+')
    FinalList = []
    saltador = -1
    for i in range(0, len(palabras4)-2):
        if i > saltador:
            a = palabras4[i]
            b = palabras4[i + 1]
            c = palabras4[i + 2]
            frase = False
            endwhitfrase = False
            if numbcheck.match(a) and b == "." and numbcheck.match(c):
                FinalList.append(a+b+c)
                saltador = i+2
                frase = True
                if i == len(palabras4)-3:
                    endwhitfrase = True
            elif (a == "GROUP" and b == "BY") or (a == "group" and b == "by"):
                FinalList.append(a+' '+b)
                saltador = i+1
                frase = True
                if i == len(palabras4)-2:
                    FinalList.append(c)
                    endwhitfrase = True
            elif (a == "ORDER" and b == "BY") or (a == "order" and b == "by"):
                FinalList.append(a+' '+b)
                saltador = i+1
                frase = True
                if i == len(palabras4)-2:
                    FinalList.append(c)
                    endwhitfrase = True
            if frase == False:
                FinalList.append(a)
            if i == len(palabras4)-3 and endwhitfrase == False:
                FinalList.append(b)
                FinalList.append(c)
    for w in FinalList:
        print(w)

    continuar_sintatico = True
    iterador = Nodo("inicio","inicio",0)
    tnode = TSNodo("inicio", "inicio", 0)
    TablaSimbolos = tnode
    Lista = iterador
    #only one in varialbles
    variables = []
    palabras4 = FinalList
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
            print("ERROR en la linea: ", linea," con el valor >> ", lexema, " << no encontrado")
            continuar_sintatico = False


    Lista.PrintLista()
    TablaSimbolos.PrintTable()

    xpila = pila()

    
    x = Lista.next
    mistokens = []
    while x!=None:
        mistokens.append(x.token)
        x=x.next;
    mistokens.append('$')
    for i in mistokens:
        print(i)
    print("==============================")       

 

    if continuar_sintatico == True:
        it = Lista
        noterminal = 'S'
        it = Lista.next
        express = locate_in_table(noterminal,mistokens[0])
        if express == 'ERROR':
            print ('Error: no es posible accesar ',noterminal,' hacia ', mistokens[0])
        else:
            add_in_pila(express, mistokens, xpila, noterminal)




        





##ANALISIS SINTACTICO
if __name__ == '__main__':

    # PREPROSESAMINETO
    refined = open('Archivos/Refined.txt', "w")

    with open('Archivos/Sentencias.txt') as fileobj:
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