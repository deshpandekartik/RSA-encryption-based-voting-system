import rsa
from base64 import b64encode, b64decode
import textwrap

msg1 = "Hello Tony, I am Jarvis!"
msg2 = "Hello Toni, I am Jarvis!"
keysize = 2048
(public, private) = rsa.newkeys(keysize)
encrypted = b64encode(rsa.encrypt(msg1, public))
decrypted = rsa.decrypt(b64decode(encrypted), private)
signature = b64encode(rsa.sign(msg1, private, "SHA-512"))
verify = rsa.verify(msg1, b64decode(signature), public)

print(private.exportKey('PEM'))
print(public.exportKey('PEM'))
print("Encrypted: " + encrypted)
print("Decrypted: '%s'" % decrypted)
print("Signature: " + signature)
print("Verify: %s" % verify)
rsa.verify(msg2, b64decode(signature), public)


print "#######################################"
name = "Alice"
Regno = "21313123"
#load public key
f = open("certs/voter_server_public",'r')                                                        
public_key = rsa.importKey(f.read())
signature = b64encode(rsa.sign(name, private, "SHA-512"))

full_encrypted_msg = ""

# add name 
full_encrypted_msg = b64encode(rsa.encrypt(name, public)) + b64encode(rsa.encrypt(Regno, public)) + signature

print full_encrypted_msg

print full_encrypted_msg[0:344]

print full_encrypted_msg[344:344+344]

print full_encrypted_msg[344+344:len(full_encrypted_msg)]


# decryption

decrypted = rsa.decrypt(b64decode(full_encrypted_msg[344:344+344]), private)
print decrypted
