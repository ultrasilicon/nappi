import socket
import json
import time
from _thread import start_new_thread
from rpi_backlight import Backlight

PROTO_VERSION = "0.0.1"
UDP_PORT = 65282
BROADCAST_ADDR = "255.255.255.255"
HEARTBEAT_DELAY = 0.3	# must be less than screen_timeout for the listen loop to work (lazy implementation)

MSG_HEARTBEAT = {'version': PROTO_VERSION, 'type': 'heartbeat'}

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
udp_sock.bind(('', UDP_PORT))

backlight = Backlight()

screen_on = True
screen_timeout = 1


def toggleScreen(switch):
	if switch != backlight.power:
		backlight.power = switch

def broadcast(msgJson):
	udp_sock.sendto(bytes(json.dumps(msgJson), "utf-8"), (BROADCAST_ADDR, UDP_PORT))

def listen():
	time_stamp = time.time()
	while True:
		data, address = udp_sock.recvfrom(UDP_PORT)
		print(data)
		message = {}
		try:
			message = json.loads(data)
		except:
			pass
		if message != {} and message['version'] == PROTO_VERSION and message['type'] == 'wake':
			time_stamp = time.time()
		if time.time() - time_stamp < screen_timeout:
			toggleScreen(True)
		else:
			toggleScreen(False)


def heartbeat():
	while True:
		time.sleep(HEARTBEAT_DELAY)
		broadcast(MSG_HEARTBEAT)

if __name__ == "__main__":
	start_new_thread(listen, ())
	start_new_thread(heartbeat, ())
	while True:
   		pass





