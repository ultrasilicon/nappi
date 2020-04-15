import socket
import json
import time
from _thread import start_new_thread

PROTO_VERSION = "0.0.1"
UDP_PORT = 65282
BROADCAST_ADDR = "255.255.255.255"
WAKE_MSG_DELAY = 0.3	# must be less than screen_timeout for the listen loop to work (lazy implementation)

MSG_WAKE = {'version': PROTO_VERSION, 'type': 'wake'}

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
udp_sock.bind(('', UDP_PORT))


def broadcast(msgJson):
	udp_sock.sendto(bytes(json.dumps(msgJson), "utf-8"), (BROADCAST_ADDR, UDP_PORT))

def sendWake():
	while True:
		time.sleep(WAKE_MSG_DELAY)
		broadcast(MSG_WAKE)

if __name__ == "__main__":
	start_new_thread(sendWake, ())
	while True:
   		pass





