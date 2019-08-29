# Standard imports.
import pygame

# Game objects to save state during pause.
paddles = []
balls = []

# PLAYER PADDLE CLASS
class Paddle(pygame.Rect):
	def __init__(self, velocity, up_key, down_key, *args, **kwargs):
		self.velocity = velocity
		self.up_key = up_key
		self.down_key = down_key
		super().__init__(*args, **kwargs)
		
	def move_paddle(self, window_height):
		keys_pressed = pygame.key.get_pressed()
		
		if keys_pressed[self.up_key]:
			if self.y - self.velocity > 0:
				self.y -= self.velocity
				
		if keys_pressed[self.down_key]:	
			if self.y + self.velocity < window_height - self.height:
				self.y += self.velocity
		
# BALL
class Ball(pygame.Rect):
	def __init__(self, velocity, *args, **kwargs):
		self.velocity = velocity
		self.angle = 0
		super().__init__(*args, **kwargs)
		
	def move_ball(self):
		self.x += self.velocity
		self.y += self.angle