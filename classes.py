from events import *
from pickers import *
from util import *
import os


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
            self.stats.alive = len(get_survivors(self.harpies))

        self.events = []
        self.events.append(Assassination(90, self.harpies, self.weapons, KillerPicker(), VictimPicker()))
        self.events.append(Coffee(2.5, self.harpies, RandomPicker()))
        self.events.append(Suicide(2.5, self.harpies, KillerPicker()))
        self.events.append(Revive(2.5, self.harpies, RandomPickerNoDelete(), RandomPickerNoDelete()))
        self.events.append(Curse(2.5, self.harpies, RandomPicker(), RandomPicker()))


    def i_command_you_to_pick_the_event(self):
        threshold = random.random()
        random.shuffle(self.events)

        #TODO Normalize the frequencies after initialization of colosseum
        pot = self.events[0].get_frequency()/100.
        i = 0
        while pot < threshold:
            pot += self.events[i].get_frequency()/100.
            i += 1

        return self.events[i]

    def is_over(self):
        return self.stats.omedetoo

    def let_the_games_begin(self):
        if self.stats.omedetoo:
            return False
        else:
            event = self.i_command_you_to_pick_the_event()
            tweet= event.bang()

            print(tweet)
            return True