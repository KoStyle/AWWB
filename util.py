import pickle

from classes import Arpio

IMG = "imagen"
ARPIOS = "fichero"
OBJETOS = 'ficheroObj'
STATUS = 'status'
TXT = '.txt'
PNG = '.png'
FONT = "font.ttf"
CAFE = 'cafes.txt'
NA = 'NA'
TOKENS = 'tokens'
ACCESS_TOKENS_DIC = {'CONSUMER_KEY': NA, 'CONSUMER_SECRET': NA, 'ACCESS_KEY': NA, 'ACCESS_SECRET': NA}


def load_pickle(file):
    f = open(file, 'rb')
    listaObj = pickle.load(f)
    f.close()
    return listaObj


def save_pickle(file, obj):
    f = open(file, 'wb')
    pickle.dump(obj, f)
    f.close()


def read_harpies(file):
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
