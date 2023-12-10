import os
from .actions import MoveAction, EscapeAction

class Modifiers:
    NONE = 'none'
    COMMAND = 'command'
    CTRL = 'ctrl'
    ALT = 'alt'
    SHIFT = 'shift'


class Keys:
    UP_ARROW = 'up_arrow'
    DOWN_ARROW = 'down_arrow'
    LEFT_ARROW = 'left_arrow'
    RIGHT_ARROW = 'right_arrow'

    ESCAPE_KEY = 'escape'


if os.name == 'nt':
    import msvcrt

    def is_keypress_detected():
        return msvcrt.kbhit()

    def get_keypress():
        if not is_keypress_detected():
            return None

        keycode = msvcrt.getch()

        if keycode == b'\xe0':

            extended_keycode = msvcrt.getch()

            if extended_keycode == b'H':
                return Keys.UP_ARROW, Modifiers.NONE

            elif extended_keycode == b'P':
                return Keys.DOWN_ARROW, Modifiers.NONE

            elif extended_keycode == b'K':
                return Keys.LEFT_ARROW, Modifiers.NONE

            elif extended_keycode == b'M':
                return Keys.RIGHT_ARROW, Modifiers.NONE

        elif keycode == b'\x00':
            pass
        else:
            if keycode == b'\x1b':
                return Keys.ESCAPE_KEY, Modifiers.NONE

        return None


elif os.name == 'unix':
    raise NotImplementedError("MacOS and Linux support coming soon..")

    def get_keypress():
        pass

    def is_keypress_detected():
        pass


def handle_input():
    keypress = get_keypress()

    if keypress is None:
        return None

    elif keypress == (Keys.ESCAPE_KEY, Modifiers.NONE):
        return EscapeAction()

    elif keypress == (Keys.UP_ARROW, Modifiers.NONE):
        return MoveAction(0, -1)
    elif keypress == (Keys.DOWN_ARROW, Modifiers.NONE):
        return MoveAction(0, 1)
    elif keypress == (Keys.LEFT_ARROW, Modifiers.NONE):
        return MoveAction(-1, 0)
    elif keypress == (Keys.RIGHT_ARROW, Modifiers.NONE):
        return MoveAction(1, 0)

    return None
