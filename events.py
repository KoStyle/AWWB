import random

import util


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
        tmpHarpies = util.get_survivors(self.harpies)
        drinkers = self.choose_drinkers(tmpHarpies)
        tweet = "Coffee tweet"

        # TODO tweet construction

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
