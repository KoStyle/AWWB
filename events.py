import random

from constants import WEAPONFILE, COFFEEFILE, SUICIDEFILE, CURSEFILE, REVIVEFILE, DRAWFILE
from errors import EventError
from io_sama import InputKun


# TODO create a parent event class and move getFrequency there and some attributes (maybe get rid of get frequency altogheter
class Assassination:
    flavour_file = WEAPONFILE

    def __init__(self, frequency, col, killer_picker, victim_picker):
        if killer_picker is None or victim_picker is None or col is None:
            raise EventError("Init error: Null parameters passed to the constructor method")

        self.frequency = frequency if not frequency is None else 1
        self.lastTweet = ""
        self.curretTweet = ""
        self.colosseum = col
        self.killerPicker = killer_picker
        self.victimPicker = victim_picker
        self.weapons = InputKun.read_file(self.flavour_file)

    def refresh(self):
        self.weapons = InputKun.read_file(self.flavour_file)

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
            motif = 'con la vara de la aleatoriedad'

        tweet +='{} ha matado a {} {}.'.format(assasinpy, victimpy, motif)
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
        return tweet

    def get_frequency(self):
        return self.frequency


class Coffee:
    flavour_file = COFFEEFILE

    def __init__(self, frequency, col, picker):
        if picker is None or col is None:
            raise EventError("Init error: Null parameters passed to the constructor method")

        self.frequency = frequency if not frequency is None else 1
        self.lastTweet = ""
        self.curretTweet = ""
        self.colosseum = col
        self.picker = picker
        self.coffees = InputKun.read_file(self.flavour_file)

    def refresh(self):
        self.coffees = InputKun.read_file(self.flavour_file)

    def bang(self):
        stats = self.colosseum.stats
        if stats.omedetoo:
            return "Se acabó pinche"

        surviors = self.colosseum.get_survivors()
        drinkers = self.choose_drinkers(surviors)
        tweet = ""

        for i in range(0, len(drinkers)):
            if i == len(drinkers) - 1:
                tweet += str(drinkers[i]) + " "
            elif i == len(drinkers) - 2:
                tweet += str(drinkers[i]) + " y "
            else:
                tweet += str(drinkers[i]) + ", "

        if len(self.coffees) < 1:
            self.coffees.append("ido a tomar un [404: edible item missing]")

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
    flavour_file = SUICIDEFILE

    def __init__(self, frequency, col, killer_picker):
        if killer_picker is None  or col is None:
            raise EventError("Init error: Null parameters passed to the constructor method")

        self.frequency = frequency if not frequency is None else 1
        self.colosseum = col
        self.killerPicker = killer_picker
        self.suicides = InputKun.read_file(self.flavour_file)

    def refresh(self):
        self.suicides = InputKun.read_file(self.flavour_file)

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

        if len(self.suicides) < 1:
            self.suicides.append("inició su secuencia de autodestrucción con éxito. Enhorabuena! #UnexpectedSkynet")
        tweet = "{} {}".format(suicidalpy, random.choice(self.suicides))

        return tweet

    def get_frequency(self):
        return self.frequency


class Revive:
    flavour_file = REVIVEFILE

    def __init__(self, frequency, col, shaman_picker, corpse_picker):
        if shaman_picker is None or corpse_picker is None or col is None:
            raise EventError("Init error: Null parameters passed to the constructor method")

        self.frequency = frequency if not frequency is None else 1
        self.colosseum = col
        self.shamanPiker = shaman_picker
        self.corpsePicker = corpse_picker
        self.revives = InputKun.read_file(self.flavour_file)

    def refresh(self):
        self.revives = InputKun.read_file(self.flavour_file)

    def bang(self):
        stats = self.colosseum.stats
        if stats.omedetoo:
            raise EventError("Omedetoo! Git out!")

        surviors = self.colosseum.get_survivors()
        corpses = self.colosseum.get_corpses()

        if len(corpses) == 0:
            return "Me comentan que alguien intentaba revivir a otro alguien, pero todos estamos vivos. Por motivos de RGPD no revelaré nombres."

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

        if len(self.revives) < 1:
            self.revives.append(". Alabado sea Gilgamesh.")
        tweet = "{} ha revivido a {}{}".format(shamanpy, corpsepy, random.choice(self.revives))

        return tweet

    def get_frequency(self):
        return self.frequency


class Curse:
    flavour_file = CURSEFILE

    def __init__(self, frequency, col, shaman_picker, cursed_picker):
        if shaman_picker is None or cursed_picker is None or col is None:
            raise EventError("Init error: Null parameters passed to the constructor method")

        self.frequency = frequency if not frequency is None else 1
        self.colosseum = col
        self.shamanPiker = shaman_picker
        self.cursedPicker = cursed_picker
        self.curses = InputKun.read_file(self.flavour_file)

    def refresh(self):
        self.curses = InputKun.read_file(self.flavour_file)

    def bang(self):
        stats = self.colosseum.stats
        if stats.omedetoo or stats.alive < 2:
            raise EventError("Omedetoo! Git out!")

        surviors = self.colosseum.get_survivors()

        shamanpy = self.shamanPiker.pick(surviors)
        acursedpy = self.cursedPicker.pick(surviors)
        surviors.append(shamanpy)

        shamanpy.percKill += acursedpy.percKill / 2.
        acursedpy.percKill = acursedpy.percKill / 2.
        acursedpy.percVictim += self.colosseum.leech_attribute("percVictim", acursedpy.percVictim, surviors)

        if len(self.curses) < 1:
            self.curses.append(". Se ha convertido en un imán para el peligro")
        tweet = "{} le ha lanzado una maldición a {}{}".format(shamanpy, acursedpy, random.choice(self.curses))

        return tweet

    def get_frequency(self):
        return self.frequency


class Draw:
    flavour_file = DRAWFILE

    def __init__(self, frequency, col, killer_picker, victim_picker):
        if killer_picker is None or victim_picker is None or col is None:
            raise EventError("Init error: Null parameters passed to the constructor method")

        self.frequency = frequency if not frequency is None else 1
        self.colosseum = col
        self.killer_picker = killer_picker
        self.victim_picker = victim_picker
        self.draws = InputKun.read_file(self.flavour_file)

    def refresh(self):
        self.draws = InputKun.read_file(self.flavour_file)

    def bang(self):
        stats = self.colosseum.stats
        if stats.omedetoo or stats.alive < 2:
            raise EventError("Omedetoo! Git out!")

        surviors = self.colosseum.get_survivors()

        killer = self.killer_picker.pick(surviors)
        victim = self.victim_picker.pick(surviors)

        if len(self.draws) < 1:
            self.draws.append(". Alto! Parece que no ha muerto! Con algo de suerte vivirá para luchar un día más")
        tweet = "{} le ha disparado y derribado a {}{}".format(killer, victim,random.choice(self.draws))

        return tweet

    def get_frequency(self):
        return self.frequency
