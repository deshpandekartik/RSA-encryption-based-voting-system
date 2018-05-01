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
		#public_vf = self.crypto.load_public("voter_server_public")
              	private_vf = self.crypto.load_private("voter_server_private")

        	cipher = self.request.recv(MAX_REQUEST_SIZE)

		# TODO : Remove this part later	
		####################################
                obj = Voting_Crypto ()
                name = "Bob"
                reg_no = "113880000"
                public_vf = obj.load_public("voter_server_public")
                private_vf = obj.load_private("voter_server_private")
                private_cl = obj.load_private(name + "_" + reg_no + "_" + "private")
                cip =  obj.encrypt_message(public_vf, private_cl, name, reg_no,"0","")
		####################################

		# decrypt this message
		plaintext = self.crypto.decrypt_message(private_vf,cipher)

		# Print both encrypted and decrypted text
		print "Encrypted cipher text : "
		print cipher
		print "Decrypted plain text : "
		print plaintext

		status = plaintext[0]
		name = plaintext[1].strip()
		reg_no = plaintext[2].strip()
		stage = int(plaintext[3].strip())
		extension = plaintext[4].strip()

		respnse_success_status = "0"
		resonse_failure_status = "1"

		#print self.elec_vote.voter_database
		#print self.elec_vote.election_database

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
			extension = int(extension)
			if self.elec_vote.electionVote(reg_no,extension) == False:
				self.request.send(resonse_failure_status)
			else:
				self.request.send(respnse_success_status)

			# check if all candidates have voted, if yes print the result
			if self.elec_vote.get_election_result() != "False":
				print self.elec_vote.get_election_result()
	
		elif stage == 2 :
			# voter history
			
			if self.elec_vote.get_voter_history(reg_no) != "False":
				response = self.elec_vote.get_voter_history(reg_no)
				response = self.format_string(response)
			else:
				response = resonse_failure_status
			self.request.send(response)

		elif stage == 3 :
			# election result

			if self.elec_vote.get_election_result() != "False":
                                response =  self.elec_vote.get_election_result()
				response = self.format_string(response)
			else:
				response = resonse_failure_status
			self.request.send(response)

		else:
			# Invalid 
			print "EXCEPTION ! This stage was not supposed to be considered " + stage


	def format_string(self,inmsg):
		return "######################################### \n" + inmsg + "#########################################"

	
