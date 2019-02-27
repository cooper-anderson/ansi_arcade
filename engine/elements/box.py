#!/usr/bin/env python3
# -*- coding: utf8 -*-

from .element import Element


class Box(Element):
	def draw(self, fg=-1, bg=-1):
		self.fg = self.fg if fg == -1 else fg
		self.bg = self.bg if bg == -1 else bg
		self.width = max(self.width, 9)
		self.height = max(self.height, 2)
		for h in range(1, self.height - 1):
			self.parent.addstr(self.y + h, self.x, '│', self.fg, self.bg)
			self.parent.addstr(self.y + h, self.x + self.width - 1, '│', self.fg, self.bg)
		self.parent.addstr(self.y + self.height - 1, self.x, '└' + '─' * (self.width - 2) + '┘', self.fg, self.bg)
		if self.label == "":
			self.parent.addstr(self.y, self.x, '┌' + '─' * (self.width - 2) + '┐', self.fg, self.bg)
		else:
			label = self.label + ' ' + ('─' * (self.width - len(self.label) - 6)) if len(self.label) < self.width - 7 else self.label[:self.width - 8] + ".. "
			self.parent.addstr(self.y, self.x, "┌─ " + label + '─┐', self.fg, self.bg)

