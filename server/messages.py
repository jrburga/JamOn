import json

def fromJSON(json_string):
	py_dict = json.loads(json_string)
	return Message(**py_dict)

def toJSON(message):
	return json.dumps(message)

class Message(dict):
	def __init__(self, type, data={}, message_id=None):
		super(Message, self).__init__()
		self['type'] = type
		self['data'] = data.copy()
		self['message_id'] = message_id if message_id else id(self)

	@property
	def type(self):
		return self['type']

	@property
	def id(self):
		return self['message_id']
	@property
	def data(self):
		return self['data']

class Action(Message):
	def __init__(self, data={}):
		super(Action, self).__init__('action', data)


class Post(Message):
	def __init__(self, data={}):
		super(Post, self).__init__('post', data)

class Get(Message):
	def __init__(self, data={}):
		super(Get, self).__init__('get', data)

class Connect(Message):
	def __init__(self, data={}):
		super(Connect, self).__init__('connect', data)

class Disconnect(Message):
	def __init__(self, data={}):
		super(Connect, self).__init__('disconnect', data)

class Join(Message):
	def __init__(self, data={}):
		super(Join, self).__init__('join', data)

class Tether(Message):
	def __init__(self, data={}):
		super(Tether, self).__init__('tether', data)

class Close(Message):
	def __init__(self, data={}):
		super(Tether, self).__init__('close', data)

class Error(Message):
	def __init__(self, data={}):
		super(Error, self).__init__('error', data)

class ServerAction(Message):
	def __init__(self, action):
		super(ServerAction, self).__init__(
			'server_action', action=action)
