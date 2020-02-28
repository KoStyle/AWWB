import random


# TODO Fusion KillerPicker and VictimPicker into a generic StatPicker using __getAttrib__
class KillerPicker:

    def pick(self, harpies):
        if harpies is None:
            raise PickerError("Argument error: No harpies received")
        threshold = random.random()
        random.shuffle(harpies)
        remainingPercKiller = sum(c.percKill for c in harpies)
        threshold = threshold * remainingPercKiller

        pot = harpies[0].percKill
        i = 0
        while pot < threshold:
            i += 1
            pot = pot + harpies[i].percKill

        killer = harpies[i]
        del harpies[i]
        return killer


class VictimPicker:

    def pick(self, harpies):
        if harpies is None:
            raise PickerError("Argument error: No harpies received")
        threshold = random.random()
        random.shuffle(harpies)
        remainingPercVictim = sum(c.percVictim for c in harpies)
        threshold = threshold * remainingPercVictim

        pot = harpies[0].percVictim
        i = 0
        while pot < threshold:
            i += 1
            pot += harpies[i].percVictim

        victim = harpies[i]
        del harpies[i]
        return victim


class RandomPicker:

    def pick(self, harpies):
        if harpies is None:
            raise PickerError("Argument error: No harpies received")
        random.shuffle(harpies)
        harpy = random.choice(harpies)
        harpies.remove(harpy)
        return harpy


# Deprecated: All pickers MUST remove the picked element from the original list
class RandomPickerNoDelete:

    def pick(selfs, harpies):
        if harpies is None:
            raise PickerError("Argument error: No harpies received")
        random.shuffle(harpies)
        harpy = random.choice(harpies)
        return harpy
