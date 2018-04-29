#!/usr/bin/python

import os
import time
import sys
import SocketServer
import socket
from threading import Lock,Thread
import time

import rsa
from Socket_Sender import *



class Electorial_Voting:

        voter_file = "votercli"
        initialization_status = False
        voter_database = {}
        election_database = {}
        election_candidates = ['Tim' , 'Linda']
        CERT_DIR = "certs/"
	
	persistent_storage = "db/"
	result_file = "result"
	history_file = "history"
	write_to_storage = True

        def initialize(self,voterfile_arg):

                self.initialization_status = True

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
		voting_time = time.asctime( time.localtime(time.time()) )
                self.voter_database[registration_no] = [name, public_key, voting_status, voted_candidate, voting_time]


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
				if self.election_database[candidate][0] == index:
					self.election_database[candidate][1] = self.election_database[candidate][1] + 1
					elec_candidate = candidate
					break
			if elec_candidate == False:
				return False
			
                        self.voter_database[registration_no][2] = True
                        self.voter_database[registration_no][3] = elec_candidate
			voting_time = time.asctime( time.localtime(time.time()) )
			self.voter_database[registration_no][4] = voting_time

			if self.write_to_storage == True:
				if not os.path.isdir(self.persistent_storage):
					# create the directory
		                        os.makedirs(self.persistent_storage)

				filename = self.persistent_storage + self.result_file
				file_handle = open(filename, "w+")
				for candidate in self.election_database:
					buffer = candidate + " \t " + str(self.election_database[candidate][1]) + "\n"
					file_handle.write(buffer)
				file_handle.close()

				filename = self.persistent_storage + self.history_file
				file_handle = open(filename, "w+")
				for reg_no in self.voter_database:
					if self.voter_database[reg_no][2] == True:
						buffer = str(reg_no) + " \t " + str(self.voter_database[reg_no][4]) + "\n"
						file_handle.write(buffer)
				file_handle.close()

			return True

        def get_election_result(self):

                # check if all voters have voted in election
                for reg_no in self.voter_database:
                        if self.voter_database[reg_no][2] == False:
                                return "False"

		# print the result

		max = 0	
		# find candidate with maximum maximum votes	
		for candidate in self.election_database:
			if int(self.election_database[candidate][1]) > max:
				max = int(self.election_database[candidate][1])
		
		winner = ""
		for candidate in self.election_database:
			if int(self.election_database[candidate][1]) == max:	
				winner = winner + candidate + " "
	
		buffer = winner + " Win \n"
		resultant = buffer
		for candidate in self.election_database:
               		buffer = candidate + " \t " + str(self.election_database[candidate][1]) + "\n"
			resultant = resultant + buffer
		
		return resultant

	def get_voter_history(self,reg_no):

		resultant = ""
              	if self.voter_database[reg_no][2] == True:
                    	buffer = str(reg_no) + " \t " + str(self.voter_database[reg_no][4]) + "\n"
			resultant = resultant + buffer
		
		return resultant

	def hasVoted(self,registration_no):
		if self.voter_database[registration_no][2] == True: 
			return True
		else:
			return False

