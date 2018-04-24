#!/usr/bin/python

import os
import time
import sys
import SocketServer
import socket
from threading import Lock,Thread

from Socket_Receive import *

if __name__ == '__main__':
        
	if len(sys.argv) != 3:
                print "Invalid Parameters: <Port> <VoterClient_File"
                sys.exit(0)
        else:
                PORT = int(sys.argv[1])
                HOST = socket.gethostbyname(socket.gethostname())
                VOTER_FILE = sys.argv[2]


        print('Starting Voting Server on ' + str(HOST) + ':' + str(PORT) + '...')

	try:
		server = SocketServer.TCPServer((HOST, PORT), Socket_Receive)
                server.serve_forever()
                pass
	except Exception as e: 
		print e
