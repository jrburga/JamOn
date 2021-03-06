from game import GameObject
from random import choice
from server.client import Client
from server.store import Store

member_names = ['Rudolph', 'Dasher', 'Prancer', 'Eran', 'Barry', 'Dancer', 'Vixen', 'Donner', 'Cupid']

def _default_callback(message):
	if message.data['success']:
		result = message.data['result']
		if isinstance(result, dict):
			return Store(result)
		return result

class ClientObject(GameObject):
	'''
	Light weight wrapper to interface with the Client
	'''
	def __init__(self, username=None):
		super(ClientObject, self).__init__()
		self._client = Client()
		self.username = username if username else choice(member_names)
		self.band_members = []
		self.client.register_tether_callback(self.on_action)

	@property
	def client(self):
		return self._client

	@property 
	def id(self):
		return self.client.id

	@property
	def is_host(self):
		return self.client.is_host

	@property
	def addr_str(self):
		return self.client.ip

	@property
	def info(self):
		return {'username': self.username, 
				'id': self.id, 
				'is_host': self.is_host, 
				'addr_str': self.addr_str}

	def post_info(self, info_name, info, callback=_default_callback):
		'''
		Blocking. Use callback to get responses
		'''
		return self.client.post(info_name, info, callback)

	def add_pattern(self, inst, callback=_default_callback):
		pattern_info = {'inst': inst}
		return self.post_info('patterns', pattern_info, callback)

	def add_band_member(self, member_info, callback=_default_callback):
		return self.post_info('band_members', member_info, callback)

	def delete_info(self, info_name, identifier, callback=_default_callback):
		return self.client.delete(info_name, identifier, callback)

	def delete_pattern(self, pattern_id, callback=_default_callback):
		return self.delete_info('patterns', pattern_id, callback)

	def join(self, callback=_default_callback):
		member_id = self.post_info('band_members', self.info, callback)
		self.send_action('on_join')
		return member_id

	def get_info(self, info_name, identifier, callback=_default_callback):
		return self.client.get(info_name, identifier, callback)

	def get_band_members(self, callback=_default_callback):
		return self.get_info('band_members', None, callback)

	def get_pattern(self, identifier, callback=_default_callback):
		return self.get_info('patterns', identifier, callback)

	def connect(self, ip):
		self.client.connect(ip)

	def disconnect(self):
		self.client.disconnect()

	def on_action(self, action):
		self.trigger_event(action['event_type'], **action['action'])

	def send_action(self, event_type, **args):
		'''
		Non blocking. Actions sent to the server
		will be sent back to the other clients
		who will then execute those actions respectively 
		via their event handlers
		'''
		action = {'event_type': event_type, 'action': args}
		self.client.send('action', action)