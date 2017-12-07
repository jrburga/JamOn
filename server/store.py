class Store(dict):
	def __init__(self, kwargs):
		super(Store, self).__init__(kwargs)

	def __getattr__(self, name):
		return self[name]

	def __setattr__(self, name, value):
		assert False, 'cannot change store values'

	def __setitem__(self, key, value):
		assert False, 'cannot change store values'

class MemberStore(Store):
	def __init__(self, username, id, ip, is_host):
		store_dict = {'username': username, 
					 'id': id, 'ip': ip, 
					 'is_host': is_host}
		super(MemberStore, self).__init__(**store_dict)

class PatternStore(Store):
	def __init__(self, member_id, pattern):
		store_dict = {'member_id': member_id, 'pattern': pattern}
		super(PatternStore, self).__init__(store_dict)

if __name__ == '__main__':
	bm = MemberStore('jake', 1234, '0.0.0.0', True)
	print bm.is_host