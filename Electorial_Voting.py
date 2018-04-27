#!/usr/bin/python

import os
import time
import sys
import SocketServer
import socket
from threading import Lock,Thread
import rsa
from Socket_Sender import *



class Electorial_Voting:


        voter_file = "votercli"
        initialization_status = False
        voter_database = {}
        election_database = {}
        election_candidates = ['Tim' , 'Linda']
        CERT_DIR = "certs/"


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
                                                        public_key = rsa.importKey(f.read())

                                                        # insert in database
                                                        self.put(name,registration_no,public_key)
                                                except Exception as e:
                                                        print e
                                        else:
                                                print "EXCEPTION ! File " + filename + " not found"
                else:
                        print "Voter File not found " + self.voter_file

                # initialize election candidates	
		index = 0
                for candidate in self.election_candidates:
			index = index + 1
                        self.election_database[candidate] = [index, 0]

        def put(self,name,registration_no, public_key):
                voting_status = False
                voted_candidate = None
                self.voter_database[registration_no] = [name, public_key, voting_status, voted_candidate]


        def get(self,registration_no):
                return self.voter_database[registration_no]

        def update(self,registration_no, voting_status):
                self.voter_database[registration_no][2] = voting_status


        def validate_voter(self,name,registration_no):
                if registration_no in self.voter_database:
                        if self.voter_database[registration_no][0] == name:
                                return True
                        else:
                                return False
                else:
                        return False

        def electionVote(self,registration_no,index):

                if self.voter_database[registration_no][2] == True:
                        # has already voted
                        return False
                else:
			elec_candidate = None
			for candidate in self.election_database:
				if self.election_database[candidate][1] == index:
					self.election_database[candidate][1] = self.election_database[candidate][1] + 1
					elec_candidate = candidate
					break
			if elec_candidate == False:
				return False
			
                        self.voter_database[registration_no][2] = True
                        self.voter_database[registration_no][3] = elec_candidate
                        return True


        def election_result(self):

                # check if all voters have voted in election
                for reg_no in self.voter_database:
                        if self.voter_database[reg_no][2] == False:
                                return False

		# get the electorial candidate with maximum votes

	def hasVoted(self,registration_no):
		if self.voter_database[registration_no][2] == True: 
			return True
		else:
			return False

