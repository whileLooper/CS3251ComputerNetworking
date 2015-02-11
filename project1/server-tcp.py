'''
Created on Feb 9, 2015

@author: bo chen
'''
from _socket import *
import sys
import random
import md5
import string
    
def serverTCP(argv):

    debugMode = False
    
    #creating basic simple user information
    userinfo = {'userone':'passwordone', 'usertwo': 'passwordtwo', 
                'userthree': 'passwordthree'}
    #checking valid arguments
    if len(sys.argv) != 2:
        if len(sys.argv) == 3 and sys.argv[2] != '-d':
            print("Invalid input argument")
            sys.exit()
    
    if len(sys.argv) == 3: debugMode = True
    
    #getting the port number from argument
    try:
        serverPort = int(sys.argv[1])
    except:
        print 'Invalid input argument, please enter correct format command.\n' \
            'Example: python server-tcp.py 8591'
        sys.exit()    
    #creating the TCP server socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    if debugMode: print 'Creating TCP server socket.'
    
    #binding the port with socket
    serverSocket.bind(('', serverPort))
    
    #setting the default queue connection 
    serverSocket.listen(10)
    
    #while loop to keep server keep running
    while 1:
        randomString = ''
        #creating socket in the server to particular client 
        connectionSocket, addr = serverSocket.accept()
        if debugMode: print 'Server-tcp connected to client'
        
        #TCP connection is established
        sentence1 = connectionSocket.recv(1024)
        
        #checking Authentication Request
        if sentence1 == "Authentication Request" :
            randomString = ''.join(random.choice(string.ascii_letters 
                             + string.digits) for i in range(64))
            connectionSocket.send(randomString)
            if debugMode: print 'Sending random 64 bit string to client'
        
        #receive the following request from client
        if debugMode: print 'Receiving request message from client'
        sentence2 = connectionSocket.recv(1024)
        
        #split the username and mdHash
        index = sentence2.index(':')
        username = sentence2[0:index]
        mdHash = sentence2[index+1:]
        
        #finding the corresponding password
        password = ''
        if username in userinfo:
            password = userinfo[username]
        
        #generating new mdHash
        if debugMode: print 'Hashing the information'
        newHash = md5.new()
        newHash.update(username + password + randomString)
        
        #comparing the mdHash with server mdHash
        if debugMode: print 'Matching the user password'
        if newHash.digest() == mdHash:
            print 'Welcome to our service'
            connectionSocket.sendto('Y', addr)
        else:
            print 'User authorization failed'
            connectionSocket.sendto('N', addr)
        
        #server socket close
        if debugMode: print 'Closing TCP connection'
        connectionSocket.close()
        
if __name__ == '__main__':
    serverTCP(sys.argv)