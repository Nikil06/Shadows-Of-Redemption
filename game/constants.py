import colors
from .tile import TileData, GraphicData

# Game Settings #-------------------------------------------------------------------------#

MAP_WIDTH = 40
MAP_HEIGHT = 40

CAMERA_WIDTH = 26
CAMERA_HEIGHT = 26

FOV_RADIUS = 5

FPS = 20

# Graphic Datas #-------------------------------------------------------------------------#

WALL_GRAPHIC = GraphicData(base_char='#', base_color=colors.LIGHT_GRAY)
FLOOR_GRAPHIC = GraphicData(base_char=',', base_color=colors.GREEN,
                            rand_char_from=['`', '"', ',', ':', '.'],
                            rand_color_from=[
                             colors.GREEN, colors.LIGHT_GRAY])
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
