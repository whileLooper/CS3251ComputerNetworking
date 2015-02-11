'''
Created on Feb 9, 2015

@author: bo chen
'''
from socket import *
import md5
import sys
import random
import string
from time import sleep
from matplotlib.cbook import Null
from numpy import empty

def main(argv):
    
    debugMode = False
    
    #creating basic simple user information
    userinfo = {'userone':'passwordone', 'usertwo':'passwordtwo', 'userthree':'passwordthree'}
    
    #checking valid input argument
    if len(sys.argv) != 2:
        if len(sys.argv) == 3 and sys.argv[2] != '-d':
            print 'Invalid number of argument'
            sys.exit()
    if len(sys.argv) == 3: debugMode = True
    
    #getting the information from argument
    try:
        port = int(sys.argv[1])
    except:
        print 'Invalid input argument, please enter correct format command.\n' \
            'Example: python server-udp.py 8591'
        sys.exit()
    
    #creating a server UDP socket
    if debugMode: print 'Creating server UDP socket'
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    
    #binding the port to socket
    serverSocket.bind(('', port))
    

    
    #while loop to keep server running
    while 1:
        

        #getting request and client address from client
        if debugMode: print 'Receiving request from client socket'
        sentence, addr = serverSocket.recvfrom(2048)
        
        #generating 64 bit random string
        if sentence == 'Authentication request':
            
            if debugMode: print 'Generating random 64 bit string'
            randomString = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(64))
            #sending random string to client addr
            if debugMode: print 'Sending random string to client socket'
            serverSocket.sendto(randomString, addr)
        
        #receiving client's username and hashcode
        if debugMode: print 'Receiving username and hashcode from client socket'        
        sentence2, addr = serverSocket.recvfrom(2048)

        #split hashcode and username
        index = sentence2.index(':')
        username = sentence2[0:index]
        hashcode = sentence2[index+1:]
        
        password = ''
        #findding corresponding password
        if username in userinfo:
            password = userinfo[username]       
        
        #comparing the mdHash with server mdHash
        if debugMode: print 'Genrating own hashcode and comparing income hashcode'
        mdHash = md5.new()
        mdHash.update(username + password + randomString)
        
        if mdHash.hexdigest() == hashcode:
            print 'Welcome to our service'
            serverSocket.sendto('Y', addr)
        else:
            print 'User authorization failed'
            serverSocket.sendto('N', addr)
        
if __name__ == '__main__':
    main(sys.argv)
