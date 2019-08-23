# TUTORIAL - https://nick.sarbicki.com/blog/learn-pygame-with-pong/

# IMPORTS
import pygame
from random import randint
from sys import exit

# PADDLE CLASS
class Paddle(pygame.Rect):
	def __init__(self, velocity, up_key, down_key, *args, **kwargs):
		self.velocity = velocity
		self.up_key = up_key
		self.down_key = down_key
		super().__init__(*args, **kwargs)
		
	def move_paddle(self, board_height):
		keys_pressed = pygame.key.get_pressed()
		
		if keys_pressed[self.up_key]:
			if self.y - self.velocity > 0:
				self.y -= self.velocity
				
		if keys_pressed[self.down_key]:	
			if self.y + self.velocity < board_height - self.height:
				self.y += self.velocity
		
# BALL CLASS
class Ball(pygame.Rect):
	def __init__(self, velocity, *args, **kwargs):
		self.velocity = velocity
		self.angle = 0
		super().__init__(*args, **kwargs)
		
	def move_ball(self):
		self.x += self.velocity
		self.y += self.angle

# MAIN
class Pong:
	HEIGHT = 800
	WIDTH = 1600
	
	PADDLE_WIDTH = 10
	PADDLE_HEIGHT = 100
	
	BALL_WIDTH = 10
	BALL_VELOCITY = 10
	
	COLOR = (255, 255, 255)
	
	def __init__(self):
		# Start Pygame instance.
		pygame.init()
		
		# Screen setup.
		self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
		self.clock = pygame.time.Clock()
		print("\nWelcome to Pygame & Pong!")
		
		# Create player objects.
		self.paddles = []
		self.balls = []
		
		self.paddles.append(Paddle( # Left paddle.
			self.BALL_VELOCITY,
			pygame.K_w,
			pygame.K_s,
			0,
			self.HEIGHT / 2 - self.PADDLE_HEIGHT / 2,
			self.PADDLE_WIDTH,
			self.PADDLE_HEIGHT
		))

		self.paddles.append(Paddle( # Right paddle.
			self.BALL_VELOCITY,
			pygame.K_UP,
			pygame.K_DOWN,
			self.WIDTH - self.PADDLE_WIDTH,
			self.HEIGHT / 2 - self.PADDLE_HEIGHT / 2,
			self.PADDLE_WIDTH,
			self.PADDLE_HEIGHT
		))
		
		self.balls.append(Ball(
			self.BALL_VELOCITY,
			self.WIDTH / 2 - self.BALL_WIDTH / 2,
			self.HEIGHT / 2 - self.BALL_WIDTH / 2,
			self.BALL_WIDTH,
			self.BALL_WIDTH
		))
		
		# Add "net" to middle of screen.
		self.central_line = pygame.Rect(self.WIDTH/2, 0, 1, self.HEIGHT)
		
	def check_ball_hits_wall(self):
		for ball in self.balls:
			if ball.x > self.WIDTH or ball.x <0:
				print("\nThe ball got by a paddle - GAME OVER!")
				exit(1)
			if ball.y > self.HEIGHT - self.BALL_WIDTH or ball.y <0:
				ball.angle = -ball.angle
				
	def check_ball_hits_paddle(self):
		for ball in self.balls:
			for paddle in self.paddles:
				if ball.colliderect(paddle):
					ball.velocity = -ball.velocity
					ball.angle = randint(-10, 10)
					break
	
	def game_loop(self):
		while True:
			# Exit by clicking windows' close button.
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
					
			# Check for ball collisions.
			self.check_ball_hits_paddle()
			self.check_ball_hits_wall()
					
			# Redraw the screen.
			self.screen.fill((0, 0, 0))
			
			# MOVE & DRAW
			pygame.draw.rect(self.screen, self.COLOR, self.central_line)
			
			for paddle in self.paddles:
				paddle.move_paddle(self.HEIGHT)
				pygame.draw.rect(self.screen, self.COLOR, paddle)
				
			for ball in self.balls:
				ball.move_ball()
				pygame.draw.rect(self.screen, self.COLOR, ball)
				
			# Flip drawn graphics to screen, and manage the clock.
			pygame.display.flip()
			self.clock.tick(60)
		
# START
if __name__ == '__main__':
	pong = Pong()
	pong.game_loop()