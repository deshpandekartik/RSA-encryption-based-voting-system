#!/usr/bin/python

import os
import time
import sys
import socket
import re

import rsa
from Socket_Sender import *
from Voting_Crypto import *

###########################
# stage 0 : Auth voting client with server
# stage 1 : Voting someone ( election ), ( check if voter has voted )
# stage 2 : Vote history
# stage 3 : Election result
# stage 4 : Quit 
###########################

class Client_Instance:
	sender = Socket_Sender()	# this will handle sending and receiving messages, socket
	crypto = Voting_Crypto()

	HOST = None
	PORT = None

	def __init__(self, host,port):
		self.HOST = host
		self.PORT = int(port)
		print "Connected to server " + str(host) + ":" + str(port)

	def auth_voting_client(self):

		stage = 0

		# console for user input
		while True:

        		name = raw_input("\nPlease enter your name\n")
        		regno = raw_input("\nPlease enter your registration number\n")

		        if name != "" and regno != "" :
				name = name.replace("\n\r",'')
				regno = regno.replace("\n\r",'')
				try:
					public_cl = self.crypto.load_public(name + "_" + regno + "_" + "public")
					private_cl = self.crypto.load_private(name + "_" + regno + "_" + "private")
					
					public_vf = self.crypto.load_public("voter_server_public")
                                        private_vf = self.crypto.load_private("voter_server_private")
				
					ciphertext = self.crypto.encrypt_message(public_vf,private_cl,name,regno,stage,"")
					print ciphertext

				except Exception as e:
					print "Private key of user " + name + " not found"
					print e
					sys.exit(0)
					
                		return_message = self.sender.send_message(self.HOST, self.PORT, ciphertext)
 

if len(sys.argv) != 3:
        print "Invalid Parameters: <VotingServer IP> <Port>"
        sys.exit(0)
else:
        HOST = sys.argv[1]
        PORT = sys.argv[2]

if __name__ == "__main__":
	client = Client_Instance(HOST,PORT)
	client.auth_voting_client()
