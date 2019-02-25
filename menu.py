#!/usr/bin/env python3
# -*- coding: utf8 -*-

from engine import Game, GameObject
from engine.color import Color
from engine.elements.box import Box

color_bar = [Color(r=215, g=215, b=105), Color(r=88, g=88, b=88)]
color_bar_active = [Color(r=200, g=200, b=200), Color(r=174, g=96, b=96)]
color_button = [Color(r=0, g=0, b=0), Color(r=215, g=215, b=105)]
color_button_active = [Color(r=0, g=0, b=0), Color(r=125, g=215, b=85)]
color_box = [Color(r=255, g=255, b=255), -1]
color_box_active = [Color(r=215, g=96, b=96), -1]

games = {"Braille": "braille.py", "Dithering": "dithering.py", "2D Rubics Cube": "puzzle.py", "Exit": "-1"}


class Library(GameObject):
	def start(self):
		self.box_games = Box("games")
		self.box_description = Box("description")
		self.resize()
		self.selected = 0

	def update(self):
		self.resize()
		if self.game.tab == 0:
			self.draw()
			c = -1 if self.game.escaped else self.game.getKeyRaw()
			if c == ord('h'):
				self.selected = self.selected - 1 if self.selected > 0 else 1
			elif c == ord('l'):
				self.selected = self.selected + 1 if self.selected < 1 else 0

	def resize(self):
		self.box_games.set_pos(0, 0, self.game.screen.width // 4, self.game.screen.height - 4)
		self.box_description.set_pos(self.game.screen.width // 4, 0, 3 * self.game.screen.width // 4, self.game.screen.height - 4)

	def draw(self):
		self.box_games.draw(self.game.screen, color_box_active[0] if self.selected == 0 else color_box[0], color_box_active[1] if self.selected == 0 else color_box[1])
		self.box_description.draw(self.game.screen, color_box_active[0] if self.selected == 1 else color_box[0], color_box_active[1] if self.selected == 0 else color_box[1])


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
		self.box_browse.draw(self.game.screen, color_box_active[0] if self.selected == 0 else color_box[0], color_box_active[1] if self.selected == 0 else color_box[1])
		self.box_view.draw(self.game.screen, color_box_active[0] if self.selected == 1 else color_box[0], color_box_active[1] if self.selected == 0 else color_box[1])


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
		self.box_output.draw(self.game.screen, color_box_active[0] if self.selected == 2 else color_box[0], color_box_active[1] if self.selected == 0 else color_box[1])
		self.box_prompt.draw(self.game.screen, color_box_active[0] if self.selected == 1 else color_box[0], color_box_active[1] if self.selected == 0 else color_box[1])
		self.box_log.draw(self.game.screen, color_box_active[0] if self.selected == 0 else color_box[0], color_box_active[1] if self.selected == 0 else color_box[1])


class Menu(Game):
	def start(self):
		self.tab = 0
		self.target = 0
		self.escaped = False
		self.tab_settings = self.instantiate(Settings)
		self.tab_library = self.instantiate(Library)
		self.tab_console = self.instantiate(Console)
		self.debug = False

	def update(self):
		c = self.getKeyRaw()
		if self.debug:
			self.screen.addstr(0, 0, c)
		if c == 127:
			self.debug = not self.debug
		if c == ord('a'):
			self.target = 0
		elif c == ord('s'):
			self.target = 1
		elif c == ord('`'):
			self.target = 2
		elif self.tab == 3 or c == 4:
			self.close()
			return
		elif c == 27:
			self.escaped = not self.escaped
			self.target = self.tab
		elif c == 10:
			if self.escaped:
				self.escaped = False
				self.tab = self.target
		elif self.escaped and c == ord('h'):
			self.target = self.target - 1 if self.target > 0 else 3
		elif self.escaped and c == ord('l'):
			self.target = self.target + 1 if self.target < 3 else 0
		if not self.escaped:
			self.tab = self.target
		self.screen.addstr(self.screen.height - 1, 0, ' ' * self.screen.width, color_bar_active[0] if self.escaped else color_bar[0], color_bar_active[1] if self.escaped else color_bar[1])
		# Library
		self.screen.addstr(self.screen.height - 1, self.screen.width // 2 - 25, ' a ', color_button_active[0] if self.target == 0 else color_button[0], color_button_active[1] if self.target == 0 else color_button[1])
		self.screen.addstr(self.screen.height - 1, self.screen.width // 2 - 21, "library", color_bar_active[0] if self.escaped else color_bar[0], color_bar_active[1] if self.escaped else color_bar[1])
		# Settings
		self.screen.addstr(self.screen.height - 1, self.screen.width // 2 - 11, ' s ', color_button_active[0] if self.target == 0 else color_button[0], color_button_active[1] if self.target == 1 else color_button[1])
		self.screen.addstr(self.screen.height - 1, self.screen.width // 2 - 7, "settings", color_bar_active[0] if self.escaped else color_bar[0], color_bar_active[1] if self.escaped else color_bar[1])
		# Console
		self.screen.addstr(self.screen.height - 1, self.screen.width // 2 + 2, ' ` ', color_button_active[0] if self.target == 0 else color_button[0], color_button_active[1] if self.target == 2 else color_button[1])
		self.screen.addstr(self.screen.height - 1, self.screen.width // 2 + 6, "console", color_bar_active[0] if self.escaped else color_bar[0], color_bar_active[1] if self.escaped else color_bar[1])
		# Quit
		self.screen.addstr(self.screen.height - 1, self.screen.width // 2 + 15, ' ^D ', color_button_active[0] if self.target == 0 else color_button[0], color_button_active[1] if self.target == 3 else color_button[1])
		self.screen.addstr(self.screen.height - 1, self.screen.width // 2 + 20, "quit", color_bar_active[0] if self.escaped else color_bar[0], color_bar_active[1] if self.escaped else color_bar[1])
		self.screen.refresh()


if __name__ == "__main__":
	menu = Menu()

