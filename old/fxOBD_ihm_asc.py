'''
Programme de test d'IHM pour OBD.
'''
import sys
import math
import datetime #debug only
import time #debug only
from random import randint #debug only


from asciimatics.effects import Print
from asciimatics.renderers import BarChart, FigletText, DynamicRenderer
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError

import fxobdfiglet

def wv(x):
    #TODO : remplacer par les valeurs OBD.
    if x == 1:
        y = lambda: datetime.datetime.now().timetuple().tm_sec
    elif x == 2:
        y = lambda: datetime.datetime.now().timetuple().tm_min
    elif x == 3:
        y = lambda: datetime.datetime.now().timetuple().tm_hour
    elif x == 4:
        y = lambda: datetime.datetime.now().timetuple().tm_mday
    else:
        y = lambda: 1 + math.sin(math.pi * (2*time.time()+x) / 5)
    return y
#end wv

def demo(screen):
    #self._screen = screen
    scenes = []
    #Taille Rpi avec ecran 3,5" : 60x20
    message = "Resize to 60x20\nActual %sx%s" % (screen.width,screen.height)
    if screen.width != 60 or screen.height != 20:
        effects = [
            Print(screen, FigletText(message),
                  y=screen.height//2-3),
        ]
    else:
        # Rendu permettant l'affichage de l'horloge.
        renderClock = fxobdfiglet.FigletClock(screen.width, screen.height)
        renderExtTemp = fxobdfiglet.FigletExtTemp(screen.width, screen.height)
        renderRPM = fxobdfiglet.FigletRPM(screen.width, screen.height)
        
        #Creation de l'effet (inclusion de plusieurs rendus).
        effects = [
            #Ext Temperature
            Print(screen,
                  BarChart(5, 40, [wv(3)], char="=",
                       gradient=[(12, Screen.COLOUR_GREEN),
                                 (20, Screen.COLOUR_YELLOW),
                                 (24, Screen.COLOUR_RED)],
                       scale=24,
                       intervals=5,
                       labels=True),
                  x=5, y=1, transparent=False, speed=2),     
            Print(screen, FigletText("%s"%screen.width, font=u'lcd'),
                y=1, x= 40),
            #Engine temperature
            Print(screen,
                  BarChart(7, 40, [wv(2)],
                       char="=",
                       gradient=[(20, Screen.COLOUR_GREEN),
                                 (40, Screen.COLOUR_YELLOW),
                                 (60, Screen.COLOUR_RED)],
                       scale=80,
                       intervals=10,
                       labels=False),
                  x=5, y=5, transparent=False, speed=2),
            Print(screen, renderRPM, y=10, x= 40),
            #Affichage de la date et de l heure pb de rafraichissement il faut utiliser le fliglet dynamique.
            Print(screen, renderClock,
                  x=(screen.width)//2-renderClock.max_width, y= screen.height-1),
                  #x=(screen.width-wv(4).__len__())//2, y= screen.height-1),
        ]
    scenes.append(Scene(effects, -1))
    screen.play(scenes, stop_on_resize=True)
#end demo

def main():
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass
        except KeyboardInterrupt:
            print('Bye-Bye')
            return
        #finally:
        #Close the OBD file.
#end main           
        
if (__name__ == '__main__'):
    main()
    sys.exit()
#end if    

