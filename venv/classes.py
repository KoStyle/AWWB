import util
from util import getSurvivors


class Arpio:
    def __init__(self, name):
        self.name = name
        self.percKill = float(0.7)
        self.percHelp = float(0.5)
        self.percCafe = float(0.05)
        self.percHit = float(0.7)
        self.isAlive = True
        self.kills = int(0)


class Status:
    def __init__(self):
        self.kills = int(0)
        self.year = int(2019)
        self.alive = 0
        self.omedetoo = False
        self.winner = Arpio('N/A')


class Colosseum:
    def __init__(self):
        if (os.path.isfile(_ARPIOS + _TXT)):
            self.harpies = loadPickle(_ARPIOS + _TXT)
        else:
            self.harpies = readArpios('arpios.txt')

        if (os.path.isfile(_OBJETOS + _TXT)):
            self.weapons = loadPickle(_OBJETOS + _TXT)
        else:
            self.weapons = readList('objetos.txt')

        if (os.path.isfile(_STATUS + _TXT)):
            self.stats = loadPickle(_STATUS + _TXT)
        else:
            self.stats = Status()
            self.stats.alive = len(getSurvivors(self.harpies));