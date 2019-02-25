#!/usr/bin/env python3
# -*- coding: utf8 -*-

from time import sleep
from elements.element import Element
from screen import Screen
from color import Color


class Box(Element):
	def __init__(self, x=0, y=0, width=10, height=5, label="", color=-1):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.label = label
		self.color = color

	def draw(self, screen):
		self.width = max(self.width, 9)
		self.height = max(self.height, 2)
		for h in range(1, self.height - 1):
			screen.addstr(self.y + h, self.x, '│', self.color)
			screen.addstr(self.y + h, self.x + self.width - 1, '│', self.color)
		screen.addstr(self.y + self.height - 1, self.x, '└' + '─' * (self.width - 2) + '┘', self.color)
		if self.label == "":
			screen.addstr(self.y, self.x, '┌' + '─' * (self.width - 2) + '┐', self.color)
		else:
			label = self.label + ' ' + ('─' * (self.width - len(self.label) - 6)) if len(self.label) < self.width - 7 else self.label[:self.width - 8] + ".. "
			screen.addstr(self.y, self.x, "┌─ " + label + '─┐', self.color)


if __name__ == "__main__":
	screen = Screen()
	box = Box(1, 1, 10, 5, "example", Color(r=255, g=255, b=255))
	try:
		while True:
			c = screen.getch()
			if c == ord('l'):
				box.width += 1
			elif c == ord('h'):
				box.width -= 1
			elif c == ord('k'):
				box.height -= 1
			elif c == ord('j'):
				box.height += 1
			screen.addstr(0, 11, "a")
			screen.addstr(6, 0, "a")
			box.draw(screen)
			screen.refresh()
			sleep(1.0 / 30.0)
	finally:
		screen.close()

