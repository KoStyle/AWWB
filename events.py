import random


# TODO Events need a reference to InputKun
# TODO Make each event get its own flavour list using InputKun (colosseum doesn't need to know about them as they only make sense in their respective event)
class Assassination:
    def __init__(self, frequency, col, weapons, killer_picker, victim_picker):
        self.frequency = frequency
        self.lastTweet = ""
        self.curretTweet = ""
        self.colosseum = col
        self.killerPicker = killer_picker
        self.victimPicker = victim_picker
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

        # Transfer of stats
        assasinpy.percKill += victimpy.percKill
        assasinpy.percVictim += victimpy.percVictim / 3.
        victimpy.percVictim = 2 * (victimpy.percVictim / 3.)

        surviors.append(assasinpy)  # We put it back in survivors so he can receive more victimness
        self.colosseum.share_attribute("percVictim", victimpy.percVictim, surviors)

        # Recording of statistics
        assasinpy.kills += 1
        stats.kills += 1
        stats.alive -= 1
        if len(surviors) == 1:  # should be empty after the last standoff
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
        max_drinkers = min(len(surviors), 5)
        n_drinkers = random.randint(2, max_drinkers)

        random.shuffle(surviors)

        for i in range(0, n_drinkers):
            aux_harpy = self.picker.pick(surviors)
            drinkers.append(aux_harpy)

        return drinkers


class Suicide:
    def __init__(self, frequency, col, killer_picker):
        self.frequency = frequency
        self.colosseum = col
        self.killerPicker = killer_picker

    def bang(self):
        stats = self.colosseum.stats
        if stats.omedetoo:
            return "Se acabó pinche"

        surviors = self.colosseum.get_survivors()
        suicidalpy = self.killerPicker.pick(surviors)
        suicidalpy.isAlive = False

        self.colosseum.share_attribute("percKill", suicidalpy.percKill, surviors)
        self.colosseum.share_attribute("percVictim", suicidalpy.percVictim, surviors)

        suicidalpy.kills += 1
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
    def __init__(self, frequency, col, shaman_picker, corpse_picker):
        self.frequency = frequency
        self.colosseum = col
        self.shamanPiker = shaman_picker
        self.corpsePicker = corpse_picker

    def bang(self):
        # TODO create flavour text for revives
        stats = self.colosseum.stats
        if stats.omedetoo:
            return "Se acabó pinche"

        surviors = self.colosseum.get_survivors()
        corpses = self.colosseum.get_corpses()

        shamanpy = self.shamanPiker.pick(surviors)
        corpsepy = self.corpsePicker.pick(corpses)

        # Resurrected gets half of the victim pecentaje of the shaman
        # TODO how much killPerc the corpse gets: minimum, average, the same that the shaman (i think this one is best)

        # We add the shaman back in the list so we can leech of him aswell
        surviors.append(shamanpy)
        corpsepy.percKill = self.colosseum.leech_attribute("percKill", 0.1, surviors)
        corpsepy.percVictim = self.colosseum.leech_attribute("percVictim", 0.1, surviors)
        corpsepy.isAlive = True

        corpsepy.percVictim += shamanpy.percVictim / 2.
        shamanpy.percVictim = shamanpy.percVictim / 2.

        stats.alive += 1

        return shamanpy.name + " ha revivido a " + corpsepy.name + ". Alabado sea Gilgamesh."

    def get_frequency(self):
        return self.frequency


class Curse:
    def __init__(self, frequency, col, shaman_picker, cursed_picker):
        self.frequency = frequency
        self.colosseum = col
        self.shamanPiker = shaman_picker
        self.cursedPicker = cursed_picker

    def bang(self):
        stats = self.colosseum.stats
        if stats.omedetoo or stats.alive < 2:
            return "Se acabó pinche"

        surviors = self.colosseum.get_survivors()

        shamanpy = self.shamanPiker.pick(surviors)
        acursedpy = self.cursedPicker.pick(surviors)
        surviors.append(shamanpy)

        shamanpy.percKill += acursedpy.percKill / 2.
        acursedpy.percKill = acursedpy.percKill / 2.
        acursedpy.percVictim += self.colosseum.leech_attribute("percVictim", acursedpy.percVictim, surviors)

        # TODO Create flavour text for curses
        return shamanpy.name + " le ha lanzado una maldición a " + acursedpy.name + ". Se ha convertido en un imán para el peligro"

    def get_frequency(self):
        return self.frequency
