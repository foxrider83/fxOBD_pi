'''
OBD software using pip obd library
Application to test the physical connection.
JSO 2017/10
'''
import obd
import sys

def main():
    #connection = obd.OBD() # auto-connects to USB or RF port
    connection = obd.OBD("/dev/ttyUSB0")
    #TODO : Verify if the connection is available.
    if (connection.is_connected()):
        cmd = obd.commands.SPEED # select an OBD command (sensor)
        response = connection.query(cmd) # send the command, and parse the response
        print(response.value) # returns unit-bearing values thanks to Pint
        
        cmd = obd.commands.COOLANT_TEMP
        response = connection.query(cmd)
        print(response.value)
        #print(response.value.to("mph")) # user-friendly unit conversions
        cmd = obd.commands.AMBIANT_AIR_TEMP
        response = connection.query(cmd)
        print(response.value)
        
        cmd = obd.commands.OIL_TEMP
        response = connection.query(cmd)
        print(response.value)
        
        if (connection.is_connected()):
            connection.close()
#end main

if (__name__ == '__main__'):
    main()
    sys.exit()
#end if
