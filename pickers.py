import random


#TODO change pickers so they all work with withdrawl, NO exceptions
class KillerPicker:

    def pick(self, harpies):
        threshold = random.random()
        random.shuffle(harpies)

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
        threshold = random.random()
        random.shuffle(harpies)
        remainingPercVictim=sum(c.percVictim for c in harpies)
        threshold= threshold*remainingPercVictim

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
        random.shuffle(harpies)
        harpy = random.choice(harpies)
        harpies.remove(harpy)
        return harpy

class RandomPickerNoDelete:

    def pick(selfs, harpies):
        random.shuffle(harpies)
        harpy = random.choice(harpies)
        return harpy
