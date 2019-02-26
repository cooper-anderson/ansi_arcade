#!/usr/bin/env python3
# -*- coding: utf8 -*-

from engine import GameObject
from engine.elements import Box, Selector

from tabs import colors
from tabs import games


class Library(GameObject):
	def start(self):
		self.selector_games = Selector("games", games.games)
		self.box_description = Box("description")
		self.box_search = Box("search")
		self.resize()
		self.selected = 0

	def update(self):
		self.resize()
		if self.game.tab == 0:
			self.draw()
			c = -1 if self.game.escaped else self.game.getKeyRaw()
			if c == ord('h'):
				self.selected = self.selected - 1 if self.selected > 0 else 2
			elif c == ord('l'):
				self.selected = self.selected + 1 if self.selected < 2 else 0
			if self.selected == 0:
				if c == ord('j'):
					self.selector_games.down()
				elif c == ord('k'):
					self.selector_games.up()
				elif c == 10:
					self.game.game = self.selector_games.get()
					self.game.close()
			self.game.screen.addstr(2, 23, games.descriptions[self.selector_games.get()])

	def resize(self):
		self.selector_games.set_pos(0, 0, self.game.screen.width // 4, self.game.screen.height - 4)
		self.box_description.set_pos(self.game.screen.width // 4, 0, 3 * self.game.screen.width // 4, self.game.screen.height - 4)
		self.box_search.set_pos(0, self.game.screen.height - 4, self.game.screen.width, 3)

	def draw(self):
		self.selector_games.draw(self.game.screen, [colors.box_active[0] if self.selected == 0 else colors.box[0], colors.box_active[1] if self.selected == 0 else colors.box[1]], [-1, -1], colors.button_active)
		self.box_description.draw(self.game.screen, colors.box_active[0] if self.selected == 1 else colors.box[0], colors.box_active[1] if self.selected == 1 else colors.box[1])
		self.box_search.draw(self.game.screen, colors.box_active[0] if self.selected == 2 else colors.box[0], colors.box_active[1] if self.selected == 2 else colors.box[1])
