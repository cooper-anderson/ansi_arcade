#!/usr/bin/env python3
# -*- coding: utf8 -*-

from engine import Game
from tabs import Library, Settings, Console, games, colors


class Menu(Game):
	def start(self):
		self.game = ""
		self.tab = 0
		self.target = 0
		self.escaped = 0
		self.tab_settings = self.instantiate(Settings)
		self.tab_library = self.instantiate(Library)
		self.tab_console = self.instantiate(Console)
		self.debug = False

	def update(self):
		if self.escaped == 1:
			self.escaped = 0
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
			self.escaped = 2 - self.escaped
			self.target = self.tab
		elif c == 10:
			if self.escaped:
				self.escaped = 1
				self.tab = self.target
		elif self.escaped and c == ord('h'):
			self.target = self.target - 1 if self.target > 0 else 3
		elif self.escaped and c == ord('l'):
			self.target = self.target + 1 if self.target < 3 else 0
		if not self.escaped:
			self.tab = self.target
		self.screen.addstr(self.screen.height - 1, 0, ' ' * self.screen.width, colors.bar_active[0] if self.escaped else colors.bar[0], colors.bar_active[1] if self.escaped else colors.bar[1])
		# Library
		self.screen.addstr(self.screen.height - 1, self.screen.width // 2 - 25, ' a ', colors.button_active[0] if self.target == 0 else colors.button[0], colors.button_active[1] if self.target == 0 else colors.button[1])
		self.screen.addstr(self.screen.height - 1, self.screen.width // 2 - 21, "library", colors.bar_active[0] if self.escaped else colors.bar[0], colors.bar_active[1] if self.escaped else colors.bar[1])
		# Settings
		self.screen.addstr(self.screen.height - 1, self.screen.width // 2 - 11, ' s ', colors.button_active[0] if self.target == 0 else colors.button[0], colors.button_active[1] if self.target == 1 else colors.button[1])
		self.screen.addstr(self.screen.height - 1, self.screen.width // 2 - 7, "settings", colors.bar_active[0] if self.escaped else colors.bar[0], colors.bar_active[1] if self.escaped else colors.bar[1])
		# Console
		self.screen.addstr(self.screen.height - 1, self.screen.width // 2 + 2, ' ` ', colors.button_active[0] if self.target == 0 else colors.button[0], colors.button_active[1] if self.target == 2 else colors.button[1])
		self.screen.addstr(self.screen.height - 1, self.screen.width // 2 + 6, "console", colors.bar_active[0] if self.escaped else colors.bar[0], colors.bar_active[1] if self.escaped else colors.bar[1])
		# Quit
		self.screen.addstr(self.screen.height - 1, self.screen.width // 2 + 15, ' ^D ', colors.button_active[0] if self.target == 0 else colors.button[0], colors.button_active[1] if self.target == 3 else colors.button[1])
		self.screen.addstr(self.screen.height - 1, self.screen.width // 2 + 20, "quit", colors.bar_active[0] if self.escaped else colors.bar[0], colors.bar_active[1] if self.escaped else colors.bar[1])
		self.screen.refresh()


if __name__ == "__main__":
	menu = Menu()
	if menu.game in games.executables:
		games.executables[menu.game]()

