import sys
import time

from .entity import Entity
from .constants import *
from .game_map import GameMap
from .engine import Engine
from .rendering import Camera

from templaters.dungeon_explore import get_formatted_template, sample_player_data, sample_log_data
import smooth_console as console

def run_game():
    per_frame_delay = 1 / FPS

    player = Entity(
        pos_x=int(MAP_WIDTH / 2), pos_y=int(MAP_HEIGHT / 2),
        graphic_data=PLAYER_GRAPHIC
    )

    enemy = Entity(
        pos_x=int(MAP_WIDTH / 2) + 1, pos_y=int(MAP_HEIGHT / 2) + 1,
        graphic_data=ENEMY_GRAPHIC
    )

    camera = Camera(CAMERA_WIDTH, CAMERA_HEIGHT, player)

    entities = [enemy, player]
    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT, camera)

    engine = Engine(entities, game_map, player)

    try:
        console.init_console()
        while True:
            engine.handle_input()
            screen = get_formatted_template('Test Area', engine.get_render(), sample_player_data, sample_log_data)

            console.clear_console()
            console.print_to_console(screen)
            console.update_console(align_center=True)

            time.sleep(per_frame_delay)
    except KeyboardInterrupt:
        sys.stdout.flush()
        console.clear_screen()
        console.set_cursor_visibility(True)
    finally:
        console.clear_console()
        sys.stdout.flush()
        console.clear_screen()
        console.set_cursor_visibility(True)
