from dataclasses import dataclass
import colors

class GraphicData:
    def __init__(self, base_char: str, base_color: str):
        self.base_color = base_color
        self.base_char = base_char

        self.current_color = base_color
        self.current_char = base_char

    def get_display_char(self):
        return f"{self.current_color}{self.current_char}{colors.RESET}"
        #return self.current_char

    def revert_display_char(self):
        self.current_char = self.base_char
        self.current_color = self.base_color

    def set_display_char(self, new_char, new_color):
        self.current_char = new_char
        self.current_color = new_color

    def get_copy(self):
        return GraphicData(self.base_char, self.base_color)

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
