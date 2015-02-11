'''
Created on Feb 9, 2015

@author: bo chen
'''
from socket import *
import sys
import md5
import string
    
def main(argv):
    debugMode = False   

     #checking valid input arguments
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print("Invalid input arguments")
        sys.exit()
    elif len(sys.argv) ==5 and sys.argv[4] != '-d':
        print("Invalid input arguments")
        sys.exit()
    
    if len(sys.argv) == 5 and sys.argv[4] == '-d':
        debugMode = True
    
    #splitting the input arguments
    hostAddress = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    
    #separate address into server address and port number
    try:
        index = hostAddress.index(":")
    except:
        print 'Invalid input argument, please enter correct format command.\n' \
            'Example: python letmein-tcp.py 127.0.0.1:8591 username password'
        sys.exit()
    
    try:    
        hostIP = hostAddress[0:index]
    except:
        print 'Invalid input argument, please enter correct format command.\n' \
            'Example: python letmein-tcp.py 127.0.0.1:8591 username password'
        sys.exit()
        
    if not valid_ip(hostIP): 
        print 'Invalid input argument, please enter correct format command.\n (address)' \
            'Example: python letmein-tcp.py 127.0.0.1:8591 username password'
        sys.exit()
        
    try:
        hostPort = int(hostAddress[index+1:]) 
    except:
        print 'Invalid input argument, please enter correct format command.\n' \
            'Example: python letmein-tcp.py 127.0.0.1:8591 username password'
        sys.exit()   
    
    #creating client side TCP socket
    if debugMode: print 'Creating client-tcp socket'
    clientSocket = socket(AF_INET, SOCK_STREAM)
    
    #initiating the TCP connection 
    if debugMode: print 'Connecting server'
    clientSocket.connect((hostIP, hostPort))
    
    #sending authentication request
    if debugMode: 
        print 'Sending authentication request to server ( ' + hostIP + ':' + str(hostPort) + ' )'
    clientSocket.send("Authentication Request")
    
    #receiving random 64 bit string from server
    if debugMode: print 'Receiving random 64 bit string from server'
    randomString = clientSocket.recv(1024)
    
    #hashing the username, password and random string
    if debugMode: print 'Hashing the user information'
    mdHash = md5.new()
    mdHash.update(username + password + randomString)
    
    #sending the username + hashcode
    if debugMode: print 'Sending the username and hash to server'
    clientSocket.send(username + ":" + mdHash.digest())
    
    #receiving the confirmation from server socket
    sentence, addr = clientSocket.recvfrom(2048)
    if sentence == 'Y':
        print 'Welcome to our service.'
    else:
        print 'User authorization failed.'
    
    #close socket 
    if debugMode: print 'Closing client socket'
    clientSocket.close()
    
def valid_ip(address):
    try:
        host_bytes = address.split('.')
        valid = [int(b) for b in host_bytes]
        valid = [b for b in valid if b >= 0 and b<=255]
        return len(host_bytes) == 4 and len(valid) == 4
    except:
        return False
    
if __name__ == '__main__':
    #getting the request message beside argv 1
    main(sys.argv)