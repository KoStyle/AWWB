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
        if (os.path.isfile(util.ARPIOS + util.TXT)):
            self.harpies = util.load_pickle(util.ARPIOS + util.TXT)
        else:
            self.harpies = util.read_harpies('arpios.txt')

        if (os.path.isfile(util.OBJETOS + util.TXT)):
            self.weapons = util.load_pickle(util.OBJETOS + util.TXT)
        else:
            self.weapons = util.read_file('objetos.txt')

        if os.path.isfile(util.STATUS + util.TXT):
            self.stats = util.load_pickle(util.STATUS + util.TXT)
        else:
            self.stats = Status()
            self.stats.alive = len(util.get_survivors(self.harpies));