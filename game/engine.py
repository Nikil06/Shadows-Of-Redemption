from .game_map import GameMap
from .entity import Entity
from .rendering import compute_fov

from .constants import FOV_RADIUS

from .input_handler import handle_input

class Engine:
    def __init__(self, entities: list[Entity], game_map: GameMap, player: Entity):
        self.entities = entities
        self.game_map = game_map
        self.player = player

    def handle_input(self):
        action = handle_input()

        if action is None:
            return False

        action.perform(self, self.player)
        return True

        # TODO: Update Field of View

    def get_render(self):
        self.update_fov()
        render = self.game_map.get_map_render()

        for entity in self.entities:

            if self.game_map.camera.is_xy_in_camera_bounds(entity.pos_x, entity.pos_y) \
                    and self.game_map.is_tile_visible(entity.pos_x, entity.pos_y):

                x_rel, y_rel = self.game_map.camera.adjust_xy_to_camera(entity.pos_x, entity.pos_y)
                render[y_rel][x_rel] = entity.graphic_data.get_display_char()

        return render

    def update_fov(self):
        compute_fov(self.game_map, self.player, FOV_RADIUS)

