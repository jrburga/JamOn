import sys
import logging
import time
import socket

from messages import *

from urllib2 import urlopen

IP = '0.0.0.0'
try:
	PUBLIC = urlopen('http://ip.42.pl/raw').read()
except:
	PUBLIC = '0.0.0.0'
PORT = 21385
MAX_CONNS = 20
TIMEOUT = 10

MSG_SIZE = 2**10

class Connection(object):
	def __init__(self, connection, address):
		self.conn = connection
		self.addr = address
		self.id = id(self)
		self._closed = False

	@property
	def ip(self):
		return self.addr[0]

	@property
	def port(self):
		return self.addr[1]

	@property
	def closed(self):
		return self._closed

	def _parse(self, msg_string):
		return msg_string.replace('}{', '}*{').split('*')

	def send(self, message):
		assert isinstance(message, Message), 'Can only send type: Message'
		msg = toJSON(message)
		self.conn.send(msg)

	def recv(self, size=MSG_SIZE):
		'''
		receive any number of messages at a given time
		blocking
		'''
		messages = []
		msg_string = self.conn.recv(size)
		if msg_string:
			self._empties = 0
			for json_str in self._parse(msg_string):
				messages.append(fromJSON(json_str))
		else:
			print self, 'we appear to have lost connection'
			self.close()

		return messages

	def close(self):
		self.conn.close()
		self._closed = True


	def __repr__(self):
		return '<Connection:%i - %r>' % (self.id, self.addr)

