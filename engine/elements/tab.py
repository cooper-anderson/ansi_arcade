#!/usr/bin/env python3
# -*- coding: utf8 -*-

from .element import Element


class Tab(Element):
	def __init__(self, screen, element_id=0):
		self.screen = screen
		self.element_id = element_id
		self.children = []
		self.set_label()
		self.set_pos()
		self.start()
		self.resize()

	def resize(self):
		self.set_pos(0, 0, self.screen.width, self.screen.height)

	def addstr(self, y=0, x=0, string="", fg=-1, bg=-1):
		self.screen.addstr(self.y + y, self.x + x, string, fg, bg)

