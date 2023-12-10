import os
import sys
from copy import deepcopy

from .terminal_utils import set_cursor_visibility, set_cursor_position, clear_screen
from .console_errors import ConsoleSizeError

__text_buffer = ""
__grid_cache = {}


def get_ansi_excluded_count(text):
    char_count = 0
    in_ansi_code = False

    for char in text:
        if char == "\x1b":  # ANSI escape code indicator
            in_ansi_code = True
        elif char == "m" and in_ansi_code:  # End of ANSI escape code
            in_ansi_code = False
        elif not in_ansi_code:
            char_count += 1

    return char_count


def init_console(_hide_cursor: bool = True, _clear_screen: bool = True):
    """
    Initializes the console with the given parameters.
    :param _hide_cursor: Hides the cursor when set to True
    :param _clear_screen: Clears the screen when set to True
    :return: None
    """

    global __text_buffer, __grid_cache
    __text_buffer = ""  # clear the buffer
    __grid_cache = {}  # clear the grid cache

    set_cursor_visibility(not _hide_cursor)

    if _clear_screen:
        clear_screen()




def __generate_grid():
    """
    Generates the grid based on the current terminal window size
    :return: A 2D array with the same size as the current terminal window
    """
    # Get the current terminal window size
    size = os.get_terminal_size()

    # Check if there is a cached grid for current terminal and return it.
    if size in __grid_cache:
        # We return the deepcopy to prevent any references to be attached to the cache.
        # Since 2D List is a mutable array of mutable array of string. (i.e. list[list[str]])
        return deepcopy(__grid_cache[size])

    clear_console()
    sys.stdout.flush()
    clear_screen()

    # If there is no cached grid then create a new one and cache it, then return it.
    grid = [[" " for _ in range(size.columns)] for _ in range(size.lines)]
    __grid_cache[size] = grid

    # We return the deepcopy to prevent any references to be attached to the cache.
    # Since 2D List is a mutable array of mutable array of string. (i.e. list[list[str]])
    return deepcopy(grid)


def write_to_console(text):
    """
    Adds the text to the text_buffer.
    :param text: string to be added.
    :return: None.
    """
    # Just add the text to the text_buffer
    global __text_buffer
    __text_buffer += text


def print_to_console(*args, sep=' ', end='\n'):
    """
    Similar to the default print function, except it writes the output to the text_buffer.
    :param args: The strings that need to be displayed.
    :param sep: Separator between every two arg elements. Defaults to ' '.
    :param end: End Suffix for the output. Defaults to '\n'.
    :return: None.
    """
    # Perform operation to get output similar to the default print function
    text = sep.join(map(str, args)) + end
    # then write it to the text_buffer
    write_to_console(text)


def clear_console():
    """
    Empty/Clear the text_buffer. and sets the cursor position to top-left corner(0, 0).
    :return: None.
    """
    global __text_buffer
    __text_buffer = ""
    set_cursor_position(0, 0)


def center_the_text_buffer(text_buffer, grid_size):
    lines = text_buffer.split('\n')
    size_x, size_y = grid_size

    for line in lines:
        char_count = 0
        in_ansi_code = False

        for char in line:
            if char == "\x1b":  # ANSI escape code indicator
                in_ansi_code = True
            elif char == "m" and in_ansi_code:  # End of ANSI escape code
                in_ansi_code = False
            elif not in_ansi_code:
                char_count += 1

        line = " " * (int((size_x - char_count) / 2) + 1) + line

    empty_line = " " * size_x
    num_of_top_lines = int((size_y - len(lines)) / 2) + 1

    [lines.insert(0, empty_line) for _ in range(num_of_top_lines)]

    return '\n'.join(lines)


def align_buffer_center(text, grid_size, padding_char=' '):
    lines = text.split('\n')
    width, height = grid_size

    # Calculate vertical padding
    vertical_padding = (height - len(lines)) // 2

    # Ensure non-negative vertical padding
    vertical_padding = max(0, vertical_padding)

    # Initialize the centered lines
    centered_lines = []

    for _ in range(vertical_padding):
        centered_lines.append(padding_char * width)

    for line in lines:
        # Calculate horizontal padding
        horizontal_padding = (width - get_ansi_excluded_count(line)) // 2

        # Ensure non-negative horizontal padding
        horizontal_padding = max(0, horizontal_padding)

        # Center the line horizontally and add to the result
        centered_line = padding_char * horizontal_padding + line
        centered_lines.append(centered_line)

    # Join the lines to get the final centered text
    centered_text = '\n'.join(centered_lines)

    return centered_text


def update_console(align_center: bool = False):
    """
    Updates the text_buffer onto the terminal window. (i.e. displays the buffer)
    :return: None.
    """
    global __text_buffer
    __text_buffer = __text_buffer.rstrip()
    grid = __generate_grid()

    x, y = 0, 0
    max_x, max_y = len(grid[0]) - 1, len(grid) - 1

    buffer_size = (max(get_ansi_excluded_count(line) for line in __text_buffer.split('\n')), len(__text_buffer.split('\n')))
    grid_size = (max_x, max_y)

    __text_buffer += f"\nBuffer Size: {buffer_size} | Window Size: {grid_size}"

    if align_center:
        __text_buffer = align_buffer_center(__text_buffer, grid_size)

    ansi_bucket = None

    for char in __text_buffer:
        if char == "\n":
            x = 0
            y += 1

        elif ansi_bucket is None and char == "\033":
            ansi_bucket = char
        elif ansi_bucket is not None and ansi_bucket[-1] != 'm':
            ansi_bucket += char

        else:
            if y > max_y or x > max_x:
                raise ConsoleSizeError(grid_size, buffer_size)

            if ansi_bucket is not None and ansi_bucket[-1] == 'm':
                char = ansi_bucket + char
                ansi_bucket = None

            grid[y][x] = char

            x += 1

    print(end="".join("".join(row) for row in grid))
