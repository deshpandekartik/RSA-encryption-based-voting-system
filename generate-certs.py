import rsa
from base64 import b64encode, b64decode
import os
import shutil

KEYSIZE_DEFAULT = 2048

class GnerateCerts:

	keysize = KEYSIZE_DEFAULT
	file_votercli = None
	CERT_DIR = "certs/"

	def __init__(self, keysize_arg, filename_arg):
		self.keysize = keysize_arg
		self.file_votercli = filename_arg

	def write_tofile(self, private_key, public_key, name_of_file):
		
		try:
			# write private key
			filename = self.CERT_DIR +  name_of_file + "_private"
			priv_file_handle = open(filename, "w+")
			priv_file_handle.write(private_key.exportKey('PEM'))
			priv_file_handle.close()
		except IOError:
	                print "ERROR! The file " + filename + " was not found!"
			return			

		try:
			# write public key
			filename = self.CERT_DIR + name_of_file + "_public"
			pub_file_handle = open(filename, "w+")
	                pub_file_handle.write(public_key.exportKey('PEM'))
			pub_file_handle.close()
		except IOError:
                        print "ERROR! The file " + filename + " was not found!"
                        return


	def gnerate_cert(self):

		if os.path.isdir(self.CERT_DIR):
	
			# first empty all cert files in dir
			shutil.rmtree(self.CERT_DIR)

			# create the directory
                        os.makedirs(self.CERT_DIR)

		else:
			# create the directory
			os.makedirs(self.CERT_DIR)			

		# Generate Voter Server certs first
		(public, private) = rsa.newkeys(self.keysize)

		self.write_tofile(private,public,"voter_server")

		# generate public private keys for each voter
		if os.path.exists(self.file_votercli)  :
			file_handle = open(self.file_votercli, "r")
			for line in file_handle:
				line = line.rstrip()
				if line.strip() != "":
					a_line = line.split(' ')

					(public, private) = rsa.newkeys(self.keysize)
			                self.write_tofile(private,public,a_line[0] + "_" + a_line[1])
if __name__ == '__main__':
	cer = GnerateCerts(2048, "votercli")
	cer.gnerate_cert()
