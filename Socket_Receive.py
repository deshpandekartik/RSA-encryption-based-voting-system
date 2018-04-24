#!/usr/bin/python

import os
import time
import sys
import SocketServer
import socket
from threading import Lock,Thread

import rsa
from Socket_Sender import *

MAX_REQUEST_SIZE = 10000

class Socket_Receive(SocketServer.ThreadingTCPServer):
        def __init__(self, server_address, RequestHandlerClass, FILENAME):
		SocketServer.ThreadingTCPServer.__init__(self,server_address,RequestHandlerClass)
		self.votingfile = FILENAME


class Handle_Receive(SocketServer.BaseRequestHandler):

	voter_file = "votercli"
	initialization_status = False
	voter_database = {}
	election_database = {}
	election_candidates = ['Tim' , 'Linda']
	CERT_DIR = "certs/"

	# handle incoming socket requests from clients
    	def handle(self):
		if initialization_status == False:
			self.initialize(self.server.votingfile)

        	message = self.request.recv(MAX_REQUEST_SIZE)
		print message


	def initialize(self,voterfile_arg):
		
		initialization_status = True
		
		self.voter_file = voterfile_arg

		# store all voter_info in local memory
                if os.path.exists(self.voter_file)  :
                        file_handle = open(self.voter_file, "r")
                        for line in file_handle:
                                line = line.rstrip()
                                if line.strip() != "":
                                        a_line = line.split(' ')
					name = a_line[0]
					registration_no = a_line[1]

					filename = self.CERT_DIR + name + "_" + registration_no  + "_public"
					if os.path.isfile(filename) :
						try:
							f = open(filename,'r')
							public_key = RSA.importKey(f.read())
							
							# insert in database
							self.put(name,registration_no,public_key)
						except Exception as e:
							print e
					else:
						print "EXCEPTION ! File " + filename + " not found"
		else:
			print "Voter File not found " + self.voter_file

		# initialize election candidates
		for candidate in election_candidates:
			election_database[candidate] = 0	

	def put(self,name,registration_no, public_key):
		voting_status = False
		self.voter_database[registration_no] = [name, public_key, voting_status]


	def get(self,registration_no):
		return self.voter_database[registration_no]

	def update(self,registration_no, voting_status):
		self.voter_database[registration_no][2] = voting_status
