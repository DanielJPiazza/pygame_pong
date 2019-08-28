# Standard imports.
import pygame
from random import randint

# Custom imports.
import parameters as pm
import game_objects

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
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
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
                    self.switch_to_scene(GameScene(self.screen, self.clock))
                # Handle clicks on "Exit" button.
                elif self.exit_button.collidepoint(x, y):
                    pygame.quit()
                    exit(0)
    
    def update(self):
        # Check current FPS.
        self.current_fps = "FPS: " + str(int(self.clock.get_fps()))
    
    def render(self, screen):
        # Clear the screen.
        screen.fill(pm.BLACK)

        # Current FPS.
        self.current_fps_render = pm.FONT_SM.render(self.current_fps, True, pm.WHITE)
        self.screen.blit(self.current_fps_render, (10, 10))

        # Title text
        title_menu_text = pm.FONT_LG.render("PYGAME PONG", True, pm.WHITE)
        self.screen.blit(
            title_menu_text, (
                (pm.WIDTH/2) - (title_menu_text.get_rect().width/2),
                pm.HEIGHT * 0.20
            )
        )
        
        # "New Game" button.
        self.newgame_button = pygame.draw.rect(
            self.screen,
            pm.GREEN, (
                (pm.WIDTH/2) - (pm.TITLE_BUTTON_WIDTH/2),
                pm.HEIGHT - (pm.TITLE_BUTTON_WIDTH + (pm.TITLE_BUTTON_WIDTH * 0.75)),
                pm.TITLE_BUTTON_WIDTH,
                pm.TITLE_BUTTON_HEIGHT
            )
        )

        # "New Game" button text.
        newgame_button_text = pm.FONT_SM.render("NEW GAME", True, pm.WHITE)
        newgame_button_text_rect = newgame_button_text.get_rect()
        newgame_button_text_rect.center = self.newgame_button.center
        self.screen.blit(newgame_button_text, newgame_button_text_rect)

        # "Exit" button.
        self.exit_button = pygame.draw.rect(
            self.screen,
            pm.RED, (
                (pm.WIDTH/2) - (pm.TITLE_BUTTON_WIDTH/2),
                pm.HEIGHT - pm.TITLE_BUTTON_WIDTH,
                pm.TITLE_BUTTON_WIDTH,
                pm.TITLE_BUTTON_HEIGHT
            )
        )

        # "Exit" button text.
        exit_button_text = pm.FONT_SM.render("EXIT", True, pm.WHITE)
        exit_button_text_rect = exit_button_text.get_rect()
        exit_button_text_rect.center = self.exit_button.center
        self.screen.blit(exit_button_text, exit_button_text_rect)

class GameScene(SceneManager):
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        super().__init__()

        # Reset paddles, ball, positions, etc. for new game.

        # Create player objects.
        self.paddles = []
        self.balls = []

		# Left paddle.
        self.paddles.append(game_objects.Paddle(
			pm.BALL_VELOCITY,
			pygame.K_w,
			pygame.K_s,
			0,
			pm.HEIGHT / 2 - pm.PADDLE_HEIGHT / 2,
			pm.PADDLE_WIDTH,
			pm.PADDLE_HEIGHT
		))

		# Right paddle.
        self.paddles.append(game_objects.Paddle(
			pm.BALL_VELOCITY,
			pygame.K_UP,
			pygame.K_DOWN,
			pm.WIDTH - pm.PADDLE_WIDTH,
			pm.HEIGHT / 2 - pm.PADDLE_HEIGHT / 2,
			pm.PADDLE_WIDTH,
			pm.PADDLE_HEIGHT
		))
		
		# Ball.
        self.balls.append(game_objects.Ball(
			pm.BALL_VELOCITY,
			pm.WIDTH / 2 - pm.BALL_WIDTH / 2,
			pm.HEIGHT / 2 - pm.BALL_WIDTH / 2,
			pm.BALL_WIDTH,
			pm.BALL_WIDTH
		))
    
    def process_input(self, events, pressed_keys):
        # Paddle and Ball input/movement handled by respective classes.

        for event in events:
            # Handle window close button.
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
     
    def update(self):
        # Check current FPS.
        self.current_fps = "FPS: " + str(int(self.clock.get_fps()))

         # Check if the ball has collided with a wall.
        for ball in self.balls:
            if ball.x > pm.WIDTH or ball.x < 0:
                self.switch_to_scene(TitleScene(self.screen, self.clock))
            elif ball.y > pm.HEIGHT - pm.BALL_WIDTH or ball.y < 0:
                ball.angle = -ball.angle

        # Check if the ball has collided with either paddle.
        for ball in self.balls:
            for paddle in self.paddles:
                if ball.colliderect(paddle):
                    ball.velocity = -ball.velocity
                    ball.angle = randint(-10, 10)
    
    def render(self, screen):
        # Clear the screen.
        self.screen.fill(pm.BLACK)

        # Current FPS.
        self.current_fps_render = pm.FONT_SM.render(self.current_fps, True, pm.WHITE)
        self.screen.blit(self.current_fps_render, (10, 10))
        
        # Net.
        pygame.draw.rect(self.screen, pm.WHITE, pm.NET)
			
        # Paddles.
        for paddle in self.paddles:
            paddle.move_paddle(pm.HEIGHT)
            pygame.draw.rect(self.screen, pm.WHITE, paddle)
            
        # Ball.
        for ball in self.balls:
            ball.move_ball()
            pygame.draw.rect(self.screen, pm.WHITE, ball)