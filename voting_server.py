#!/usr/bin/python

import os
import time
import sys
import SocketServer
import socket
from threading import Lock,Thread

from Socket_Receive import *

if __name__ == '__main__':
        
	if len(sys.argv) != 2:
                print "Invalid Parameters: <Port> "
                sys.exit(0)
        else:
                PORT = int(sys.argv[1])
                HOST = socket.gethostbyname(socket.gethostname())


        print('Starting Voting Server on ' + str(HOST) + ':' + str(PORT) + '...')

	try:
		server = SocketServer.TCPServer((HOST, PORT), Handle_Receive)
                server.serve_forever()
                pass
	except Exception as e: 
		print e
