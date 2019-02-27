#!/usr/bin/env python3
# -*- coding: utf8 -*-


class Element(object):
	def __init__(self, parent, element_id=0):
		self.parent = parent
		self.element_id = element_id
		self.screen = self.parent.screen
		self.children = []
		self.set_label().set_pos().set_color()
		self.element_id = len(self.parent.children)

	def add_child(self, child):
		instance = child(self)
		self.children.append(instance)
		instance.start()
		return instance

	def set_pos(self, x=0, y=0, width=0, height=0):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		return self

	def set_label(self, label=""):
		self.label = label
		return self

	def set_color(self, fg=-1, bg=-1):
		self.fg = fg
		self.bg = bg
		return self

	def set_id(self, element_id=0):
		self.element_id = element_id
		return self

	def addstr(self, y=0, x=0, string="", fg=-1, bg=-1):
		self.parent.addstr(self.y + y + 1, self.x + x + 1, string, fg, bg)

	def start(self):
		pass

	def update(self, c=-1):
		pass

	def resize(self):
		pass

	def draw(self):
		pass

	def __update__(self, c=-1):
		self.resize()
		self.update(c)
		self.draw()
		for child in self.children:
			child.__update__(c)

