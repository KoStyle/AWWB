import random

from classes import Status, Arpio
from events import Assassination, Coffee, Suicide, Revive, Curse
from pickers import KillerPicker, VictimPicker, RandomPicker


class Colosseum:
    def __init__(self):

        #TODO Change this to make the read from InputKun
        self.harpies = Arpio.harpy_factory('files/arpios.txt')

        self.stats = Status()
        self.stats.alive = len(self.harpies)

        self.events = []
        self.events.append(Assassination(90, self, KillerPicker(), VictimPicker()))
        self.events.append(Coffee(2.5, self, RandomPicker()))
        self.events.append(Suicide(2.5, self, KillerPicker()))
        self.events.append(Revive(2.5, self, RandomPicker(), RandomPicker()))
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

    def leech_attribute(self, att_name, leech_percent, harpies):
        total_leeched = 0
        for harpy in harpies:
            total_leeched += harpy.decrease_percentage(att_name, leech_percent)
        return total_leeched

    def share_attribute(self, att_name, to_share, harpies):
        share = to_share / float(len(harpies))
        for harpy in harpies:
            harpy.increase_attribute(att_name, share)
