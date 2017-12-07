from connections import *
from thread import *
from client import Client

MAX_CLIENTS = 4

class Server(object):
	def __init__(self, ip=IP):
		self.ip = ip
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._host_id = None
		self._sync = {}
		self._async = {}
		self._accept_thread = None
		self._info = {}
		self._max_clients = MAX_CLIENTS
		self._clients = 0


		self._on_join_callback = lambda conn, res: None

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
			accepting = self._connect(connection)
		print 'host no longer accepting connections'
		self._accept_thread = None

	def register_on_join(self, callback):
		self._on_join_callback = callback

	def _connect(self, conn):
		print 'found connection', conn.id
		conn.send(Connect({'success': True}))
		print 'waiting for client to respond'
		res = conn.recv()[0]
		if res.type == 'join':
			return self._join(conn, res)
		elif res.type == 'tether':
			return self._tether(conn, res)
		elif res.type == 'server':
			return self._server(conn, res)

	def _server(self, conn, res):
		conn.send(ServerMessage({'success': True}))
		return False

	def _join(self, conn, res):
		is_host = False
		if self._host_id == None:
			is_host = True
			self._host_id = conn.id
		self._sync[conn.id] = conn
		start_new_thread(self._listen, (conn, ))
		conn.send(Join({'success': True, 'id': conn.id, 'host': is_host}))
		self._clients += 1
		self._on_join_callback(conn, res)
		return True

	def _tether(self, conn, res):
		conn.id = res.id
		self._async[res.id] = conn
		start_new_thread(self._listen_tether, (conn, ))
		conn.send(Tether({'success': True}))
		return True

	def start(self):
		self._bind(PORT)
		self.start_accepting()


	def start_accepting(self):
		if not self._accept_thread:
			self._accept_thread = start_new_thread(self._accept, ())
			self._accept_thread = True

	def stop_accepting(self):
		ServerClient().connect(PUBLIC)
		
	def close(self):
		print 'closing server'
		# for conn in self._sync.values():
		# 	conn.close()
		# for conn in self._async.values():
		# 	conn.close()

		self._socket.close()
		print 'server closed'

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
		while not connection.closed:
			for message in connection.recv():
				if message.type == 'post':
					self._post(message, connection)
				elif message.type == 'get':
					self._get(message, connection)
				else:
					self._error(message, connection)
		print connection, 'exiting join'

	def _listen_tether(self, connection):
		while not connection.closed:
			for message in connection.recv():
				self._send_all(message, connection)

		print connection, 'exiting tether'



class ServerClient(Client):
	def __init__(self, ip=IP):
		super(ServerClient, self).__init__(ip)

	def _server(self, ip, port, timeout):
		conn = self._connect(self._socket_sync, ip, port, timeout)
		conn.send(ServerMessage())
		res = conn.recv().pop(0)
		if res.data['success']:
			conn.close()
			print 'server client successfully closed'

	def connect(self, ip, port=PORT, timeout=TIMEOUT):
		self._server(ip, port, timeout)

if __name__ == '__main__':
	server = Server()
	server.start()
