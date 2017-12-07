from jamon.main import *
import sys
from kivy.core.window import Window


if __name__ == '__main__':
	Window.fullscreen = 'auto'
	run(MainWidget, sys.argv)