"""
import os
import time

filename = "main.py"


print(f"Running {filename}")
os.system(f"start /MAX cmd /c python {filename}")
time.sleep(2)

"""

from game.run_game import run_game
from smooth_console.clock_example import run_clock

run_game()
