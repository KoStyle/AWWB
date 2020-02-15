import os

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
            self.harpies = load_pickle(ARPIOS + TXT)
        else:
            self.harpies = read_harpies('arpios.txt')

        if os.path.isfile(OBJETOS + TXT):
            self.weapons = load_pickle(OBJETOS + TXT)
        else:
            self.weapons = read_file('objetos.txt')

        if os.path.isfile(STATUS + TXT):
            self.stats = load_pickle(STATUS + TXT)
        else:
            self.stats = Status()
            self.stats.alive = len(get_survivors(self.harpies));