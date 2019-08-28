# Standard imports.
import pygame
from os import environ
from random import randint
from sys import exit

# Initialize Pygame engine.
pygame.init()

# Custom imports.
import game_objects

# Screen setup.
WINDOW_X, WINDOW_Y = 40, 50
environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (WINDOW_X, WINDOW_Y)
WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Pong")

# Clock setup.
clock = pygame.time.Clock()
FPS = 120

# Paddle, ball, and net parameters.
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_WIDTH, BALL_VELOCITY = 10, 5
NET = pygame.Rect(WIDTH/2, 0, 1, HEIGHT)

# TitleScene menu button parameters.
TITLE_BUTTON_WIDTH, TITLE_BUTTON_HEIGHT = 100, 50

# Global colors.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Global fonts.
FONT_SM = pygame.font.SysFont(pygame.font.get_default_font(), 24)
FONT_LG = pygame.font.SysFont(pygame.font.get_default_font(), 124)

# Parent class for all game scenes.
class SceneManager:
    def __init__(self):
        # The next scene to be loaded.
        self.next = self
    
    def process_input(self, events, pressed_keys):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def render(self, screen):
        raise NotImplementedError

    # Called at the end of the main game loop to load the next scene.
    def switch_to_scene(self, next_scene):
        self.next = next_scene
    
    def terminate(self):
        self.switch_to_scene(None)

class TitleScene(SceneManager):
    def __init__(self):
        super().__init__()
    
    def process_input(self, events, pressed_keys):
        for event in events:
            # Handle window close button
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)	
        
            # Handle button clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Set the x, y postions of the mouse click.
                x, y = event.pos
                # Handle clicks on "New Game" button.
                if self.newgame_button.collidepoint(x, y):
                    self.switch_to_scene(GameScene())
                # Handle clicks on "Exit" button.
                elif self.exit_button.collidepoint(x, y):
                    pygame.quit()
                    exit(0)
    
    def update(self):
        # Nothing to update, only checking for user button clicks.
        pass
    
    def render(self, screen):
        screen.fill(BLACK)

        # Title text
        title_menu_text = FONT_LG.render("PYGAME PONG", True, WHITE)
        screen.blit(
            title_menu_text, (
                (WIDTH/2) - (title_menu_text.get_rect().width/2),
                HEIGHT * 0.20
            )
        )
        
        # "New Game" button.
        self.newgame_button = pygame.draw.rect(
            screen,
            GREEN, (
                (WIDTH/2) - (TITLE_BUTTON_WIDTH/2),
                HEIGHT - (TITLE_BUTTON_WIDTH + (TITLE_BUTTON_WIDTH * 0.75)),
                TITLE_BUTTON_WIDTH,
                TITLE_BUTTON_HEIGHT
            )
        )

        # "New Game" button text.
        newgame_button_text = FONT_SM.render("NEW GAME", True, WHITE)
        newgame_button_text_rect = newgame_button_text.get_rect()
        newgame_button_text_rect.center = self.newgame_button.center
        screen.blit(newgame_button_text, newgame_button_text_rect)

        # "Exit" button.
        self.exit_button = pygame.draw.rect(
            screen,
            RED, (
                (WIDTH/2) - (TITLE_BUTTON_WIDTH/2),
                HEIGHT - TITLE_BUTTON_WIDTH,
                TITLE_BUTTON_WIDTH,
                TITLE_BUTTON_HEIGHT
            )
        )

        # "Exit" button text.
        exit_button_text = FONT_SM.render("EXIT", True, WHITE)
        exit_button_text_rect = exit_button_text.get_rect()
        exit_button_text_rect.center = self.exit_button.center
        screen.blit(exit_button_text, exit_button_text_rect)

class GameScene(SceneManager):
    def __init__(self):
        super().__init__()
		
        # Reset paddles, ball, positions, etc. for new game.

        # Create player objects.
        self.paddles = []
        self.balls = []

		# Left paddle.
        self.paddles.append(game_objects.Paddle(
			BALL_VELOCITY,
			pygame.K_w,
			pygame.K_s,
			0,
			HEIGHT / 2 - PADDLE_HEIGHT / 2,
			PADDLE_WIDTH,
			PADDLE_HEIGHT
		))

		# Right paddle.
        self.paddles.append(game_objects.Paddle(
			BALL_VELOCITY,
			pygame.K_UP,
			pygame.K_DOWN,
			WIDTH - PADDLE_WIDTH,
			HEIGHT / 2 - PADDLE_HEIGHT / 2,
			PADDLE_WIDTH,
			PADDLE_HEIGHT
		))
		
		# Ball.
        self.balls.append(game_objects.Ball(
			BALL_VELOCITY,
			WIDTH / 2 - BALL_WIDTH / 2,
			HEIGHT / 2 - BALL_WIDTH / 2,
			BALL_WIDTH,
			BALL_WIDTH
		))
    
    def process_input(self, events, pressed_keys):
        # Paddle and Ball input/movement handled by respective classes.

        for event in events:
            # Handle window close button.
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
     
    def update(self):
         # Check if the ball has collided with a wall.
        for ball in self.balls:
            if ball.x > WIDTH or ball.x < 0:
                self.switch_to_scene(TitleScene())
            elif ball.y > HEIGHT - BALL_WIDTH or ball.y < 0:
                ball.angle = -ball.angle

        # Check if the ball has collided with either paddle.
        for ball in self.balls:
            for paddle in self.paddles:
                if ball.colliderect(paddle):
                    ball.velocity = -ball.velocity
                    ball.angle = randint(-10, 10)
    
    def render(self, screen):
        screen.fill(BLACK)
        
        # Net.
        pygame.draw.rect(screen, WHITE, NET)
			
        # Paddles.
        for paddle in self.paddles:
            paddle.move_paddle(HEIGHT)
            pygame.draw.rect(screen, WHITE, paddle)
            
        # Ball.
        for ball in self.balls:
            ball.move_ball()
            pygame.draw.rect(screen, WHITE, ball)

# Game loop.
def run_game(starting_scene):
    # Only called once to start the initial scene.
    active_scene = starting_scene

    # Primary game loop.
    while active_scene != None:
        pressed_keys = pygame.key.get_pressed()
        
        # Event filtering.
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            
            if quit_attempt:
                active_scene.terminate()
            else:
                filtered_events.append(event)
        
        active_scene.process_input(filtered_events, pressed_keys)
        active_scene.update()
        active_scene.render(screen)
        
        # Loads "next" scene set by switch_to_scene() for next game loop.
        active_scene = active_scene.next
        
        # Flip renders to the screen and tick the clock.
        pygame.display.flip()
        clock.tick(FPS)

# Start the program.
if __name__ == "__main__":
    run_game(TitleScene())