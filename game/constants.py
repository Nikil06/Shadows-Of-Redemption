import colors
from .tile import TileData, GraphicData

# Game Settings #-------------------------------------------------------------------------#

MAP_WIDTH = 26
MAP_HEIGHT = 26

# Graphic Datas #-------------------------------------------------------------------------#

WALL_GRAPHIC = GraphicData(base_char='#', base_color=colors.BROWN)
FLOOR_GRAPHIC = GraphicData(base_char='`', base_color=colors.GREEN)
SHROUD_GRAPHIC = GraphicData(base_char=' ', base_color=colors.LIGHT_WHITE)

PLAYER_GRAPHIC = GraphicData(base_char='@', base_color=colors.LIGHT_CYAN)
ENEMY_GRAPHIC = GraphicData(base_char='E', base_color=colors.LIGHT_RED)

# Tile Datas #----------------------------------------------------------------------------#

WALL_DATA = TileData(
    graphic_data=WALL_GRAPHIC,
    is_walkable=False,
    blocks_light=True,
)

FLOOR_DATA = TileData(
    graphic_data=FLOOR_GRAPHIC,
    is_walkable=True,
    blocks_light=False,
)

# -----------------------------------------------------------------------------------------#
