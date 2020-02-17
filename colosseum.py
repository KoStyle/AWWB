# TODO try to refactor the bangs to streamline then. Find all the redundant code and do somethin like with the pickers
import os
import random

from classes import InputKun, STATUS, TXT, CAFE, OBJETOS, ARPIOS, Status, Arpio
from events import Assassination, Coffee, Suicide, Revive, Curse
from pickers import KillerPicker, VictimPicker, RandomPicker, RandomPickerNoDelete


class Colosseum:
    def __init__(self):

        if os.path.isfile(ARPIOS + TXT):
            self.harpies = InputKun.load_pickle(ARPIOS + TXT)
        else:
            self.harpies = Arpio.harpy_factory('files/arpios.txt')

        if os.path.isfile(OBJETOS + TXT):
            self.weapons = InputKun.load_pickle(OBJETOS + TXT)
        else:
            self.weapons = InputKun.read_file('files/objetos.txt')

        if os.path.isfile(CAFE + TXT):
            self.coffees = InputKun.load_pickle(CAFE + TXT)
        else:
            self.coffees = InputKun.read_file('files/cafes.txt')

        if os.path.isfile(STATUS + TXT):
            self.stats = InputKun.load_pickle(STATUS + TXT)
        else:
            self.stats = Status()
            self.stats.alive = len(self.harpies)

        self.events = []
        self.events.append(Assassination(90, self, self.weapons, KillerPicker(), VictimPicker()))
        self.events.append(Coffee(2.5, self, self.coffees, RandomPicker()))
        self.events.append(Suicide(2.5, self, KillerPicker()))
        self.events.append(Revive(2.5, self, RandomPickerNoDelete(), RandomPickerNoDelete()))
        self.events.append(Curse(2.5, self, RandomPicker(), RandomPicker()))

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
            tweet = event.bang()
            # print(tweet)
            # self.print_percs()
            return tweet

    def print_percs(self):
        survivors = self.get_survivors()
        potVict = 0
        potKill = 0
        for harpy in survivors:
            potVict += harpy.percVictim
            potKill += harpy.percKill

        print("Kill: " + str(potKill) + " Vict: " + str(potVict))

    def get_survivors(self):
        listatmp = []
        for index in range(len(self.harpies)):
            if self.harpies[index].isAlive:
                listatmp.append(self.harpies[index])
        return listatmp

    def get_corpses(self):
        corpses = []
        for index in range(len(self.harpies)):
            if not self.harpies[index].isAlive:
                corpses.append(self.harpies[index])
        return corpses
