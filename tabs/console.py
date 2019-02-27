#!/usr/bin/env python3
# -*- coding: utf8 -*-

from engine.elements import Tab, List, Box

from tabs import colors


class Output(Box):
	def resize(self):
		self.set_pos(0, 0, self.parent.width // 2, self.parent.height - 3)


class Prompt(Box):
	def resize(self):
		self.set_pos(0, self.parent.height - 3, self.parent.width // 2, 3)


class Log(Box):
	def resize(self):
		self.set_pos(self.parent.width // 2, 0, self.parent.width // 2, self.parent.height)


class Console(Tab):
	def start(self):
		self.list = self.add_child(List)
		self.list.set_colors(colors.box, colors.box_active)
		self.box_prompt = self.list.add_child(Prompt).set_label("prompt")
		self.box_output = self.list.add_child(Output).set_label("output")
		self.box_log = self.list.add_child(Log).set_label("log")
		# self.box_output = Box("command output")
		# self.box_prompt = Box("prompt")
		# self.box_log = Box("debug log")
		# self.resize()
		# self.selected = 1

	def update(self, c=-1):
		if c == ord('h'):
			self.list.prev()
		elif c == ord('l'):
			self.list.next()

	def resize(self):
		self.set_pos(0, 0, self.screen.width, self.screen.height - 1)

		# self.resize()
		# if self.game.tab == 2:
		# 	self.draw()
		# 	c = -1 if self.game.escaped else self.game.getKeyRaw()
		# 	if c == ord('h'):
		# 		self.selected = self.selected - 1 if self.selected > 0 else 2
		# 	elif c == ord('l'):
		# 		self.selected = self.selected + 1 if self.selected < 2 else 0

	# def resize(self):
	# 	self.box_output.set_pos(0, 0, self.game.screen.width // 2, self.game.screen.height - 4)
	# 	self.box_prompt.set_pos(0, self.game.screen.height - 4, self.game.screen.width // 2, 3)
	# 	self.box_log.set_pos(self.game.screen.width // 2, 0, self.game.screen.width // 2, self.game.screen.height - 1)

	# def draw(self):
	# 	self.box_output.draw(self.game.screen, colors.box_active[0] if self.selected == 2 else colors.box[0], colors.box_active[1] if self.selected == 0 else colors.box[1])
	# 	self.box_prompt.draw(self.game.screen, colors.box_active[0] if self.selected == 1 else colors.box[0], colors.box_active[1] if self.selected == 0 else colors.box[1])
	# 	self.box_log.draw(self.game.screen, colors.box_active[0] if self.selected == 0 else colors.box[0], colors.box_active[1] if self.selected == 0 else colors.box[1])

