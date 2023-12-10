from smooth_console.console_logic import init_console, clear_console, print_to_console, update_console
from smooth_console.terminal_utils import clear_screen, set_cursor_visibility
import time
import sys
import colors

def run_clock():
    init_console()
    clock_format = \
        f"""
Test Clock : Updates the clock smoothly
{colors.LIGHT_GREEN}+==========+
| {colors.CYAN}{'{}'}{colors.LIGHT_GREEN} |
+----------+{colors.RESET}
'{colors.NEGATIVE}{colors.LIGHT_GREEN}Light Green Line Testing coloured output{colors.RESET}'"""
    try:
        while True:
            clear_console()

            print_to_console(clock_format.format(time.strftime("%H:%M:%S")))

            update_console(True)

            time.sleep(0.25)

    except KeyboardInterrupt:

        clear_screen()
        set_cursor_visibility(True)

    finally:
        clear_console()
        sys.stdout.flush()
        clear_screen()
