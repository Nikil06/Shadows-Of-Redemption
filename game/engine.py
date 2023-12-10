from .game_map import GameMap
from .entity import Entity

from .input_handler import handle_input

class Engine:
    def __init__(self, entities: list[Entity], game_map: GameMap, player: Entity):
        self.entities = entities
        self.game_map = game_map
        self.player = player

    def handle_input(self):
        action = handle_input()

        if action is None:
            return None

        action.perform(self, self.player)

        # TODO: Update Field of View

    def get_render(self):
        render = self.game_map.get_map_render()

        for entity in self.entities:
            if self.game_map.is_tile_visible(entity.pos_x, entity.pos_y):
                render[entity.pos_y][entity.pos_x] = entity.graphic_data.get_display_char()

        # render the render
        #return '\n'.join(' '.join(row) for row in render)
        return render

    def update_fov(self):
        pass
