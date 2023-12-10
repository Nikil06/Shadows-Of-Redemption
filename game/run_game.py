import sys

from .entity import Entity
from .constants import *
from .game_map import GameMap
from .engine import Engine

from templaters.dungeon_explore import get_formatted_template, sample_player_data, sample_log_data
import smooth_console as console

def run_game():
    import time

    frame_rate = 1 / 60

    player = Entity(
        pos_x=int(MAP_WIDTH / 2), pos_y=int(MAP_HEIGHT / 2),
        graphic_data=PLAYER_GRAPHIC
    )

    enemy = Entity(
        pos_x=int(MAP_WIDTH / 2) + 1, pos_y=int(MAP_HEIGHT / 2) + 1,
        graphic_data=ENEMY_GRAPHIC
    )

    entities = [enemy, player]
    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)

    engine = Engine(entities, game_map, player)

    try:
        console.init_console()
        while True:
            engine.handle_input()
            screen = get_formatted_template('Test Area', engine.get_render(), sample_player_data, sample_log_data)

            console.clear_console()
            console.print_to_console(screen)
            console.update_console(align_center=True)

            time.sleep(frame_rate)
    except KeyboardInterrupt:
        sys.stdout.flush()
        console.clear_screen()
        console.set_cursor_visibility(True)
    finally:
        console.clear_console()
        sys.stdout.flush()
        console.clear_screen()
        console.set_cursor_visibility(True)
