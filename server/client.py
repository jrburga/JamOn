from connections import *	
from messages import *
from thread import *

import time

class Client(object):
	def __init__(self, ip=IP):
		# super(Client, self).__init__t__()
		self.ip = ip
		self.id = None
		self._socket_sync = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._socket_async = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._sync = None
		self._async = None
		self._messages = []
		self._is_host = False
		self._tether_callback = lambda *_: None
		self._init_info = {}

	def register_tether_callback(self, callback):
		self._tether_callback = callback

	@property
	def is_host(self):
		return self._is_host

	def _join(self, ip, port, timeout):
		print 'joining to ip'
		conn = self._connect(self._socket_sync, ip, port, timeout)
		conn.send(Join(self._init_info))
		res = conn.recv().pop(0)
		if res.data['success']:
			print 'successfully joined'
			self._sync = conn
			self.id = res.data['id']
			self._is_host = res.data['host']
		else:
			print 'unable to join. closing connection'
			conn.close()

	def _tether(self, ip, port, timeout):
		print 'tethering to ip'
		conn = self._connect(self._socket_async, ip, port, timeout)
		conn.send(Tether({'id': self.id}))
		res = conn.recv().pop(0)
		if res.data['success']:
			print 'successfully tethered'
			start_new_thread(self._listen_tether, (conn, ))
			self._async = conn
		else:
			conn.close()

	def _listen_tether(self, connection):
		while not connection.closed:
			for message in connection.recv():
				if message.type == 'action':
					self.recv_action(message)

	def _connect(self, sock, ip, port, timeout):
		print 'connecting socket to %r' % ((ip, port), )
		sock.settimeout(timeout)
		sock.connect((ip, port))
		sock.settimeout(None)
		conn = Connection(sock, (ip, port))
		print 'waiting for response from server'
		res = conn.recv().pop(0)
		if res.data['success']:
			return conn
		return None

	def connect(self, ip, port=PORT, timeout=TIMEOUT):
		self._join(ip, port, timeout)
		self._tether(ip, port, timeout)
		print 'successfully connected'


	def disconnect(self):
		if self._sync:
			self._sync.close()
		if self._async:
			self._async.close()

	def recv_action(self, action):
		if 'success' in action:
			return
		else:
			self._tether_callback(action.data)

	def post(self, info_name, info, callback):
		post = Post(info_name, info)
		self._sync.send(post)
		message = self._sync.recv()[0]
		return callback(message)

	def get(self, info_name, identifier, callback):
		get = Get(info_name, identifier)
		self._sync.send(get)
		message = self._sync.recv()[0]
		return callback(message)

	def send(self, msg_type, data):
		'''
		Non blocking. Sends without listening.
		Good if you don't care about how your message is handled.
		'''
		message = Message(msg_type, data)
		self._async.send(message)


if __name__ == '__main__':
	client = Client()
	client.connect(IP, PORT)
	time.sleep(1)
	client.send_action({'type': 'key_press'})
	time.sleep(2)