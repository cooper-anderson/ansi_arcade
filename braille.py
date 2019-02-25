#!/usr/bin/env python3
# -*- coding: utf8 -*-

from engine import Game, GameObject
from random import randint
from sys import argv
from time import time
import json
import os.path

DATA_DIRECTORY = "data/braille/"


class Letter(GameObject):
	ALPHABET = "abcdefghijklmnopqrstuvwxyz"
	BRAILLE = "⠁⠃⠉⠙⠑⠋⠛⠓⠊⠚⠅⠇⠍⠝⠕⠏⠟⠗⠎⠞⠥⠧⠺⠭⠽⠵"
	PROGRESS = " ⣀⣤⣶⣿"
	COOLDOWN = 0.5

	def start(self):
		self.x = 0
		self.y = 0
		self.letter = 0
		self.streak = 0
		self.start_time = 0
		self.hint_time = 3.0
		self.cooldown = 0
		self.next()

	def update(self):
		percent = min((time() - self.start_time) / self.hint_time, 1)
		self.game.screen.addstr(self.y - 2, self.x - 5, "┌───┬───┬─┐")
		self.game.screen.addstr(self.y - 1, self.x - 5, "│   │   │ │")
		self.game.screen.addstr(self.y, self.x - 5, "├───┴───┤ │")
		self.game.screen.addstr(self.y + 1, self.x - 5, "│       │ │")
		self.game.screen.addstr(self.y + 2, self.x - 5, "└───────┴─┘")
		self.game.screen.addstr(self.y - 1, self.x - 3, Letter.BRAILLE[self.letter])
		streak = str(max(self.streak, 0))
		self.game.screen.addstr(self.y + 1, self.x + 2 - len(streak), streak)
		for i in range(1, 4):
			t = 4 if percent >= i / 3.0 else percent * 12 % 4 if percent > (i - 1) / 3.0 else 0
			self.game.screen.addstr(self.y + 2 - i, self.x + 4, Letter.PROGRESS[int(t)])
		if percent == 1.0:
			self.game.screen.addstr(self.y - 1, self.x + 1, Letter.ALPHABET[self.letter])
			self.streak = -1

	def check(self, key):
		success = self.letter == key - (64 if key < 97 else 97)
		self.streak = self.streak + 1 if success else 0
		return success

	def next(self):
		prev = self.letter
		while self.letter == prev:
			self.letter = randint(0, 25)
		self.start_time = time()


class Braille(Game):
	def start(self):
		self.gamemode = 0
		self.user = "default"
		if len(argv) > 1:
			self.user = argv[1]
		self.file_name = DATA_DIRECTORY + self.user + ".json"
		if self.user != "default":
			if not os.path.isfile(self.file_name):
				with open(self.file_name, 'w') as file:
					file.write("{}")
			with open(self.file_name, 'r') as file:
				self.data = json.loads(file.readline())
		else:
			self.data = {}
		self.frame = 0
		self.l = Letter(self)
		self.selector = '1'
		self.auto_timer = 0

	def update(self):
		c = self.getKeyRaw()
		if self.gamemode == 0:
			self.quiz(c)
		elif self.gamemode == 1:
			self.graph(c)
		else:
			self.close()

	def quiz(self, c):
		if c == 27:
			self.save()
			self.l.destroy()
			self.gamemode = 1
			self.auto_timer = time()
			return
		self.l.x = self.screen.width // 2
		self.l.y = self.screen.height // 2
		if c != -1:
			key = c - (63 if c < 97 else 96)
			if key <= 26 and key > 0:
				if str(self.l.letter + 1) not in self.data:
					self.data[str(self.l.letter + 1)] = {}
				if str(key) not in self.data[str(self.l.letter + 1)]:
					self.data[str(self.l.letter + 1)][str(key)] = 0
				self.data[str(self.l.letter + 1)][str(key)] += 1
			if self.l.check(c):
				self.l.next()
		self.screen.refresh()

	def graph(self, c):
		x = 6
		y = 20
		data = {}
		count = 0.0
		height = 13.0
		if c == 27:
			self.gamemode = 2
			return
		c += 32 if c < 97 else 0
		if c >= 97 and c <= 122:
			self.selector = str(c - 96)
			self.auto_timer = -1
		if c == 76:
			self.selector = str(int(self.selector) - 1)
			self.auto_timer = -1
		elif c == 78:
			self.selector = str(int(self.selector) + 1)
			self.auto_timer = -1
		elif c == 79:
			self.auto_timer = 0.5
		if self.selector in self.data:
			data = self.data[self.selector]
		for item in data:
			count += data[item]
		self.screen.addstr(y, x, "└─")
		for i in range(26):
			self.screen.addstr(y, x + 2 + i * 2, "┬─")
			self.screen.addstr(y + 1, x + 2 + i * 2, chr(i + 97))
			if i + 1 == int(self.selector):
				# self.screen.addstr(y - 16, x + 1 + i * 2, "┌─┐")
				# self.screen.addstr(y - 15, x + 1 + i * 2, "│ │")
				# self.screen.addstr(y - 14, x + 1 + i * 2, "└─┘")
				self.screen.addstr(y - 16, x + i * 2, "┌───┐")
				self.screen.addstr(y - 15, x + i * 2, "│   │")
				self.screen.addstr(y - 14, x + i * 2, "└───┘")
			self.screen.addstr(y - 15, x + 2 + i * 2 - (1 if i+1 < int(self.selector) else -1 if i+1 > int(self.selector) else 0), chr(i + 97))
			percent = 0
			if str(i + 1) in data:
				percent = float(data[str(i + 1)]) / count
			for h in range(1, int(height)):
				t = 4 if percent >= h / height else int(percent * ((height - 1) * 4) % 4) if percent > (h - 1) / height else 0
				self.screen.addstr(y - h, x + 2 + i * 2, Letter.PROGRESS[t])
		for i in range(12):
			self.screen.addstr(y - 1 - i, x, '┤')
			if (i + 1) % 3 == 0:
				p = str(int((i + 1) * 8.4)) + '%'
				self.screen.addstr(y - 1 - i, x - 1 - len(p), p)
		if self.auto_timer != -1 and time() - self.auto_timer > 0.5:
			self.auto_timer = time()
			self.selector = str(int(self.selector) + 1)
		if self.selector == '0':
			self.selector = "26"
		elif self.selector == "27":
			self.selector = '1'
		self.screen.refresh()

	def save(self):
		with open(self.file_name, 'w') as file:
			file.write(json.dumps(self.data).replace(' ', ""))


if __name__ == "__main__":
	braille = Braille()

