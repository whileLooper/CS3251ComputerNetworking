'''
Created on Feb 9, 2015

@author: bochen
'''
from socket import *
import random
import sys
import md5
import string

def main(argv):
    
    debugMode = False
    received = False
    #checking valid input arguments
    if len(sys.argv) != 4:
        if len(sys.argv) == 6 and sys.argv[4] != '-d':
            print 'Invalid number of argument'
            sys.exit()
            
    if len(sys.argv) == 5: debugMode = True
    
    #splitting input arguments
    addressport = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    
    try: 
        index = addressport.index(':')
    except:
        print 'Invalid input argument, please enter correct format command.\n' \
            'Example: python letmein-udp.py 127.0.0.1:8591 username password'
        sys.exit()
    
    try:        
        address = addressport[0:index]
    except:
        print 'Invalid input argument, please enter correct format command.\n (address)' \
            'Example: python letmein-udp.py 127.0.0.1:8591 username password'
        sys.exit()
    if not valid_ip(address): 
        print 'Invalid input argument, please enter correct format command.\n (address)' \
            'Example: python letmein-udp.py 127.0.0.1:8591 username password'
        sys.exit()
    
    try:
        port = int(addressport[index+1:])
    except:
        print 'Invalid input argument, please enter correct format command.\n' \
            'Example: python letmein-udp.py 127.0.0.1:8591 username password'
        sys.exit()
        
    #creating the client's UDP socket
    if debugMode: print 'Creating client socket'
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    
    clientSocket.settimeout(2)
    
    
    #sending authentication request with server address
    if debugMode: print 'Sending authentication request'
    clientSocket.sendto('Authentication request', (address, port))
    
    while(not received): 
    #Handling lost message but setting time out section
        try:
            if debugMode: print 'Receiving random 64 bit string from server socket'
            sentence, addr = clientSocket.recvfrom(2048)
            received = True
        except timeout:
            print 'resending message'
            clientSocket.sendto('Authentication request', (address, port))        
    
    
    #receiving random 64 bit string from server socket
    '''if debugMode: print 'Receiving random 64 bit string from server socket'
    sentence, addr = clientSocket.recvfrom(2048)'''
    
    #generating hashcode by using username, password and random string
    if debugMode: print 'Generating hashcode'
    mdHash = md5.new()
    mdHash.update(username + password + sentence)
    
    #sending username + hashcode to server socket
    if debugMode: print 'Sending username and hashcode to server socket'
    clientSocket.sendto(username + ':' + mdHash.hexdigest(), (address, port))
    
    #receiving confirmation from server socket
    sentence, addr = clientSocket.recvfrom(2048)
    if sentence == 'Y':
        print 'Welcome to our service.'
    else:
        print 'User authorization failed.'
        
    #close socket
    if debugMode: print 'Closing client UDP socket'
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
    main(sys.argv)