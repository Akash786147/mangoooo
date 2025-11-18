"""
Main file for Magma Boy and Hydro Girl game.
"""

# import pygame and orther needed libraries
import sys
import pygame
from pygame.locals import *

# import classes
from game import Game
from board import Board
from character import MagmaBoy, HydroGirl
from controller import ArrowsController, WASDController, GeneralController
from gates import Gates
from doors import FireDoor, WaterDoor
from level_select import LevelSelect
from collectibles import CollectiblesManager
from scoring import ScoreCalculator


def main():
    pygame.init()
    controller = GeneralController()
    game = Game()
    show_intro_screen(game, controller)


def show_intro_screen(game, controller):
    intro_screen = pygame.image.load('data/screens/intro_screen.png')
    game.display.blit(intro_screen, (0, 0))
    while True:
        game.refresh_window()
        if controller.press_key(pygame.event.get(), K_RETURN):
            show_level_screen(game, controller)


def show_level_screen(game, controller):
    level_select = LevelSelect()
    level = game.user_select_level(level_select, controller)
    run_game(game, controller, level)


def show_win_screen(game, controller, elapsed_time=0, diamonds_collected=0, total_diamonds=0):
    """
    Show win screen with score and grade.
    
    Args:
        game: Game object
        controller: Controller object
        elapsed_time: float - Time taken to complete level
        diamonds_collected: int - Number of diamonds collected
        total_diamonds: int - Total diamonds in level
    """
    # Calculate score and grade
    score_calc = ScoreCalculator()
    grade = score_calc.calculate_grade(elapsed_time, diamonds_collected, total_diamonds)
    time_str = score_calc.format_time(elapsed_time)
    description = score_calc.get_grade_description(grade)
    
    # Load win screen
    win_screen = pygame.image.load('data/screens/win_screen.png')
    win_screen.set_colorkey((255, 0, 255))
    
    # Create font for score display
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 28)

    while True:
        game.display.blit(win_screen, (0, 0))
        
        # Draw grade with large font
        grade_color = {
            'A': (0, 255, 0),     # Green
            'B': (100, 200, 255),  # Blue
            'C': (255, 255, 0),    # Yellow
            'D': (255, 100, 0)     # Orange
        }.get(grade, (255, 255, 255))
        
        grade_text = font_large.render(f"Grade: {grade}", True, grade_color)
        grade_x = (game.display.get_width() - grade_text.get_width()) / 2
        game.display.blit(grade_text, (grade_x, 150))
        
        # Draw time
        time_text = font_medium.render(f"Time: {time_str}", True, (255, 255, 255))
        time_x = (game.display.get_width() - time_text.get_width()) / 2
        game.display.blit(time_text, (time_x, 230))
        
        # Draw diamonds collected
        diamonds_text = font_medium.render(
            f"Diamonds: {diamonds_collected}/{total_diamonds}", 
            True, (100, 200, 255)
        )
        diamonds_x = (game.display.get_width() - diamonds_text.get_width()) / 2
        game.display.blit(diamonds_text, (diamonds_x, 270))
        
        # Draw description
        desc_text = font_small.render(description, True, (255, 215, 0))
        desc_x = (game.display.get_width() - desc_text.get_width()) / 2
        game.display.blit(desc_text, (desc_x, 320))
        
        # Draw instructions
        inst_text = font_small.render("Press ENTER to continue", True, (200, 200, 200))
        inst_x = (game.display.get_width() - inst_text.get_width()) / 2
        game.display.blit(inst_text, (inst_x, 370))
        
        game.refresh_window()
        if controller.press_key(pygame.event.get(), K_RETURN):
            show_level_screen(game, controller)


def show_death_screen(game, controller, level):
    death_screen = pygame.image.load('data/screens/death_screen.png')
    death_screen.set_colorkey((255, 0, 255))
    game.display.blit(death_screen, (0, 0))
    while True:
        game.refresh_window()
        events = pygame.event.get()
        if controller.press_key(events, K_RETURN):
            run_game(game, controller, level)
        if controller.press_key(events, K_ESCAPE):
            show_level_screen(game, controller)


def run_game(game, controller, level="level1"):
    # load level data
    if level == "level1":
        board = Board('data/level1.txt')
        gate_location = (285, 128)
        plate_locations = [(190, 168), (390, 168)]
        gate = Gates(gate_location, plate_locations)
        gates = [gate]

        fire_door_location = (64, 48)
        fire_door = FireDoor(fire_door_location)
        water_door_location = (128, 48)
        water_door = WaterDoor(water_door_location)
        doors = [fire_door, water_door]

        magma_boy_location = (16, 336)
        magma_boy = MagmaBoy(magma_boy_location)
        hydro_girl_location = (35, 336)
        hydro_girl = HydroGirl(hydro_girl_location)
        
        # Create collectibles manager and add diamonds
        collectibles = CollectiblesManager()
        # Add some sample diamonds (these positions should be adjusted per level)
        collectibles.add_diamond((80, 150), "blue")
        collectibles.add_diamond((300, 80), "red")
        collectibles.add_diamond((200, 200), "blue")
        collectibles.add_diamond((400, 150), "red")
        collectibles.add_diamond((150, 300), "blue")
        collectibles.add_diamond((450, 250), "red")

    if level == "level2":
        board = Board('data/level2.txt')
        gates = []

        fire_door_location = (390, 48)
        fire_door = FireDoor(fire_door_location)
        water_door_location = (330, 48)
        water_door = WaterDoor(water_door_location)
        doors = [fire_door, water_door]

        magma_boy_location = (16, 336)
        magma_boy = MagmaBoy(magma_boy_location)
        hydro_girl_location = (35, 336)
        hydro_girl = HydroGirl(hydro_girl_location)
        
        # Create collectibles for level 2
        collectibles = CollectiblesManager()
        collectibles.add_diamond((100, 150), "blue")
        collectibles.add_diamond((250, 100), "red")
        collectibles.add_diamond((350, 200), "blue")
        collectibles.add_diamond((450, 150), "red")

    if level == "level3":
        board = Board('data/level3.txt')
        gates = []

        fire_door_location = (5 * 16, 4 * 16)
        fire_door = FireDoor(fire_door_location)
        water_door_location = (28 * 16, 4 * 16)
        water_door = WaterDoor(water_door_location)
        doors = [fire_door, water_door]

        magma_boy_location = (28 * 16, 4 * 16)
        magma_boy = MagmaBoy(magma_boy_location)
        hydro_girl_location = (5 * 16, 4 * 16)
        hydro_girl = HydroGirl(hydro_girl_location)
        
        # Create collectibles for level 3
        collectibles = CollectiblesManager()
        collectibles.add_diamond((200, 150), "blue")
        collectibles.add_diamond((300, 200), "red")
        collectibles.add_diamond((400, 150), "blue")
        collectibles.add_diamond((150, 250), "red")

    # initialize needed classes

    arrows_controller = ArrowsController()
    wasd_controller = WASDController()

    clock = pygame.time.Clock()
    
    # Initialize timer
    start_time = pygame.time.get_ticks()
    elapsed_time = 0

    # main game loop
    while True:
        # pygame management
        clock.tick(60)
        events = pygame.event.get()
        
        # Update timer
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) / 1000.0  # Convert to seconds

        # draw features of level
        game.draw_level_background(board)
        game.draw_board(board)
        if gates:
            game.draw_gates(gates)
        game.draw_doors(doors)
        
        # Draw collectibles (diamonds)
        game.draw_collectibles(collectibles)
        
        # Draw timer and diamond counter
        game.draw_timer(elapsed_time)
        game.draw_diamond_counter(
            collectibles.get_collected_count(), 
            collectibles.get_total_count()
        )

        # draw player
        game.draw_player([magma_boy, hydro_girl])

        # move player
        arrows_controller.control_player(events, magma_boy)
        wasd_controller.control_player(events, hydro_girl)

        game.move_player(board, gates, [magma_boy, hydro_girl])
        
        # Check for diamond collection
        collectibles.check_collection(magma_boy.rect, magma_boy.get_type())
        collectibles.check_collection(hydro_girl.rect, hydro_girl.get_type())

        # check for player at special location
        game.check_for_death(board, [magma_boy, hydro_girl])

        game.check_for_gate_press(gates, [magma_boy, hydro_girl])

        game.check_for_door_open(fire_door, magma_boy)
        game.check_for_door_open(water_door, hydro_girl)

        # refresh window
        game.refresh_window()

        # special events
        if hydro_girl.is_dead() or magma_boy.is_dead():
            show_death_screen(game, controller, level)

        if game.level_is_done(doors):
            show_win_screen(
                game, 
                controller, 
                elapsed_time,
                collectibles.get_collected_count(),
                collectibles.get_total_count()
            )

        if controller.press_key(events, K_ESCAPE):
            show_level_screen(game, controller)

        # close window is player clicks on [x]
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    main()
