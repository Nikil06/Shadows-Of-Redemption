import json.decoder
import math

from .tile import Tile
from .constants import FLOOR_DATA, WALL_DATA, SHROUD_GRAPHIC
from .entity import Entity
from .rendering import Camera


class GameMap:
    def __init__(self, width, height, camera):
        self.width = width
        self.height = height

        self._map = [
            [
                Tile(i, j, WALL_DATA) if i in (0, self.width - 1) or j in (0, self.height - 1)
                else Tile(i, j, FLOOR_DATA)

                for i in range(self.width)
            ]
            for j in range(self.height)
        ]

        self._map[8][3].set_tile_data(WALL_DATA)
        self._map[8][4].set_tile_data(WALL_DATA)
        self._map[8][5].set_tile_data(WALL_DATA)
        self._map[8][6].set_tile_data(WALL_DATA)

        self.visible_tiles = [[True for i in range(self.width)] for j in range(self.height)]
        self.explored_tiles = [[False for i in range(self.width)] for j in range(self.height)]

        self.camera = camera

    def get_map_render(self):
        x1, y1, x2, y2 = self.camera.get_render_area(self.width, self.height)

        render = [[SHROUD_GRAPHIC.get_display_char() for _ in range(x1, x2 + 1)] for _ in range(y1, y2 + 1)]

        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                if self.is_tile_visible(x, y):
                    x_rel, y_rel = self.camera.adjust_xy_to_camera(x, y)
                    render[y_rel][x_rel] = self._map[y][x].graphic_data.get_display_char()
                elif self.is_tile_explored(x, y):
                    x_rel, y_rel = self.camera.adjust_xy_to_camera(x, y)
                    render[y_rel][x_rel] = self._map[y][x].graphic_data.get_display_char(faint_effect=True)


        return render

    def is_tile_in_bounds(self, x, y):
        return 0 <= x <= (self.width - 1) and 0 <= y <= (self.height - 1)

    def is_tile_walkable(self, x, y):
        if not self.is_tile_in_bounds(x, y):
            return False

        return self._map[y][x].is_walkable

    def is_tile_visible(self, x, y):
        if not self.is_tile_in_bounds(x, y):
            return False

        return self.visible_tiles[y][x]

    def is_tile_explored(self, x, y):
        if not self.is_tile_in_bounds(x, y):
            return False

        return self.explored_tiles[y][x]

    def is_tile_light_blocker(self, x, y):
        if not self.is_tile_in_bounds(x, y):
            raise ValueError("Tile needs to be in bounds to check if it blocks light or not.")

        return self._map[y][x].tile_data.blocks_light

    def set_tile_visibility(self, x, y, is_visible: bool):
        if not self.is_tile_in_bounds(x, y):
            raise ValueError("Tile needs to be in bounds to set its visibility.")

        self.visible_tiles[y][x] = is_visible

        if not self.is_tile_explored(x, y):
            self.set_tile_explored(x, y, True)

    def set_tile_explored(self, x, y, is_explored: bool):
        if not self.is_tile_in_bounds(x, y):
            raise ValueError("Tile needs to be in bounds to set if its explored.")

        self.explored_tiles[y][x] = is_explored



