#Simplernetworks

import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(port='COM3',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

if ser.isOpen():
    ser.close()
ser.open()
ser.isOpen()

print ('Enter your commands below.\r\nInsert "exit" to leave the application.')

input1='dsa'
while 1 :
    
        # send the character to the device
        # (note that I happed a \r\n carriage return and line feed to the characters - this is requested by my device)
        input1 = '\r\n'
        ser.write(input1.encode('utf-8'))
        out = ''
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        #time.sleep(5)
        while True:
           response = ser.readline()
           
           print("read data: " , str(response) , response.decode('utf-8','ignore' ) )
           time.sleep(1)
           ser.write(input1.encode('utf-8'))
       
ser.close()