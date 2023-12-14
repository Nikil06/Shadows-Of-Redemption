import random
from dataclasses import dataclass
import colors

class GraphicData:
    def __init__(self, base_char: str, base_color: str,
                 rand_char_from: list[str] | None = None, rand_color_from: list[str] | None = None):
        self.base_color = base_color
        self.base_char = base_char
        self.rand_char_from = rand_char_from
        self.rand_color_from = rand_color_from

        if rand_char_from is not None:
            self.base_char = random.choice(rand_char_from)

        if rand_color_from is not None:
            self.base_color = random.choice(rand_color_from)

        self.current_color = self.base_color
        self.current_char = self.base_char

    def get_display_char(self, faint_effect=False):
        faint = ""
        if faint_effect:
            faint = colors.FAINT

        return f"{self.current_color}{faint}{self.current_char}{colors.RESET}"

    def revert_display_char(self):
        self.current_char = self.base_char
        self.current_color = self.base_color

    def set_display_char(self, new_char, new_color):
        self.current_char = new_char
        self.current_color = new_color

    def get_copy(self):
        return GraphicData(
            self.base_char,
            self.base_color,
            rand_char_from=self.rand_char_from.copy() if self.rand_char_from else None,
            rand_color_from=self.rand_color_from.copy() if self.rand_color_from else None
        )

@dataclass
class TileData:
    graphic_data: GraphicData
    is_walkable: bool
    blocks_light: bool

class Tile:
    def __init__(self, pos_x: int, pos_y: int, tile_data: TileData):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.tile_data = tile_data

        self.graphic_data = tile_data.graphic_data.get_copy()
        self.is_walkable = tile_data.is_walkable
        self.blocks_light = tile_data.blocks_light

    def get_tile_data(self):
        return self.tile_data

    def set_tile_data(self, new_tile_data: TileData):
        self.tile_data = new_tile_data

        self.graphic_data = new_tile_data.graphic_data.get_copy()
        self.is_walkable = new_tile_data.is_walkable
        self.blocks_light = new_tile_data.blocks_light
