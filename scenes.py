# Standard imports.
import pygame
from random import randint

# Custom imports.
import parameters
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
        screen.fill(parameters.BLACK)

        # Current FPS.
        self.current_fps_render = parameters.FONT_SM.render(self.current_fps, True, parameters.WHITE)
        self.screen.blit(self.current_fps_render, (10, 10))

        # Title text
        title_menu_text = parameters.FONT_LG.render("PYGAME PONG", True, parameters.WHITE)
        self.screen.blit(
            title_menu_text, (
                (parameters.WIDTH/2) - (title_menu_text.get_rect().width/2),
                parameters.HEIGHT * 0.20
            )
        )
        
        # "New Game" button.
        self.newgame_button = pygame.draw.rect(
            self.screen,
            parameters.GREEN, (
                (parameters.WIDTH/2) - (parameters.TITLE_BUTTON_WIDTH/2),
                parameters.HEIGHT - (parameters.TITLE_BUTTON_WIDTH + (parameters.TITLE_BUTTON_WIDTH * 0.75)),
                parameters.TITLE_BUTTON_WIDTH,
                parameters.TITLE_BUTTON_HEIGHT
            )
        )

        # "New Game" button text.
        newgame_button_text = parameters.FONT_SM.render("NEW GAME", True, parameters.WHITE)
        newgame_button_text_rect = newgame_button_text.get_rect()
        newgame_button_text_rect.center = self.newgame_button.center
        self.screen.blit(newgame_button_text, newgame_button_text_rect)

        # "Exit" button.
        self.exit_button = pygame.draw.rect(
            self.screen,
            parameters.RED, (
                (parameters.WIDTH/2) - (parameters.TITLE_BUTTON_WIDTH/2),
                parameters.HEIGHT - parameters.TITLE_BUTTON_WIDTH,
                parameters.TITLE_BUTTON_WIDTH,
                parameters.TITLE_BUTTON_HEIGHT
            )
        )

        # "Exit" button text.
        exit_button_text = parameters.FONT_SM.render("EXIT", True, parameters.WHITE)
        exit_button_text_rect = exit_button_text.get_rect()
        exit_button_text_rect.center = self.exit_button.center
        self.screen.blit(exit_button_text, exit_button_text_rect)

class GameScene(SceneManager):
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        super().__init__()

        # Skip new game object creation (reset) if resuming from pause menu.
        if not parameters.RESUME_FROM_PAUSED:
            # Reset paddles, ball, positions, etc. for new game.

            # Create player objects.
            game_objects.paddles = []
            game_objects.balls = []

            # Left paddle.
            game_objects.paddles.append(game_objects.Paddle(
                parameters.BALL_VELOCITY,
                pygame.K_w,
                pygame.K_s,
                0,
                parameters.HEIGHT / 2 - parameters.PADDLE_HEIGHT / 2,
                parameters.PADDLE_WIDTH,
                parameters.PADDLE_HEIGHT
            ))

            # Right paddle.
            game_objects.paddles.append(game_objects.Paddle(
                parameters.BALL_VELOCITY,
                pygame.K_UP,
                pygame.K_DOWN,
                parameters.WIDTH - parameters.PADDLE_WIDTH,
                parameters.HEIGHT / 2 - parameters.PADDLE_HEIGHT / 2,
                parameters.PADDLE_WIDTH,
                parameters.PADDLE_HEIGHT
            ))
            
            # Ball.
            game_objects.balls.append(game_objects.Ball(
                parameters.BALL_VELOCITY,
                parameters.WIDTH / 2 - parameters.BALL_WIDTH / 2,
                parameters.HEIGHT / 2 - parameters.BALL_WIDTH / 2,
                parameters.BALL_WIDTH,
                parameters.BALL_WIDTH
            ))
        
        # Reset pause flag.
        if parameters.RESUME_FROM_PAUSED:
            parameters.RESUME_FROM_PAUSED = False
    
    def process_input(self, events, pressed_keys):
        # Paddle and Ball input/movement handled by respective classes.

        for event in events:
            # Handle window close button.
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.switch_to_scene(PauseScene(self.screen, self.clock))
     
    def update(self):
        # Check current FPS.
        self.current_fps = "FPS: " + str(int(self.clock.get_fps()))

         # Check if the ball has collided with a wall.
        for ball in game_objects.balls:
            if ball.x > parameters.WIDTH or ball.x < 0:
                self.switch_to_scene(TitleScene(self.screen, self.clock))
            elif ball.y > parameters.HEIGHT - parameters.BALL_WIDTH or ball.y < 0:
                ball.angle = -ball.angle

        # Check if the ball has collided with either paddle.
        for ball in game_objects.balls:
            for paddle in game_objects.paddles:
                if ball.colliderect(paddle):
                    ball.velocity = -ball.velocity
                    ball.angle = randint(-10, 10)
    
    def render(self, screen):
        # Clear the screen.
        self.screen.fill(parameters.BLACK)

        # Current FPS.
        self.current_fps_render = parameters.FONT_SM.render(self.current_fps, True, parameters.WHITE)
        self.screen.blit(self.current_fps_render, (10, 10))
        
        # Net.
        pygame.draw.rect(self.screen, parameters.WHITE, parameters.NET)
			
        # Paddles.
        for paddle in game_objects.paddles:
            paddle.move_paddle(parameters.HEIGHT)
            pygame.draw.rect(self.screen, parameters.WHITE, paddle)
            
        # Ball.
        for ball in game_objects.balls:
            ball.move_ball()
            pygame.draw.rect(self.screen, parameters.WHITE, ball)

class PauseScene(SceneManager):
    def __init__(self, screen, clock):
        parameters.RESUME_FROM_PAUSED = True
        self.screen = screen
        self.clock = clock
        super().__init__()
    
    def process_input(self, events, pressed_keys):
        for event in events:
            # Handle window close button
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.switch_to_scene(GameScene(self.screen, self.clock))

            # Handle button clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Set the x, y postions of the mouse click.
                x, y = event.pos
                # Handle clicks on "New Game" button.
                if self.resume_button.collidepoint(x, y):
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
        screen.fill(parameters.BLACK)
        
        # Current FPS.
        self.current_fps_render = parameters.FONT_SM.render(self.current_fps, True, parameters.WHITE)
        self.screen.blit(self.current_fps_render, (10, 10))

        # Pause menu text
        pause_menu_text = parameters.FONT_LG.render("PAUSED", True, parameters.WHITE)
        self.screen.blit(
            pause_menu_text, (
                (parameters.WIDTH/2) - (pause_menu_text.get_rect().width/2),
                parameters.HEIGHT * 0.20
            )
        )
        
        # "Resume" button.
        self.resume_button = pygame.draw.rect(
            self.screen,
            parameters.GREEN, (
                (parameters.WIDTH/2) - (parameters.TITLE_BUTTON_WIDTH/2),
                parameters.HEIGHT - (parameters.TITLE_BUTTON_WIDTH + (parameters.TITLE_BUTTON_WIDTH * 0.75)),
                parameters.TITLE_BUTTON_WIDTH,
                parameters.TITLE_BUTTON_HEIGHT
            )
        )

        # "Resume" button text.
        resume_button_text = parameters.FONT_SM.render("RESUME", True, parameters.WHITE)
        resume_button_text_rect = resume_button_text.get_rect()
        resume_button_text_rect.center = self.resume_button.center
        self.screen.blit(resume_button_text, resume_button_text_rect)

        # "Exit" button.
        self.exit_button = pygame.draw.rect(
            self.screen,
            parameters.RED, (
                (parameters.WIDTH/2) - (parameters.TITLE_BUTTON_WIDTH/2),
                parameters.HEIGHT - parameters.TITLE_BUTTON_WIDTH,
                parameters.TITLE_BUTTON_WIDTH,
                parameters.TITLE_BUTTON_HEIGHT
            )
        )

        # "Exit" button text.
        exit_button_text = parameters.FONT_SM.render("EXIT", True, parameters.WHITE)
        exit_button_text_rect = exit_button_text.get_rect()
        exit_button_text_rect.center = self.exit_button.center
        self.screen.blit(exit_button_text, exit_button_text_rect)