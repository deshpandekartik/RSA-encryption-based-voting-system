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

MAX_REQUEST_SIZE = 1000

class Socket_Receive(SocketServer.ThreadingTCPServer):
        def __init__(self, server_address, RequestHandlerClass, FILENAME):
		SocketServer.ThreadingTCPServer.__init__(self,server_address,RequestHandlerClass)
		self.votingfile = FILENAME


class Handle_Receive(SocketServer.BaseRequestHandler):
	
	elec_vote = Electorial_Voting()
	voter_file = "votercli"

	# handle incoming socket requests from clients
    	def handle(self):
		if self.elec_vote.initialization_status == False:
			#self.initialize(self.server.votingfile)
			self.elec_vote.initialize(self.voter_file)

        	message = self.request.recv(MAX_REQUEST_SIZE)
		print message

		# check if string in 46 bits encoded
		try:
			b64decode(message)
		except:
			# first message from voting_client to me
			a_line = message.split(':')
			print self.elec_vote.validate_voter(a_line[0],a_line[1])
