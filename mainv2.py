import pickle
import os
import random
import math
import util
from util import read_file
import twython
import datetime
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from twython import Twython
from shutil import copyfile


#TODO ideas:
#Events structure
    #Kills (Done)
    #Coffees (Done)
    #Draws
    #Love affairs
    #Missed hits
    #Revives
    #Curses (Boost victim selection probability of a player)

#Event randomization

#EasterEggs for certain combinations
    #Neutral Manu

#Support for mentions










def randomKill(lista, objetos):
    listatmp = []
    cafes = read_file(util.CAFE)
    tweet = ''
    for index in range(len(lista)):
        if lista[index].isAlive:
            listatmp.append(lista[index])

    if len(listatmp) > 1:
        tmpio = choose_killer(listatmp)
        muerpio = random.choice(listatmp)
        if random.random() < 0.05:  # suicidio 5%
            print(tmpio.name + ' inició su secuencia de autodestrucción con éxito. Enhorabuena! #UnexpectedSkynet')
            tweet = tmpio.name + ' inició su secuencia de autodestrucción con éxito. Enhorabuena! #UnexpectedSkynet'
            muerpio.percKill = tmpio.percKill + muerpio.percKill
            tmpio.isAlive = False
        else:
            if random.random() < 0.025:  # café 2.5%
                print(tmpio.name + ' se ha %s con ' % random.choice(cafes) + muerpio.name + '. La vida sigue.')
                tweet = tmpio.name + ' se ha %s con ' % random.choice(cafes) + muerpio.name + '. La vida sigue.'
            else:
                if len(objetos) >= 1:
                    objeto = random.choice(objetos)
                    objetos.remove(objeto)
                else:
                    objeto = 'con la "Vara de la aleatoreidad"!'
                print(tmpio.name + ' ha matado a ' + muerpio.name + ' %s.' % objeto)
                tweet = tmpio.name + ' ha matado a ' + muerpio.name + ' %s.' % objeto
                muerpio.isAlive = False
                tmpio.percKill = tmpio.percKill + muerpio.percKill
                tmpio.kills = tmpio.kills + 1
        return tweet
    else:
        # Deprecated
        print('Enhorabuena a ' + listatmp[0].name + '! Lo celebraremos en parranda')
        tweet = 'Enhorabuena a ' + listatmp[0].name + '! Lo celebraremos en parranda'
        return tweet




def generateStatusImage(lista):
    pic = Image.open(util.IMG + util.PNG)
    width, height = pic.size
    col = width / 3.0
    rows = math.ceil(len(lista) / 3.0)
    row = height / rows
    draw = ImageDraw.Draw(pic)
    font = ImageFont.truetype(util.FONT, 20)
    draw.rectangle((0, 0, width, height), (255, 255, 255))

    for i in range(len(lista)):
        x = math.floor(i / rows) * col + 20
        y = i % rows * row + 20
        xl, yl = font.getsize(lista[i].name)

        draw.text((x, y), lista[i].name + ' (' + str(lista[i].kills) + ' kills)', (0, 0, 0), font=font)
        if not lista[i].isAlive:
            draw.line((x, y, x + xl, y + yl), (255, 0, 0), 5)
    pic.save(util.IMG + util.PNG)










##script


##TODO I don't remember why was I testing inheritance.... something something participant class?
class Matrioshka:
    def bang(self):
        print("All of this over-")


class Baba(Matrioshka):
    def bang(self):
        print("-a car and-")


class Yaga(Matrioshka):
    def bang(self):
        print("-a fucking puppy")


a = Matrioshka()
b = Baba()
c = Yaga()

lista = []
lista.append(a)
lista.append(b)
lista.append(c)

for i in range(len(lista)):
    lista[i].bang()

# if os.path.isfile(_ARPIOS + _TXT):
#     lista = loadPickle(_ARPIOS + _TXT)
# else:
#     lista = leerArpios('arpios.txt')
#
# if os.path.isfile(_OBJETOS + _TXT):
#     listaObj = loadPickle(_OBJETOS + _TXT)
# else:
#     listaObj = abrirLista('objetos.txt')
#
# if os.path.isfile(_STATUS + _TXT):
#     stats = loadPickle(_STATUS + _TXT)
# else:
#     stats = Status()
#     stats.alive = len(listaVivos(lista))
#
# tweet = ''
# if not stats.omedetoo:
#     tweet = randomKill(lista, listaObj)
#     # printStatusArpios(lista)
#     generaImagenStatus(lista)
#
#     api = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
#     photo = open(imagen, 'rb')
#     image_ids = api.upload_media(media=photo)
#     api.update_status(status=tweet, media_ids=image_ids['media_id'])
#
#     vivos = listaVivos(lista)
#     stats.alive = len(vivos)
#     stats.winner = vivos[0]
#
#     print(stats.alive)
#
#     savePickle(_ARPIOS + _TXT, lista)
#     savePickle(_OBJETOS + _TXT, listaObj)
#     savePickle(_STATUS + _TXT, stats)
#
#     # log
#     now = datetime.datetime.now()
#     copyfile(_ARPIOS + _TXT, 'history/' + _ARPIOS + '_' + now.strftime('%Y%m%d%H%M') + _TXT)
#     copyfile(_IMG + _PNG, 'history/' + _IMG + '_' + now.strftime('%Y%m%d%H%M') + _PNG)
#     copyfile(_OBJETOS + _TXT, 'history/' + _OBJETOS + '_' + now.strftime('%Y%m%d%H%M') + _TXT)
#     copyfile(_STATUS + _TXT, 'history/' + _STATUS + '_' + now.strftime('%Y%m%d%H%M') + _TXT)
#
# if stats.alive == 1 and not stats.omedetoo:
#     print('Omedetoo')
#     stats.omedetoo = True
#     savePickle(_STATUS + _TXT, stats)
#     print(
#         '[Sonido de arranque de Windows XP] Finalmente sabemos quien es el último superviviente. Enhorabuena ' + stats.winner.name + '! Lo celebraremos en parranda! [ENTRANDO EN MODO HIBERNACIÓN]')
#     tweet = '[Sonido de arranque de Windows XP] Finalmente sabemos quien es el último superviviente. Enhorabuena ' + stats.winner.name + '! Lo celebraremos en parranda! [ENTRANDO EN MODO HIBERNACIÓN]'
#     api = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
#     api.update_status(status=tweet)
#
# if stats.omedetoo:
#     print('esto deberia ser lo unico - ' + str(stats.alive))
