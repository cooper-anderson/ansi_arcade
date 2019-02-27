#!/usr/bin/env python3
# -*- coding: utf8 -*-

from .element import Element


class Label(Element):
	def draw(self):
		if self.element_id < self.parent.height - 2:
			self.addstr(0, 0, self.label + ' ' * (self.parent.width - len(self.label) - 2), self.fg, self.bg)

