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

    def __adjust_attribute__(self, att_name, delta):
        tmp_sum = self.__getattribute__(att_name) + delta
        if tmp_sum > 1.1 or tmp_sum < 0:
            raise Exception("Final value would be outside the range [0;1]")

        self.__setattr__(att_name, tmp_sum)

    def increase_attribute(self, att_name, delta):
        if att_name is None:
            raise Exception("No attribute name")
        if delta is None or delta < 0 or delta > 1:
            raise Exception("Delta is not a number in the range [0;1]")
        self.__adjust_attribute__(att_name, delta)

    def decrease_attribute(self, att_name, delta):
        if att_name is None:
            raise Exception("No attribute name")
        if delta is None or delta < 0 or delta > 1:
            raise Exception("Delta is not a number in the range [0;1]")
        self.__adjust_attribute__(att_name, -delta)

    def decrease_percentage(self, att_name, percentage):
        if percentage < 0 or percentage > 1:
            raise Exception("Invalid percentage")
        if att_name is None:
            raise Exception("No attribute name")

        old_value = self.__getattribute__(att_name)
        new_value = old_value * (1 - percentage)
        self.__setattr__(att_name, new_value)
        return old_value - new_value

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
