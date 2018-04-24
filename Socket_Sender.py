#!/usr/bin/python


import sys
import socket

MAX_REQUEST_SIZE = 10000

class Socket_Sender:

    # sending messages to server / clients
    def send_message(self, ip, port_num, message):
        try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, int(port_num)))
                sock.sendall(message)
                server_response = sock.recv(MAX_REQUEST_SIZE)
                sock.close()
                if server_response == "" :
                        # ERROR ! Empty response, probably the server does not want to send anything
                        return None
                else:
                        return server_response
        except Exception as e:
                print "ERROR ! Socket exception in send_message Socket Sender while sending message to " + str(ip) + " " + str(port_num) + e
		return None
