import os
import util


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
        if (os.path.isfile(_ARPIOS + _TXT)):
            self.harpies = util.loadPickle(_ARPIOS + _TXT)
        else:
            self.harpies = util.readArpios('arpios.txt')

        if (os.path.isfile(_OBJETOS + _TXT)):
            self.weapons = util.loadPickle(_OBJETOS + _TXT)
        else:
            self.weapons = util.readList('objetos.txt')

        if (os.path.isfile(_STATUS + _TXT)):
            self.stats = util.loadPickle(_STATUS + _TXT)
        else:
            self.stats = Status()
            self.stats.alive = len(util.getSurvivors(self.harpies));