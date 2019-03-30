#!/usr/bin/env python3
# -*- coding: utf8 -*-

from engine import Game


class Helper(Game):
	def start(self):
		self.number = 0
		self.chars = ''
		self.updateChars()

	def update(self):
		c = self.getKeyRaw()
		if c == ord(']'):
			self.number = (self.number + 1) % 81
			# self.updateChars()
		elif c == ord('['):
			self.number = (self.number - 1) % 81
			# self.updateChars()
		# elif c == ord('.'):
		# 	self.updateChars()
		self.updateChars()
			
		number = self.number
		up = number // 27
		number -= up * 27
		down = number // 9
		number -= down * 9
		left = number // 3
		number -= left * 3
		right = number
		self.screen.addstr(0, 0, self.number)
		self.screen.addstr(1, 0, up)
		self.screen.addstr(2, 0, down)
		self.screen.addstr(3, 0, left)
		self.screen.addstr(4, 0, right)
		y = 1
		x = 5
		self.screen.addstr(y - 1, x + 1, 'V')
		self.screen.addstr(y + 1, x - 1, '>   <')
		self.screen.addstr(y + 4, x + 1, '^')
		self.screen.addstr(y + 0, x + 1, [' ', '╻', '║'][up % 3])
		self.screen.addstr(y + 2, x + 1, [' ', '╹', '║'][down])
		self.screen.addstr(y + 1, x + 0, [' ', '╺', '═'][left])
		self.screen.addstr(y + 1, x + 2, [' ', '╸', '═'][right])
		self.screen.addstr(y + 1, x + 1, self.chars[self.number] if self.number < len(self.chars) - 1 else ' ')
		self.screen.refresh()

	def updateChars(self):
		with open("chars", 'r') as chars:
			self.chars = chars.readline()
			chars.close()


if __name__ == "__main__":
	helper = Helper()

