#Simplernetworks

import time
import serial
import colorama
import sys
from pyparsing import *
import yld
import orderedYld

 
# prepare time for logger
def timestamp():
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) 

def remTerminalEsc (line):
    readableString = nonAnsiString(line)
    nnn = ['1 -' , '2 -' , '3 -' , '4 -' , '5 -' , '6 -', '7 -' , '8 -']
    for nn in nnn: readableString = readableString.replace( nn , ' \n' + nn )
    return  readableString

def testScriptLoader(scriptFile):
    pass


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

def serialLoginTest(varlist):
    
    
    sUser = varlist[1] 
    sPass= varlist[2] 
    testType= varlist[3]
    logfilepath = varlist[4]
    try :
        id  = varlist[5]
    except:
        id = 'login test---'
    testId = id  + ' --- ' + timestamp()+ ' *** '  + 'test type-->> ' + testType

    global isLoginTest
    isLoginTest = False
    logger = []
    testResault = 'failed'
    badlogin_tried = 1

    #firs logout from anywhere and prepare system for login test
    cPage = gotoPageBackward('anywhere' , 'exit' , '') 

    logger.append(timestamp() +' Login test has been start by sending user <<'+ sUser + '>>  pass <<'+ sPass +'>> and test type is ' + testType )
    print (timestamp() +' Login test has been start by sending user <<'+ sUser + '>>  pass <<'+ sPass +'>> and test type is ' + testType )
    
    while not isLoginTest:
        line = ser.readline()
        li = line.decode()
        
        if li == '' : 
            print('wait for ez-edge connection it may blocked and reply after 60s ...' )
            ser.write(b'\r')
            line = ser.readline()
            li = line.decode()
            
        while li == '' : 
            for ch in [ ' .\  ' , ' .|  ' , ' ./  ' , ' .-- '] :
                    print(ch , end = '\r')
                    time.sleep(0.15)
            ser.write(b'\r')
            line = ser.readline()
            li = line.decode()

        rli = remTerminalEsc(li)
        logger.append( timestamp()+ ' *** ' + rli)
        print (rli)

        # check if Too many invalid login
        if li.find('Too many invalid login')>=0 : 
            print ('please wait')
            for i in range(1,61):
                for ch in [ ' .\  ' , ' .|  ' , ' ./  ' , ' .-- '] :
                    print(ch + str (i) , end = '\r')
                    time.sleep(0.25)
                
                
            ser.write(b'\r')


        #check if asking for user:
        if li.find('User:')>= 0: 
                for l in sUser:
                    ser.write(l.encode('ascii'))
                    bLr = ser.read(1)
                    logger.append( bLr.decode())
                    if not bLr== l.encode('ascii'): 
                        testResault = 'failed'
                        print ('test has failed, program expected << ' + l + ' >>but ez-edge sends << ' + bLr.decode()+ ' >>') 
                        logger.append( timestamp() + ' *** ' +  'test has failed, program expected << ' + l + ' >> but ez-edge sends << ' + bLr.decode() + ' >>')
                        dataForLog = { testId : {'logs' : logger , 'test result' : testResault }}
                        oyf.orderedYaml_append(logfilepath , dataForLog)
                        return testResault 
                ser.write(b'\r')
                lines = ser.readlines()
                for line in lines:
                    li = line.decode()
                    rli = remTerminalEsc(li)
                    print (rli)
                    logger.append( timestamp() + ' *** ' + rli)
                    if li.find('Password:')>= 0: 
                        for l in sPass:
                            ser.write(l.encode('ascii'))
                            #print ('--> ' , l)
                            time.sleep(0.25)
                            #print('<-- ' , bLr)
                        ser.write(b'\r')
                        line = ser.readline()
                        li = line.decode()
                        rli = remTerminalEsc(li)
                        print (rli)
                        logger.append( timestamp() + ' *** ' + rli)
                        while not li == '':
                            if  li.find('EZ-EDGE Local Craft Interface - Main Menu')>=0 : 
                                isLoginTest = True
                                if testType == 'login' : testResault = 'passed'
                                
                            elif li.find('Error: incorrect login')>=0 : 
                                if testType == 'badlogin' : testResault = 'passed'

                            if li.find('Too many invalid login')>=0 : 
                                if testType == 'wait' : testResault = 'passed'
                                print ('program will be reconnect after 60s please wait')
                                for i in range(1,61):
                                    for ch in [ ' .\  ' , ' .|  ' , ' ./  ' , ' .-- '] :
                                        print(ch + str (i) , end = '\r')
                                        time.sleep(0.25)
                                    
                                ser.write(b'\r')

                            line = ser.readline()
                            li = line.decode()  
                            rli = remTerminalEsc(li)  
                            print (rli)
                            logger .append( timestamp() + ' *** ' + rli)
                     
                    
                           
                        if testResault == 'passed' : 
                            print ('test has been passed')
                            logger.append( timestamp() + ' *** ' + 'test passed')
                            dataForLog = { testId : {'logs' : logger , 'test result' : testResault }}
                            oyf.orderedYaml_append(logfilepath , dataForLog)
                            return testResault

                if testType == 'wait' and badlogin_tried<=3 :
                    badlogin_tried = badlogin_tried + 1
                else:
                    print ('test failed,  program expects ' + testType+ ' but es-edge is not, system logged in << '  + str( isLoginTest) + ' >>')
                    testResault = 'failed'
                    logger.append( timestamp() + ' *** ' + 'test failed,  program expects ' + testType+ ' but es-edge is not, system logged in << '  + str( isLoginTest) + ' >>')
                    dataForLog = {testId : {'logs' : logger , 'test result' : testResault }}
                    oyf.orderedYaml_append(logfilepath , dataForLog)
                    return testResault 

        
            
# to find out session of serial connection, if it was logged in initially     
def whereAmI(toWrite = ''):
    knownPage = False
    currentPage = 'unKnown'
    if not toWrite=='' :  ser.write(toWrite.encode('ascii' , 'replace'))
    while not knownPage:
        li = ser.readline()
        if li ==b'' : 
            ser.write(b'\r')
            li = ser.readline()
            
            if li == b'' : print('wait for ez-edge connection it may blocked and reply after 60s ...' )
            while li == b'' :
               for ch in [ ' .\  ' , ' .|  ' , ' ./  ' , ' .-- '] :
                    print(ch  , end = '\r')
                    time.sleep(0.25)
               ser.write(b'\r')
               li = ser.readline()
               
        
        sli  = li.decode()
        for item in serStrc :
            if serStrc[item]['idf'] in sli : 
                    knownPage = True
                    currentPage = item
                    print (item)
    return currentPage

# to logout (please notice that code is intelligent enough to logout from any pages    
def gotoPageBackward(dcurrentPage = 'anywhere' , toPage = 'exit' , mssg = ''):

    # depends on the current page we need different action to logout, each def will provide steps to logout from each page, in future if we add new 
    # pages to LCI, new def should be added here as well as in serialStructure.yaml file
    def notloginLogout():
        return dcurrentPage
    def waitLogout():
        print ('you are logged out because of too many invalid login you need to wait 1 min to be able to reconnect to system (wait please ...)')
        for ch in [ ' .\  ' , ' .|  ' , ' ./  ' , ' .-- '] :
             print(ch  , end = '\r')
             time.sleep(0.25)
        return dcurrentPage

    def badLoginLogout(): 
        return dcurrentPage

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
 
        
# find the path to each page in tree
def structureBrowser (serDic , toPage):
    global forwardTree
    forwardTree = []
    #this recursive function will return the path to each page in tree
    def spider(subSerDic):
        global strcFoundflag
        strcFoundflag = True
        for itm in subSerDic :
            forwardTree.append(itm)
            if subSerDic[itm]['expectedPage'] == toPage : 
                strcFoundflag = False
                return forwardTree
            else: 
                    rSerDic = subSerDic[itm]['PageOptions']
                    if not rSerDic is'0': spider (rSerDic)
                    if strcFoundflag : forwardTree.pop()
                    else : return
        #return 

    spider(serDic)
    return forwardTree
          
# to configuration test 
def configTest(varlist):
    testType = varlist.pop(0)
    toPage = varlist.pop(0)
    id = varlist.pop()
    logfilepath = varlist.pop()
    testId = id  + ' --- ' + timestamp()+ ' *** '  + 'test type-->> ' # + testType


    #first item and last two items in varilist is not parameters 
    paramiteres = varlist
    
    

    logger = []
    logger.append(timestamp() +' Config test start the command is <<'+ str (varlist) + '>>'  )
    print (timestamp() +' Config test start the command is <<'+ str( varlist) + '>>')

    pageNavigator = structureBrowser (serConfStrc , toPage)
    gotoPageBackward('anywhere' , 'mainMenu' , mssg = '') #default value is logout
    line = ser.readline()
    li = line.decode()
    while not li =="" : 
            rli = remTerminalEsc(li)
            logger.append( timestamp()+ ' *** ' + rli)
            print (rli)
            line = ser.readline()
            li = line.decode()

    for page in pageNavigator : 
        ser.write(str ( page).encode('ascii' , 'replace'))
        rr = ser.read(1)
        logger.append(timestamp() +' ' + str (rr) )
        time.sleep(0.15)
        ser.write(b'\r')
        line = ser.readline()
        li = line.decode()
        while not li =="" : 
            rli = remTerminalEsc(li)
            logger.append( timestamp()+ ' *** ' + rli)
            print (rli)
            line = ser.readline()
            li = line.decode()
    
    if 1:
         for page in pageNavigator:
             
             pass

         for par in paramiteres:
             for l in str (par):
                    ser.write(l.encode('ascii'))
                    bLr = ser.read(1)
                    logger.append( bLr.decode())
                    if not bLr== l.encode('ascii'): 
                        testResault = 'failed'
                        print ('test has failed, program expected << ' + l + ' >>but ez-edge sends << ' + bLr.decode()+ ' >>') 
                        logger.append( timestamp() + ' *** ' +  'test has failed, program expected << ' + l + ' >> but ez-edge sends << ' + bLr.decode() + ' >>')
                        dataForLog = { testId : {'logs' : logger , 'test result' : testResault }}
                        oyf.orderedYaml_append(logfilepath , dataForLog)
                        return testResault 
             ser.write(b'\r')
             
             line = ser.readline()
             li = line.decode()
             while not li =="" : 
                rli = remTerminalEsc(li)
                logger.append( timestamp()+ ' *** ' + rli)
                print (rli)
                line = ser.readline()
                li = line.decode()
         testResault = 'pass'
    
    else:
        logger.append(timestamp() +' test failed <<'+ str( varlist) + '>>'  )
        print (timestamp() +' test failed <<'+ str(varlist) + '>>' )
        testResault = 'failed'
    

    dataForLog = {testId : {'logs' : logger , 'test result' : testResault }}
    oyf.orderedYaml_append(logfilepath , dataForLog)
    return testResault 
    



     

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

    #if not input('please confirm you want run the test[y]: ') == 'y' : exit()


    #Parameters and variables
    
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


    #load variables for test 
    sUser = vars['serialUser']
    sPass = vars['serialPass']
    loggerPath = vars['loggerPath']


    #load ez-edge LCI structure
    fStructure = vars['fStructure']
    global serStrc
    serStrc  = yf.yaml_loader(fStructure)
    

    #Load test structure from serialconfigurationTest.yaml
    oyf = orderedYld.orderedYld
    fserconfStrc = vars['fserconfStrc']
    serConfStrc = oyf.orderedYaml_loader(fserconfStrc)
    

    # load test script file name
    scriptFile = vars['scriptFile']
    testScripts = oyf.orderedYaml_loader(scriptFile)
    
    

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

    

    

    theLogFile = loggerPath + 'serialPortTest_'+ timestamp() +'.yaml'
    
    for script in testScripts:
            par = []
            for pa in str (testScripts[script]).split(';'):
                par.append(pa.strip())
            par.append(theLogFile)
            par.append(script)
            
            ################################rem
            pageNavigator = structureBrowser (serConfStrc , par[1])
            print ( pageNavigator)


            eval(par[0])(par)
         
         
        
        
        
        
        
        
        
        
        
        
        
        
        
    # to find out session of serial connection, if it was logged in initially     
    #initialCurrentPage = gotoPageBackward('anywhere' , 'exit' , '')


    #login to ez-edge
    #serialLogin()



    ''''
    theLogFile = loggerPath + 'serialPortTest_'+ timestamp() +'.yaml'
    varlist = (sUser + 'dd',sPass,'login',theLogFile)
    serialLoginTest(varlist)
    varlist = (sUser+'dd',sPass,'badlogin',theLogFile)
    serialLoginTest(varlist)
    varlist = (sUser +'dd',sPass,'badlogin',theLogFile)
    serialLoginTest(varlist)
    varlist = (sUser +'dd' ,sPass + 'dd','badlogin',theLogFile)
    serialLoginTest(varlist)
    varlist = [sUser +'dd',sPass,'badlogin',theLogFile]
    serialLoginTest(varlist)
    testScriptLoader(scriptFile)
  
    while 1 :
           li1 = ser.readline()
           if li1 == b'':
               input1 = input('>> ') 
               ser.write(input1.encode('ascii' , 'replace'))
               rr = ser.read(1)
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
                    time.sleep(0.15)
                    ser.write(b'\r')
               else:
                   unColorString2 = nonAnsiString(li2.decode())
                   for nn in nnn: unColorString2 = unColorString2.replace( nn , ' \n' + nn )            
                   print(unColorString1)
                   print(unColorString2)

    ser.close() '''