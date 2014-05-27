from scene import *
from random import *


#For errors with the platforms
class PlatformError (Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)


#The jumping object
class Jumper (object):
	def __init__(self, center):
		self.frame = Rect(0, 0, 30, 40)
		self.frame.center(center)
		self.color = Color(1, 0, 0)
		self.fall_gravity = .3
		self.vspeed = 7
		self.jump_speed = 10
		self.sensitivity = 22


#The platform object
class Platform (object):
	def __init__(self, type, x, y):
		self.type = type
		if type == 'normal':
			self.color = Color(0, 1, 0)
			self.frame = Rect(x, y, 55, 12)
		elif type == 'break':
			self.color = Color(.7, .3, 0)
			self.frame = Rect(x, y, 55, 12)
		elif type == 'move':
			self.color = Color(0, .7, 1)
			self.frame = Rect(x, y, 55, 12)
		elif type == 'cloud':
			self.color = Color(1, 1, 1)
			self.frame = Rect(x, y, 55, 12)
		elif type == 'move cloud'
			self.color = Color(1, 1, 1)
			self.frame = Rect(x, y, 55, 12)
		else:
			raise PlatformError('Invalid platform type.')


#The scene of the game
class MyScene (Scene):
	#Setup the scene
	def setup(self):
		#Define jumper
		self.jumper = Jumper(self.bounds.center())
		self.jumper.oldpos = self.jumper.frame.origin()
		#Define score
		self.score = 0
		#Create and clean preliminary platforms
		self.platforms = []
		for i in xrange(12):
			platform = Platform('normal', randint(0, self.size.w - 60), randint(0, self.size.h/2))
			if not self.platform_overlap(platform):
				self.platforms.append(platform)
		for i in xrange(12):
			platform = Platform('normal', randint(0, self.size.w - 60), randint(self.size.h/2, self.size.h-12))
			if not self.platform_overlap(platform):
				self.platforms.append(platform)
	

	#Update the scene
	def draw(self):
		background(0,0,0)
		#Update position, spawn and update platforms and outside wrap
		g = gravity()
		self.jumper.hspeed = g.x * self.jumper.sensitivity
		self.jumper.vspeed -= self.jumper.fall_gravity
		self.jumper.frame.x += self.jumper.hspeed
		if self.jumper.vspeed > 0 and (self.jumper.frame.y + self.jumper.frame.h/2) >= self.size.h/2:
			self.clean_platforms()
			self.score += self.jumper.vspeed * .9
			self.jumper.frame.y = self.size.h/2 - self.jumper.frame.h/2
			for i in xrange(0, len(self.platforms)):
				self.platforms[i].frame.y -= self.jumper.vspeed
			highest = 0
			for platform in self.platforms:
				if platform.frame.y > highest:
					highest = platform.frame.y
			dist = self.size.h - highest
			if random() < .2:
				choice = random()
				if choice < .85:
					platform = Platform('cloud', randint(0, self.size.w - platform.frame.w), self.size.h)
				elif choice < .875:
					platform = Platform('move cloud', randint(0, self.size.w - platform.frame.w), self.size.h)
					platform.speed = 2
				elif choice < .90:
					platform = Platform('normal', randint(0, self.size.w - platform.frame.w), self.size.h)
				elif choice < .95:
					platform = Platform('move', randint(0, self.size.w - platform.frame.w), self.size.h)
					platform.speed = 2
				else:
					platform = Platform('break', randint(0, self.size.w - platform.frame.w), self.size.h)
				if not self.platform_overlap(platform):
					self.platforms.append(platform)
		else:
			self.jumper.frame.y += self.jumper.vspeed
		if self.jumper.frame.x <= -self.jumper.frame.w/2:
			self.jumper.frame.x += self.size.w
		elif self.jumper.frame.x >= self.size.w - self.jumper.frame.w/2:
			self.jumper.frame.x -= self.size.w
		#Test for and handle collisions
		if self.jumper.vspeed < 0:
			try:
				m = (self.jumper.frame.y - self.jumper.oldpos.y)/(self.jumper.frame.x - self.jumper.oldpos.x)
				for platform in self.platforms:
					if self.jumper.frame.y < (platform.frame.y + platform.frame.h) and self.jumper.oldpos.y > (platform.frame.y + platform.frame.h):
						x = (platform.frame.y + platform.frame.h - self.jumper.oldpos.y)/m + self.jumper.oldpos.x
						if x > (platform.frame.x - self.jumper.frame.w) and x < (platform.frame.x + platform.frame.w):
							if platform.type == 'normal' or platform.type == 'move':
								self.jumper.frame.x = x
								self.jumper.frame.y = platform.frame.y + platform.frame.h
								self.jumper.vspeed = self.jumper.jump_speed
							elif platform.type == 'break':
								self.platforms.remove(platform)
							elif platform.type == 'cloud' or platform.type == 'move cloud':
								self.jumper.frame.x = x
								self.jumper.frame.y = platform.frame.y + platform.frame.h
								self.jumper.vspeed = self.jumper.jump_speed
								self.platforms.remove(platform)
			except ZeroDivisionError:
				pass
		for i in xrange(0, len(self.platforms)):
			platform = self.platforms[i]
			if platform.type == 'move' or platform.type == 'move cloud':
				if platform.speed < 0:
					if platform.frame.x <= 0:
						self.platforms[i].speed *= -1
						self.platforms[i].frame.x = 0
					else:
						self.platforms[i].frame.x += platform.speed
				elif platform.speed > 0:
					if platform.frame.x >= self.size.w - platform.frame.w:
						self.platforms[i].speed *= -1
						self.platforms[i].frame.x = self.size.w - platform.frame.w
					else:
						self.platforms[i].frame.x += platform.speed
		#Draw jumper, platforms and score
		for platform in self.platforms:
			r, g, b, a = platform.color
			fill(r, g, b)
			x, y, w, h = platform.frame
			rect(x, y, w, h)
		x, y, w, h = self.jumper.frame
		r, g, b, a = self.jumper.color
		fill(r, g, b)
		rect(x, y, w, h)
		tint(0, 0, 0)
		fill(0, .7, 1, .8)
		rect(0, self.size.h - 30, self.size.w, 30)
		text('Score: ' + str(int(self.score)), x = self.size.w/2, y = self.size.h - 15)
		#Set old position
		self.jumper.oldpos = self.jumper.frame.origin()
		

	#Check if the platform overlaps existing platforms
	def platform_overlap(self, platform):
		for other_platform in self.platforms:
			if platform.frame.intersects(other_platform.frame):
				return True
		return False

	#Remove old platforms
	def clean_platforms(self):
		for platform in self.platforms:
			if platform.frame.y < -platform.frame.h:
				self.platforms.remove(platform)
				
run(MyScene())