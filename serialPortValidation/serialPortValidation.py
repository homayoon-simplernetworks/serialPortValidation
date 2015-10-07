#Simplernetworks

import time
import serial
import colorama
import sys
from pyparsing import *


#to login into ez-edge
def serialLogin():
    global isLogin
    global isLoginStr
    isLogin = False
    ser.write(b'\r')
    while not isLogin:
        line = ser.readline()
        li = line.decode()
        unColorString = nonAnsiString(li)
        nnn = ['1 -' , '2 -' , '3 -' , '4 -' , '5 -' , '6 -', '7 -' , '8 -']
        for nn in nnn: unColorString = unColorString.replace( nn , ' \n' + nn )
        if li.find('Enter number ')>=0 : 
                isLogin=True  #in this stage we expect serial port is logged in successfully 
                isLoginStr = (unColorString )
        print(unColorString )
        sUser = 'admin'
        sPass = 'ez-edge#1'
        #check if asking for user:
        if li.find('User:')>= 0: 
                for l in sUser:
                    ser.write(l.encode('ascii'))
                    #print ('--> ' , l)
                    bLr = ser.read(1)
                    #print('<-- ' , bLr)
                    if not bLr== l.encode('ascii'): break
                ser.write(b'\r')
        elif li.find('Password:')>= 0: 

            for l in sPass:
                    ser.write(l.encode('ascii'))
                    #print ('--> ' , l)
                    time.sleep(0.25)
                    #print('<-- ' , bLr)
            ser.write(b'\r')
        elif li.find('Press any key')>= 0: 
                ser.write(b'\r')
            
            
        

if __name__ == "__main__":


    
    print (
'''
************************************************************************
********************Serial port auto tester*****************************

this program will log in into ez-edge automatically to test serial port
          this test may change settings on your system
           
  do not run this program if you have running services on your system

************************************************************************

''')

    if not input('please confirm you want run the test[y]: ') == 'y' : exit()

    


    # configure the serial connections (the parameters differs on the device you are connecting to)
    port='COM3'
    try:
        ser = serial.Serial(port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout = 1 )

        if not ser.isOpen(): ser.open()

    except :
        print (port + '  is not ready please check the port and try again')
        rr = input('press enter to exit ...')
        exit()

        
    # this part of program will remove the ESC ansi codes from strings 
    ESC = Literal('\x1b')
    integer = Word(nums)
    escapeSeq = Combine(ESC + '[' + Optional(delimitedList(integer,';')) + oneOf(list(alphas)))
    nonAnsiString = lambda s : Suppress(escapeSeq).transformString(s)

    
    
    #login to ez-edge
    serialLogin()
            
    while 1 :
           '''response = ser.readlines()
           
           for li in response:
               unColorString = nonAnsiString(li.decode())
               nnn = ['1 -' , '2 -' , '3 -' , '4 -' , '5 -' , '6 -', '7 -' , '8 -']
               for nn in nnn: unColorString = unColorString.replace( nn , ' \n' + nn )
               print(unColorString ) '''

           li1 = ser.readline()
           
           
           if li1 == b'':
               input1 = input('>> ') 
               ser.write(input1.encode('ascii' , 'replace'))
               rr = ser.read(1)
               #print (rr)
               time.sleep(0.15)
               ser.write(b'\r')
           else :
               li2 = ser.readline()
               unColorString1 = nonAnsiString(li1.decode())
               nnn = ['1 -' , '2 -' , '3 -' , '4 -' , '5 -' , '6 -', '7 -' , '8 -']
               for nn in nnn: unColorString1 = unColorString1.replace( nn , ' \n' + nn )
               if li2 == b'' :
                    input1 = input(unColorString1 + ' >>') 
                    ser.write(input1.encode('ascii' , 'replace'))
                    rr = ser.read(1)
                    #print (rr)
                    time.sleep(0.15)
                    ser.write(b'\r')
               else:
                   unColorString2 = nonAnsiString(li2.decode())
                   for nn in nnn: unColorString2 = unColorString2.replace( nn , ' \n' + nn )            
                   print(unColorString1)
                   print(unColorString2)

           

           
           
           
    ser.close()