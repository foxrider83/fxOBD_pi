#!/usr/bin/env python
# -*- coding:Utf-8 -*-
"""
OBD software using fxlibobd library and threading
The IhmObd class is used to manage the display on console mode.
The ObdInterface is used to manage the car communication.
JSO 2018/04

Application to debug fxlibobd with threading mode.
"""

import os
import sys
import argparse #import the argument parser module
import time
import fxlibobd #import the module fxlibobd
from threading import Thread
from subprocess import call

#Global variables definition


# define our clear function 
def clear(): 
    """Clear Screen function"""
    # for windows 
    if os.name == 'nt': 
        call('cls', shell = True) 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        call('clear', shell = True) 
#end clear

def main():
    fichier = open("/tmp/fxobd.dat","w")
    try:
        #ar = ihmobd()
        jobd = fxlibobd.fxlibOBD()
        #connect the OBD sensor
        jobd.connect()
        #start the thread
        jobd.start()
         
        while True:
            fichier.seek(0)
            clear()
            message = 'vitesse : %s %s\n' % (jobd.speed_value, jobd.speed_unit)
            message += 'cool temp : %s %s\t' % (jobd.coolTemp_value, jobd.coolTemp_unit)
            message += 'oil temp : %s %s\n' % (jobd.oilTemp_value, jobd.oilTemp_unit)
            message += 'air temp : %s %s\n' % (jobd.airTemp_value, jobd.airTemp_unit)
            message += 'pressure : %s %s\n' % (jobd.pressure_value, jobd.pressure_unit)
            fichier.write(message)
            if args.verbose:
                print(message)
            fichier.flush()
            time.sleep(1)
    except KeyboardInterrupt:
        message = 'Program End'
        fichier.write(message)
        if args.verbose:
            print(message)  
    finally:
        #end askobd
        #Stop the thread
        jobd.stop()
        #wait the end of the thread
        jobd.join()

        #close OBD connection
        message = 'OBD connection closed'
        fichier.write(message)
        if args.verbose:
            print(message)
        jobd.obdclose()
        fichier.close()
#end main

if (__name__ == '__main__'):
    #Get the transmitted arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true", help = "augmente la verbosité")
    parser.add_argument("-l", "--log", action = "store_true", help = "active le mode log")
    args = parser.parse_args()
    
    main()
    sys.exit()
#end if
