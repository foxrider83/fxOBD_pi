'''
OBD software using fxlibobd library
The IhmObd class is used to manage the display on console mode.
The ObdInterface is used to manage the car communication.
JSO 2017/10

Application to debug fxlibobd without threading mode.
'''

import os
import sys
import urwid
import fxlibobd #import the module fxlibobd
from threading import Thread

def main():
    #ar = ihmobd()
    jobd = fxlibobd.fxlibOBD()
    jobd.connect()
 
    jobd.askinfo()
    print('vitesse : %s\ncool temp : %s\nairtemp : %s\noil temp : %s' % (jobd.speed, jobd.cool_temp, jobd.air_temp, jobd.oil_temp))
    #end askobd
    jobd.obdclose()
#end main

if (__name__ == '__main__'):
    main()
    sys.exit()
#end if
