

# Introduction

An RSA encryption based secure voting booth.

# Working

The voters connect to the Voting Facility (VF) to vote. All voters have the public keys of Voting Facility and Voting Facility has the public keys of all voters. 
All the voters name's and registration details are added to a file named voterinfo.

To generate the private and public keys for each voter and Voting Facility.

```
python generate-certs.py

```

Let || represent concatenation, pub(X) represent the public-key of X, priv(X) represent the private-key of X, DS(X) represent the digital signature of X, and E(K,M) represent encrypting message M using key K. 

The detailed steps are given below:

1. The voter invokes voter-cli to connect to the VF server

2. Upon connection, the voter is prompted to enter his/her name and voter registration number vnumber

3. After the voter enters vnumber, voter-cli sends E(pub(VF), name||vnumber)||DS(name) to the VF server ("||" represents concatenation).

4. The VF server checks whether the name and vnumber received match the information in file voterinfo. If not, the VF server sends 0 to voter-cli. voter-cli then prints   " Invalid name or registration number" and terminates the connection. Otherwise, VF sends 1 to voter-cli. Voter-cli prints the user’s name and prompts the user to 
   select an action to perform:


Starting the server.

```
python voting_server.py VF_IP PORTNUM

```

Starting the client.

```
python voting_client.py VF_IP PORTNUM

```

# References
https://www.dlitz.net/software/pycrypto/api/current/Crypto.PublicKey.RSA-module.html
