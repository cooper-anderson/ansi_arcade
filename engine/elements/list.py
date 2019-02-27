#!/usr/bin/env python3
# -*- coding: utf8 -*-

from .element import Element


class List(Element):
	def __init__(self, parent, element_id=0):
		self.parent = parent
		self.screen = self.parent.screen
		self.element_id = len(self.parent.children)
		self.children = []
		self.set_label().set_pos().set_color().set_loop().set_colors()
		self.selected = 0
		self.moved = 0

	def set_loop(self, loop=True):
		self.loop = loop
		return self

	def set_colors(self, default=[-1, -1], active=[-1, -1]):
		self.color_default = default
		self.color_active = active
		return self

	def addstr(self, y=0, x=0, string="", fg=-1, bg=-1):
		self.parent.addstr(self.y + y, self.x + x, string, fg, bg)

	def resize(self):
		self.set_pos(0, 0, self.parent.width, self.parent.height)

	def __update__(self, c=-1):
		self.resize()
		self.update(c)
		self.draw()
		self.moved -= 1 if self.moved else 0
		for child in self.children:
			color = self.color_active if self.selected == child.element_id else self.color_default
			child.set_color(color[0], color[1])
			child.__update__(c if self.selected == child.element_id and not self.moved else -1)

	def next(self):
		self.selected = self.selected + 1 if self.selected < len(self.children) - 1 else (0 if self.loop else len(self.children) - 1)
		self.moved = 2

	def prev(self):
		self.selected = self.selected - 1 if self.selected > 0 else (len(self.children) - 1 if self.loop else 0)
		self.moved = 2
