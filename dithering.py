#!/usr/bin/env python3
# -*- coding: utf8 -*-

from engine import Game, GameObject
from engine.color import Colors, Color
from random import random, randint
from os import environ
from math import sin, cos, pi
from time import time

HJKL = "HJKL" in environ and environ["HJKL"] == '1'


class Input:
	up = 'k' if HJKL else 'i'
	down = 'j' if HJKL else 'k'
	left = 'h' if HJKL else 'j'
	right = 'l' if HJKL else 'l'


class Particle(GameObject):
	def start(self):
		self.x = 0
		self.y = 0
		self.clampX = [-5, 5, .2]
		self.clampY = [-3, 1, .2]
		self.dx = (random() * (self.clampX[1] - self.clampX[0]) + self.clampX[0]) * self.clampX[2]
		self.dy = (random() * (self.clampY[1] - self.clampY[0]) + self.clampY[0]) * self.clampY[2]
		# t = time() - self.game.start_time
		# scale = 2
		# self.dx = 1 * cos(t*scale)
		# self.dy = 3/5.0 * sin(t*scale)
		self.sprite = randint(0, 9)
		self.frame = 0
		self.time = randint(40, 100)

	def update(self):
		if self.frame < self.time:
			self.x += self.dx
			self.y += self.dy
			self.dy += .1
		elif self.frame == self.time:
			self.destroy()
		y = min(max(round(self.y), 0), self.game.screen.height * 4 - 1)
		x = min(max(round(self.x), 0), self.game.screen.width * 2 - 1)
		self.game.map[y//4][x//2][4*(x % 2) + y % 4] = True
		self.game.tiles[(y//4, x//2)] = True
		self.frame += 1


class Player(GameObject):
	def start(self):
		self.x = self.game.screen.width // 2
		self.y = self.game.screen.height // 2
		self.sprite = 'o'
		# self.color = self.game.screen.curses.color_pair(3)
		self.time = 0
		self.duration = 0.5
		self.sword_life = 3
		self.sword = self.game.instantiate(Sword)
		self.sword.parent = self
		self.frame = 0

	def update(self):
		c = self.game.getKeyRaw()
		if c == ord(Input.left):
			self.x -= 1
		elif c == ord(Input.down):
			self.y += 1
		elif c == ord(Input.up):
			self.y -= 1
		elif c == ord(Input.right):
			self.x += 1
		elif self.sword.direction == -1:
			if c == ord('w'):
				self.sword.direction = 7
			elif c == ord('e'):
				self.sword.direction = 0
			elif c == ord('d'):
				self.sword.direction = 1
			elif c == ord('c'):
				self.sword.direction = 2
			elif c == ord('x'):
				self.sword.direction = 3
			elif c == ord('z'):
				self.sword.direction = 4
			elif c == ord('a'):
				self.sword.direction = 5
			elif c == ord('q'):
				self.sword.direction = 6
		elif c == ord('s'):
			self.sword.direction = -1
		elif c == ord('-'):
			self.sword.lifetime -= 1
		elif c == ord('='):
			self.sword.lifetime += 1
		self.render()
		self.frame += 1

	def render(self):
		if self.time >= self.duration:
			self.sprite = 'O' if self.sprite == 'o' else 'o'
			self.time = 0
		self.game.screen.addstr(self.y, self.x, self.sprite)
		self.time += self.game.delta_time


class Sword(GameObject):
	def start(self):
		self.parent = None
		# self.color = self.game.screen.curses.color_pair(36)
		self.direction = -1
		self.speed = 0.0625 * 2
		self.time = 0
		self.frame = 0
		self.lifetime = 3

	def update(self):
		if self.direction != -1:
			if self.time >= self.speed:
				self.direction += 1
				self.direction %= 8
				self.time = 0
				self.frame += 1
			self.time += self.game.delta_time
			if self.frame >= self.lifetime:
				self.direction = -1
			else:
				self.render()
		else:
			self.time = 0
			self.frame = 0

	def render(self):
		sprites = ['|', '/', '-', '\\']
		offsets = [0, 1, 1, 1, 0, -1, -1, -1]
		sprite = sprites[self.direction % 4]
		x = offsets[self.direction % 8]
		y = offsets[(self.direction + 6) % 8]
		self.game.screen.addstr(self.parent.y + y, self.parent.x + x, sprite)


class Shape(GameObject):
	def start(self):
		self.x = self.game.screen.width // 2
		self.y = self.game.screen.height // 2
		self.rotation = 0
		self.delta_rotation = pi / 12
		self.sides = 4
		self.apothem = 10
		self.radius = self.apothem / cos(pi / (self.sides * 2))
		self.auto_rotation = False

	def update(self):
		c = self.game.getKeyRaw()
		if c == ord('a'):
			self.x -= 1
		elif c == ord('s'):
			self.y += 1
		elif c == ord('w'):
			self.y -= 1
		elif c == ord('d'):
			self.x += 1
		elif c == ord('q'):
			self.rotation -= self.delta_rotation
		elif c == ord('e'):
			self.rotation += self.delta_rotation
		elif c == ord('r'):
			self.apothem += 1
		elif c == ord('f'):
			self.apothem -= 1
		elif c == ord('z'):
			self.sides = max(self.sides - 1, 2)
		elif c == ord('x'):
			self.sides += 1
		elif c == ord('c'):
			self.auto_rotation = not self.auto_rotation
		elif c == ord('v'):
			self.rotation = 0
		self.radius = self.apothem / cos(pi / (self.sides * 2))
		if self.auto_rotation:
			pass
			# self.rotation += pi/60
			self.rotation = self.game.f / 10 + pi / 2
			# self.rotation += sin(self.game.f / 10.0) * pi / 2
			# self.x += cos(self.game.f / 10.0) * pi / 2
			# self.y += sin(self.game.f / 10.0) * pi / 2
		self.render()

	def render(self):
		for s in range(0, self.sides + 1):
			x1 = self.radius * cos(2*s*pi/self.sides + self.rotation + pi/self.sides)
			y1 = self.radius * sin(2*s*pi/self.sides + self.rotation + pi/self.sides)
			x2 = self.radius * cos(2*(s + 1)*pi/self.sides + self.rotation + pi/self.sides)
			y2 = self.radius * sin(2*(s + 1)*pi/self.sides + self.rotation + pi/self.sides)
			m = int(max(abs(x1) + abs(x2), abs(y1) + abs(y2))) + 1
			for i in range(0, m):
				dx = x1 + (x2 - x1) * i / m
				dy = y1 + (y2 - y1) * i / m
				# + cos(self.game.f / 10) * self.apothem * 3)
				x = min(max(round(self.x + dx), 0), self.game.screen.width * 2 - 1)
				y = min(max(round(self.y + dy), 0), self.game.screen.height * 4 - 1)
				self.game.map[y//4][x//2][4*(x % 2) + y % 4] = True
				self.game.tiles[(y//4, x//2)] = True


class Guy(GameObject):
	def start(self):
		self.x = self.game.screen.width
		self.y = self.game.screen.height * 2
		self.radius = 0
		self.precision = 64
		self.grow = False
		self.sword_life = 3
		self.sword = self.game.instantiate(Sword)
		self.sword.parent = self

	def update(self):
		c = self.game.getKeyRaw()
		if c == ord(Input.left):
			self.x -= 1
		elif c == ord(Input.down):
			self.y += 1
		elif c == ord(Input.up):
			self.y -= 1
		elif c == ord(Input.right):
			self.x += 1
		elif c == ord('-'):
			self.radius -= 1
		elif c == ord('='):
			self.radius += 1
		elif c == ord('_'):
			self.precision -= 1
		elif c == ord('+'):
			self.precision += 1
		elif c == ord('i'):
			self.grow = not self.grow
		elif self.sword.direction == -1:
			if c == ord('w'):
				self.sword.direction = 7
			elif c == ord('e'):
				self.sword.direction = 0
			elif c == ord('d'):
				self.sword.direction = 1
			elif c == ord('c'):
				self.sword.direction = 2
			elif c == ord('x'):
				self.sword.direction = 3
			elif c == ord('z'):
				self.sword.direction = 4
			elif c == ord('a'):
				self.sword.direction = 5
			elif c == ord('q'):
				self.sword.direction = 6
		elif c == ord('s'):
			self.sword.direction = -1
		self.render()

	def render(self):
		y = min(max(round(self.y), 0), self.game.screen.height * 4 - 1)
		x = min(max(round(self.x), 0), self.game.screen.width * 2 - 1)
		for i in range(self.precision):
			theta = i/float(self.precision) * 2 * pi
			dy = round(self.radius * sin(theta) * (sin(time()*2)/2+1 if self.grow else 1))
			dx = round(self.radius * cos(theta) * (sin(time()*2)/-2+1 if self.grow else 1))
			self.game.map[(y+dy)//4][(x+dx)//2][4*((x+dx) % 2) + (y+dy) % 4] = True
			self.game.tiles[((y+dy)//4, (x+dx)//2)] = True


class Braille(Game):
	def start(self):
		# self.screen.curses.start_color()
		# self.screen.curses.use_default_colors()
		# for i in range(0, self.screen.curses.COLORS):
		# 	self.screen.curses.init_pair(i + 1, i, -1)
		# self.guy = self.instantiate(Guy)
		self.player = self.instantiate(Player)
		self.shape = self.instantiate(Shape)
		self.map = [[[False for i in range(8)] for x in range(self.screen.width)] for y in range(self.screen.height)]
		self.tiles = {}
		self.correction = [0, 1, 2, 6, 3, 4, 5, 7]
		self.fountain = False
		self.clear = True
		self.monochrome = False
		self.c = -1
		self.f = 0

	def update(self):
		self.f += 1
		c = self.getKeyRaw()
		if c != -1:
			self.c = c
		c = self.getKeyRaw()
		if self.getKeyRaw() == ord('o'):
			self.fountain = not self.fountain
		elif c == ord('m'):
			self.clear = not self.clear
		elif c == ord('n'):
			self.monochrome = not self.monochrome
		if self.fountain:
			p = self.instantiate(Particle)
			p.x = self.screen.width
			p.y = self.screen.height * 4 // 5
		delta_time = str(round(1 / self.delta_time))
		fixed_delta_time = str(round(1 / self.fixed_delta_time))
		gameObjects = str(len(self.gameObjects))
		self.screen.addstr(0, self.screen.width - len(delta_time), delta_time)
		self.screen.addstr(1, self.screen.width - len(fixed_delta_time), fixed_delta_time)
		self.screen.addstr(0, 0, gameObjects)
		color = Color(h=(self.f * 2) if not self.monochrome else 0, s=1.0, l=0.5).toRGB()
		"""for y, row in enumerate(self.map):
			for x, column in enumerate(row):
				# if True in self.map[y][x]:
				if self.tiles[y][x]:
					char = sum([2**self.correction[i] if column[i] else 0 for i in range(8)])
					self.screen.addstr(y, x, chr(10240 + char), color)"""
		for pos in self.tiles:
			y = pos[0]
			x = pos[1]
			char = sum([2**self.correction[i] if self.map[y][x][i] else 0 for i in range(8)])
			# self.screen.addstr(y, x, chr(10240 + char), color, -1)
			self.screen.addstr(y, x, chr(10240 + char), color)
		self.screen.addstr(0, 0, "", Colors.white)
		if self.clear:
			self.tiles = {}
			self.map = [[[False for i in range(8)] for x in range(self.screen.width)] for y in range(self.screen.height)]
		keyboard = ["1234567890-=", "qwertyuiop[]", "asdfghjkl;'", "zxcvbnm,./"]
		# usable = "qweasdzxcomrf-=" + ("hjkl" if HJKL else "ijkl")
		for i in range(0, 4):
			layer = keyboard[i]
			offset = i - 1 if i > 1 else 0
			for s in layer:
				self.screen.addstr(self.screen.height - 5 + i, self.screen.width - 25 + offset, s, Colors.green if s in "wasdqezxcvrfmnohjkl" else Colors.white)
				offset += 2
		# self.screen.addstr(self.screen.height - 5, self.screen.width - 30, "1 2 3 4 5 6 7 8 9 0 - =")
		# self.screen.addstr(self.screen.height - 4, self.screen.width - 30, "q w e r t y u i o p [ ] \\")
		# self.screen.addstr(self.screen.height - 3, self.screen.width - 29, "a s d f g h j k l ; ' ent")
		# self.screen.addstr(self.screen.height - 2, self.screen.width - 28, "z x c v b n m , . / shft")
		if self.c == ord('p'):
			self.close()
			return
		elif self.c != -1:
			self.screen.addstr(1, 0, chr(self.c))
		# if self.clear:
		# 	self.screen.clear()
		self.screen.refresh()


if __name__ == "__main__":
	braille = Braille()

