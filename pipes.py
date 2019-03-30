#!/usr/bin/env python3
# -*- coding: utf8 -*-

from engine import Game, GameObject


class Vector(object):
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def copy(self):
		return Vector(self.x, self.y)

	def __add__(self, other):
		return Vector(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Vector(self.x - other.x, self.y - other.y)

	def __mul__(self, scalar):
		return Vector(self.x * scalar, self.y * scalar)

	def __div__(self, scalar):
		return Vector(self.x * scalar, self.y * scalar) if scalar != 0 else Vector()

	def __eq__(self, other):
		return other is not None and self.x == other.x and self.y == other.y

	def __ne__(self, other):
		return not (self == other)

	def __hash__(self):
		return hash((self.x, self.y))

	def __repr__(self):
		return "<Vector(" + str(self.x) + ", " + str(self.y) + ")>"

	def __str__(self):
		return str(self.__repr__())


class Player(GameObject):
	def start(self):
		self.position = Vector()

	def update(self):
		c = self.game.getKeyRaw()
		togglePos = None
		if c == ord('h'):
			self.position.x -= 1
		elif c == ord('j'):
			self.position.y -= 1
		elif c == ord('k'):
			self.position.y += 1
		elif c == ord('l'):
			self.position.x += 1
		elif c == ord('w'):
			togglePos = Vector(0, 1)
		elif c == ord('s'):
			togglePos = Vector(0, -1)
		elif c == ord('a'):
			togglePos = Vector(-1, 0)
		elif c == ord('d'):
			togglePos = Vector(1, 0)
		elif c == ord('x'):
			togglePos = Vector(0, 0)
		elif c == ord('v'):
			self.game.add_valve(self.position.copy())
		elif c == ord('z'):
			self.game.add_pipe(self.position.copy())
		elif c == ord('t'):
			self.game.add_tank(self.position.copy())
		elif c == ord('r'):
			if self.position in self.game.pipes:
				obj = self.game.pipes[self.position]
				if type(obj) == Valve:
					obj.rotate()
		elif c == ord('c'):
			self.game.remove(self.position)
		if togglePos is not None:
			if self.position + togglePos in self.game.pipes:
				obj = self.game.pipes[self.position + togglePos]
				if type(obj) == Valve:
					obj.toggle()
		self.game.screen.addstr(self.game.screen.height // 2, self.game.screen.width // 2, "o")


class Connections(object):
	blockChars = " ╾━╼─╼━╾━╿┌┍┐┬┮┑┭┯┃┎┏┒┰┲┓┱┳╽└┕┘┴┶┙┵┷│├┝┤┼┾┥┽┿╽┟┢┧╁╆┪╅╈┃┖┗┚┸┺┛┹┻╿┞┡┦╀╄┩╃╇┃┠┣┨╂╊┫╉╋"

	def __init__(self):
		self.up = 2
		self.down = 2
		self.left = 2
		self.right = 2

	def getChar(self, blocked=False):
		if not blocked:
			if self.up + self.down + self.left + self.right in [0, 8]:
				return '╬'
			elif self.up != 0 and self.down != 0 and self.left != 0 and self.right != 0:
				return '╬'
			elif self.up == 0 and self.down != 0 and self.left != 0 and self.right != 0:
				return '╦'
			elif self.up != 0 and self.down == 0 and self.left != 0 and self.right != 0:
				return '╩'
			elif self.up != 0 and self.down != 0 and self.left == 0 and self.right != 0:
				return '╠'
			elif self.up != 0 and self.down != 0 and self.left != 0 and self.right == 0:
				return '╣'
			elif self.up != 0 and self.left != 0:
				return '╝'
			elif self.up != 0 and self.right != 0:
				return '╚'
			elif self.down != 0 and self.left != 0:
				return '╗'
			elif self.down != 0 and self.right != 0:
				return '╔'
			elif self.up == 0 and self.down == 0:
				return '═'
			elif self.left == 0 and self.right == 0:
				return '║'
		return Connections.blockChars[self.up * 27 + self.down * 9 + self.left * 3 + self.right]

	def isAlone(self):
		return self.up + self.down + self.left + self.right == 0

	@staticmethod
	def getType(pipes, position, offset):
		if position + offset not in pipes:
			return 0
		obj = pipes[position + offset]
		t = type(obj)
		if t == Pipe:
			return 2
		elif t == Valve:
			if (offset == Vector(0, -1) and obj.rotation == 0) or (offset == Vector(-1, 0) and obj.rotation == 1) or (offset == Vector(0, 1) and obj.rotation == 2) or (offset == Vector(1, 0) and obj.rotation == 3):
				return 1
			return 0


class Pipe(GameObject):
	def start(self):
		self.position = Vector()
		self.connections = Connections()
		self.character = ''
		self.blocked = False
		# self.hard_update()

	def update(self):
		pos = Vector(self.game.screen.width // 2 - self.game.player.position.x + self.position.x, self.game.screen.height // 2 + self.game.player.position.y - self.position.y)
		self.game.screen.addstr(pos.y, pos.x, self.character)
		# self.game.screen.addstr(pos.y + 1, pos.x, self.connections.up)
		# self.game.screen.addstr(pos.y + 2, pos.x, self.connections.down)
		# self.game.screen.addstr(pos.y + 3, pos.x, self.connections.left)
		# self.game.screen.addstr(pos.y + 4, pos.x, self.connections.right)
		# self.game.log("test")
		# self.game.log(self.connections.left)

	def hard_update(self):
		self.soft_update()
		# v = Vector(1, 0)
		# if self.position + v in self.game.pipes:
		# 	self.game.log("right")
		# 	self.game.pipes[self.position + v].soft_update()
		# v = Vector(-1, 0)
		# if self.position + v in self.game.pipes:
		# 	self.game.log("left")
		# 	self.game.pipes[self.position + v].soft_update()
		# v = Vector(0, 1)
		# if self.position + v in self.game.pipes:
		# 	self.game.log("up")
		# 	self.game.pipes[self.position + v].soft_update()
		# v = Vector(0, -1)
		# if self.position + v in self.game.pipes:
		# 	self.game.log("down")
		# 	self.game.pipes[self.position + v].soft_update()

	def soft_update(self):
		pipes = self.game.pipes
		self.connections.up = Connections.getType(pipes, self.position, Vector(0, 1))
		self.connections.down = Connections.getType(pipes, self.position, Vector(0, -1))
		self.connections.left = Connections.getType(pipes, self.position, Vector(-1, 0))
		self.connections.right = Connections.getType(pipes, self.position, Vector(1, 0))
		if self.connections.isAlone():
			self.connections = Connections()
		self.blocked = True in [
			self.connections.up == 1 and pipes[self.position + Vector(0, 1)].active,
			self.connections.down == 1 and pipes[self.position - Vector(0, 1)].active,
			self.connections.left == 1 and pipes[self.position - Vector(1, 0)].active,
			self.connections.right == 1 and pipes[self.position + Vector(1, 0)].active,
		]
		self.character = self.connections.getChar(self.blocked)


class Valve(GameObject):
	def start(self):
		self.position = Vector()
		self.rotation = 0
		self.active = False

	def update(self):
		pos = Vector(self.game.screen.width // 2 - self.game.player.position.x + self.position.x, self.game.screen.height // 2 + self.game.player.position.y - self.position.y)
		self.game.screen.addstr(pos.y, pos.x, self.getChar())

	def rotate(self):
		self.rotation = (self.rotation + 1) % 4
		self.game.hard_update(self.position)

	def toggle(self):
		self.active = not self.active
		self.game.hard_update(self.position)

	def getChar(self):
		if self.active:
			return ['╹', '╺', '╻', '╸'][self.rotation]
		return ['╽', '╾', '╿', '╼'][self.rotation]

	def hard_update(self):
		self.game.log(self.position)

	def soft_update(self):
		pass


class Tank(GameObject):
	def start(self):
		self.vertecies = []

	def update(self):
		pass


class Pipes(Game):
	def start(self):
		self.player = self.instantiate(Player)
		self.pipes = {}
		self.add_pipe(Vector(3, 3))
		self.add_pipe(Vector(4, 3))
		self.add_pipe(Vector(4, 4))

	def remove(self, pos):
		if pos in self.pipes:
			self.pipes[pos].destroy()
			del self.pipes[pos]
			self.hard_update(pos)

	def add_pipe(self, pos):
		self.remove(pos)
		p = self.instantiate(Pipe)
		p.position = pos
		self.pipes[p.position] = p
		self.hard_update(p.position)

	def add_valve(self, pos):
		self.remove(pos)
		v = self.instantiate(Valve)
		v.position = pos
		self.pipes[v.position] = v
		self.hard_update(v.position)

	def add_tank(self, pos):
		pass

	def hard_update(self, pos):
		if pos in self.pipes:
			self.pipes[pos].hard_update()
		self.soft_update(pos + Vector(1, 0))
		self.soft_update(pos - Vector(1, 0))
		self.soft_update(pos + Vector(0, 1))
		self.soft_update(pos - Vector(0, 1))

	def soft_update(self, pos):
		if pos in self.pipes:
			self.pipes[pos].soft_update()

	def update(self):
		c = self.getKeyRaw()
		self.log(len(self.gameObjects))
		self.screen.refresh()
		if c == ord('q'):
			self.close()


if __name__ == "__main__":
	pipes = Pipes()
