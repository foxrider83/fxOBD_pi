#!/usr/bin/python
# -*- coding : UTF-8 -*-
'''
Reset OBD via ATZ serial command
JSO - 27/03/2017
'''

try:
    import sys
    import serial
    import serial.tools.list_ports
    import time
except ImportError:
    print("pyserial is needed")
    exit()

#import threading

#### local class definition ####

class ReceptionSerie():
    '''
    Define base objects for the serial reception.
    '''
    def __init__(self):
        '''
        Constructor ReceptionSerie
        '''
        #Attriute declaration
        self.status = 0
        self.messagerecu = "aucun"
        #Define COM port specific configuration.
        self.__port = serial.Serial()
        self.__port.baudrate = 38400
        self.__port.parity   = serial.PARITY_NONE
        self.__port.stopbits = 1
        self.__port.bytesize = 8
        self.__port.timeout = 1
        
        _p = None
    #end __init__
    
    #def run(self):
        #while(1):
            #x = self.__port.read(100)
            #if (x != ""):
                #Decodage de la trame.
                #self.messagerecu = x
                #print(x)

    def open(self, port):
        '''
        Open the serial port
        :param self: 
        :param port: serial port to open
        '''
        self.__port.port = port
        self.__port.open()
        return

    def read_serial(self):
        '''
        Read serial port and store the result to the messagerecu attribute.
        '''
        if self.__port.isOpen():
            #self.messagerecu = self.__port.readline()
            self.messagerecu = self.__port.read(32)
            print(self.messagerecu)
        else:
            print("Port not open.")

    def write_serial(self, command):
        '''
        Write command on the serial port.
        :param self:
        :param command: the command send on the serial port.
        '''
        command = command + "\r"
        #self.flushTX()
        #self.flushRX()
        self.__port.write(command.encode('utf-8'))
    
#    @staticmethod
    def list_serial(self):
        COM_ports = list(serial.tools.list_ports.comports())
        return COM_ports

    def flushRX(self):
        self.__port.flushInput()
        return

    def flushTX(self):
        self.__port.flushOutput()
        return
        
    def close(self):
        """ Closes the connection """
        self.stop()
        super(Async, self).close()        

############    Definition of the local functions #####################

        
############    Software  #####################
def main():
    lecteur = ReceptionSerie()
    ports = lecteur.list_serial()
    if (len(ports) > 0):
        print("plusieurs ports disponibles")
    else:
        print("Pas de ports de communication serie disponibles")
    #print (ReceptionSerie.port)
    for p in ports:
        print(p)
        #print(p.description)
        #print(p.device)
    #print(ports[0].device)
    print("Selectionner le port a utiliser.")
    print(ports[0][0])
    lecteur.open(ports[0][0])
    lecteur.flushRX()
    lecteur.flushTX()
    print("Envoie des commandes")
    lecteur.write_serial("ATZ")
    time.sleep(1)
    lecteur.read_serial()
    lecteur.close()
#end main

if (__name__ == '__main__'):
    err = main()
    sys.exit(err)
#end if
