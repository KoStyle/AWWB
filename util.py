IMG = "files/imagen"
ARPIOS = "files/pickle_harpies"
OBJETOS = 'files/piclke_weapons'
STATUS = 'files/pickle_status'
TXT = '.txt'
PNG = '.png'
FONT = "files/font.ttf"
CAFE = 'files/cafes.txt'
NA = 'NA'
TOKENS = 'tokens'
ACCESS_TOKENS_DIC = {'CONSUMER_KEY': NA, 'CONSUMER_SECRET': NA, 'ACCESS_KEY': NA, 'ACCESS_SECRET': NA}


def print_status_harpies(lista):
    for index in range(len(lista)):
        print(lista[index].name + '-' + str(lista[index].isAlive) + '-' + str(lista[index].kills))


def read_file(file):
    lista = []
    f = open(file, 'r', encoding='latin1')
    line = f.readline()
    while line:
        lista.append(line.strip())
        line = f.readline()
    return lista


def get_survivors(listar):
    listatmp = []
    for index in range(len(listar)):
        if listar[index].isAlive:
            listatmp.append(listar[index])
    return listatmp


def get_corpses(harpies):
    corpses = []
    for index in range(len(harpies)):
        if not harpies[index].isAlive:
            corpses.append(harpies[index])
    return corpses


def read_tokens(file):
    f = open(file, 'r', encoding='latin1')
    line = f.readline()
    while line:
        tokenized = line.split('=')
        if ACCESS_TOKENS_DIC.get(tokenized[0].strip()) is None and len(tokenized) == 2:
            ACCESS_TOKENS_DIC[tokenized[0].strip()] = tokenized[1].strip()
        line = f.readline()
    return
