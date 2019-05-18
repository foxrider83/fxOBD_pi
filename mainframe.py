'''
Mainframe class for the fxCar software
Part of fxOBD_pi
Foxrider83 - May 2019
'''

from sys import version_info
if version_info[0] < 3:
    import Tkinter as tk
    from Tkinter.messagebox import *
else:
    import tkinter as tk
    #from tkinter.messagebox import *

import fxlibobd
import fxmeter as m
from threading import Thread
import time
import datetime
import random
from os import system


class Mainframe(tk.Frame):
    
    def __init__(self,master,*args,**kwargs):
        self._debugmode = False
        self._fg_val = 'white'
        #self._fg_lbl = '#FFFEFF'
        self._bg = '#000000'
        self._lum = 1.0 #luminosity variable
        valuefont = ('Courier', 12) 
        
        #OBD part
        self.jobd = fxlibobd.fxlibOBD()
        try:
            self.jobd.connect()
            self.jobd.start()
        finally:
            pass
        
        #IHM part
        tk.Frame.__init__(self,master,*args,**kwargs)
        
        self.tempframe = m.Meterframe(self,text = 'T moteur',width = 250,scale = (30,130))
        self.tempframe.grid(row = 0,column = 0, rowspan = 2)
        
        self.frmR2C0 = tk.Frame(self)
        self.frmR2C0.grid(row = 2, column = 0)
        #Luminosity buttons placement.
        tk.Button(self.frmR2C0, text ='Lum-', command = self.lumMin, font = valuefont).pack(side = 'left')
        tk.Button(self.frmR2C0, text ='D/N', command = self.lumAlt, font = valuefont).pack(side = 'left')
        tk.Button(self.frmR2C0, text ='Lum+', command = self.lumPlus, font = valuefont).pack(side = 'left')
        
        #self.lmbtnframe = tk.Frame(self.leftframe)
        #self.lmbtnframe.grid(row = 0, column = 0, sticky = 'N', pady = 10)
        
        self.frmR0C1 = tk.Frame(self)
        self.frmR0C1.grid(row = 0, column = 1, sticky = 'NW')
        self.lblDate = tk.StringVar()
        tk.Label(self.frmR0C1,textvariable = self.lblDate, font = ('Courier', 16)).grid(row = 4,column = 0, columnspan = 2, sticky = 'S')
        self.lblDate.set('dd/MM/yyyy\nhh:mm')
        
        #Text frame for other informations
        self.frmR1C1 = tk.Frame(self)
        self.frmR1C1.grid(row = 1, column = 1, sticky = 'NW')
        
        tk.Label(self.frmR1C1, text = 'Ext Temp').grid(row = 0, column = 0, sticky = 'W')
        self.lblTemp = tk.StringVar()
        lblexttemp = tk.Label(self.frmR1C1, textvariable = self.lblTemp, fg = self._fg_val)
        lblexttemp.grid(row = 0, column = 1, sticky = 'E')
        
        tk.Label(self.frmR1C1, text = 'Speed').grid(row = 1, column = 0, sticky = 'W')
        self.lblSpeed = tk.StringVar()
        lblspeed = tk.Label(self.frmR1C1, textvariable = self.lblSpeed, fg = self._fg_val)
        lblspeed.grid(row = 1, column = 1, sticky = 'E')
        
        tk.Label(self.frmR1C1, text = 'Pres').grid(row = 2, column = 0, sticky = 'W')
        self.lblPressure = tk.StringVar()
        lblpressure = tk.Label(self.frmR1C1, textvariable = self.lblPressure, fg = self._fg_val)
        lblpressure.grid(row = 2, column = 1, sticky = 'E')
        
        tk.Label(self.frmR1C1, text = 'RPM').grid(row = 3, column = 0, sticky = 'W')
        self.lblRPM = tk.StringVar()
        lblrpm = tk.Label(self.frmR1C1, textvariable = self.lblRPM, fg = self._fg_val)
        lblrpm.grid(row = 3, column = 1, sticky = 'E')
        #self.lblConso = tk.StringVar()
        #tk.Label(self.frmR1C1, textvariable = self.lblConso, font = ('Courier', 12)).grid(row = 5, column = 0)
        btnerr = tk.Button(self.frmR1C1, text = 'OBD errors', command = self.showObdErr, font = valuefont)
        #btnerr = tk.Button(self.frmR1C1, text = 'OBD errors', command = showObdError, font = valuefont)
        btnerr.grid(row = 4, column = 0, columnspan = 2)
        
        self.frmR2C1 = tk.Frame(self)
        self.frmR2C1.grid(row = 2, column = 1)
        btnquit = tk.Button(self.frmR2C1,text = 'Quit',width = 15,command = self.stop, font = valuefont)
        btnquit.grid(row = 0,column = 0, pady = 5)
        
        self._thread = Thread(target = self.updateValues)
        self._thread.start()
    #end __init__
        
    def updateValues(self):
        self._active = True
        while(self._active):
            if self._debugmode:
                valOil = random.randint(30,120)
                valCool = random.randint(30,120)
                valInTemp = random.randint(-30,50)
            else:
                valOil = self.jobd.oilTemp_value
                valCool = self.jobd.coolTemp_value
                valInTemp = self.jobd.intakeTemp_value
            #Update the IHM.
            self.tempframe.setmeter(int(valOil), int(valCool), int(valInTemp))
            #Update labels values
            self.lblRPM.set('%s' % (self.jobd.rpm_value))
            self.lblSpeed.set('%s %s' % (self.jobd.speed_value, self.jobd.speed_unit))
            self.lblPressure.set('%s %s' % (self.jobd.pressure_value, self.jobd.pressure_unit))
            self.lblTemp.set('%s %s' % (self.jobd.airTemp_value, self.jobd.airTemp_unit))
            #self.lblConso.set('%s %s' % (self.jobd.conso_value, self.jobd.conso_unit))
            #print('%s %s %s' % (valOil, valCool, valAmb))
            
            date = datetime.datetime.now()
            #self.lblDate.set('%s' % (date.isoformat()))
            self.lblDate.set('%s' % (date.strftime('%d/%m/%Y\n%H:%M')))
            time.sleep(2)
    #end updateValues
    def setdebugmode(self, value):
        self._debugmode = value
        
    def lumPlus(self):
        if self._lum < 1.0:
            self._lum += 0.1
        self.setLum()
    #end lumPlus
    
    def lumMin(self):
        if self._lum > 0.2:
            self._lum -= 0.1
        self.setLum()
    #end lumMin
    
    def lumAlt(self):
        if self._lum <= 0.5:
            self._lum = 1.0
        else:
            self._lum = 0.5
        self.setLum()
    #end lumAlt
        
    def setLum(self):
        #ASUS eeePC
        #system('xrandr --output DVI-I-1 --brightness %s' % (self._lum))
        #M15x
        system('xrandr --output LVDS-1 --brightness %s' % (self._lum))
        #RPi
        #system('echo %s > /sys/class/backlight/rpi_backlight/brightness' % (self.lum))
    #end setLum
        
    def stop(self):
        #print('bye bye')
        try:
            #Stop the thread
            self.jobd.stop()
            #print('OBD thread stopped')
            #wait the end of the thread
            self.jobd.join()
            #print('OBD thread joined')
            #close OBD connection
            self.jobd.obdclose()
            #print('Closing OBD connection')
        #end try
        except:
            pass
        self._active = False
        #print('Destroy master')
        self.master.destroy()
    #end stop
    
    def showObdErr(self):
        #showinfo('OBD errors', 'no OBD errors')
        showObdError(self).pack()
        
#end Mainframe
