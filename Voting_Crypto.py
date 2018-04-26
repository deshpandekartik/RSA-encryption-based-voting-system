#!/usr/bin/python

import os
import time
import sys
import SocketServer
import socket
from threading import Lock,Thread
from base64 import b64encode, b64decode
import rsa

class Voting_Crypto:

	def votercli_auth_encrypt(self, public, private, name, reg_no):

		try:	
			# E(pub(VF), name||vnumber)||DS(name)
		
			# name || vnumber
			plaintex = name + ":" + reg_no
		
			# encrypt, E(pub(VF), name||vnumber)
			ciphertext = b64encode(rsa.encrypt(plaintex, public))
		
			# sign name, DS(name)
			signature = b64encode(rsa.sign(name, private, "SHA-512"))

			# concatinate and return
			return ciphertext + signature

		except Exception as e:
			print "EXCEPTION ! Invalid key, votercli_auth_encrypt"
                        print e
                        return False

	def votercli_auth_decrypt(self, public, private, ciphertext):
	
		try:	
			# break message into parts, 1st part is cipher text next is the signature
			signature = ciphertext[344:344+344]
			ciphertext = ciphertext[0:344]
		
			# decrypt cipher text
			plaintext = rsa.decrypt(b64decode(ciphertext), private)	
	
			plaintext = plaintext.split(":")
			
			name = plaintext[0]
			reg_no = plaintext[1]
		
			# verify signature first
			verify = rsa.verify(name, b64decode(signature), public)
	
			if verify == False:
				return False
		
			return (name,reg_no)
		except Exception as e:
			print "EXCEPTION ! Invalid key, votercli_auth_decrypt"
			print e
			return False

'''
obj = Voting_Crypto ()
keysize = 2048
(public, private) = rsa.newkeys(keysize)
name = "Alice"
reg_no = "121241241"

cip =  obj.votercli_auth_encrypt(public, private, name, reg_no)
print cip
plain = obj.votercli_auth_decrypt(public,private,cip)
'''
