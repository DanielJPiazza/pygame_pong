# BASE TUTORIAL - https://nick.sarbicki.com/blog/learn-pygame-with-pong/

# IMPORTS
import pygame
import os
from random import randint
from sys import exit

# PLAYER PADDLE
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
		
# BALL
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
	def __init__(self):
		# Start Pygame instance.
		pygame.init()
		
		# GAME & MAIN MENU VARIABLES
		# Window parameters, for screen edge offset and initial position.
		self.WINDOW_HEIGHT_OFFSET = 200
		self.WINDOW_WIDTH_OFFSET = 300
		self.WINDOW_X = 40
		self.WINDOW_Y = 60
		
		# Paddle gameplay parameters.
		self.PADDLE_WIDTH = 10
		self.PADDLE_HEIGHT = 100
		
		# Ball gameplay parameters.
		self.BALL_WIDTH = 10
		self.BALL_VELOCITY = 5
		
		# White/black constants
		self.WHITE = (255, 255, 255)
		self.BLACK = (0, 0, 0)

		# Main menu button properties.
		self.MENU_BUTTON_WIDTH = 100
		self.MENU_BUTTON_HEIGHT = 50
		self.MENU_GREEN = (0, 255, 0)
		self.MENU_RED = (255, 0, 0)

		# Create a main menu fonts.
		self.TITLE_MENU_FONT = pygame.font.SysFont(pygame.font.get_default_font(), 130)
		self.BUTTON_MENU_FONT = pygame.font.SysFont(pygame.font.get_default_font(), 22)

		
		# Screen setup.
		pygame.display.set_caption("Pygame Pong")										# Window caption.
		os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (self.WINDOW_X, self.WINDOW_Y)	# Initial window position.
		self.DISPLAY_INFO = pygame.display.Info()										# Get window info.
		self.HEIGHT = self.DISPLAY_INFO.current_h - self.WINDOW_HEIGHT_OFFSET			# Screen height.
		self.WIDTH = self.DISPLAY_INFO.current_w - self.WINDOW_WIDTH_OFFSET				# Screen width.
		self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))				# Set display mode,
		self.clock = pygame.time.Clock()												# Create clock.
		
	# Check if the ball has collided with a wall.
	def check_ball_hits_wall(self):
		for ball in self.balls:
			if ball.x > self.WIDTH or ball.x <0:
				self.main_menu()
			if ball.y > self.HEIGHT - self.BALL_WIDTH or ball.y <0:
				ball.angle = -ball.angle
				
	# Check if the ball has collided with either paddle.
	def check_ball_hits_paddle(self):
		for ball in self.balls:
			for paddle in self.paddles:
				if ball.colliderect(paddle):
					ball.velocity = -ball.velocity
					ball.angle = randint(-10, 10)
					break
	
	# Start a new game via main menu button.
	def reset_game(self):
		# Create player objects.
		self.paddles = []
		self.balls = []
		
		self.paddles.append(Paddle( # LEFT PADDLE
			self.BALL_VELOCITY,
			pygame.K_w,
			pygame.K_s,
			0,
			self.HEIGHT / 2 - self.PADDLE_HEIGHT / 2,
			self.PADDLE_WIDTH,
			self.PADDLE_HEIGHT
		))

		self.paddles.append(Paddle( # RIGHT PADDLE
			self.BALL_VELOCITY,
			pygame.K_UP,
			pygame.K_DOWN,
			self.WIDTH - self.PADDLE_WIDTH,
			self.HEIGHT / 2 - self.PADDLE_HEIGHT / 2,
			self.PADDLE_WIDTH,
			self.PADDLE_HEIGHT
		))
		
		self.balls.append(Ball(		# BALL
			self.BALL_VELOCITY,
			self.WIDTH / 2 - self.BALL_WIDTH / 2,
			self.HEIGHT / 2 - self.BALL_WIDTH / 2,
			self.BALL_WIDTH,
			self.BALL_WIDTH
		))
		
		# NET
		self.central_line = pygame.Rect(self.WIDTH/2, 0, 1, self.HEIGHT)
	
	# Main menu - allows users to play or exit the program.
	def main_menu(self):
		while True:			
			# Redraw the screen.
			self.screen.fill(self.BLACK)

			# Title text
			self.title_menu_text = self.TITLE_MENU_FONT.render("PYGAME PONG", True, self.WHITE)
			self.screen.blit(
				self.title_menu_text, (
					(self.WIDTH/2) - (self.title_menu_text.get_rect().width/2),
					self.HEIGHT * 0.20
				)
			)
			
			# New Game menu button.
			self.newgame_button = pygame.draw.rect(
				self.screen,
				self.MENU_GREEN, (
					(self.WIDTH/2) - (self.MENU_BUTTON_WIDTH/2),
					self.HEIGHT - (self.MENU_BUTTON_WIDTH + (self.MENU_BUTTON_WIDTH * 0.75)),
					self.MENU_BUTTON_WIDTH,
					self.MENU_BUTTON_HEIGHT
				)
			)

			# New Game menu button text.
			self.newgame_button_text = self.BUTTON_MENU_FONT.render("NEW GAME", True, self.WHITE)
			self.newgame_button_text_rect = self.newgame_button_text.get_rect()
			self.newgame_button_text_rect.center = self.newgame_button.center
			self.screen.blit(self.newgame_button_text, self.newgame_button_text_rect)

			# Exit menu button.
			self.exit_button = pygame.draw.rect(
				self.screen,
				self.MENU_RED, (
					(self.WIDTH/2) - (self.MENU_BUTTON_WIDTH/2),
					self.HEIGHT - self.MENU_BUTTON_WIDTH,
					self.MENU_BUTTON_WIDTH,
					self.MENU_BUTTON_HEIGHT
				)
			)

			# Exit menu button text.
			self.exit_button_text = self.BUTTON_MENU_FONT.render("EXIT", True, self.WHITE)
			self.exit_button_text_rect = self.exit_button_text.get_rect()
			self.exit_button_text_rect.center = self.exit_button.center
			self.screen.blit(self.exit_button_text, self.exit_button_text_rect)

			# Check for mouse clicks on menu and OS close window buttons.
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit(0)			
			
				if event.type == pygame.MOUSEBUTTONDOWN:
					# Set the x, y postions of the mouse click.
					x, y = event.pos
					# START GAME
					if self.newgame_button.collidepoint(x, y):
						self.reset_game()
						self.game_loop()
					# EXIT GAME
					if self.exit_button.collidepoint(x, y):
						pygame.quit()
						exit(0)						

			# Flip drawn graphics to screen, and manage the clock.
			pygame.display.flip()
			self.clock.tick(60)
	
	# Main game loop.
	def game_loop(self):
		while True:
			# Exit by clicking windows' close button.
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit(0)
					
			# Redraw the screen.
			self.screen.fill(self.BLACK)			
			
			# Check for ball collisions.
			self.check_ball_hits_paddle()
			self.check_ball_hits_wall()
			
			# MOVE & DRAW
			pygame.draw.rect(self.screen, self.WHITE, self.central_line)	# NET
			
			for paddle in self.paddles:										# PADDLES
				paddle.move_paddle(self.HEIGHT)
				pygame.draw.rect(self.screen, self.WHITE, paddle)
				
			for ball in self.balls:											# BALL
				ball.move_ball()
				pygame.draw.rect(self.screen, self.WHITE, ball)
				
			# Flip drawn graphics to screen, and manage the clock.
			pygame.display.flip()
			self.clock.tick(120)
		
# START
if __name__ == '__main__':
	pong = Pong()
	pong.main_menu()