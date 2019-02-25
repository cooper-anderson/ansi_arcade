#!/usr/bin/env python
# -*- coding: utf8 -*-

import locale
import os
import termios
import sys
import time
from array import array
from fcntl import ioctl
from select import select
from signal import signal, SIGWINCH
from random import randint

if __name__ == "__main__":
	from color import Color, Colors
else:
	from . import color

locale.setlocale(locale.LC_ALL, '')
os.environ.setdefault("ESCDELAY", "25")
ESC = "\033["


class Size(object):
	width = 0
	height = 0


class Vector(object):
	x = 0
	y = 0

	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y


class Row(object):
	def __init__(self):
		pass


class Map(object):
	def __init__(self):
		pass


class Screen(object):
	def __init__(self):
		print(ESC + "?1049h" + ESC + "?25l" + ESC + "2J", end="")
		self.size = Size()
		self._initial = termios.tcgetattr(1)
		t = termios.tcgetattr(1)
		t[3] &= ~(termios.ECHO | termios.ICANON | termios.OPOST)
		termios.tcsetattr(1, termios.TCSANOW, t)
		self._resize()
		self.queue = ""
		self.colorIndex = -1
		signal(SIGWINCH, self._resize)

	def _resize(self, a=0, b=0):
		buf = array('h', [0, 0])
		ioctl(1, termios.TIOCGWINSZ, buf, 1)
		self.size.width = buf.pop()
		self.size.height = buf.pop()
		self.width = self.size.width
		self.height = self.size.height

	def clear(self):
		print(ESC + "2J", end="")

	def close(self):
		termios.tcsetattr(1, termios.TCSANOW, self._initial)
		print("\033[?1049l", end="")
		print("\033[?25h", end="")
		termios.tcflush(sys.stdin, termios.TCIOFLUSH)
		print("[Process closed]")

	def addstr(self, y=0, x=0, string="", fg=-1):
		if fg == -1:
			# print(ESC + str(y+1) + ';' + str(x+1) + 'H' + str(string), end='\r')
			self.queue += ESC + str(y+1) + ';' + str(x+1) + 'H' + str(string)
		else:
			colorIndex = 16 + 36 * round(fg.getRed() / 51.0) + 6 * round(fg.getGreen() / 51.0) + round(fg.getBlue() / 51)
			# print(ESC + str(y+1) + ';' + str(x+1) + 'H' + ESC + "38;5;" + str(colorIndex) + "m" + str(string), end='\r')
			self.queue += ESC + str(y+1) + ';' + str(x+1) + 'H' + ESC + "38;5;" + str(colorIndex) + "m" + str(string)

	def refresh(self):
		print(self.queue, end='\r')
		self.queue = ""

	def getch(self, timeout=0, flush=True):
		# rlist, _, _ = select([sys.stdin], [], [], timeout)
		# if rlist:
		# 	s = sys.stdin.read(1)
		# 	if flush:
		# 		termios.tcflush(sys.stdin, termios.TCIOFLUSH)
		# 	return ord(s)
		# return -1
		if select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
			s = ord(sys.stdin.read(1))
			self.flushinp()
			return s
		else:
			return -1

	def flushinp(self):
		termios.tcflush(sys.stdin, termios.TCIOFLUSH)

	def autoflushinp(self, flag=True):
		pass

	def inpdelay(self, flag):
		pass


if __name__ == "__main__":
	screen = Screen()
	guy = Vector(screen.size.width // 2, screen.size.height // 2)
	clear = True
	rand = False
	letter = 0
	sprites = ['o', 'O']
	sIndex = 0
	r = 5
	g = 5
	b = 5
	try:
		color2 = Color(r=0, g=255, b=0)
		count = 0
		while True:
			if clear:
				screen.clear()
			if rand:
				for i in range(int(screen.size.width * screen.size.height * .0125)):
					x = randint(0, screen.size.width)
					y = randint(0, screen.size.height)
					screen.addstr(y, x, str(randint(0, 9)))
			c = screen.getch()
			if c != -1:
				letter = c
			if c == ord('w'):
				guy.y -= 1
			elif c == ord('s'):
				guy.y += 1
			elif c == ord('a'):
				guy.x -= 1
			elif c == ord('d'):
				guy.x += 1
			elif c == ord('m'):
				clear = not clear
			elif c == ord('r'):
				rand = not rand
			elif c == ord('u'):
				r = min(r+1, 5)
			elif c == ord('j'):
				r = max(r-1, 0)
			elif c == ord('i'):
				g = min(g+1, 5)
			elif c == ord('k'):
				g = max(g-1, 0)
			elif c == ord('o'):
				b = min(b+1, 5)
			elif c == ord('l'):
				b = max(b-1, 0)
			# r = randint(0, 5)
			# g = randint(0, 5)
			# b = randint(0, 5)
			if count % 30 == 0:
				sIndex = 1 - sIndex
			screen.addstr(guy.y, guy.x, sprites[sIndex], color2)
			color2.setHue(count * 2)
			screen.addstr(1, 1, count, Colors.white)
			screen.addstr(2, 1, chr(letter))
			screen.addstr(screen.height - 2, screen.width - 25, "Try resizing your window")
			screen.addstr(screen.height - 3, screen.width - 25, "Buttons: wasdrmuiojkl")
			count += 1
			screen.refresh()
			time.sleep(1.0 / 60.0)
	except KeyboardInterrupt:
		pass
	finally:
		screen.close()

