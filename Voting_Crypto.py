#!/usr/bin/python

from base64 import b64encode, b64decode
import rsa

class Voting_Crypto:
	CERT_DIR = "certs/"

	##################################################
	# loads public cert and returns
	def load_public(self, certfile):
		certfile = self.CERT_DIR + "/" + certfile
		f = open(certfile,'r')
       		key = rsa.importKey(f.read())
		return key

	##################################################
	# Loads private cert and returns
	def load_private(self, certfile):
		certfile = self.CERT_DIR + "/" + certfile
		f = open(certfile,'r')
                key = rsa.importKey(f.read())                                               
                return key

	###################################################
	# Encrypt plain text using public key of Voting server
	# Sign the message using private key of voting client
	def encrypt_message(self, public_vf, private_cl, name, reg_no, extension):

		try:	
			# E(pub(VF), name||vnumber)||DS(name)
		
			# name || vnumber
			plaintex = name + ":" + reg_no + ":" + extension
		
			# encrypt, E(pub(VF), name||vnumber)
			ciphertext = b64encode(rsa.encrypt(plaintex, public_vf))
		
			# sign name, DS(name), signed by voter clients private key
			signature = b64encode(rsa.sign(name, private_cl, "SHA-512"))

			# concatinate and return
			return ciphertext + signature

		except Exception as e:
			print "EXCEPTION ! Invalid key, encrypt_message"
                        print e
                        return False

	#####################################################
	# Decrypt message using private key of voting server
	# Verify signature using public key of client
	def decrypt_message(self, private_vf, ciphertext):

		ciphertext = ciphertext.rstrip()	
		try:
			# break message into parts, 1st part is cipher text next is the signature
			signature = ciphertext[344:344+344]
			ciphertext = ciphertext[0:344]
		
			# decrypt cipher text
			plaintext = rsa.decrypt(b64decode(ciphertext), private_vf)	
	
			plaintext = plaintext.split(":")
			
			name = plaintext[0]
			reg_no = plaintext[1]
			extension = plaintext[2]
			
			public_cl = self.load_public(name + "_" + reg_no + "_" + "public")

			# verify signature first
			verify = rsa.verify(name, b64decode(signature), public_cl)
	
			if verify == False:
				return False
	
			return (name,reg_no,extension)

		except Exception as e:
			print "EXCEPTION ! Invalid key, decrypt_message"
			print e
			return False

if __name__ == "__main__":
	obj = Voting_Crypto ()
	name = "Alice"
	reg_no = "112550000"

	public_vf = obj.load_public("voter_server_public")
       	private_vf = obj.load_private("voter_server_private")
	
	private_cl = obj.load_private(name + "_" + reg_no + "_" + "private")
	
	cip =  obj.encrypt_message(public_vf, private_cl, name, reg_no,"")

	print cip
	plain = obj.decrypt_message(private_vf,cip)
	print plain
