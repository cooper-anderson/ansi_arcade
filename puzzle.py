#!/usr/bin/env python
# -*- coding: utf8 -*-

from engine import Game, GameObject
from engine.color import Color, Colors
from random import randint
from os import environ
from time import sleep

HJKL = "HJKL" in environ and environ["HJKL"] == '1'


class Move:
	up = [ord('k'), ord('K')] if HJKL else [ord('i'), ord('I')]
	down = [ord('j'), ord('J')] if HJKL else [ord('k'), ord('K')]
	left = [ord('h'), ord('H')] if HJKL else [ord('j'), ord('J')]
	right = [ord('l'), ord('L')] if HJKL else [ord('l'), ord('L')]
	upper = [ord('K'), ord('J'), ord('H'), ord('L'), ord('I')]


class Select:
	up = [ord('w'), ord('W')]
	down = [ord('s'), ord('S')]
	left = [ord('a'), ord('A')]
	right = [ord('d'), ord('D')]


class Grid(GameObject):
	def start(self):
		self.x = 5
		self.y = 2
		self.width = 5
		self.height = 5
		self.tiles = [[] for y in range(self.height)]
		for y in range(self.height):
			for x in range(self.width):
				i = y * self.width + x % self.width
				self.tiles[y].append(self.game.instantiate(Tile))
				self.tiles[y][x].x = x
				self.tiles[y][x].y = y
				self.tiles[y][x].value = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz!?"[i]
				self.tiles[y][x].parent = self
				self.tiles[y][x].set_color()
		self.selector = self.game.instantiate(Selector)
		self.selector.parent = self

	def update(self, key=None):
		if self.game.waiting or self.game.victory:
			return
		c = key or self.game.getKeyRaw()
		columns = []
		rows = []
		dx = 0
		dy = 0
		tile = None
		if c in Move.up:
			columns = [self.selector.x]
			rows = [(self.selector.y + i) % self.height for i in range(self.height)]
			dx = 0
			dy = -1
		elif c in Move.down:
			columns = [self.selector.x]
			rows = [(self.selector.y - i) % self.height for i in range(self.height)]
			dx = 0
			dy = 1
		elif c in Move.left:
			columns = [(self.selector.x + i) % self.width for i in range(self.width)]
			rows = [self.selector.y]
			dx = -1
			dy = 0
		elif c in Move.right:
			columns = [(self.selector.x - i) % self.width for i in range(self.width)]
			rows = [self.selector.y]
			dx = 1
			dy = 0
		if dx != 0 or dy != 0:
			self.game.running = not self.game.randomizing
			tile = self.tiles[self.selector.y][self.selector.x]
			self.selector.x = (self.selector.x + dx) % self.width
			self.selector.y = (self.selector.y + dy) % self.height
			for x in columns:
				for y in rows:
					self.tiles[y][x].x = (self.tiles[y][x].x + dx) % self.width
					self.tiles[y][x].y = (self.tiles[y][x].y + dy) % self.height
					self.tiles[y][x] = self.tiles[(y - dy) % self.height][(x - dx) % self.width]
			self.tiles[self.selector.y][self.selector.x] = tile
			if c in Move.upper:
				self.selector.x = (self.selector.x - dx) % self.width
				self.selector.y = (self.selector.y - dy) % self.height


class Tile(GameObject):
	def start(self):
		self.x = 0
		self.y = 0
		self.posx = 0
		self.posy = 0
		self.value = 'A'
		self.parent = None
		self.color_index = 0
		self.color = 0
		self.frame = 0

	def update(self):
		targetx = self.parent.x + self.x * 4
		targety = self.parent.y + self.y * 2
		if abs(self.posx - targetx) > 5:
			self.posx = targetx - 3*int(abs(self.posx - targetx) / (self.posx - targetx))
		if abs(self.posy - targety) > 5:
			self.posy = targety - 2*int(abs(self.posy - targety) / (self.posy - targety))
		self.posx += 1 if self.posx < targetx else -1 if self.posx > targetx else 0
		self.posy += 1 if self.posy < targety else -1 if self.posy > targety else 0
		self.render()

	def render(self):
		fg = Colors.black if self.y * self.parent.width + self.x % self.parent.width + 1 == self.color_index else Colors.white
		bg = self.color if self.y * self.parent.width + self.x % self.parent.width + 1 == self.color_index else -1
		self.game.screen.addstr(self.posy, self.posx - 1, ' ' + self.value + ' ', fg, bg)
		# , self.game.screen.curses.color_pair(3 if self.y * self.parent.width + self.x % self.parent.width + 1 == self.color_index else 2))

	def set_color(self):
		self.color_index = self.y * self.parent.width + self.x % self.parent.width + 1
		self.color = Colors.white
		# self.color = Color(h=360.0 * self.color_index / (self.parent.width * self.parent.height), s=1.0, l=0.5)
		# self.color = Color(r=min(64 * self.x, 255), g=min(64 * self.y, 255), b=255 - min(64 * min(self.x, self.y), 255))
		# self.color = Color(r=127 + min(32 * self.x, 128), g=127 + min(32 * self.y, 128), b=0)
		# self.color = Color(r=255 - min(64 * min(self.x, self.y), 255), g=min(64 * self.y, 255), b=min(64 * self.x, 255))
		self.posx = self.x
		self.posy = self.y


class Selector(GameObject):
	def start(self):
		self.x = 0
		self.y = 0
		self.parent = None

	def update(self):
		c = self.game.getKeyRaw()
		if c in Select.up:
			self.y = (self.y - 1) % self.parent.height
		elif c in Select.down:
			self.y = (self.y + 1) % self.parent.height
		elif c in Select.left:
			self.x = (self.x - 1) % self.parent.width
		elif c in Select.right:
			self.x = (self.x + 1) % self.parent.width
		self.render()

	def render(self):
		self.game.screen.addstr(self.parent.y + self.y * 2 - 1, self.parent.x + self.x * 4 - 2, "┌───┐")
		self.game.screen.addstr(self.parent.y + self.y * 2, self.parent.x + self.x * 4 - 2, '│')
		self.game.screen.addstr(self.parent.y + self.y * 2, self.parent.x + self.x * 4 + 2, '│')
		self.game.screen.addstr(self.parent.y + self.y * 2 + 1, self.parent.x + self.x * 4 - 2, "└───┘")


class Puzzle(Game):
	def start(self):
		self.randomizing = True
		# self.screen.curses.start_color()
		# self.screen.curses.init_pair(2, self.screen.curses.COLOR_WHITE, self.screen.curses.COLOR_BLACK)
		# self.screen.curses.init_pair(3, self.screen.curses.COLOR_BLACK, self.screen.curses.COLOR_WHITE)
		# self.screen.curses.use_default_colors()
		# for i in range(25):
		# 	self.screen.curses.init_color(i+1, 750, int((i % 5) / 5 * 1250), int((i // 5) / 1250))
		# 	self.screen.curses.init_pair(i+1, i+1, i+1)
		self.grid = self.instantiate(Grid)
		self.running = False
		self.waiting = False
		self.victory = False
		self.time = 3.0
		for i in range(1000):
			keys = "wasdhjklHJKL"
			self.grid.update(ord(keys[randint(1, len(keys))-1]))

	def update(self):
		# c = self.getKeyRaw()
		if self.randomizing:
			keys = "wasdhjklHJKL"
			self.triggerKey(ord(keys[randint(1, len(keys))-1]))
		if self.randomizing and self.time <= 0:
			self.randomizing = False
			self.waiting = True
			self.time = 1.0
			sleep(0.1)
			self.grid.selector.x = self.grid.width // 2
			self.grid.selector.y = self.grid.height // 2
		if self.waiting and self.time <= 0:
			self.waiting = False
			self.time = 0.0
		# self.screen.clear()
		# self.screen.border(x=1, width=self.grid.width * 4 + 24, height=self.grid.height * 2 + 3)
		self.screen.addstr(self.grid.height, self.grid.width * 4 + 10, round(self.time, 3))
		self.screen.addstr(self.grid.height + 2, self.grid.width * 4 + 10, str(round(self.percent() * 100, 2)) + '%')
		if self.victory:
			self.screen.addstr(self.grid.height + 1, self.grid.width * 4 + 10, "Victory!")
		self.running = self.running and not self.check_win()
		self.victory = self.check_win()
		if self.randomizing or self.waiting:
			self.time -= self.delta_time
		self.time += self.delta_time if self.running else 0
		self.screen.refresh()

	def randomize(self, count=100):
		self.randomize_index += count
		self.running = True

	def check_win(self):
		prev = -1
		for y in range(self.grid.height):
			for x in range(self.grid.width):
				if prev > self.grid.tiles[y][x].color_index - 1:
					return False
				prev = self.grid.tiles[y][x].color_index
		return True and not self.randomizing

	def percent(self):
		count = 0
		for y in range(self.grid.height):
			for x in range(self.grid.width):
				count += 1 if self.grid.tiles[y][x].color_index - 1 == y * self.grid.height + x % self.grid.width else 0
		return count / (self.grid.height * self.grid.width)


if __name__ == "__main__":
	puzzle = Puzzle()

