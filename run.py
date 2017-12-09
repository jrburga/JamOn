import sys
from server.store import Store
from jamon.main import *
from kivy.core.window import Window

defaults = {
	'windowed': False,
	'scene': None
}

values = {
	'True': True,
	'False': False
}

def eval_val(value):
	if value in values:
		return values[value]
	
	return value

def parse_args(argv):
	for arg in argv[1:]:
		key, value = arg.split('=')
		defaults[key] = eval_val(value)
	return Store(defaults)

if __name__ == '__main__':
	args = parse_args(sys.argv)
	run(MainWidget, args)