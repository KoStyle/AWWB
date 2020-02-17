import random

# TODO Events need a reference to InputKun
# TODO Make each event get its own flavour list using InputKun (colosseum doesn't need to know about them as they only make sense in their respective event)
class Assassination:
    def __init__(self, frequency, col, weapons, killerPicker, victimPicker):
        self.frequency = frequency
        self.lastTweet = ""
        self.curretTweet = ""
        self.colosseum = col
        self.killerPicker = killerPicker
        self.victimPicker = victimPicker
        self.weapons = weapons

    def bang(self):
        stats = self.colosseum.stats
        if stats.omedetoo:
            return "Se acabó pinche"

        surviors = self.colosseum.get_survivors()
        victimpy = self.victimPicker.pick(surviors)
        assasinpy = self.killerPicker.pick(surviors)
        tweet = ""
        if len(self.weapons) >= 1:
            motif = random.choice(self.weapons)
            self.weapons.remove(motif)
        else:
            motif = 'una navajita random'

        tweet += assasinpy.name + ' ha matado a ' + victimpy.name + ' %s.' % motif
        victimpy.isAlive = False
        assasinpy.percKill += victimpy.percKill
        assasinpy.percVictim += victimpy.percVictim / 3.
        victimpy.percVictim = 2 * (victimpy.percVictim / 3.)
        assasinpy.kills += 1

        # FIXME this is repeated code, think of a way to reuse this kind of redistributions. Also it is a bit hacky

        surviors.append(assasinpy)
        shareVict = victimpy.percVictim / float(len(surviors))
        surviors.remove(assasinpy)
        for harpy in surviors:
            harpy.percVictim += shareVict

        stats.kills += 1
        stats.alive -= 1
        if len(surviors) == 0:  # should be empty after the last standoff
            stats.omedetoo = True
            stats.winner = assasinpy
        return "{:1.4f}".format(assasinpy.percKill) + " : " + "{:1.4f}".format(assasinpy.percVictim) + " " + tweet

    def get_frequency(self):
        return self.frequency


class Coffee:
    def __init__(self, frequency, col, coffees, picker):
        self.frequency = frequency
        self.lastTweet = ""
        self.curretTweet = ""
        self.colosseum = col
        self.picker = picker
        self.coffees = coffees

    def bang(self):
        stats = self.colosseum.stats
        if stats.omedetoo:
            return "Se acabó pinche"

        surviors = self.colosseum.get_survivors()
        drinkers = self.choose_drinkers(surviors)
        tweet = ""

        for i in range(0, len(drinkers)):
            if i == len(drinkers) - 1:
                tweet += drinkers[i].name + " "
            elif i == len(drinkers) - 2:
                tweet += drinkers[i].name + " y "
            else:
                tweet += drinkers[i].name + ", "

        tweet += "se han %s. La vida sigue." % random.choice(self.coffees)

        return tweet

    def get_frequency(self):
        return self.frequency

    def choose_drinkers(self, surviors):
        drinkers = []
        maxDrinkers = min(len(surviors), 5)
        nDrinkers = random.randint(2, maxDrinkers)

        random.shuffle(surviors)

        for i in range(0, nDrinkers):
            auxHarpy = self.picker.pick(surviors)
            drinkers.append(auxHarpy)

        return drinkers


class Suicide:
    def __init__(self, frequency, col, killerPiker):
        self.frequency = frequency
        self.colosseum = col
        self.killerPicker = killerPiker

    def bang(self):
        stats = self.colosseum.stats
        if stats.omedetoo:
            return "Se acabó pinche"

        surviors = self.colosseum.get_survivors()
        suicidalpy = self.killerPicker.pick(surviors)
        suicidalpy.isAlive = False

        shareKill = suicidalpy.percKill / float(len(surviors))
        shareVict = suicidalpy.percVictim / float(len(surviors))
        for harpy in surviors:
            harpy.percKill += shareKill
            harpy.percVictim += shareVict

        stats.kills += 1
        stats.alive -= 1
        if len(surviors) == 1:  # should be only one harpy left after the last suicide
            stats.omedetoo = True
            stats.winner = surviors[0]
        tweet = suicidalpy.name + ' inició su secuencia de autodestrucción con éxito. Enhorabuena! #UnexpectedSkynet'
        return tweet

    def get_frequency(self):
        return self.frequency


class Revive:
    def __init__(self, frequency, col, shamanPicker, corpsePicker):
        self.frequency = frequency
        self.colosseum = col
        self.shamanPiker = shamanPicker
        self.corpsePicker = corpsePicker

    def bang(self):
        # TODO create flavour text for revives
        stats = self.colosseum.stats
        if stats.omedetoo:
            return "Se acabó pinche"

        surviors = self.colosseum.get_survivors()
        corpses = self.colosseum.get_corpses()

        # TODO Standarize this pickers (all of then without replacement)
        shamanpy = self.shamanPiker.pick(surviors)
        corpsepy = self.corpsePicker.pick(corpses)

        # Resurrected gets half of the victim pecentaje of the shaman
        # FIXME how much killPerc the corpse gets: minimum, average, the same that the shaman (i think this one is best)
        # FIXME creates negative percKill in redistribute!!! Redistribute percentages instead of a fixed amount across the board
        self.redistribute_percentages(corpsepy, surviors)
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
    def __init__(self, frequency, col, shamanPicker, cursedPicker):
        self.frequency = frequency
        self.colosseum = col
        self.shamanPiker = shamanPicker
        self.cursedPicker = cursedPicker

    def bang(self):
        stats = self.colosseum.stats
        if stats.omedetoo or stats.alive < 2:
            return "Se acabó pinche"

        surviors = self.colosseum.get_survivors()

        shamanpy = self.shamanPiker.pick(surviors)
        acursedpy = self.cursedPicker.pick(surviors)

        shamanpy.percKill += acursedpy.percKill / 2.
        acursedpy.percKill = acursedpy.percKill / 2.
        acursedpy.percVictim = acursedpy.percVictim * 2

        # TODO Create flavour text for curses
        return shamanpy.name + " le ha lanzado una maldición a " + acursedpy.name + ". Se ha convertido en un imán para el peligro"

    def get_frequency(self):
        return self.frequency
