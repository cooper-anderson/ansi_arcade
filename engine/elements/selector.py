#!/usr/bin/env python3
# -*- coding: utf8 -*-

from .list import List
from .label import Label


class Selector(List):
	def __init__(self, parent):
		super().__init__(parent)
		self.items = []

	def set_items(self, items=[]):
		for item in items:
			self.add_item(item)
		return self

	def add_item(self, item):
		self.items.append(item)
		self.add_child(Label).set_label(item)
		return self

	def get(self):
		return self.items[self.selected]

	def __update__(self, c=-1):
		self.resize()
		self.update(c)
		self.draw()
		self.moved -= 1 if self.moved else 0
		for child in self.children:
			color = self.color_active if self.selected == child.element_id else self.color_default
			child.set_color(color[0], color[1])
			child.set_pos(self.x - 1, self.y + child.element_id - 1, 0, 0)
			child.__update__(c if self.selected == child.element_id and not self.moved else -1)


