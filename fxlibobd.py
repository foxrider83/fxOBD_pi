'''
OBD software using pip obd library
This library need to convert data to usable (string to integer).
JSO 2017/10
'''
from threading import Thread
import time

import obd
#import sys

class fxlibOBD(Thread):
    #global connection 
     
    def __init__(self):
        self.speed_value = 0 #SPEED
        self.speed_unit = '-'
        self.airTemp_value = 0 #AMBIANT_AIR_TEMP
        self.airTemp_unit = '-'
        self.coolTemp_value = 0 #COOLANT_TEMP
        self.coolTemp_unit = '-'
        self.oilTemp_value = 0 #OIL_TEMP
        self.oilTemp_unit = '-'
        self.intakeTemp_value = 0 #INTAKE_TEMP
        self.intakeTemp_unit = '-'
        self.pressure_value = 0 #BAROMETRIC_PRESSURE
        self.pressure_unit = '-'
        self.voltage_value = 0 #CONTROL_MODULE_VOLTAGE
        self.voltage_unit = '-'
        self.rpm_value = 0 #RPM
        self.rpm_unit = '-'
        self.conso_value = 0 #FUEL_RATE
        self.conso_unit = '-'
        self.carerror = None
        self.numerror = 0 #number of OBD error
        self.connection = False
        self._active = False
        self.comerr = False
        
        Thread.__init__(self)
    #end ___init___
    
    def run(self):
        '''Threading actions'''
        self._active = True
        while(self._active):
            if (self.connection.is_connected()):
                self.askinfo()
                time.sleep(1)
            #end while
    #end run
    
    def stop(self):
        '''Stop the thread'''
        self._active = False
    
    def connect(self, port='/dev/ttyUSB0'):
        '''Permit to connect to the OBD interface'''
        #connection = obd.OBD() # auto-connects to USB or RF port
        self.connection = obd.OBD(port)
    #end connect
    
    def is_connected(self):
        return self.connection.is_connected()
    #end is_connected
    
    def reconnect(self):
        '''Reconnect the OBD interface on multiple timeout answer'''
        #Run the low level ATZ command. Possibility to use the serial object ?
    #end reconnect
    
    def obdclose(self):
        self.connection.close()
    #end close
    
    def get_speed(self):
        '''This function ask for current speed. '''
        if (self.connection.is_connected()):
            cmd = obd.commands.SPEED # select an OBD command (sensor)
            self.cmd_resp = self.connection.query(cmd) # send the command, and parse the response
            (self.speed_value, self.speed_unit) = self.response_split(self.cmd_resp)
    #end get_speed
    
    def get_air_temp(self):
        if (self.connection.is_connected()):
            cmd = obd.commands.AMBIANT_AIR_TEMP
            self.cmd_resp = self.connection.query(cmd)
            (self.airTemp_value, self.airTemp_unit) = self.response_split(self.cmd_resp)
    #end get_air
            
    def get_oil_temp(self):
        if (self.connection.is_connected()):
            cmd = obd.commands.OIL_TEMP
            self.cmd_resp = self.connection.query(cmd)
            (self.oilTemp_value, self.oilTemp_unit) = self.response_split(self.cmd_resp)
    #end get_oil

    def get_cool_temp(self):
        if (self.connection.is_connected()):
            cmd = obd.commands.COOLANT_TEMP
            self.cmd_resp = self.connection.query(cmd)
            (self.coolTemp_value, self.coolTemp_unit) = self.response_split(self.cmd_resp)
    #end get_cool_temp
    
    def get_voltage(self):
        if (self.connection.is_connected()):
            cmd = obd.commands.CONTROL_MODULE_VOLTAGE
            self.cmd_resp = self.connection.query(cmd)
            (self.voltage_value, self.voltage_unit) = self.response_split(self.cmd_resp)
    #end get_voltage
    
    def get_pressure(self):
        if (self.connection.is_connected()):
            cmd = obd.commands.BAROMETRIC_PRESSURE
            self.cmd_resp = self.connection.query(cmd)
            (self.pressure_value, self.pressure_unit) = self.response_split(self.cmd_resp)
    #end get_pressure
    
    def get_intake_temp(self):
        if (self.connection.is_connected()):
            cmd = obd.commands.INTAKE_TEMP
            self.cmd_resp = self.connection.query(cmd)
            (self.intakeTemp_value, self.intakeTemp_unit) = self.response_split(self.cmd_resp)
    #end get_intake_temp
    
    def get_rpm(self):
        '''This function ask for current RPM. '''
        if (self.connection.is_connected()):
            cmd = obd.commands.RPM # select an OBD command (sensor)
            self.cmd_resp = self.connection.query(cmd) # send the command, and parse the response
            (self.rpm_value, self.rpm_unit) = self.response_split(self.cmd_resp)
    #end get_rpm

    def get_conso(self):
        '''This function ask for consumption. '''
        ''' TODO debug the response '''
        if (self.connection.is_connected()):
            cmd = obd.commands.FUEL_RATE # select an OBD command (sensor)
            self.cmd_resp = self.connection.query(cmd) # send the command, and parse the response
            #(self.conso_value, self.conso_unit) = self.response_split(self.cmd_resp)
            self.conso.value = self.cmd.resp
    #end get_conso
    
    def get_carerror(self):
        '''Get the vehicule error codes.'''
        if(self.connection.is_connected()):
            cmd = obd.commands.GET_DTC
            self.carerror = self.connection.query(cmd)
            try:
                self.numerror = len(self.carerror)
            except:
                self.numerror = 0
                pass
    
    def response_split(self, response):
        '''Split the OBD response to Value, Unit tuple.'''
        try:
            response_str = str(response)
            response_value = response_str.split(' ')[0]
            response_unit = response_str.split(' ')[1]
            self.comerr = False
        except:
            response_value = 0
            response_unit = '-'
            self.comerr = True
            pass
        return (response_value, response_unit)
    #end response_split
    
    def askinfo(self):
        '''this function collect all OBD informations'''
        self.get_speed()
        self.get_rpm()
        self.get_air_temp()
        self.get_cool_temp()
        self.get_oil_temp()
        self.get_intake_temp()
        self.get_pressure()
        #self.get_conso()
        self.get_voltage()
        self.get_pressure()
        self.get_carerror()
    #end askinfo
#end fxOBD
