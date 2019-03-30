#!/usr/bin/env python
# -*- coding: utf8 -*-

from engine import Game, GameObject
import aspects
import random
import math


xScale = 2


class Player(GameObject):
	def start(self):
		self.sprite = '@'
		self.color = [-1, -1]
		self.x = 0
		self.y = 0
		self.rotation = 0
		self.dr = math.pi / 120
		self.autorotate = False
		self.zoom = 1
		self.frame = 0

	def update(self):
		self.frame += 1
		c = self.game.getKeyRaw()
		if c == ord('w'):
			self.x -= math.sin(self.rotation)
			self.y -= math.cos(self.rotation)
		elif c == ord('s'):
			self.x += math.sin(self.rotation)
			self.y += math.cos(self.rotation)
		elif c == ord('a'):
			self.y += math.sin(self.rotation)
			self.x -= math.cos(self.rotation)
		elif c == ord('d'):
			self.y -= math.sin(self.rotation)
			self.x += math.cos(self.rotation)
		elif c == ord('e'):
			self.rotation -= self.dr
		elif c == ord('q'):
			self.rotation += self.dr
		elif c == ord('r'):
			self.zoom *= 1.1
		elif c == ord('f'):
			self.zoom /= 1.1
		elif c == ord('x'):
			self.autorotate = not self.autorotate
		if self.autorotate:
			self.rotation += math.pi / 60


class Slime(GameObject):
	def start(self):
		self.sprites = ['o', 'O']
		self.spriteIndex = random.randint(0, len(self.sprites) - 1)
		self.duration = 0.5
		self.color = [-1, -1]
		multiplier = 0.5
		# self.x = int(multiplier * (random.randint(0, self.game.screen.width - 1) - self.game.screen.width) // 2)
		# self.y = int(multiplier * (random.randint(0, self.game.screen.height - 1) - self.game.screen.height // 2) // 2)
		# self.x = int(multiplier * random.random() * self.game.screen.width - self.game.screen.width // 2) // 2
		# self.y = int(multiplier * random.random() * self.game.screen.height) - self.game.screen.height // 2
		self.x = int(multiplier * (random.random() - 0.5) * self.game.screen.width / xScale)
		self.y = int(multiplier * (random.random() - 0.5) * self.game.screen.height)
		# self.y = 0
		# self.x = 0
		self.frame = 0
		self.time = random.random() * self.duration
		self.move_chance = 100

	def update(self):
		self.frame += 1
		chance = (random.randint(0, 5 if self.game.getKeyRaw() == ord(' ') else self.move_chance)) if self.move_chance > 0 else 100
		if chance < 1:
			self.x -= 2 if self.x > 1 else 0
		elif chance < 2:
			self.x += 2 if self.x < self.game.screen.width - 2 else 0
		elif chance < 3:
			self.y -= 1 if self.y > 0 else 0
		elif chance < 4:
			self.y += 1 if self.y < self.game.screen.height - 1 else 0
		if self.time >= self.duration:
			self.spriteIndex = (self.spriteIndex + 1) % len(self.sprites)
			self.time = 0
		self.time += self.game.delta_time


class Slimes(Game):
	def start(self):
		self.player = self.instantiate(Player)
		self.slimes = {
			"water": self.instantiate(Slime),
			"fire": self.instantiate(Slime),
			"earth": self.instantiate(Slime),
			"air": self.instantiate(Slime),
			"order": self.instantiate(Slime),
			"entropy": self.instantiate(Slime),
			"positive": self.instantiate(Slime),
			"negative": self.instantiate(Slime)
		}
		self.slimes["water"].color[0] = aspects.water
		self.slimes["fire"].color[0] = aspects.fire
		self.slimes["earth"].color[0] = aspects.earth
		self.slimes["air"].color[0] = aspects.air
		self.slimes["order"].color[0] = aspects.order
		self.slimes["entropy"].color[0] = aspects.entropy
		self.slimes["positive"].color[0] = aspects.positive
		self.slimes["negative"].color[0] = aspects.negative

		self.clear = True

		# self.slimes["water"].y = -4
		# self.slimes["fire"].y = -6
		# self.slimes["earth"].y = -4
		# self.slimes["order"].y = 4
		# self.slimes["entropy"].y = 6
		# self.slimes["positive"].y = 4

		# m = 1
		# self.slimes["positive"].x = m * -4
		# self.slimes["negative"].x = m * -6
		# self.slimes["water"].x = m * -4
		# self.slimes["earth"].x = m * 4
		# self.slimes["air"].x = m * 6
		# self.slimes["order"].x = m * 4

	def update(self):
		c = self.getKeyRaw()
		if c == ord('c'):
			self.screen.clear()
		elif c == ord('z'):
			self.clear = not self.clear
		elif c == ord('t'):
			clear = self.clear
			autorotate = self.player.autorotate
			self.player.destroy()
			for g in self.slimes:
				self.slimes[g].destroy()
			self.screen.clear()
			self.start()
			self.clear = clear
			self.player.autorotate = autorotate

	def late_update(self):
		self.screen.addstr(0, 0, round(-self.player.rotation * 180 / math.pi))
		for s in self.slimes:
			slime = self.slimes[s]
			yOrig = self.player.zoom * (slime.y - self.player.y)
			xOrig = self.player.zoom * (slime.x - self.player.x)
			y = round(xOrig * math.sin(self.player.rotation) + yOrig * math.cos(self.player.rotation)) + self.screen.height // 2
			x = xScale * round(xOrig * math.cos(self.player.rotation) - yOrig * math.sin(self.player.rotation)) + self.screen.width // 2
			y = min(max(y, 0), self.screen.height - 1)
			x = min(max(x, 0), self.screen.width - 1)
			# if x >= 0 and x < self.screen.width and y >= 0 and y < self.screen.height:
			self.screen.addstr(y, x, slime.sprites[slime.spriteIndex], slime.color[0], slime.color[1])
		self.screen.addstr(self.screen.height // 2, self.screen.width // 2, '@')
		self.screen.refresh(self.clear)


if __name__ == "__main__":
	slimes = Slimes()

