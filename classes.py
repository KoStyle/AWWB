from errors import *


class Arpio:
    def __init__(self, csv_data):
        data = csv_data.split(";")

        self.name = data[0].strip()
        self.t_handle = None if len(data) <= 1 or not data[1] else data[1].strip()
        self.presentation = None if len(data) <= 2 or not data[2] else data[2].strip()
        self.percKill = float(0.7)
        self.percVictim = float(0.7)
        self.isAlive = True
        self.kills = int(0)

    @staticmethod
    def harpy_factory(csv_data):
        harpies = []
        for csv_line in csv_data:
            harpies.append(Arpio(csv_line.strip()))
        total_harpies = len(harpies)

        for harpy in harpies:
            harpy.percKill = 1. / total_harpies
            harpy.percVictim = 1. / total_harpies
        harpies.sort(key=lambda x: x.name)
        return harpies

    def __str__(self):
        if self.t_handle is not None:
            tostr = self.name + " (" + self.t_handle + ")"
        else:
            tostr = self.name

        return tostr

    def __adjust_attribute__(self, att_name, delta):
        tmp_sum = self.__getattribute__(att_name) + delta
        if tmp_sum > 1.1 or tmp_sum < 0:
            raise InvalidAdjustError("Final value would be outside the range [0;1]")

        self.__setattr__(att_name, tmp_sum)

    def increase_attribute(self, att_name, delta):
        if att_name is None:
            raise InvalidAdjustError("No attribute name")
        if delta is None or delta < 0 or delta > 1:
            raise InvalidAdjustError("Delta is not a number in the range [0;1]")
        self.__adjust_attribute__(att_name, delta)

    def decrease_attribute(self, att_name, delta):
        if att_name is None:
            raise InvalidAdjustError("No attribute name")
        if delta is None or delta < 0 or delta > 1:
            raise InvalidAdjustError("Delta is not a number in the range [0;1]")
        self.__adjust_attribute__(att_name, -delta)

    def decrease_percentage(self, att_name, percentage):
        if percentage < 0 or percentage > 1:
            raise InvalidAdjustError("Invalid percentage")
        if att_name is None:
            raise InvalidAdjustError("No attribute name")

        old_value = self.__getattribute__(att_name)
        new_value = old_value * (1 - percentage)
        self.__setattr__(att_name, new_value)
        return old_value - new_value

    @staticmethod
    def print_status_harpies(lista):
        for index in range(len(lista)):
            print(lista[index].name + '-' + str(lista[index].isAlive) + '-' + str(lista[index].kills))


class Status:
    def __init__(self):
        self.kills = int(0)
        self.year = int(2019)
        self.alive = int(0)
        self.omedetoo = False
        self.winner = Arpio('N/A')
