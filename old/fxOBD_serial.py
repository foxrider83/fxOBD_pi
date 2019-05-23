#!/usr/bin/python
# -*- coding : ASCII -*-
#Programme de test sur les ports serie
#JSO - 27/03/2017

try:
    import sys
    import serial
    import serial.tools.list_ports
except ImportError:
    print('pyserial is needed')
    exit()

#import threading

#### Definition de la classe local ####
class ReceptionSerie():
    
    def __init__(self):
        #Attriute declaration
        self.status = 0
        self.messagerecu = 'aucun'
        #Define COM port specific configuration.
        self.__port = serial.Serial()
        self.__port.baudrate = 38400
        self.__port.parity   = serial.PARITY_NONE
        self.__port.stopbits = 1
        self.__port.bytesize = 8
        self.__port.timeout = 10
        
        _p = None

    def run(self):
        while(1):
            x = self.__port.read(100)
            if (x != ''):
                #Decodage de la trame.
                self.messagerecu = x
                print(x)

    def open(self, port):
        self.__port.port = port
        self.__port.open()
        return

    def read_serial(self):
        if self.__port.isOpen():
            self.messagerecu = self.__port.readline()
            print(self.messagerecu)
        else:
            print('Port %s not open.' %(self._port.name))

    def write_serial(self, command):
        command = command + '\r\n'
        self.__port.write(command.encode('utf-8'))
    
#   @staticmethod
    def list_serial(self):
        COM_ports = list(serial.tools.list_ports.comports())
        return COM_ports

    def flushRX(self):
        self.__port.flushInput()
        return

    def flushTX(self):
        self.__port.flushOutput()
        return

#### Definition des fonctions locales ####
        
#### Programme ####
def main():
    lecteur = ReceptionSerie()
    ports = lecteur.list_serial()
    if (len(ports) > 0):
        print('plusieurs ports disponibles')
    else:
        print('Pas de ports de communication serie disponibles')
        quit()
    #print (ReceptionSerie.port)
    for p in ports:
        print(p)
        #print(p.description)
        #print(p.device)
    #print(ports[0].device)
    print('Selectionner le port a utiliser.')
    print(ports[0][0])
    lecteur.open(ports[0][0])
    #Reset all
    print('sending reset comand')
    lecteur.write_serial('ATZ')
    lecteur.read_serial()
    #Read the ELM version
    #print('Sending command ATI')
    #lecteur.write_serial('ATI')
    #lecteur.read_serial()
    #Read ELM327 Voltage
    print('Sending command ATRV')
    lecteur.write_serial('ATRV')
    lecteur.read_serial()
    #Remove Echo
    print('Sending command ATE0')
    lecteur.write_serial('ATE0')
    lecteur.read_serial()
    #Enable headers
    print('sending command ATH1')
    lecteur.write_serial('ATH1')
    lecteur.read_serial()
    #Disable LF after CR
    lecteur.write_serial('ATL0')
    lecteur.read_serial()
    #Automatic protocol selection
    print('Sending command ATSP0')
    lecteur.write_serial('ATSP0')
    lecteur.read_serial()
    #Monitor all command
    print('Sending command ATMA')
    lecteur.write_serial('ATMA')
    while(1):
        lecteur.read_serial()

if (__name__ == '__main__'):
    sys.exit(main())
    

