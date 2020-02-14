class Assasination:
    def __init__(self):
        self.frecuency=0.0
        self.lastTweet=""
        self.curretTweet=""
        self.harpies=None

    def __init__(self, frecuency):
        self.frecuency=frecuency
        self.lastTweet=""
        self.curretTweet=""
        self.harpies=None

    def __init__(self, frecuency, harpies):
        self.frecuency=frecuency
        self.lastTweet=""
        self.curretTweet=""
        self.harpies=harpies

    def bang(self):



        return "Tweet"

    def chooseKiller(self, tmpHarpies):
        threshold = random.random()
        random.shuffle(tmpHarpies)
        pot = tmpHarpies[0].percKill
        i = 0
        while pot < threshold:
            pot = pot + tmpHarpies[i].percKill
            ++i
        killer = tmpHarpies[i]
        del tmpHarpies[i]
        return killer