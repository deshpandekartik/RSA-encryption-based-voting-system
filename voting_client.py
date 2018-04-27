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
	elec_vote = Electorial_Voting()

	voter_file = "votercli"
	public_cl = None
	private_cl = None
	public_vf = None
	private_vf = None
	respnse_success_status = 0
	resonse_failure_status = 1
	write_to_file = True
	

	HOST = None
	PORT = None

	def __init__(self, host,port):
		self.HOST = host
		self.PORT = int(port)
		print "Connected to server " + str(host) + ":" + str(port)
		try:
			self.public_vf = self.crypto.load_public("voter_server_public")
			self.private_vf = self.crypto.load_private("voter_server_private")
		except Exception as e:
			print e
		self.elec_vote.initialize(self.voter_file)

	def auth_voting_client(self):

		stage = 0

		# console for user input
		while True:

        		name = raw_input("\nPlease enter your name\n")
        		regno = raw_input("\nPlease enter your registration number\n")

		        if name != "" and regno != "" :
				try:
					self.public_cl = self.crypto.load_public(name + "_" + regno + "_" + "public")
					self.private_cl = self.crypto.load_private(name + "_" + regno + "_" + "private")
					
					ciphertext = self.crypto.encrypt_message(self.public_vf,self.private_cl,name,regno,stage,"")
					print ciphertext

				except Exception as e:
					print "Private key of user " + name + " not found"
					print e
					sys.exit(0)
					
                		return_message = self.sender.send_message(self.HOST, self.PORT, ciphertext)
				if return_message == self.resonse_failure_status :
					print "Invalid userID and registration number"
				else:
					break

		self.main_menu(name,regno)

	def main_menu(self,name,regno):
 		
		while True:
			print "Welcome " + name	
			print "Main menu"
			print "Please enter a number (1-4)"
			print "1. Vote"
			print "2. My vote history"
			print "3. Election result"
			print "4. Quit"
			print "\n"
	
			userinput = raw_input()
			
			if userinput == 1:
				stage = 1
				extension = ""
				ciphertext = self.crypto.encrypt_message(self.public_vf,self.private_cl,name,regno,stage,extension)
			
				return_message = self.sender.send_message(self.HOST, self.PORT, ciphertext)
                                if return_message == self.resonse_failure_status:
                                        print "ERROR ! You have already voted"
                                else:
                                        self.electorate(name,regno)
	
			elif userinput == 2:
				stage = 2			
				extension = ""
				ciphertext = self.crypto.encrypt_message(self.public_vf,self.private_cl,name,regno,stage,extension)
			
                                return_message = self.sender.send_message(self.HOST, self.PORT, ciphertext)
                                if return_message == self.resonse_failure_status:
                                        print "Invalid userID and registration number"
                                else:
                                        break
			elif userinput == 3:
				stage = 3		
				extension = ""
                                ciphertext = self.crypto.encrypt_message(self.public_vf,self.private_cl,name,regno,stage,extension)
                                return_message = self.sender.send_message(self.HOST, self.PORT, ciphertext)
                                if return_message == self.resonse_failure_status :
                                        print "Invalid userID and registration number"
                                else:
                                        break
			elif userinput == 4:
                                print "Good Bye"
                                sys.exit(0)
			else:
				print "Invalid choice"
								
	def electorate(self,name,regno):
		while True :
			stage = 11
			
			print "Please enter a number ( 1 - " + len(self.elec_vote.election_database) + " ) "
			# get all election candidates to display
			for candidate in self.elec_vote.election_database:
				print self.elec_vote.election_database[candidate] + ". " + candidate 
				last_index = self.elec_vote.election_database[candidate]
				back_id = self.elec_vote.election_database[candidate] + 1
				quit_id = back + 1
			print back_id + ". Back "
			print quit_id + ". Quit" 
			print "\n"		

			userinput = raw_input()
				
			if userinput > quit_id or userinput < 1 :
				print "Invalid option"
			elif userinput == back_id:
				break
			elif back_id == quit_id :
				print "Good Bye"
                                sys.exit(0)
			else:
				stage = 11
				extension = userinput
				ciphertext = self.crypto.encrypt_message(self.public_vf,self.private_cl,name,regno,stage,extension)
                                return_message = self.sender.send_message(self.HOST, self.PORT, ciphertext)
                                if return_message == self.resonse_failure_status :
                                        print "Something went wrong, while registering your vote"
                                else:
                                        print "Vote Registration Success"
					break
	

if len(sys.argv) != 3:
        print "Invalid Parameters: <VotingServer IP> <Port>"
        sys.exit(0)
else:
        HOST = sys.argv[1]
        PORT = sys.argv[2]

if __name__ == "__main__":
	client = Client_Instance(HOST,PORT)
	client.auth_voting_client()
