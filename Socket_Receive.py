#!/usr/bin/python

import os
import time
import sys
import SocketServer
import socket
from threading import Lock,Thread

import rsa
from Socket_Sender import *
from Electorial_Voting import *
from Voting_Crypto import *

MAX_REQUEST_SIZE = 10000

class Socket_Receive(SocketServer.ThreadingTCPServer):
        def __init__(self, server_address, RequestHandlerClass, FILENAME):
		SocketServer.ThreadingTCPServer.__init__(self,server_address,RequestHandlerClass)
		self.votingfile = FILENAME

###########################
# stage 0 : Auth voting client with server
# stage 1 : Voting someone ( election ), ( check if voter has voted )
# stage 2 : Vote history
# stage 3 : Election result
# stage 4 : Quit
###########################

class Handle_Receive(SocketServer.BaseRequestHandler):
	
	elec_vote = Electorial_Voting()
	crypto = Voting_Crypto()

	voter_file = "votercli"
	private_vf = None
	public_vf = None


	# handle incoming socket requests from clients
    	def handle(self):
		if self.elec_vote.initialization_status == False:
			#self.initialize(self.server.votingfile)
			self.elec_vote.initialize(self.voter_file)

			# init private and public key
			self.public_vf = self.crypto.load_public("voter_server_public")
                     	self.private_vf = self.crypto.load_private("voter_server_private")

        	cipher = self.request.recv(MAX_REQUEST_SIZE)

		# decrypt this message
		plaintex = self.crypto.decrypt_message(self.private_vf,cipher)
			
		name = plaintext[0]
		reg_no = plaintext[1]
		stage = plaintext[2]
		extension = plaintext[3]

		if stage == 0:
			# auth user
			if elec_vote.validate_voter(name,reg_no) == True:
				# reply with a 1 to client
				
					
		elif stage == 1 :

		elif stage == 2 :

		elif stage == 3 :

		else:
			# Invalid 
			print "EXCEPTION ! This stage was not supposed to be considered " + plaintext[2]

