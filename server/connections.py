import sys
import logging
import time
import socket
import threading

from messages import *

IP = 'localhost'
PORT = 21385
MAX_CONNS = 4

MSG_SIZE = 2**10

class Connection(object):
	def __init__(self, connection, address):
		self.conn = connection
		self.addr = address
		self.id = id(self)
		self._empties = 0
		self._tol = 100

	@property
	def ip(self):
		return self.addr[0]

	@property
	def port(self):
		return self.addr[1]

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
			self._empties += 1

		if self._empties > self._tol:
			print self, 'we appear to have lost connection'
			self.close()

		return messages

	def close(self):
		self.conn.close()

	def __repr__(self):
		return '<Connection:%i - %r>' % (self.id, self.addr)

