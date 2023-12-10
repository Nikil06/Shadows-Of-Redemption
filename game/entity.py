from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .tile import GraphicData

class Entity:
    def __init__(self, pos_x: int, pos_y: int, graphic_data: 'GraphicData'):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.graphic_data = graphic_data

    def move_by(self, dx: int, dy: int):
        self.pos_x += dx
        self.pos_y += dy

    def move_to(self, new_x: int, new_y: int):
        self.pos_x = new_x
        self.pos_y = new_y
