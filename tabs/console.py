#!/usr/bin/env python3
# -*- coding: utf8 -*-

from engine import GameObject
from engine.elements import Box

from tabs import colors


class Console(GameObject):
	def start(self):
		self.box_output = Box("command output")
		self.box_prompt = Box("prompt")
		self.box_log = Box("debug log")
		self.resize()
		self.selected = 1

	def update(self):
		self.resize()
		if self.game.tab == 2:
			self.draw()
			c = -1 if self.game.escaped else self.game.getKeyRaw()
			if c == ord('h'):
				self.selected = self.selected - 1 if self.selected > 0 else 2
			elif c == ord('l'):
				self.selected = self.selected + 1 if self.selected < 2 else 0

	def resize(self):
		self.box_output.set_pos(0, 0, self.game.screen.width // 2, self.game.screen.height - 4)
		self.box_prompt.set_pos(0, self.game.screen.height - 4, self.game.screen.width // 2, 3)
		self.box_log.set_pos(self.game.screen.width // 2, 0, self.game.screen.width // 2, self.game.screen.height - 1)

	def draw(self):
		self.box_output.draw(self.game.screen, colors.box_active[0] if self.selected == 2 else colors.box[0], colors.box_active[1] if self.selected == 0 else colors.box[1])
		self.box_prompt.draw(self.game.screen, colors.box_active[0] if self.selected == 1 else colors.box[0], colors.box_active[1] if self.selected == 0 else colors.box[1])
		self.box_log.draw(self.game.screen, colors.box_active[0] if self.selected == 0 else colors.box[0], colors.box_active[1] if self.selected == 0 else colors.box[1])

