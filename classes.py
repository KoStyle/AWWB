import pickle

from constants import *


class Arpio:
    def __init__(self, name):
        self.name = name
        self.percKill = float(0.7)
        self.percVictim = float(0.7)
        self.isAlive = True
        self.kills = int(0)

    @staticmethod
    def harpy_factory(file):
        lista = []
        f = open(file, 'r', encoding='latin1')
        line = f.readline()
        while line:
            lista.append(Arpio(line.strip()))
            line = f.readline()
        cantidad = len(lista)
        for i in range(len(lista)):
            lista[i].percKill = 1. / cantidad
            lista[i].percVictim = 1. / cantidad

        lista.sort(key=lambda x: x.name)
        return lista

    @staticmethod
    def print_status_harpies(lista):
        for index in range(len(lista)):
            print(lista[index].name + '-' + str(lista[index].isAlive) + '-' + str(lista[index].kills))


class Status:
    def __init__(self):
        self.kills = int(0)
        self.year = int(2019)
        self.alive = int(0)
        self.omedetoo = False
        self.winner = Arpio('N/A')


class InputKun:

    @staticmethod
    def read_file(file):
        lista = []
        f = open(file, 'r', encoding='latin1')
        line = f.readline()
        while line:
            lista.append(line.strip())
            line = f.readline()
        return lista

    @staticmethod
    def read_tokens(file):
        f = open(file, 'r', encoding='latin1')
        line = f.readline()
        while line:
            tokenized = line.split('=')
            if ACCESS_TOKENS_DIC.get(tokenized[0].strip()) is None and len(tokenized) == 2:
                ACCESS_TOKENS_DIC[tokenized[0].strip()] = tokenized[1].strip()
            line = f.readline()
        return

    @staticmethod
    def load_pickle(file):
        f = open(file, 'rb')
        listaObj = pickle.load(f)
        f.close()
        return listaObj

    @staticmethod
    def save_pickle(file, obj):
        f = open(file, 'wb')
        pickle.dump(obj, f)
        f.close()
