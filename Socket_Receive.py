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
#	    stage 11 : Vote a candidate ( A or B )
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

		status = plaintext[0]			
		name = plaintext[1]
		reg_no = plaintext[2]
		stage = plaintext[3]
		extension = plaintext[4]

		respnse_success_status = 0
		resonse_failure_status = 1

		if stage == 0:
			# auth user
			if self.elec_vote.validate_voter(name,reg_no) == False or status == False:
				# Not found in DB or signature verification failed
				self.request.send(resonse_failure_status)	
			else:
				self.request.send(respnse_success_status)	
		elif stage == 1 :
			# check if client has already voted
			if self.elec_vote.hasVoted(reg_no) == True:
				# he already has voted, can't change that
				self.request.send(resonse_failure_status)		
			else:
				self.request.send(respnse_success_status)	
		elif stage == 11 :
			# voting a particular candidate
			if self.elec_vote.electionVote(reg_no,extension) == False:
				self.request.send(resonse_failure_status)
			else:
				self.request.send(respnse_success_status)
	
		elif stage == 2 :

		elif stage == 3 :

		else:
			# Invalid 
			print "EXCEPTION ! This stage was not supposed to be considered " + plaintext[2]




