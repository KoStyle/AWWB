def loadPickle(file):
    f = open(file, 'rb')
    listaObj = pickle.load(f)
    f.close()
    return listaObj


def savePickle(file, obj):
    f = open(file, 'wb')
    pickle.dump(obj, f)
    f.close()

def readArpios(file):
    lista = []
    f = open(file, 'r', encoding='latin1')
    line = f.readline()
    while line:
        lista.append(Arpio(line.strip()))
        line = f.readline()
    cantidad = len(lista)
    for i in range(len(lista)):
        lista[i].percKill = 1. / cantidad

    lista.sort(key=lambda x: x.name)
    return lista

def printStatusArpios(lista):
    for index in range(len(lista)):
        print(lista[index].name + '-' + str(lista[index].isAlive) + '-' + str(lista[index].kills))

def readList(file):
    lista = []
    f = open(file, 'r', encoding='latin1')
    line = f.readline()
    while line:
        lista.append(line.strip())
        line = f.readline()

    return lista

def getSurvivors(listar):
    listatmp = []
    tweet = ''
    for index in range(len(listar)):
        if listar[index].isAlive:
            listatmp.append(listar[index])
    return listatmp

def readTokens(file):
    f = open(file, 'r', encoding='latin1')
    line = f.readline()
    while line:
        tokenized = line.split('=')
        if ACCESS_TOKENS_DIC.get(tokenized[0].strip()) is None and len(tokenized) == 2:
            ACCESS_TOKENS_DIC[tokenized[0].strip()] = tokenized[1].strip()
        line = f.readline()
    return
