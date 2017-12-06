from connections import *
from messages import *

import time

class Client(object):
	def __init__(self, ip=IP):
		self.ip = ip
		self.id = None
		self._socket_sync = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._socket_async = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._sync = None
		self._async = None
		self._messages = []
		self._is_host = False

	@property
	def is_host(self):
		return self._is_host

	def _join(self, ip, port):
		print 'joining to ip'
		conn = self._connect(self._socket_sync, ip, port)
		conn.send(Join())
		res = conn.recv().pop(0)
		if res.data['success']:
			print 'successfully joined'
			self._sync = conn
			self.id = res.data['id']
		else:
			print 'unable to join. closing connection'
			conn.close()

	def _tether(self, ip, port):
		print 'tethering to ip'
		conn = self._connect(self._socket_async, ip, port)
		conn.send(Tether({'id': self.id}))
		res = conn.recv().pop(0)
		if res.data['success']:
			print 'successfully tethered'
			t = threading.Thread(target=self._listen_tether, args=(conn, ))
			t.start()
			self._async = conn
		else:
			conn.close()

	def _listen_tether(self, connection):
		listening = True
		while listening:
			for message in connection.recv():
				if message.type == 'action':
					self.recv_action(message)

	def _connect(self, sock, ip, port):
		print 'connecting socket to %r' % ((ip, port), )
		sock.connect((ip, port))
		conn = Connection(sock, (ip, port))
		print 'waiting for response from server'
		res = conn.recv().pop(0)
		if res.data['success']:
			print 'successfully connected'
			return conn
		return None

	def connect(self, ip, port=PORT):
		self._join(ip, port)
		self._tether(ip, port)


	def disconnect(self):
		self._socket_async.close()
		self._socket_sync.close()

	def recv_action(self, action):
		if 'success' in action.data:
			print action
			return

	def post(self, data={}, callback=lambda *_: None):
		post = Post(data)
		self._sync.send(post)
		# message = self._listen('post')

	def get(self, data={}, callback=lambda *_: None):
		get = Get(data)
		self._sync.send(get)
		# message = self._listen('get')

	def send(self, msg_type, data):
		'''
		Non blocking. Sends without listening.
		Good if you don't care about how your message is handled.
		'''
		message = Message(msg_type, data)
		self._async.send(message)

	def send_action(self, data):
		self.send('action', data)


if __name__ == '__main__':
	client = Client()
	client.connect(IP, PORT)
	time.sleep(1)
	client.send_action({'type': 'key_press'})
	time.sleep(2)