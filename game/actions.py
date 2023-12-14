from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from .entity import Entity

class Action:
    def perform(self, engine: 'Engine', entity: 'Entity') -> None:
        """
        Perform this action with the objects needed to determine its scope.

        :param engine: It is the scope this action is being performed in.

        :param entity: It is the object performing the action.

        This method must be overridden by Action subclass.
        """
        raise NotImplementedError()

class EscapeAction(Action):
    """Action to exit the game."""
    def perform(self, engine: 'Engine', entity: 'Entity') -> None:
        raise SystemExit()

class MoveAction(Action):
    """Action to move the player character"""
    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy

    def perform(self, engine: 'Engine', entity: 'Entity') -> None:
        target_x = entity.pos_x + self.dx
        target_y = entity.pos_y + self.dy

        if not engine.game_map.is_tile_in_bounds(target_x, target_y):
            return None     # Target Location is not in bounds of GameMap

        if not engine.game_map.is_tile_walkable(target_x, target_y):
            return None     # Target Location is not a walkable tile

        if any(_entity.pos_x == target_x and _entity.pos_y == target_y for _entity in engine.entities):
            return None     # Target Location is occupied by another entity

        entity.move_by(self.dx, self.dy)
