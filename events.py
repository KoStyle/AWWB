import random

from pip._internal.utils.deprecation import deprecated

from util import *


class Assasination:
    def __init__(self, frequency, harpies, weapons, killerPicker, victimPicker):
        self.frecuency = frequency
        self.lastTweet = ""
        self.curretTweet = ""
        self.harpies = harpies
        self.killerPicker = killerPicker
        self.victimPicker = victimPicker
        self.weapons = weapons

    def bang(self):
        tmpHarpies = get_survivors(self.harpies)
        assasinpy: Arpio = self.killerPicker.pick(tmpHarpies)
        victimpy: Arpio = self.victimPicker.pick(tmpHarpies)
        tweet = ""
        if len(self.weapons) >= 1:
            motif = random.choice(self.weapons)
            self.weapons.remove(motif)
        else:
            motif = 'una navajita random'

        # TEST how good does the victim perc distribution
        tweet += assasinpy.name + ' ha matado a ' + victimpy.name + ' %s.' % motif
        victimpy.isAlive = False
        assasinpy.percKill += victimpy.percKill
        assasinpy.percVictim += victimpy.percVictim / 2.
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
    def __init__(self, frequency, harpies, picker):
        self.frecuency = frequency
        self.lastTweet = ""
        self.curretTweet = ""
        self.harpies = harpies
        self.picker = picker

    def bang(self):
        coffees = read_file(CAFE)

        tmpHarpies = get_survivors(self.harpies)
        drinkers = self.choose_drinkers(tmpHarpies)
        tweet = ""

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


class Suicide:
    def __init__(self, frequency, harpies, killerPiker):
        self.frequency = frequency
        self.harpies = harpies
        self.killerPicker = killerPiker

    def bang(self):
        tmpHarpies = get_survivors(self.harpies)
        suicidalpy = self.killerPicker.pick(tmpHarpies)
        suicidalpy.isAlive = False

        # TODO: Think of a different form to do this. It might lose kill percentage (a small amount) if the division gives irrational numbers
        share = suicidalpy.percKill / float(len(tmpHarpies))
        for harpy in tmpHarpies:
            harpy.percKill += share

        tweet = suicidalpy.name + ' inició su secuencia de autodestrucción con éxito. Enhorabuena! #UnexpectedSkynet'
        return tweet


# Both pickers come without withdrawing from the list
class Revive:
    def __init__(self, frequency, harpies, shamanPicker, corpsePicker):
        self.frequency = frequency
        self.harpies = harpies
        self.shamanPiker = shamanPicker
        self.corpsePicker = corpsePicker

    def bang(self):
        # TODO create flavour text for revives
        tmpHarpies = get_survivors(self.harpies)
        deadHarpies = get_corpses(self.harpies)

        shamanpy: Arpio = self.shamanPiker.pick(tmpHarpies)
        corpsepy: Arpio = self.corpsePicker.pick(deadHarpies)

        # Resurrected gets half of the victim pecentaje of the shaman

        corpsepy.isAlive = True
        corpsepy.percVictim += shamanpy.percVictim / 2.
        shamanpy.percVictim = shamanpy.percVictim / 2.
        self.redistribute_kill_percentage(corpsepy, tmpHarpies)
        return shamanpy.name + " ha revivido a " + corpsepy.name + ". Alabado sea Gilgamesh."

    def redistribute_kill_percentage(self, corpsepy, survivors):
        corpsepy.percKill = 1. / (len(survivors) + 1)
        killDecrement = corpsepy.percKill / float(len(survivors))

        for auxpy in survivors:
            auxpy.percKill -= killDecrement


class Curse:
    def __init__(self, frequency, harpies, shamanPicker, cursedPicker):
        self.frequency = frequency
        self.harpies = harpies
        self.shamanPiker = shamanPicker
        self.cursedPicker = cursedPicker

    def bang(self):
        tmpHarpies = get_survivors(self.harpies)

        shamanpy: Arpio = self.shamanPiker.pick(tmpHarpies)
        acursedpy: Arpio = self.cursedPicker.pick(tmpHarpies)

        shamanpy.percKill += acursedpy.percKill / 2.
        acursedpy = acursedpy.percKill / 2.
        acursedpy.percVictim = acursedpy.percVictim * 2

        # TODO Create flavour text for curses
        return shamanpy.name + " le ha lanzado una maldición a " + acursedpy.name + ". Se ha convertido en un imán para el peligro"
