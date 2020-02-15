import random

import util
from util import *


class Assasination:
    def __init__(self, frecuency, harpies):
        self.frecuency = frecuency
        self.lastTweet = ""
        self.curretTweet = ""
        self.harpies = harpies

    def bang(self):
        return "Killer Tweet"

    def choose_killer(self, tmpHarpies):
        threshold = random.random()
        random.shuffle(tmpHarpies)

        pot = tmpHarpies[0].percKill
        i = 0
        while pot < threshold:
            pot = pot + tmpHarpies[i].percKill
            i += 1

        killer = tmpHarpies[i]
        del tmpHarpies[i]
        return killer


class Coffee:
    def __init__(self, frecuency, harpies):
        self.frecuency = frecuency
        self.lastTweet = ""
        self.curretTweet = ""
        self.harpies = harpies

    def bang(self):
        coffees = read_file(CAFE)

        tmpHarpies = get_survivors(self.harpies)
        drinkers = self.choose_drinkers(tmpHarpies)
        tweet = "Coffee tweet"

        for i in range(0, len(drinkers)):
            if i == len(drinkers) - 1:
                tweet += drinkers[i].name + " "
            elif i == len(drinkers) - 2:
                tweet += drinkers[i].name + " and  "
            else:
                tweet += drinkers[i].name + ", "

        tweet += "se han %s. La vida sigue." % random.choice(coffees)

        return tweet

    def choose_drinkers(self, tmpHarpies):
        drinkers = []
        nDrinkers = random.randint(2, 5)

        random.shuffle(tmpHarpies)

        for i in range(0, nDrinkers):
            auxHarpy = random.choice(tmpHarpies)
            tmpHarpies.remove(auxHarpy)
            drinkers.append(auxHarpy)

        return drinkers
