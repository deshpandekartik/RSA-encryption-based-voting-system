#!/usr/bin/python

import os
import time
import sys
import socket
import re

import rsa
from Socket_Sender import *

class Client_Instance:
	sender = Socket_Sender()

	def validate_voter(self,name, reg_no):
		
		 

if len(sys.argv) != 3:
        print "Invalid Parameters: <VotingServer IP> <Port>"
        sys.exit(0)
else:
        HOST = sys.argv[1]
        PORT = sys.argv[2]

sender = Socket_Sender()

print "Connected to server " + str(HOST) + ":" + str(PORT)

# console for user input
while True:

	name = raw_input("\nPlease enter your name\n")

	regno = raw_input("\nPlease enter your registration number\n")

	if name != "" and regno != "" :
		# send it to validate
		return_message = sender.send_message(HOST, PORT, name + ":" + regno)
