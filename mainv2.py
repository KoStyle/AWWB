import pickle
import os
import random
import math
import twython
import datetime
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from twython import Twython
from shutil import copyfile

_IMG = "imagen"
_ARPIOS = "fichero"
_OBJETOS = 'ficheroObj'
_STATUS = 'status'
_TXT = '.txt'
_PNG = '.png'
_FONT = "font.ttf"
_CAFE = 'cafes.txt'
_NA = 'NA'
_TOKENS = 'tokens'


ACCESS_TOKENS_DIC = {'CONSUMER_KEY': _NA, 'CONSUMER_SECRET': _NA, 'ACCESS_KEY': _NA, 'ACCESS_SECRET': _NA}

#TODO ideas:
#Events structure
    #Kills
    #Coffees
    #Draws
    #Love affairs
    #Missed hits
    #Revives
    #Curses (Boost victim selection probability of a player)

#Event randomization

#EasterEggs for certain combinations
    #Neutral Manu

#Support for mentions



class Arpio:
    def __init__(self, name):
        self.name = name
        self.percKill = float(0.7)
        self.percHelp = float(0.5)
        self.percCafe = float(0.05)
        self.percHit = float(0.7)
        self.isAlive = True
        self.kills = int(0)


class Status:
    def __init__(self):
        self.kills = int(0)
        self.year = int(2019)
        self.alive = 0
        self.omedetoo = False
        self.winner = Arpio('N/A')


def readTokens(file):
    f = open(file, 'r', encoding='latin1')
    line = f.readline()
    while line:
        tokenized = line.split('=')
        if ACCESS_TOKENS_DIC.get(tokenized[0].strip()) is None and len(tokenized) == 2:
            ACCESS_TOKENS_DIC[tokenized[0].strip()] = tokenized[1].strip()
        line = f.readline()
    return


def chooseKiller(lista):
    threshold = random.random()
    random.shuffle(lista)
    pot = lista[0].percKill
    i = 0
    while pot < threshold:
        pot = pot + lista[i].percKill
        ++i
    killer = lista[i]
    del lista[i]
    return killer


def readList(file):
    lista = []
    f = open(file, 'r', encoding='latin1')
    line = f.readline()
    while line:
        lista.append(line.strip())
        line = f.readline()

    return lista


def randomKill(lista, objetos):
    listatmp = []
    cafes = readList(_CAFE)
    tweet = ''
    for index in range(len(lista)):
        if lista[index].isAlive:
            listatmp.append(lista[index])

    if len(listatmp) > 1:
        tmpio = chooseKiller(listatmp)
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
                    objeto = 'una navajita random'
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


def printStatusArpios(lista):
    for index in range(len(lista)):
        print(lista[index].name + '-' + str(lista[index].isAlive) + '-' + str(lista[index].kills))


def generateStatusImage(lista):
    pic = Image.open(_IMG + _PNG)
    width, height = pic.size
    col = width / 3.0
    rows = math.ceil(len(lista) / 3.0)
    row = height / rows
    draw = ImageDraw.Draw(pic)
    font = ImageFont.truetype(_FONT, 20)
    draw.rectangle((0, 0, width, height), (255, 255, 255))

    for i in range(len(lista)):
        x = math.floor(i / rows) * col + 20
        y = i % rows * row + 20
        xl, yl = font.getsize(lista[i].name)

        draw.text((x, y), lista[i].name + ' (' + str(lista[i].kills) + ' kills)', (0, 0, 0), font=font)
        if not lista[i].isAlive:
            draw.line((x, y, x + xl, y + yl), (255, 0, 0), 5)
    pic.save(_IMG + _PNG)


def readArpios(file):
    lista = []
    f = open(file, 'r', encoding='latin1')
    line = f.readline()
    while line:
        lista.append(Arpio(line.strip()))
        line = f.readline()
    cantidad = len(lista)
    for i in range(len(lista)):
        lista[i].percKill = 1. / cantidad

    lista.sort(key=lambda x: x.name)
    return lista


def getSurvivors(listar):
    listatmp = []
    tweet = ''
    for index in range(len(listar)):
        if listar[index].isAlive:
            listatmp.append(listar[index])
    return listatmp


def savePickle(file, obj):
    f = open(file, 'wb')
    pickle.dump(obj, f)
    f.close()


def loadPickle(file):
    f = open(file, 'rb')
    listaObj = pickle.load(f)
    f.close()
    return listaObj


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
