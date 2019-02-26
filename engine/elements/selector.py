#!/usr/bin/env python3
# -*- coding: utf8 -*-

from .box import Box


class Selector(Box):
	def __init__(self, label="", items=[]):
		super().__init__(label)
		self.items = items
		self.selector = 0
		self.scroll = 0

	def draw(self, screen, box_color=[-1, -1], item_color=[-1, -1], selected_color=[-1, -1]):
		super().draw(screen, box_color[0], box_color[1])
		while self.selector < self.scroll or (len(self.items) > self.height - 2 and self.scroll > len(self.items) - self.height + 2):
			self.scroll -= 1
		while self.selector > self.scroll + self.height - 3:
			self.scroll += 1
		for i in range(self.scroll, self.scroll + min(self.height - 2, len(self.items) - self.scroll)):
			if i == self.selector:
				screen.addstr(self.y + i - self.scroll + 1, self.x + 1, self.items[i] + ' ' * (self.width - len(self.items[i]) - 2), selected_color[0], selected_color[1])
			else:
				screen.addstr(self.y + i - self.scroll + 1, self.x + 1, self.items[i], item_color[0], item_color[1])
		self.draw_scrollbar(screen, box_color)

	def draw_scrollbar(self, screen, box_color=[-1, -1]):
		divisor = len(self.items) - self.height + 2
		quotient = (float(self.scroll) / divisor) if divisor != 0 else 0
		screen.addstr(self.y + min(int((self.height - 3) * quotient) + 1, self.height - 2), self.x + self.width - 1, '█', box_color[0], box_color[1])

	def down(self):
		self.selector = min(self.selector + 1, len(self.items) - 1)
		self.scroll += 1 if self.selector == self.height + self.scroll - 3 and self.selector < len(self.items) - 1 else 0

	def up(self):
		self.selector = max(self.selector - 1, 0)
		self.scroll -= 1 if self.selector == self.scroll and self.selector > 0 else 0

	def get(self):
		return self.items[self.selector]

