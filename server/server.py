from connections import *
from client import Client

class Server(object):
	def __init__(self, ip=IP):
		self.ip = ip
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._host_id = None
		self._sync = {}
		self._async = {}
		self._accept_thread = None

	def _bind(self, port):
		print 'host binding to (%s, %i)' % (self.ip, port)
		self._socket.bind((self.ip, port))
		self._socket.listen(16)

	def _accept(self):
		accepting = True
		while accepting:
			print 'waiting for next connection'
			conn, addr = self._socket.accept()
			connection = Connection(conn, addr)
			self._connect(connection)
			print 'synced connections', self._sync
			print 'async connections', self._async
		print 'host no longer accepting connections'

	def _connect(self, conn):
		print 'found connection', conn.id
		conn.send(Connect({'success': True}))
		print 'waiting for client to respond'
		res = conn.recv()[0]
		print res
		if res.type == 'join':
			self._join(conn)
		if res.type == 'tether':
			self._tether(conn, res.data['id'])

	def _join(self, conn):
		is_host = False
		if self._host_id == None:
			is_host = True
			self._host_id = conn.id
		self._sync[conn.id] = conn
		t = threading.Thread(target=self._listen, args=(conn, ))
		t.start()
		conn.send(Join({'success': True, 'id': conn.id, 'host': is_host}))

	def _tether(self, conn, id):
		conn.id = id
		self._async[id] = conn
		t = threading.Thread(target=self._listen_tether, args=(conn, ))
		t.start()
		conn.send(Tether({'success': True}))

	def start(self):
		if self._accept_thread != None: return
		self._bind(PORT)
		self._accept_thread = threading.Thread(target=self._accept)
		self._accept_thread.start()
		
	def close(self):
		self._socket.close()

	def _post(self, msg, conn):
		print 'echoing post'
		conn.send(Post({'success': True, 'message_id': msg.id}))

	def _get(self, msg, conn):
		print 'echoing get'
		conn.send(Get({'success': True, 'message_id': msg.id}))

	def _error(self, msg, conn):
		print 'echoing error'
		conn.send(Error({'success': False, 
						 'message': 'message type not found',
						 'code': 0,
						 'message_id': msg.id}))

	def _send_all(self, message, connection):
		if message.type != 'action': return
		for conn in self._async.values():
			conn.send(message)

	def _listen(self, connection):
		listening = True
		while listening:
			for message in connection.recv():
				if message.type == 'post':
					self._post(message, connection)
				elif message.type == 'get':
					self._get(message, connection)
				else:
					self._error(message, connection)

	def _listen_tether(self, connection):
		listening = True
		while listening:
			for message in connection.recv():
				self._send_all(message, connection)



class ServerClient(Client):
	def __init__(self, ip=IP):
		super(OwnClient, self).__init__(ip)
		self._server_action = 'stop_accepting'

if __name__ == '__main__':
	server = Server()
	server.start()
