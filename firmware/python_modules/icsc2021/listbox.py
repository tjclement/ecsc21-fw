import display, gc, easydraw

_activeList = {}

# Listbox UI element
class List():
	def __init__(self, x, y, w, h, font="roboto_regular12", header=None, logo=None):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.font = font
		self.header = header
		self.logo = logo
		self.items = []
		self.selected = 0
		global _activeList
		_activeList[self] = True
		self.lines = self.h // (display.getTextHeight(" ", "roboto_regular12")+6)
		self.offset = 0
		self.visible(True)
		self.enabled(True)
	
	def draw(self):
		if self._visible:
			display.drawRect(self.x, self.y, self.w, self.h, True, 0x000000)
			display.drawRect(self.x, self.y, self.w, self.h, False, 0xFFFFFF)
			cursor = (self.x+1,self.y+1)
			if self.logo:
				cursor = (cursor[0], cursor[1] + 10)
				display.drawPng(self.x + (self.w-60)//2, cursor[1], self.logo)
				cursor = (cursor[0], cursor[1] + 60)
			if self.header:
				cursor = (cursor[0], cursor[1] + 10)
				lineHeight = display.getTextHeight(" ", "exo2_bold12")
				lines = easydraw.lineSplit(self.header, self.w, "exo2_bold12")
				for line in lines:
					display.drawText(cursor[0]+2, cursor[1], line, 0xFFFFFF, "exo2_bold12")
					cursor = (cursor[0], cursor[1] + lineHeight)
				cursor = (cursor[0], cursor[1] + 20)

			totalHeight = 0
			for i in range(len(self.items)-self.offset):
				cursor = (self.x+1,cursor[1])
				item = self.items[self.offset+i]
				lineHeight = display.getTextHeight(item, "roboto_regular12")

				while display.getTextWidth(item, "roboto_regular12") > self.w:
					item = item[:-1]

				totalHeight += lineHeight+6
				if totalHeight >= self.h:
					break
				color = 0xFFFFFF
				if self.offset+i == self.selected:
					display.drawRect(self.x, cursor[1], self.w, lineHeight+6, True, 0xFFFFFF)
					color = 0x000000
				cursor = (self.x,cursor[1]+3)
				display.drawText(cursor[0]+2, cursor[1], item+"\n", color, "roboto_regular12")
				cursor = (self.x,cursor[1]+3+display.getTextHeight(item+"\n", "roboto_regular12"))
	
	def add_item(self, caption):
		if type(caption) == type(""):
			i = self.items.append(caption)
		elif type(caption) == type(b""):
			i = self.items.append(caption.decode('utf-8'))
		else:
			i = self.items.append(str(caption))
		if self._enabled:
			self.draw()
		return i
	
	def count(self):
		return len(self.items)
	
	def selected_text(self):
		return self.items[self.selected]
	
	def remove_item(self, pos):
		self.items.pop(pos)
		if self.selected >= pos and self.selected > 0:
			self.selected -= 1
		if self._enabled:
			self.draw()
		#print("Remove item from pos", pos,"selected",self.selected)
	
	def selected_index(self, setValue=None):
		if setValue:
			self.selected = setValue
			if self.selected < self.offset:
				self.offset = self.selected
			if self.selected >= self.offset+self.lines:
				self.offset = self.selected+self.lines-1
			self.draw()
		else:
			return self.selected
	
	def destroy(self):
		global _activeList
		self.items = []
		self.selected = 0
		del _activeList[self]

	def moveUp(self):
		if self.selected > 0:
			self.selected-=1
			if self.selected < self.offset:
				self.offset = self.selected
		else:
			self.selected = len(self.items)-1
			self.offset = max(0, self.selected - self.lines + 1)
		self.draw()
			
	def moveDown(self):
		if self.selected < len(self.items)-1:
			self.selected+=1
			if self.selected >= self.offset+self.lines:
				self.offset += 1
		else:
			self.selected = 0
			self.offset = 0
		self.draw()
	
	def visible(self, arg):
		self._visible = arg
		self.draw()

	def enabled(self, val):
		global _listUpCallback, _listDownCallback
		self._enabled = val
	
	def clear(self):
		while len(self.items): #Keep the same list!
			self.items.pop()
		self.offset = 0
		self.selected = 0
		gc.collect()
