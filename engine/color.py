

def toHEX(number):
	digits = "0123456789ABCDEF"
	return digits[int(number // 16)] + digits[int(number % 16)]


def fromHEX(number):
	digits = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
	return digits[number[0]] * 16 + digits[number[1]]


def hueToRGB(p, q, t):
	if t < 0:
		t += 1
	if t > 1:
		t -= 1
	if t < 1.0/6.0:
		return p + (q - p) * 6.0 * t
	if t < 1.0/2.0:
		return q
	if t < 2.0/3.0:
		return p + (q - p) * (2.0/3.0 - t) * 6.0
	return p


class ColorMode(object):
	RGB = 0
	HSL = 1
	HEX = 2


class Color(object):
	def __init__(self, **kwargs):
		self._data = [0, 0, 0]
		self._alpha = 1.0
		self.colorMode = 0
		if 'r' in kwargs and 'g' in kwargs and 'b' in kwargs:
			self.colorMode = ColorMode.RGB
			self._data = [kwargs['r'], kwargs['g'], kwargs['b']]
		elif 'h' in kwargs and 's' in kwargs and 'l' in kwargs:
			self.colorMode = ColorMode.HSL
			self._data = [float(kwargs['h'] % 360), float(kwargs['s']), float(kwargs['l'])]
		elif 'hex' in kwargs:
			self.colorMode = ColorMode.HEX
			self._data = kwargs['hex'].upper()  # (kwargs['hex'][1:] if kwargs['hex'][0] == '#' else kwargs['hex']).upper()
		if 'a' in kwargs:
			self._alpha = kwargs['a']

	def toRGB(self):
		if self.colorMode == ColorMode.HEX:
			self._data = [fromHEX(self._data[1:3]), fromHEX(self._data[3:5]), fromHEX(self._data[5:7])]
		elif self.colorMode == ColorMode.HSL:
			hue = self._data[0] / 360.0
			saturation = float(self._data[1])
			lightness = float(self._data[2])

			if saturation == 0:
				self._data = [0, 0, 0]
			else:
				q = lightness * (1 + saturation) if lightness < 0.5 else lightness + saturation - lightness * saturation
				p = 2 * lightness - q
				self._data = [round(hueToRGB(p, q, hue + 1.0/3.0) * 255), round(hueToRGB(p, q, hue) * 255), round(hueToRGB(p, q, hue - 1.0/3.0) * 255)]
		self.colorMode = ColorMode.RGB
		return self

	def toHSL(self):
		if self.colorMode == ColorMode.HEX:
			pass
		elif self.colorMode == ColorMode.RGB:
			r = self._data[0] / 255.0
			g = self._data[1] / 255.0
			b = self._data[2] / 255.0
			maxValue = max(r, g, b)
			minValue = min(r, g, b)
			average = (maxValue + minValue) / 2
			hue = average
			saturation = average
			lightness = average

			if (maxValue == minValue):
				hue = 0
				saturation = 0
			else:
				difference = maxValue - minValue
				saturation = difference / (2 - maxValue - minValue) if lightness > 0.5 else difference / (maxValue + minValue)
				if maxValue == r:
					hue = (g - b) / difference + (6.0 if g < b else 0)
				elif maxValue == g:
					hue = (b - r) / difference + 2.0
				elif maxValue == b:
					hue = (r - g) / difference + 4.0
				hue /= 6.0
			self._data = [hue * 360.0, saturation, lightness]
		self.colorMode = ColorMode.HSL
		return self

	def toHEX(self):
		if self.colorMode == ColorMode.RGB:
			self._data = '#' + toHEX(self._data[0]) + toHEX(self._data[1]) + toHEX(self._data[2])
		self.colorMode = ColorMode.HEX
		return self

	def toColorMode(self, colorMode=0):
		if colorMode == ColorMode.RGB:
			self.toRGB()
		elif colorMode == ColorMode.HSL:
			self.toHSL()
		elif colorMode == ColorMode.HEX:
			self.toHEX()

	def getRed(self):
		colorMode = self.colorMode
		self.toRGB()
		value = self._data[0]
		self.toColorMode(colorMode)
		return value

	def setRed(self, value=0):
		colorMode = self.colorMode
		self.toRGB()
		self._data[0] = value
		self.toColorMode(colorMode)
		return self

	def getGreen(self):
		colorMode = self.colorMode
		self.toRGB()
		value = self._data[1]
		self.toColorMode(colorMode)
		return value

	def setGreen(self, value=0):
		colorMode = self.colorMode
		self.toRGB()
		self._data[1] = value
		self.toColorMode(colorMode)
		return self

	def getBlue(self):
		colorMode = self.colorMode
		self.toRGB()
		value = self._data[2]
		self.toColorMode(colorMode)
		return value

	def setBlue(self, value=0):
		colorMode = self.colorMode
		self.toRGB()
		self._data[2] = value
		self.toColorMode(colorMode)
		return self

	def getHue(self):
		colorMode = self.colorMode
		self.toHSL()
		value = self._data[0]
		self.toColorMode(colorMode)
		return value

	def setHue(self, value=0):
		colorMode = self.colorMode
		self.toHSL()
		self._data[0] = value % 360
		self.toColorMode(colorMode)
		return self

	def getSaturation(self):
		colorMode = self.colorMode
		self.toHSL()
		value = self._data[1]
		self.toColorMode(colorMode)
		return value

	def setSaturation(self, value=0):
		colorMode = self.colorMode
		self.toHSL()
		self._data[1] = value
		self.toColorMode(colorMode)
		return self

	def getLightness(self):
		colorMode = self.colorMode
		self.toHSL()
		value = self._data[2]
		self.toColorMode(colorMode)
		return value

	def setLightness(self, value=0):
		colorMode = self.colorMode
		self.toHSL()
		self._data[2] = value
		self.toColorMode(colorMode)
		return self

	def getHex(self):
		colorMode = self.colorMode
		self.toHEX()
		value = self._data
		self.toColorMode(colorMode)
		return value

	def setHex(self, value="#000000"):
		colorMode = self.colorMode
		self.toHEX()
		self._data = value
		self.toColorMode(colorMode)
		return self

	def get256(self):
		colorMode = self.colorMode
		self.toRGB()
		colorIndex = 16 + 36 * round(self._data[0] / 51.0) + 6 * round(self._data[1] / 51.0) + round(self._data[2] / 51)
		self.toColorMode(colorMode)
		return colorIndex

	def getRGB(self):
		colorMode = self.colorMode
		self.toRGB()
		colorIndex = str(self._data[0]) + ';' + str(self._data[1]) + ';' + str(self._data[2])
		self.toColorMode(colorMode)
		return colorIndex

	def __eq__(self, other):
		if type(other) == int:
			return False
		colorMode = other.colorMode
		other.toColorMode(self.colorMode)
		result = False
		if self.colorMode == ColorMode.HEX:
			result = self._data == other._data
		else:
			result = self._data[0] == other._data[0] and self._data[1] == other._data[1] and self._data[2] == other._data[2]
		other.toColorMode(colorMode)
		return result

	def __str__(self):
		if self.colorMode == ColorMode.RGB:
			return "rgb(" + str(self._data[0]) + ", " + str(self._data[1]) + ", " + str(self._data[2]) + ')'
		elif self.colorMode == ColorMode.HSL:
			return "hsl(" + str(self._data[0]) + ", " + str(self._data[1]) + ", " + str(self._data[2]) + ')'
		elif self.colorMode == ColorMode.HEX:
			return "hex('" + self._data + "')"

	def __repr__(self):
		return '<' + str(self) + '>'


class Colors(object):
	white = Color(r=255, g=255, b=255)
	black = Color()
	red = Color(r=255, g=0, b=0)
	green = Color(r=0, g=255, b=0)
	blue = Color(r=0, g=0, b=255)
	cyan = Color(r=0, g=255, b=255)
	magenta = Color(r=255, g=0, b=255)
	yellow = Color(r=255, g=255, b=0)

