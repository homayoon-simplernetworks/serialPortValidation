#Simplernetworks

import time
import serial
import colorama
import sys
from pyparsing import *
import yld
import orderedYld


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
            
# to find out session of serial connection, if it was logged in initially     
def whereAmI(toWrite):
    knownPage = False
    currentPage = 'unKnown'
    if not toWrite=='' :  ser.write(toWrite.encode('ascii' , 'replace'))
    while not knownPage:
        li = ser.readline()
        if li ==b'' : ser.write(b'\r')
        else :
            sli  = li.decode()
            for item in serStrc :
                if serStrc[item]['idf'] in sli : 
                    knownPage = True
                    currentPage = item
                    print (item)
    return currentPage

# to logout (please notice that code is intelligent enough to logout from any pages    
def gotoPageBackward(dcurrentPage , toPage , mssg):

    # depends on the current page we need different action to logout, each def will provide steps to logout from each page, in future if we add new 
    # pages to LCI, new def should be added here as well as in serialStructure.yaml file
    def notloginLogout():
        return dcurrentPage
    def waitLogout():
        print ('you are log out but because of too many invalid login you need to wait 1 min to be able to reconnect to system (wait please ...)')
        for i in range(1,60):
            print('*' , end = '')
            time.sleep(1)
        return 'notlogin'

    def badLoginLogout(): 
        return 'notlogin'

    def returnLogout(rreturnCode):
        ifany = ser.readlines() #to make sure LCI finished sending and it is ready to receive new command
        ser.write(rreturnCode.encode('ascii' , 'replace'))
        rr = ser.read(1)
        time.sleep(0.15)
        #ser.write(b'\r')
        gotoPageBackward('anywhere' , toPage , '\r')
        

    
    try :
        #anywhere is used for mention that program does not know or could not be sure where is it in LCI
        if dcurrentPage == 'anywhere' : dcurrentPage =  whereAmI(mssg)

        returnCode = serStrc[dcurrentPage]['returnCode']
        #if we use pass of the day debug menu will be added to menu, therefore we need to add 1 to return code
        if passOfDay and dcurrentPage == 'mainMenu' : returnCode = returnCode + 1

        #this line will check if we are in requested page or not
        if toPage == dcurrentPage : return dcurrentPage
        elif dcurrentPage == 'mainMenu' and  not toPage=='exit':  #and condition is extra, has been added for readability of code
            return dcurrentPage

        if  returnCode<400 : 
            returnLogout(str(returnCode))
            return
        elif returnCode<500 : 
            gotoPageBackward('anywhere' , toPage , '\r')
            return
        
        eval(dcurrentPage + 'Logout')()
    except  Exception as err:
        print('the (' + dcurrentPage +') item in serialStructure.yaml file is not implemented in code. program will act as unknown page ' , err) 
        currentPage = 'unknown'
 
        

           
# to configuration test 
def confTest():
    pass



     

if __name__ == "__main__":

    print (
'''
************************************************************************
*            Simpler Networks system test automation                   *
*                    Serial port auto tester                           *
************************************************************************

this program will log in into ez-edge automatically to test serial port
          this test may change settings on your system
           
  do not run this program if you have running services on your system

************************************************************************

''')

    if not input('please confirm you want run the test[y]: ') == 'y' : exit()


    #Parameters
    
    global passOfDay
    passOfDay = False

    # load parameters from yaml files

    #load serial port variables 
    fVariables = "variables.yaml"
    yf = yld.yld
    vars = yf.yaml_loader(fVariables)
      
    port= vars['port'].strip()
    baudrate = vars['baudrate']
    parity =  vars['parity']      #serial.PARITY_NONE
    stopbits = vars['stopbits']   #serial.STOPBITS_ONE
    bytesize = vars['bytesize']     #serial.EIGHTBITS
    timeout = vars['timeout']


    #load ez-edge LCI structure
    fStructure = vars['fStructure']
    global serStrc
    serStrc  = yf.yaml_loader(fStructure)
    

    #Load test structure from serialconfigurationTest.yaml
    oyf = orderedYld.orderedYld
    fserconfStrc = vars['fserconfStrc']
    serConfStrc = oyf.orderedYaml_loader(fserconfStrc)
    



    # this part of program will remove the ESC ansi codes from strings 
    ESC = Literal('\x1b')
    integer = Word(nums)
    escapeSeq = Combine(ESC + '[' + Optional(delimitedList(integer,';')) + oneOf(list(alphas)))
    nonAnsiString = lambda s : Suppress(escapeSeq).transformString(s)

    # opening the serial port 
    try:
        ser = serial.Serial(port,
            baudrate,
            bytesize,
            parity ,
            stopbits ,            
            timeout )
        

        if not ser.isOpen(): ser.open()

    except  ValueError as err :
        print(" please check and modify variables.yaml : {0}".format(err))
        
        rr = input('press enter to exit ...')
        exit()

    except   :
        print (port + '  is not ready please check the port and try again  ' )
        rr = input('press enter to exit ...')
        exit()

    # to find out session of serial connection, if it was logged in initially     
    gotoPageBackward('anywhere' , 'wtert' , '')


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