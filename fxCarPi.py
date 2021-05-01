#!/usr/bin/env python
# -*- coding:Utf-8 -*-
'''
fxCarPi.py
Version 1.0 - Jan 2019
Final software for Pi Car Computer
written by Jeff Salvo
'''

'''
TODO : Ajouter l'affichage du nombre d'erreur
En faire un bouton
Lorsque l'on sélectionne ce bouton, afficher la lister des erreurs. 
La méthode avec un dialog box n'est pas bonne car elle utilise le theme du bureau.
Ajouter une fenêtre
'''

from sys import version_info
if version_info[0] < 3:
    import Tkinter as tk
    from Tkinter.messagebox import *
else:
    import tkinter as tk
    #from tkinter.messagebox import *

import sys
import argparse
#from os import system
#import fxmeter as m
#import random
#from threading import Thread
#import time
import datetime
#import fxlibobd
import mainframe
import logging

#Global variable declaration space
debugmode = False
fullscreen = False
tactil = False
verbose = False
log = False

class App(tk.Tk):
    def __init__(self):
        logging.info('Démarrage de l\'application')
        tk.Tk.__init__(self)
        self.title('fxCarPi - New Car Computer')
        if tactil:
            self.config(cursor = 'none')
        #self.geometry('400x319+1+1')
        #default_font = tkFont.nametofont('TkDefaultFont')
        default_font = tk.font.nametofont('TkDefaultFont')
        default_font.configure(family='courier', size='16')
        self.option_add('*Font', default_font)
        self.tk_setPalette(background='#000000', foreground='green2',
                            activeBackground='green2', activeForeground='#000000')

        mf = mainframe.Mainframe(self)
        print('debugmode set')
        if fullscreen:
            self.attributes('-fullscreen', True)
        mf.setscreenmode(fullscreen, tactil)
        mf.setdebugmode(debugmode)
        mf.pack()
        logging.info('Extinction de l\'application')
#end App

def main():
    App().mainloop()
    
if (__name__ == '__main__'):
    #Get the transmitted arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action = 'store_true', help = 'augmente la verbosité')
    parser.add_argument('-l', '--log', action = 'store_true', help = 'active le mode log')
    parser.add_argument('-d', '--debug', action='store_true', help='debug mode')
    parser.add_argument('-f', '--fullscreen', action='store_true', help='fullscreen mode')
    parser.add_argument('-t', '--tactil', action='store_true', help='tactil mode,no cursor')
    args = parser.parse_args()
    #Set software configuration
    if args.debug:
        debugmode = True
    if args.fullscreen:
        fullscreen = True
    if args.tactil:
        tactil = True
    if args.verbose:
        verbose = True
    logfilename = datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '_fxcar.log'
    logformat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    if args.log:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARNING

    if version_info[0] == 3 and version_info[1] >= 9:
        logging.basicConfig(filename=logfilename, level=loglevel, format = logformat, encoding='UTF-8')
    else:
        logging.basicConfig(filename=logfilename, level=loglevel, format = logformat)
    
    sys.exit(main())
#end if
