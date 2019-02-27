#!/usr/bin/env python3
# -*- coding: utf8 -*-

from .element import Element


class Label(Element):
	def addstr(self, y=0, x=0, string="", fg=-1, bg=-1):
		self.parent.addstr(self.y + y + 1, self.x + x + 1, string, fg, bg)

	def draw(self):
		self.addstr(0, 0, self.label + ' ' * (self.parent.width - len(self.label) - 2), self.fg, self.bg)

