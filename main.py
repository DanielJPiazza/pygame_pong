# Standard imports.
import pygame
from sys import exit

# Initialize Pygame engine.
pygame.init()

# Custom imports.
import game_objects
import scenes
import parameters as pm

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
        
        # Required functions for each scene class.
        active_scene.process_input(filtered_events, pressed_keys)
        active_scene.update()
        active_scene.render(pm.screen)
        
        # Loads "next" scene set by switch_to_scene() for next game loop.
        active_scene = active_scene.next
        
        # Flip renders to the screen and tick the clock.
        pygame.display.flip()
        pm.clock.tick(pm.FPS)

# Start the program.
if __name__ == "__main__":
    run_game(scenes.TitleScene(pm.screen, pm.clock))