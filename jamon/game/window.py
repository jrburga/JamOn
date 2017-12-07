import platform

plat = platform.system()

if plat == 'Windows':
	# WINDOWS MACHINES
	from win32api import GetSystemMetrics
	w = GetSystemMetrics(0)
	h = GetSystemMetrics(1)
elif plat == 'Darwin':
	# MAC OSX
	import AppKit
	screen = AppKit.NSScreen.screens()[0]
	w = int(screen.frame().size.width)
	h = int(screen.frame().size.height)
else:
	raise UnsupportedSystemException


class Window:

	width = w
	height = h


class UnsupportedSystemException(Exception):
	pass