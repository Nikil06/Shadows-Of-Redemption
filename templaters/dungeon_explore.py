import os.path

from resource_manager.kvf_file import KVF_File
from resource_manager.path_manager import TEMPLATES_DIR_PATH
import os

template_file = KVF_File(
    path=os.path.join(TEMPLATES_DIR_PATH, "dungeon_explore.kvf"),
    delimiter="$$$ ", comment_marker='#', escape_prefix='/$'
)

f_main_window = template_file.get_sections("window", return_type='str')
f_player_frame = template_file.get_sections("player_frame", return_type='str')


def make_progress_bar(bar_width, current_steps, total_steps,
                      prefix_char='[', suffix_char=']', filled_char='#', empty_char='-'):
    fill_length = int((current_steps / total_steps) * bar_width)
    return f"{prefix_char}{filled_char * fill_length}{empty_char * (bar_width - fill_length)}{suffix_char}"


def wrap_text(text, wrap_length, prefix='', suffix=''):
    wrapped_lines = []
    current_line = ''

    words = text.split(' ')  # separates words

    for word in words:
        if len(current_line) + len(word) <= wrap_length:
            current_line += word + ' '
        else:
            wrapped_lines.append(prefix + current_line.rstrip() + suffix)
            current_line = word + ' '

    wrapped_lines.append(prefix + current_line.rstrip() + suffix)  # Adds the last remaining words at the end

    return wrapped_lines


def get_formatted_player_frame(player_data):
    current_artifact_count = 0
    total_artifact_count = 8

    p_stats = player_data["stats"]
    substitution_map = {
        "name_bar": f"──<< {player_data['name']} >>".ljust(60, '─'),
        "one_line_info": f"Lvl {player_data['lvl']} {player_data['race']} {player_data['class']}".title().ljust(26, ' '),

        "p_str": str(p_stats["str"]).ljust(6, " "),
        "p_def": str(p_stats["def"]).ljust(6, " "),
        "p_dex": str(p_stats["dex"]).ljust(6, " "),
        "p_int": str(p_stats["int"]).ljust(6, " "),
        "p_wis": str(p_stats["wis"]).ljust(6, " "),
        "p_luk": str(p_stats["luk"]).ljust(6, " "),

        "hp_bar": make_progress_bar(20, player_data["hp"][0], player_data["hp"][1]).ljust(25, " "),
        "hp_state": f"{player_data['hp'][0]}/{player_data['hp'][1]}".ljust(25, ' '),

        "ap_bar": make_progress_bar(20, player_data["ap"][0], player_data["ap"][1]).ljust(25, ' '),
        "ap_state": f"{player_data['ap'][0]}/{player_data['ap'][1]}".ljust(25, ' '),

        "xp_bar": make_progress_bar(20, player_data["xp"][0], player_data["xp"][1]).ljust(25, ' '),
        "xp_state": f"{player_data['xp'][0]}/{player_data['xp'][1]}".ljust(25, ' '),

        "currency": f"{player_data['currency']} G".ljust(19, ' '),
        "artifact_count": f"({current_artifact_count}/{total_artifact_count})".ljust(8)
    }

    status_effects = player_data["status_effects"]
    sorted_effects = status_effects  # TODO: Sort Effects

    EFFECT_MAX_LENGTH = 12
    MAX_DISPLAY_EFFECTS = 6

    effects_display = [" " * EFFECT_MAX_LENGTH] * MAX_DISPLAY_EFFECTS

    if len(sorted_effects) > MAX_DISPLAY_EFFECTS:
        for i in range(min(MAX_DISPLAY_EFFECTS, len(sorted_effects))):
            effects_display[i] = sorted_effects[i].ljust(EFFECT_MAX_LENGTH).title()

        effects_display[-1] = "More...".ljust(EFFECT_MAX_LENGTH)
    else:
        for i in range(len(sorted_effects)):
            effects_display[i] = sorted_effects[i].ljust(EFFECT_MAX_LENGTH).title()

    for i, status_effect in enumerate(effects_display, start=1):
        substitution_map[f'effect_{i}'] = status_effect

    return f_player_frame.format_map(substitution_map).split('\n')


def get_formatted_log_frame(logs):
    LOGS_LINE_WIDTH = 60
    LOG_LINES_COUNT = 15
    logs_display = [" " * LOGS_LINE_WIDTH] * LOG_LINES_COUNT
    prev_idx = 1

    logs_display[0] = f"──<< Logs >>".ljust(60, '─')

    try:
        if "message" in logs and logs["message"]:
            log_lines = wrap_text(logs['message'], 55, prefix="    ", suffix=" ")
            for i in range(len(log_lines)):
                if i == 0:
                    log_lines[i] = " -> " + log_lines[i][4:]
                logs_display[prev_idx + 1] = log_lines[i].ljust(LOGS_LINE_WIDTH)
                prev_idx += 1
        if "options" in logs and logs["options"]:
            prev_idx += 1
            options = logs["options"]
            for key_code, option in options.items():
                logs_display[prev_idx + 1] = f"{' ' * 3}[{key_code}] {option}".ljust(LOGS_LINE_WIDTH)
                prev_idx += 1
    except IndexError:
        logs_display[-3] = logs_display[-1] = " " * LOGS_LINE_WIDTH
        logs_display[-2] = "  Press [L] to continue reading logs  ".center(LOGS_LINE_WIDTH, '-')

    return logs_display

def get_formatted_template(location_name, dungeon_board, player_data, logs):
    substitution_map = {"world_0": f"──<< {location_name} >>".ljust(53, '─')}

    board_lines = [" ".join([*row]) for row in dungeon_board]
    for i, line in enumerate(board_lines):
        substitution_map[f"world_{i+1}"] = line

    player_frame = get_formatted_player_frame(player_data)
    logs_frame = get_formatted_log_frame(logs)

    for i, line in enumerate(player_frame):
        if i == 0:
            substitution_map[f"player_0"] = line
        else:
            substitution_map[f"p_frame_{i}"] = line

    for i, line in enumerate(logs_frame):
        substitution_map[f"logs_{i}"] = line

    return f_main_window.format_map(substitution_map)


sample_player_data = {
    "name": "Player Name",
    "lvl": 4,
    "race": "human",
    "class": "warrior",

    "stats": {
        "str": 100, "def": 100, "dex": 100,
        "int": 100, "wis": 100, "luk": 100
    },

    "hp": (47, 51),
    "ap": (21, 26),
    "xp": (18, 50),

    "currency": 126,

    "status_effects": ["haste", "poisoned", "effect 3", "effect 4"]

}

sample_log_data = {
    "message": "This is a sample log message that provides user further feedback on whats happening in the world due to the limitations of ascii graphics.",
    "options": {
        "1": "choice 1",
        "2": "choice 2",
        "3": "choice 3",
    }
}

sample_world = [["#" for _ in range(26)] for _ in range(26)]


