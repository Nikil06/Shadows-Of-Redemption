from .tile import Tile
from .constants import FLOOR_DATA, WALL_DATA, SHROUD_GRAPHIC
from .entity import Entity

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.entities = []

        self._map = [
            [
                Tile(i, j, WALL_DATA) if i in (0, self.width-1) or j in (0, self.height-1)
                else Tile(i, j, FLOOR_DATA)

                for i in range(self.width)
            ]
            for j in range(self.height)
        ]

        self.visible_tiles = [
            [
                True
                for i in range(self.width)
            ]
            for j in range(self.height)
        ]

    def get_map_render(self):
        render = [
            [
                self._map[j][i].graphic_data.get_display_char()
                for i in range(self.width)
            ]
            for j in range(self.height)
        ]

        for j in range(self.height):
            for i in range(self.width):
                if not self.visible_tiles[j][i]:
                    render[j][i] = SHROUD_GRAPHIC.get_display_char()

        return render

    def is_tile_in_bounds(self, x, y):
        return 0 <= x <= (self.width-1) and 0 <= y <= (self.height-1)

    def is_tile_walkable(self, x, y):
        if not self.is_tile_in_bounds(x, y):
            raise ValueError("Tile is not in bounds of GameMap")

        return self._map[y][x].is_walkable

    def is_tile_visible(self, x, y):
        if not self.is_tile_in_bounds(x, y):
            raise ValueError("Tile is not in bounds of GameMap")

        return self.visible_tiles[y][x]
