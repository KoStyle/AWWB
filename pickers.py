import random
from classes import *


class KillerPicker:

    def pick(self, harpies):
        threshold = random.random()
        random.shuffle(harpies)

        pot = harpies[0].percKill
        i = 0
        while pot < threshold:
            pot = pot + harpies[i].percKill
            i += 1

        killer = harpies[i]
        del harpies[i]
        return killer


class VictimPicker:

    def pick(self, harpies):
        threshold = random.random()
        random.shuffle(harpies)

        pot = harpies[0].percVictim
        i = 0
        while pot < threshold:
            pot = pot + harpies[i].percVictim
            i += 1

        victim = harpies[i]
        del harpies[i]
        return victim


class RandomPicker:

    def pick(self, harpies):
        random.shuffle(harpies)
        harpy = random.choice(harpies)
        harpies.remove(harpy)
        return harpy
