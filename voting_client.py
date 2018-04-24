#!/usr/bin/python

import os
import time
import sys
import socket
import re

import rsa
from Socket_Sender import *

MAX_REQUEST_SIZE = 10000

if len(sys.argv) != 3:
        print "Invalid Parameters: <VotingServer IP> <Port>"
        sys.exit(0)
else:
        HOST = sys.argv[1]
        PORT = sys.argv[2]

obj = Socket_Sender()

print "Connected to server " + str(HOST) + ":" + str(PORT)

# console for user input
while True:

	name = raw_input("\nPlease enter your name\n")

	regno = raw_input("\nPlease enter your registration number\n")

	if name != "" and regno != "" :
		# send it to validate
		return_message = obj.send_message(HOST, PORT, name + ":" + regno)
