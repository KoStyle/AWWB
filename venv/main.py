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

_IMG="imagen"
_ARPIOS="fichero"
_OBJETOS='ficheroObj'
_STATUS='status'
_TXT='.txt'
_PNG='.png'
_FONT="font.ttf"
_CAFE='cafes.txt'

CONSUMER_KEY = 'FneOC7OhVe56rmKsI18j9N27q'
CONSUMER_SECRET = 'oWr1yvmOh4XMcbwbvVrmxEeKJPps07tGWQSPrRg2Dmj2ViUdE2'
ACCESS_KEY = '1148576729021263873-uGxriRhJPPh7Gzt92bUpZi1KQNWVBy'
ACCESS_SECRET = 'adnhTNH0YXibyjK6XkW9xxpBiDZS60pkYU2cWsf21EvF0'

class Arpio:
    def __init__(self, name):
        self.name = name
        self.percKill = float(0.7)
        self.percHelp = float(0.5)
        self.percCafe = float(0.05)
        self.percHit = float(0.7)
        self.isAlive= True
        self.kills = int(0)

class Status:
    def __init__(self):
        self.kills= int(0)
        self.year= int(2019)
        self.alive=0
        self.omedetoo=False
        self.winner=Arpio('N/A')

def chooseKiller(lista):
    threshold= random.random()
    random.shuffle(lista)
    pot=lista[0].percKill
    i=0
    while(pot<threshold):
        pot=pot+lista[i].percKill
        ++i
    killer = lista[i]
    del lista[i]
    return killer

def abrirLista(file):
    lista = []
    f = open(file, 'r', encoding='latin1')
    line = f.readline()
    while line:
        lista.append(line.strip())
        line = f.readline()

    return lista

def randomKill(lista, objetos):
    listatmp=[]
    cafes=abrirLista(_CAFE)
    tweet=''
    for index in range(len(lista)):
        if (lista[index].isAlive):
            listatmp.append(lista[index])

    if(len(listatmp)>1):
        tmpio =chooseKiller(listatmp)
        muerpio = random.choice(listatmp)
        if(random.random()<0.05): #suicidio 5%
            print(tmpio.name + ' inició su secuencia de autodestrucción con éxito. Enhorabuena! #UnexpectedSkynet')
            tweet=tmpio.name + ' inició su secuencia de autodestrucción con éxito. Enhorabuena! #UnexpectedSkynet'
            muerpio.percKill=tmpio.percKill + muerpio.percKill
            tmpio.isAlive=False
        else:
            if(random.random()<0.025): #café 2.5%
                print(tmpio.name + ' se ha %s con ' % random.choice(cafes) + muerpio.name + '. La vida sigue.')
                tweet=tmpio.name + ' se ha %s con ' % random.choice(cafes) + muerpio.name + '. La vida sigue.'
            else:
                if(len(objetos)>=1):
                    objeto=random.choice(objetos)
                    objetos.remove(objeto)
                else:
                    objeto='una navajita random'
                print(tmpio.name + ' ha matado a ' + muerpio.name +' %s.' % objeto)
                tweet=tmpio.name + ' ha matado a ' + muerpio.name +' %s.' % objeto
                muerpio.isAlive=False
                tmpio.percKill=tmpio.percKill + muerpio.percKill
                tmpio.kills= tmpio.kills +1
        return tweet
    else:
        #Deprecated
        print('Enhorabuena a ' + listatmp[0].name + '! Lo celebraremos en parranda')
        tweet='Enhorabuena a ' + listatmp[0].name + '! Lo celebraremos en parranda'
        return tweet

def printStatusArpios(lista):
    for index in range(len(lista)):
        print (lista[index].name + '-' + str(lista[index].isAlive) + '-' + str(lista[index].kills))

def generaImagenStatus(lista):
    pic= Image.open(_IMG+_PNG)
    width, height = pic.size
    col=width/3.0
    rows=math.ceil(len(lista)/3.0)
    row=height/rows
    draw = ImageDraw.Draw(pic)
    font = ImageFont.truetype(_FONT, 20)
    draw.rectangle((0,0, width, height), (255,255,255))

    for i in range(len(lista)):
        x=math.floor(i/rows)*col +20
        y=i%rows*row+20
        xl, yl= font.getsize(lista[i].name)

        draw.text((x, y), lista[i].name + ' (' + str(lista[i].kills) + ' kills)', (0,0,0), font=font)
        if(lista[i].isAlive==False):
            draw.line((x, y,x+xl, y+yl ),(255, 0, 0), 5)
    pic.save(_IMG+_PNG)

def leerArpios(file):
    lista= []
    f= open(file, 'r', encoding='latin1')
    line=f.readline()
    while line:
        lista.append(Arpio(line.strip()))
        line = f.readline()
    cantidad=len(lista)
    for i in range(len(lista)):
        lista[i].percKill=1./cantidad

    lista.sort(key=lambda x: x.name)
    return lista

def listaVivos(lista):
    listatmp = []
    tweet = ''
    for index in range(len(lista)):
        if (lista[index].isAlive):
            listatmp.append(lista[index])
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

if(os.path.isfile(_ARPIOS+_TXT)):
    lista=loadPickle(_ARPIOS+_TXT)
else:
    lista=leerArpios('arpios.txt')

if(os.path.isfile(_OBJETOS+_TXT)):
    listaObj=loadPickle(_OBJETOS+_TXT)
else:
    listaObj=abrirLista('objetos.txt')

if(os.path.isfile(_STATUS+_TXT)):
    stats=loadPickle(_STATUS+_TXT)
else:
    stats= Status()
    stats.alive=len(listaVivos(lista))

tweet=''
if(not(stats.omedetoo)):
    tweet=randomKill(lista, listaObj)
    #printStatusArpios(lista)
    generaImagenStatus(lista)

    api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
    photo = open(imagen,'rb')
    image_ids = api.upload_media(media=photo)
    api.update_status(status=tweet, media_ids=image_ids['media_id'])

    vivos=listaVivos(lista)
    stats.alive=len(vivos)
    stats.winner=vivos[0]

    print(stats.alive)

    savePickle(_ARPIOS+_TXT, lista)
    savePickle(_OBJETOS+_TXT, listaObj)
    savePickle(_STATUS+_TXT, stats)

    # log
    now = datetime.datetime.now()
    copyfile(_ARPIOS + _TXT, 'history/' + _ARPIOS + '_' + now.strftime('%Y%m%d%H%M') + _TXT)
    copyfile(_IMG + _PNG, 'history/' + _IMG + '_' + now.strftime('%Y%m%d%H%M') + _PNG)
    copyfile(_OBJETOS + _TXT, 'history/' + _OBJETOS + '_' + now.strftime('%Y%m%d%H%M') + _TXT)
    copyfile(_STATUS + _TXT, 'history/' + _STATUS + '_' + now.strftime('%Y%m%d%H%M') + _TXT)

if(stats.alive==1 and not(stats.omedetoo)):
    print('Omedetoo')
    stats.omedetoo=True
    savePickle(_STATUS+_TXT, stats)
    print('[Sonido de arranque de Windows XP] Finalmente sabemos quien es el último superviviente. Enhorabuena ' + stats.winner.name + '! Lo celebraremos en parranda! [ENTRANDO EN MODO HIBERNACIÓN]')
    tweet='[Sonido de arranque de Windows XP] Finalmente sabemos quien es el último superviviente. Enhorabuena ' + stats.winner.name + '! Lo celebraremos en parranda! [ENTRANDO EN MODO HIBERNACIÓN]'
    api = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
    api.update_status(status=tweet)

if(stats.omedetoo):
    print('esto deberia ser lo unico - ' + str(stats.alive))










