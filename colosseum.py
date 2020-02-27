import math
import random

from PIL import Image, ImageDraw, ImageFont

from classes import Status, Arpio
from constants import IMG, PNG, FONT
from events import Assassination, Coffee, Suicide, Revive, Curse, Draw
from io_sama import InputKun
from pickers import KillerPicker, VictimPicker, RandomPicker


class Colosseum:
    def __init__(self):

        #TODO change this to constants
        self.harpies = Arpio.harpy_factory(InputKun.read_file('files/arpios.txt'))
        self.stats = Status()
        self.stats.alive = len(self.harpies)

        self.events = []
        self.events.append(Assassination(87.5, self, KillerPicker(), VictimPicker()))
        self.events.append(Coffee(2.5, self, RandomPicker()))
        self.events.append(Suicide(2.5, self, KillerPicker()))
        self.events.append(Revive(2.5, self, RandomPicker(), RandomPicker()))
        self.events.append(Curse(2.5, self, RandomPicker(), RandomPicker()))
        self.events.append(Draw(2.5, self, KillerPicker(), VictimPicker()))

    def i_command_you_to_pick_the_event(self):
        threshold = random.random()
        random.shuffle(self.events)

        # TODO Normalize the frequencies after initialization of colosseum
        pot = self.events[0].get_frequency() / 100.
        i = 0
        while pot < threshold:
            i += 1
            pot += self.events[i].get_frequency() / 100.

        return self.events[i]

    def is_over(self):
        return self.stats.omedetoo

    def let_the_games_begin(self):
        if self.stats.omedetoo:
            return False
        else:
            event = self.i_command_you_to_pick_the_event()
            tweet = event.bang()
            # print(tweet)
            # self.print_percs()
            return tweet

    def print_percs(self):
        survivors = self.get_survivors()
        potVict = 0
        potKill = 0
        for harpy in survivors:
            potVict += harpy.percVictim
            potKill += harpy.percKill

        print("Kill: " + str(potKill) + " Vict: " + str(potVict))

    def get_survivors(self):
        listatmp = []
        for index in range(len(self.harpies)):
            if self.harpies[index].isAlive:
                listatmp.append(self.harpies[index])
        return listatmp

    def get_corpses(self):
        corpses = []
        for index in range(len(self.harpies)):
            if not self.harpies[index].isAlive:
                corpses.append(self.harpies[index])
        return corpses

    def leech_attribute(self, att_name, leech_percent, harpies):
        total_leeched = 0
        for harpy in harpies:
            total_leeched += harpy.decrease_percentage(att_name, leech_percent)
        return total_leeched

    def share_attribute(self, att_name, to_share, harpies):
        share = to_share / float(len(harpies))
        for harpy in harpies:
            harpy.increase_attribute(att_name, share)


    #TODO add background to image using "drawBitmap". I could make a watermark bitmap with the same dimesions
    def generateStatusImage(self, img_str):
        # We open a template image and get its dimensions
        pic = Image.open(IMG + PNG)
        width, height = pic.size

        # We divide the image in 3 columns and as many rows needed
        # to fit al the harpies
        col = width / 3.0
        rows = math.ceil(len(self.harpies) / 3.0)
        row = height / rows

        # We load a drawable object and the font to use
        draw = ImageDraw.Draw(pic)
        font = ImageFont.truetype(FONT, 20)
        draw.rectangle((0, 0, width, height), (255, 255, 255))

        # We calculate starting coordenades to draw every name with a padding (20)
        for i in range(len(self.harpies)):
            x = math.floor(i / rows) * col + 20
            y = i % rows * row + 20

            draw.text((x, y), self.harpies[i].name + ' (' + str(self.harpies[i].kills) + ' kills)', (0, 0, 0),
                      font=font)

            # If the harpy is dead, it crosses it out in red
            if not self.harpies[i].isAlive:
                xl, yl = font.getsize(self.harpies[i].name)
                draw.line((x, y, x + xl, y + yl), (255, 0, 0), 5)
        pic.save(IMG + PNG)

