import math

from .entity import Entity

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game_map import GameMap


class Camera:
    """A Camera object that tells us which parts of the world is currently visible to the camera."""

    def __init__(self, width: int, height: int, focus_entity: Entity):
        self.width = width
        self.height = height

        self.focus_entity = focus_entity

        self.cam_x = focus_entity.pos_x
        self.cam_y = focus_entity.pos_y

    def adjust_camera_position(self, map_width: int, map_height: int):
        """
        Adjusts camera position to match the focus entity while staying in the maps bounds.
        """
        min_x = self.width // 2
        min_y = self.height // 2
        max_x = (map_width - 1) - self.width // 2
        max_y = map_height - self.height // 2

        self.cam_x = max(min_x, min(self.focus_entity.pos_x, max_x))  # clamping camera x
        self.cam_y = max(min_y, min(self.focus_entity.pos_y, max_y))  # clamping camera y

    def get_render_area(self, map_width, map_height) -> tuple[int, int, int, int]:
        """
        gets the bounding box for what is visible through the camera.

        returns (x1, y1, x2, y2) where
            - x1 is minimum visible x index.
            - y1 is minimum visible y index.
            - x2 is maximum visible x index.
            - y2 is maximum visible y index.
        """
        self.adjust_camera_position(map_width, map_height)
        return (
            self.cam_x - self.width // 2, self.cam_y - self.height // 2,
            self.cam_x + self.width // 2, self.cam_y + self.height // 2
        )

    def adjust_xy_to_camera(self, x: int, y: int) -> tuple[int, int]:
        """
        Gives the transformed x, y index with respect to the camera(the top-left corner as the origin.)

        :param x: x index on game_map
        :param y: y index on game_map
        :return: transformed x, y indices with respect to camera
        """
        return x - (self.cam_x - self.width // 2), y - (self.cam_y - self.height // 2)

    def is_xy_in_camera_bounds(self, x: int, y: int, adjusted=False):
        """
        Tells whether the given x, y indices are in camera bounds

        :param x: x index
        :param y: y index
        :param adjusted: whether the indices are adjusted with respect to the camera.
        :return: Returns True if the given x, y is visible to the camera.
        """
        x_rel, y_rel = x, y
        if not adjusted:
            x_rel, y_rel = self.adjust_xy_to_camera(x, y)

        return 0 <= x_rel < self.width and 0 <= y_rel < self.height


def rsv_compute_fov(game_map: 'GameMap', player: Entity, radius: int):
    """Compute the FOV"""

    # reset the visible tiles
    game_map.visible_tiles = [[False for _ in range(game_map.width)] for _ in range(game_map.height)]

    game_map.set_tile_visibility(player.pos_x, player.pos_y, True)

    def cast_light(center_x: int, center_y: int, row: int,
                   start_slope: float, end_slope: float,
                   _radius: int,
                   xx: int, xy: int, yx: int, yy: int):

        if start_slope < end_slope:
            return

        radius_squared = _radius * _radius

        for j in range(row, _radius + 1):
            dx, dy = -j - 1, -j
            blocked = False

            while dx <= 0:
                dx += 1

                X = center_x + dx * xx + dy * yx
                Y = center_y + dx * xy + dy * yy

                # stop if out of bounds
                if not game_map.is_tile_in_bounds(X, Y):
                    break

                # calculate slopes
                l_slope = (dx - 0.5) / (dy + 0.5)
                r_slope = (dx + 0.5) / (dy - 0.5)

                # Check visibility and update visible_tiles
                if start_slope < r_slope:
                    continue
                elif end_slope > l_slope:
                    break

                if dx * dx + dy * dy < radius_squared:
                    game_map.set_tile_visibility(X, Y, True)

                # Handle blocked tiles

                if blocked:
                    if game_map.is_tile_light_blocker(X, Y):
                        new_start_slope = r_slope
                        continue
                    else:
                        blocked = False
                        start_slope = new_start_slope

                else:
                    if game_map.is_tile_light_blocker(X, Y) and j < _radius:
                        blocked = True
                        cast_light(center_x, center_y, j + 1,
                                   start_slope, l_slope, _radius,
                                   xx, xy, yx, yy)
                        new_start_slope = r_slope

    # Octant multipliers for RSC algorithm
    octants = [
        (1, 0, 0, -1), (0, 1, 1, 0), (0, 1, -1, 0), (1, 0, 0, 1),
        (-1, 0, 0, 1), (0, -1, -1, 0), (0, -1, 1, 0), (-1, 0, 0, -1)
    ]

    for octant in range(8):
        cast_light(player.pos_x, player.pos_y, 1, 1.0, 0.0, radius, *octants[octant])

def compute_fov(game_map: 'GameMap', player: Entity, radius):
    # Initialize a FOV map with the same size as the game map
    game_map.visible_tiles = [[False for i in range(game_map.width)] for j in range(game_map.height)]

    def cast_rays(_game_map, x, y, _radius):
        for angle in range(360):
            x_dir = math.cos(math.radians(angle))
            y_dir = math.sin(math.radians(angle))

            # Start from the entity's position
            current_x, current_y = x, y

            for _ in range(_radius):
                current_x += x_dir
                current_y += y_dir

                # Check if the current position is within the map bounds
                if not (0 <= int(current_x) < _game_map.width and 0 <= int(current_y) < _game_map.height):
                    break

                tile_x, tile_y = int(current_x), int(current_y)

                # Mark the tile as visible
                _game_map.set_tile_visibility(tile_x, tile_y, True)

                # Break the loop if the tile blocks light
                if _game_map.is_tile_light_blocker(tile_x, tile_y):
                    break

    # Compute FOV for the entity's position
    cast_rays(game_map, player.pos_x, player.pos_y, radius)
