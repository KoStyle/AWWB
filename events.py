import random

from pip._internal.utils.deprecation import deprecated

from util import *


# TODO: Externalise all choice methods to choice policies so they can be reused (suicide will have a choose_killer to use that stat. Maybe class with the static methods
# Possible policies based on the stat used. Killer policy, helper policy, victim policy
class Assasination:
    def __init__(self, frecuency, harpies, weapons, killerPicker, victimPicker):
        self.frecuency = frecuency
        self.lastTweet = ""
        self.curretTweet = ""
        self.harpies = harpies
        self.killerPicker = killerPicker
        self.victimPicker = victimPicker
        self.weapons = weapons

    def bang(self):
        tmpHarpies = get_survivors(self.harpies)
        assasinpy = self.killerPicker.pick(tmpHarpies)
        victimpy = self.victimPicker.pick(tmpHarpies)
        if len(self.weapons) >= 1:
            motif = random.choice(self.weapons)
            self.weapons.remove(motif)
        else:
            motif = 'una navajita random'

        #TODO: Implement random help
        tweet = assasinpy.name + ' ha matado a ' + victimpy.name + ' %s.' % motif
        victimpy.isAlive = False
        assasinpy.percKill += victimpy.percKill
        assasinpy.kills += 1

        return tweet

    @deprecated(version='1.1', reason="Picking functions changed into property so they can be reused")
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
    def __init__(self, frecuency, harpies, picker):
        self.frecuency = frecuency
        self.lastTweet = ""
        self.curretTweet = ""
        self.harpies = harpies
        self.picker = picker

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
            auxHarpy = self.picker.pick(tmpHarpies)
            drinkers.append(auxHarpy)

        return drinkers
