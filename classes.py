import os
import pickle
import random
from constants import *
from util import *
from events import Assassination
from events import Coffee
from events import Revive
from events import Curse
from events import Suicide

from pickers import KillerPicker
from pickers import RandomPicker
from pickers import RandomPickerNoDelete
from pickers import VictimPicker


class Arpio:
    def __init__(self, name):
        self.name = name
        self.percKill = float(0.7)
        self.percVictim = float(0.7)
        self.isAlive = True
        self.kills = int(0)

    @staticmethod
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


class Colosseum:
    def __init__(self):

        if os.path.isfile(ARPIOS + TXT):
            self.harpies = IOKun.load_pickle(ARPIOS + TXT)
        else:
            self.harpies = Arpio.read_harpies('files/arpios.txt')

        if os.path.isfile(OBJETOS + TXT):
            self.weapons = IOKun.load_pickle(OBJETOS + TXT)
        else:
            self.weapons = IOKun.read_file('files/objetos.txt')

        if os.path.isfile(CAFE + TXT):
            self.coffees = IOKun.load_pickle(CAFE + TXT)
        else:
            self.coffees = IOKun.read_file('files/cafes.txt')

        if os.path.isfile(STATUS + TXT):
            self.stats = IOKun.load_pickle(STATUS + TXT)
        else:
            self.stats = Status()
            self.stats.alive = len(get_survivors(self.harpies))

        self.events = []
        self.events.append(Assassination(90, self.harpies, self.weapons, KillerPicker(), VictimPicker()))
        self.events.append(Coffee(2.5, self.harpies, self.coffees, RandomPicker()))
        self.events.append(Suicide(2.5, self.harpies, KillerPicker()))
        self.events.append(Revive(2.5, self.harpies, RandomPickerNoDelete(), RandomPickerNoDelete()))
        self.events.append(Curse(2.5, self.harpies, RandomPicker(), RandomPicker()))

    def i_command_you_to_pick_the_event(self):
        threshold = random.random()
        random.shuffle(self.events)

        # TODO Normalize the frequencies after initialization of colosseum
        pot = self.events[0].get_frequency() / 100.
        i = 0
        while pot < threshold:
            i += 1
            pot += self.events[i].get_frequency() / 100.

        return self.events[i]

    def is_over(self):
        return self.stats.omedetoo

    def let_the_games_begin(self):
        if self.stats.omedetoo:
            return False
        else:
            event = self.i_command_you_to_pick_the_event()
            tweet = event.bang(self.stats)
            # print(tweet)
            # self.print_percs()
            return tweet

    def print_percs(self):
        survivors = get_survivors(self.harpies)
        potVict = 0
        potKill = 0
        for harpy in survivors:
            potVict += harpy.percVictim
            potKill += harpy.percKill

        print("Kill: " + str(potKill) + " Vict: " + str(potVict))


class IOKun:

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
