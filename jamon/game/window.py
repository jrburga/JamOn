import platform

plat = platform.system()

if plat == 'Windows':
	# WINDOWS MACHINES
	from win32api import GetSystemMetrics
	w = GetSystemMetrics(0)
	h = GetSystemMetrics(1)
elif plat == 'Darwin':
	# MAC OSX

	# import AppKit
	# screen = AppKit.NSScreen.screens()[0]
	# w = int(screen.frame().size.width)
	# h = int(screen.frame().size.height)
	# print w,h

	import subprocess
	import re
	results = str(subprocess.Popen(['system_profiler SPDisplaysDataType'],stdout=subprocess.PIPE, shell=True).communicate()[0])
	res = re.search('Resolution: \d* x \d*', results).group(0).split(' ')
	width, height = int(res[1]), int(res[3])
	
else:
	raise UnsupportedSystemException


class Window:

	width = width
	height = height


class UnsupportedSystemException(Exception):
	pass