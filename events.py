from util import *
from pip._internal.utils.deprecation import deprecated
import random


# TODO try to refactor the bangs to streamline then. Find all the redundant code and do somethin like with the pickers
class Assassination:
    def __init__(self, frequency, harpies, weapons, killerPicker, victimPicker):
        self.frequency = frequency
        self.lastTweet = ""
        self.curretTweet = ""
        self.harpies = harpies
        self.killerPicker = killerPicker
        self.victimPicker = victimPicker
        self.weapons = weapons

    def bang(self, stats):
        if stats.omedetoo:
            return "Se acabó pinche"

        tmpHarpies = get_survivors(self.harpies)
        assasinpy = self.killerPicker.pick(tmpHarpies)
        victimpy = self.victimPicker.pick(tmpHarpies)
        tweet = ""
        if len(self.weapons) >= 1:
            motif = random.choice(self.weapons)
            self.weapons.remove(motif)
        else:
            motif = 'una navajita random'

        tweet += assasinpy.name + ' ha matado a ' + victimpy.name + ' %s.' % motif
        victimpy.isAlive = False
        assasinpy.percKill += victimpy.percKill
        assasinpy.kills += 1

        # FIXME this is repeated code, think of a way to reuse this kind of redistributions. Also it is a bit hacky

        tmpHarpies.append(assasinpy)
        shareVict = victimpy.percVictim / float(len(tmpHarpies))
        tmpHarpies.remove(assasinpy)
        for harpy in tmpHarpies:
            harpy.percVictim += shareVict

        stats.kills += 1
        stats.alive -= 1
        if len(tmpHarpies) == 0:  # should be empty after the last standoff
            stats.omedetoo = True
            stats.winner = assasinpy
        return tweet

    def get_frequency(self):
        return self.frequency


class Coffee:
    def __init__(self, frequency, harpies, picker):
        self.frequency = frequency
        self.lastTweet = ""
        self.curretTweet = ""
        self.harpies = harpies
        self.picker = picker

    def bang(self, stats):
        if stats.omedetoo:
            return "Se acabó pinche"

        coffees = read_file(CAFE)

        tmpHarpies = get_survivors(self.harpies)
        drinkers = self.choose_drinkers(tmpHarpies)
        tweet = ""

        for i in range(0, len(drinkers)):
            if i == len(drinkers) - 1:
                tweet += drinkers[i].name + " "
            elif i == len(drinkers) - 2:
                tweet += drinkers[i].name + " y "
            else:
                tweet += drinkers[i].name + ", "

        tweet += "se han %s. La vida sigue." % random.choice(coffees)

        return tweet

    def get_frequency(self):
        return self.frequency

    def choose_drinkers(self, tmpHarpies):
        drinkers = []
        maxDrinkers = min(len(tmpHarpies), 5)
        nDrinkers = random.randint(2, maxDrinkers)

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

    def bang(self, stats):
        if stats.omedetoo:
            return "Se acabó pinche"

        tmpHarpies = get_survivors(self.harpies)
        suicidalpy = self.killerPicker.pick(tmpHarpies)
        suicidalpy.isAlive = False

        # TODO: Think of a different form to do this. It might lose kill percentage (a small amount) if the division gives irrational numbers
        shareKill = suicidalpy.percKill / float(len(tmpHarpies))
        shareVict = suicidalpy.percVictim / float(len(tmpHarpies))
        for harpy in tmpHarpies:
            harpy.percKill += shareKill
            harpy.percVictim += shareVict

        stats.kills += 1
        stats.alive -= 1
        if len(tmpHarpies) == 1:  # should be only one harpy left after the last suicide
            stats.omedetoo = True
            stats.winner = tmpHarpies[0]
        tweet = suicidalpy.name + ' inició su secuencia de autodestrucción con éxito. Enhorabuena! #UnexpectedSkynet'
        return tweet

    def get_frequency(self):
        return self.frequency


# Both pickers come without withdrawing from the list
class Revive:
    def __init__(self, frequency, harpies, shamanPicker, corpsePicker):
        self.frequency = frequency
        self.harpies = harpies
        self.shamanPiker = shamanPicker
        self.corpsePicker = corpsePicker

    def bang(self, stats):
        # TODO create flavour text for revives

        if stats.omedetoo:
            return "Se acabó pinche"

        tmpHarpies = get_survivors(self.harpies)
        deadHarpies = get_corpses(self.harpies)

        shamanpy = self.shamanPiker.pick(tmpHarpies)
        corpsepy = self.corpsePicker.pick(deadHarpies)

        # Resurrected gets half of the victim pecentaje of the shaman

        self.redistribute_percentages(corpsepy, tmpHarpies)
        corpsepy.isAlive = True
        corpsepy.percVictim += shamanpy.percVictim / 2.
        shamanpy.percVictim = shamanpy.percVictim / 2.

        stats.alive += 1

        return shamanpy.name + " ha revivido a " + corpsepy.name + ". Alabado sea Gilgamesh."

    def redistribute_percentages(self, corpsepy, survivors):
        corpsepy.percKill = 1. / (len(survivors) + 1)
        killDecrement = corpsepy.percKill / float(len(survivors))

        corpsepy.percVictim = 1. / (len(survivors) + 1)
        victDecrement = corpsepy.percVictim / float(len(survivors))

        for auxpy in survivors:
            auxpy.percKill -= killDecrement
            auxpy.percVictim -= victDecrement

    def get_frequency(self):
        return self.frequency


class Curse:
    def __init__(self, frequency, harpies, shamanPicker, cursedPicker):
        self.frequency = frequency
        self.harpies = harpies
        self.shamanPiker = shamanPicker
        self.cursedPicker = cursedPicker

    def bang(self, stats):
        if stats.omedetoo or stats.alive < 2:
            return "Se acabó pinche"

        tmpHarpies = get_survivors(self.harpies)

        shamanpy = self.shamanPiker.pick(tmpHarpies)
        acursedpy = self.cursedPicker.pick(tmpHarpies)

        shamanpy.percKill += acursedpy.percKill / 2.
        acursedpy.percKill = acursedpy.percKill / 2.
        acursedpy.percVictim = acursedpy.percVictim * 2

        # TODO Create flavour text for curses
        return shamanpy.name + " le ha lanzado una maldición a " + acursedpy.name + ". Se ha convertido en un imán para el peligro"

    def get_frequency(self):
        return self.frequency
