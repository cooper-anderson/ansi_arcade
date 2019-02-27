#!/usr/bin/env python3
# -*- coding: utf8 -*-

from engine.elements import Tab, List, Box, Selector

from tabs import colors
from tabs import games


class Games(Box):
	def start(self):
		self.list = self.add_child(Selector).set_loop(False).set_colors(colors.default, colors.button_active)
		# self.list.set_items(["test" + str(i) for i in range(30)])
		self.list.set_items(games.games)

	def update(self, c=-1):
		if c == ord('j'):
			self.list.next()
		elif c == ord('k'):
			self.list.prev()
		elif c == 10:
			self.screen.pause()
			games.executables[self.list.get()]()
			self.screen.resume()

	def resize(self):
		self.set_pos(0, 0, self.parent.width // 4, self.parent.height - 3)


class Description(Box):
	def update(self, c=-1):
		self.addstr(0, 1, games.descriptions[self.parent.parent.box_games.list.get()])

	def resize(self):
		self.set_pos(self.parent.width // 4, 0, 3 * self.parent.width // 4, self.parent.height - 3)


class Search(Box):
	def update(self, c=-1):
		self.addstr(0, 1, self.parent.parent.box_games.list.get())

	def resize(self):
		self.set_pos(0, self.parent.height - 3, self.parent.width, 3)


class Library(Tab):
	def start(self):
		self.list = self.add_child(List)
		self.list.set_colors(colors.box, colors.box_active)
		self.box_games = self.list.add_child(Games).set_label("games")
		self.box_description = self.list.add_child(Description).set_label("description")
		self.box_search = self.list.add_child(Search).set_label("search")

	def update(self, c=-1):
		self.addstr(0, 0, c)
		if c == ord('h'):
			self.list.prev()
		elif c == ord('l'):
			self.list.next()

	def resize(self):
		self.set_pos(0, 0, self.screen.width, self.screen.height - 1)

