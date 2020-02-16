import os
import pickle
import events
import pickers
import random
from util import *


class Arpio:
    def __init__(self, name):
        self.name = name
        self.percKill = float(0.7)
        self.percVictim = float(0.7)
        self.isAlive = True
        self.kills = int(0)


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
            self.harpies = Colosseum.load_pickle(ARPIOS + TXT)
        else:
            self.harpies = self.read_harpies('files/arpios.txt')

        if os.path.isfile(OBJETOS + TXT):
            self.weapons = Colosseum.load_pickle(OBJETOS + TXT)
        else:
            self.weapons = read_file('files/objetos.txt')

        if os.path.isfile(STATUS + TXT):
            self.stats = Colosseum.load_pickle(STATUS + TXT)
        else:
            self.stats = Status()
            self.stats.alive = len(get_survivors(self.harpies))

        self.events = []
        self.events.append(events.Assassination(90, self.harpies, self.weapons, pickers.KillerPicker(), pickers.VictimPicker()))
        self.events.append(events.Coffee(2.5, self.harpies, pickers.RandomPicker()))
        self.events.append(events.Suicide(2.5, self.harpies, pickers.KillerPicker()))
        self.events.append(events.Revive(2.5, self.harpies, pickers.RandomPickerNoDelete(), pickers.RandomPickerNoDelete()))
        self.events.append(events.Curse(2.5, self.harpies, pickers.RandomPicker(), pickers.RandomPicker()))

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
            print(tweet)
            return True

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

        lista.sort(key=lambda x: x.name)
        return lista

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
