#!/usr/bin/env python3
# -*- coding: utf8 -*-

# from time import sleep
from .element import Element
# from screen import Screen
# from color import Color


class Box(Element):
	def __init__(self, label="", x=0, y=0, width=10, height=5, fg=-1, bg=-1):
		self.label = label
		self.set_pos(x, y, width, height)
		self.fg = fg
		self.bg = bg

	def set_pos(self, x=0, y=0, width=10, height=5):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	def draw(self, screen, fg=-1, bg=-1):
		self.fg = self.fg if fg == -1 else fg
		self.bg = self.bg if bg == -1 else bg
		self.width = max(self.width, 9)
		self.height = max(self.height, 2)
		for h in range(1, self.height - 1):
			screen.addstr(self.y + h, self.x, '│', self.fg, self.bg)
			screen.addstr(self.y + h, self.x + self.width - 1, '│', self.fg, self.bg)
		screen.addstr(self.y + self.height - 1, self.x, '└' + '─' * (self.width - 2) + '┘', self.fg, self.bg)
		if self.label == "":
			screen.addstr(self.y, self.x, '┌' + '─' * (self.width - 2) + '┐', self.fg, self.bg)
		else:
			label = self.label + ' ' + ('─' * (self.width - len(self.label) - 6)) if len(self.label) < self.width - 7 else self.label[:self.width - 8] + ".. "
			screen.addstr(self.y, self.x, "┌─ " + label + '─┐', self.fg, self.bg)


# if __name__ == "__main__":
# 	screen = Screen()
# 	box = Box(1, 1, 10, 5, "example", Color(r=255, g=255, b=255))
# 	try:
# 		while True:
# 			c = screen.getch()
# 			if c == ord('l'):
# 				box.width += 1
# 			elif c == ord('h'):
# 				box.width -= 1
# 			elif c == ord('k'):
# 				box.height -= 1
# 			elif c == ord('j'):
# 				box.height += 1
# 			screen.addstr(0, 11, "a")
# 			screen.addstr(6, 0, "a")
# 			box.draw(screen)
# 			screen.refresh()
# 			sleep(1.0 / 30.0)
# 	finally:
# 		screen.close()

