#!/usr/bin/env python3
# -*- coding: utf8 -*-

from engine import GameObject
from engine.elements import Box

from tabs import colors


class Settings(GameObject):
	def start(self):
		self.box_browse = Box("browse")
		self.box_view = Box("view")
		self.resize()
		self.selected = 0

	def update(self):
		self.resize()
		if self.game.tab == 1:
			self.draw()
			c = -1 if self.game.escaped else self.game.getKeyRaw()
			if c == ord('h'):
				self.selected = self.selected - 1 if self.selected > 0 else 1
			elif c == ord('l'):
				self.selected = self.selected + 1 if self.selected < 1 else 0

	def resize(self):
		self.box_browse.set_pos(0, 0, self.game.screen.width // 3, self.game.screen.height // 2)
		self.box_view.set_pos(self.game.screen.width // 3, 0, 2 * self.game.screen.width // 3 + 1, self.game.screen.height // 2)

	def draw(self):
		self.box_browse.draw(self.game.screen, colors.box_active[0] if self.selected == 0 else colors.box[0], colors.box_active[1] if self.selected == 0 else colors.box[1])
		self.box_view.draw(self.game.screen, colors.box_active[0] if self.selected == 1 else colors.box[0], colors.box_active[1] if self.selected == 0 else colors.box[1])

