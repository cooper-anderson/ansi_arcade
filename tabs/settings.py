#!/usr/bin/env python3
# -*- coding: utf8 -*-

from engine.elements import Element, Tab, List, Box

from tabs import colors


class Item(Element):
	def start(self):
		self.set_label(" > Item" + str(self.element_id))

	def draw(self):
		if self.element_id < self.parent.height - 2:
			self.parent.addstr(self.element_id, 0, self.label + ' ' * (self.parent.width - len(self.label) - 2), self.fg, self.bg)


class Browse(Box):
	def resize(self):
		self.set_pos(0, 0, self.parent.width // 3, self.parent.height // 2)


class View(Box):
	def resize(self):
		self.set_pos(self.parent.width // 3, 0, 2 * self.parent.width // 3 + 1, self.parent.height // 2)


class InnerList(List):
	# def __init__(self):
	# 	super().__init__()
	# 	self.set_colors(colors.box, colors.box_active)

	def update(self, c=-1):
		if c == ord('j'):
			self.next()
		elif c == ord('k'):
			self.prev()

	def __update__(self, c=-1):
		self.resize()
		self.update(c)
		self.draw()
		self.moved -= 1 if self.moved else 0
		for child in self.children:
			color = self.color_active if self.selected == child.element_id and self.parent.selected == self.element_id else self.color_default
			child.set_color(color[0], color[1])
			child.__update__(c if self.selected == child.element_id and not self.moved else -1)


class Dropdown(InnerList):
	def start(self):
		self.set_colors(colors.box, colors.box_active)
		for i in range(8):
			self.add_child(Item)

	def resize(self):
		self.set_pos(0, self.parent.height // 2, self.parent.width // 2 - 1, self.parent.height // 2 + 1)


class Checkbox(InnerList):
	def start(self):
		self.set_colors(colors.box, colors.box_active)
		for i in range(8):
			child = self.add_child(Item)
			child.set_label('[' + ('x' if i % 2 else ' ') + "] Checkbox " + str(i))

	def resize(self):
		self.set_pos(self.parent.width // 2 - 1, self.parent.height // 2, self.parent.width // 2 + 1, self.parent.height // 2 + 1)


class Settings(Tab):
	def start(self):
		self.list = self.add_child(List)
		self.list.set_colors(colors.box, colors.box_active)
		self.box_browse = self.list.add_child(Browse).set_label("browse")
		self.box_view = self.list.add_child(View).set_label("view")
		self.list_dropdown = self.list.add_child(Dropdown)
		self.list_checkbox = self.list.add_child(Checkbox)

	def update(self, c=-1):
		self.addstr(0, 0, c)
		if c == ord('h'):
			self.list.prev()
		elif c == ord('l'):
			self.list.next()

	def resize(self):
		self.set_pos(0, 0, self.screen.width, self.screen.height - 1)

