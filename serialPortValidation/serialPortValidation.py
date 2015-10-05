#Simplernetworks

import time
import serial
import colorama
import sys

# configure the serial connections (the parameters differs on the device you are connecting to)
try:
    ser = serial.Serial(port='COM3',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout = 1
    )
except  :
    print (port + '  is not ready please check the port and try again ')

if ser.isOpen():
    ser.close()
ser.open()
ser.isOpen()

print ('Enter your commands below.\r\nInsert "exit" to leave the application.')
#send inter to serial port to start communication with ez-edge
ser.write(b'''\r''')


# this part of program will remove the ESC ansi codes from strings 
from pyparsing import *
ESC = Literal('\x1b')
integer = Word(nums)
escapeSeq = Combine(ESC + '[' + Optional(delimitedList(integer,';')) + 
                oneOf(list(alphas)))
nonAnsiString = lambda s : Suppress(escapeSeq).transformString(s)


def serialLogin():
    global isLogin
    isLogin = False
    while not isLogin:
        response = ser.readlines()
        time.sleep(0.5)       
        for line in response:
            li = line.decode()
            unColorString = nonAnsiString(li)
            print(unColorString )
            #check if asking for user:
            sUser = 'admin'
            sPass = 'ez-edge#1\r\r'
            
            if li.find('User:')>= 0: 
                ser.write(sUser.encode('ascii'))
            elif li.find('Password:')>= 0: 
                ser.write(sPass.encode('ascii'))
                ser.readline()
                ser.write(b'\r')
            elif li.find('Press any key')>= 0: 
                ser.write(b'\r')
            elif li.find('Enter number ')>=0 : isLogin=True
            #else:
                #time.sleep(0.5) 
                #ser.write(b'''\r''')
        if not isLogin: ser.write(b'''\r''')

    
    #in this stage we expect serial port is logged in successfully 
    input1 = input('>> ') 
    ser.write(input1.encode('ascii' , 'replace'))
    #time.sleep(1)
    rr = ser.read()
    time.sleep(0.5)
    ser.write(b'\r')
     



serialLogin()

while 1 :
           response = ser.readlines()
           
           for li in response:
               unColorString = nonAnsiString(li.decode())
               print(unColorString )
           
           input1 = input('>> ') 
           ser.write(input1.encode('ascii' , 'replace'))
           
           rr = ser.read()
           time.sleep(0.5)
           ser.write(b'\r')
           
           
       
ser.close()