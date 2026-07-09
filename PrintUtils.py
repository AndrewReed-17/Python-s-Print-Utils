"""
Robert Henning's, Python Print-Utils (R5b), 2026
PrintUtils.py

Utilities for CLI rendering using ANSI escape sequences.

This module provides:
- Progress bar rendering
- Line clearing utilities
- Structured printing for dict and list

Compatibility:
- Requires ANSI-compatible terminal (Linux, macOS, modern Windows)

Author: Robert Henning
Licence : MIT, 2026
Repos : https://github.com/AndrewReed-17/RHs_PyPrintUtils
"""

from __future__ import annotations

import sys
import time
import os 
import shutil
from typing import Any, Dict, List


__all__ = [
    #"menue_mk_i",
    "get_terminal_size",
    "replace_with_void",
    "clear_progressbar",
    "progressbar",
    "clear_cli",
    "print_dict",
    "print_list",
]

# ---------------------------------------------------------------------------
# ANSI Coded G-UI
# ---------------------------------------------------------------------------

def menue_mk_i(tpl_terminal_size:tuple,
               str_name:str,
               dict_options:dict,
               str_message:str="",
               int_select:bool=False,
               int_mutliple:bool=False
               ) -> None :
    """
    WIP

    Parameters
        ----------
        tpl_terminal_size : tuple, cols by rows
        str_name : string, the name of the menue
        dict_options : a dictionary of Name by a tuple of func follewed by the key associeted with ; the key is non nessacry of you have the Select mode on.
        str_message : [FAC] it is a message, maybe to help, or other things, THE LIST OF OPTIONS WILL BE AUTOMACLY DISPLAYED.
        int_select : [FAC, False] True to enable the selection (on/off) mode.
        int_mutliple : [FAC, False] True to enable the multiple selection mode ; require the select mode on.
    """
    clear_cli()

    return


def deg_place_corner(terminal_size:tuple) -> None :
    default_pos = 0
    print(f"\033[{default_pos};{default_pos}HT-L") #Top Left
    print(f"\033[{default_pos};{terminal_size[0]}HR") #Top Right
    print(f"\033[{terminal_size[1]-1};{default_pos}HB-L") #Bottom Left
    print(f"\033[{terminal_size[1]-1};{terminal_size[0]}HR") #Bottom Right
    return
    
# ---------------------------------------------------------------------------
# Core ANSI utilities
# ---------------------------------------------------------------------------

def get_terminal_size() -> tuple :
    """
    Maid by R. H.
    Date : 2026-06-18T14:35
    Updated : 2026-06-18T14:35

    Maid with IA : No
    Assisted by IA : No

    Credit : granitosaurus, https://www.reddit.com/r/Python/comments/5q7b36/getting_terminal_size_in_python/ 

    Returns:
        tuple: Colums by Width
    """
    try:
        columns, rows = os.get_terminal_size(0)
    except OSError:
        columns, rows = os.get_terminal_size(1)

    return columns, rows 

COLS = get_terminal_size()[0]

def replace_with_void(lines: int) -> None:
    """
    Clear the last `lines` lines from the terminal.

    Parameters
    ----------
    lines : int
        Number of lines to erase above the current cursor position.

    Notes
    -----
    Uses ANSI escape sequences:
    - \\033[F : move cursor up
    - \\033[2K : clear line
    - \\033[E : move cursor down
    """
    if lines <= 0:
        return

    sys.stdout.write("\033[F" * lines)

    for _ in range(lines):
        sys.stdout.write("\033[2K")
        sys.stdout.write("\033[E")

    sys.stdout.write("\033[F" * lines)
    sys.stdout.flush()


def clear_progressbar(lines: int = 3) -> None:
    """
    Clear a previously printed progress bar block.

    Parameters
    ----------
    lines : int, optional
        Number of lines used by the progress bar (default is 3).
    """
    for _ in range(lines):
        sys.stdout.write("\033[2K\033[E")

    sys.stdout.write("\033[F" * lines)
    sys.stdout.flush()


def clear_cli() -> None:
    """
    Clear the entire terminal screen and reset cursor position.
    """
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


# ---------------------------------------------------------------------------
# Progress bar
# ---------------------------------------------------------------------------

def progressbar(max_value: int, value: int, start_time: float) -> None:
    """
    Render a 3-line progress bar in-place.

    Parameters
    ----------
    max_value : int
        Total expected value (completion target).
    value : int
        Current progress value.
    start_time : float
        Timestamp (from time.time()) marking the start.

    Behavior
    --------
    Displays:
    - Spinner
    - Percentage
    - Progress bar
    - Speed (units/sec)
    - ETA (seconds)

    Notes
    -----
    This function overwrites previous output using ANSI cursor movement.
    """

    if max_value <= 0:
        raise ValueError("max_value must be > 0")

    spinner = ("|", "/", "-", "\\")
    bar_length = 20

    # Move cursor to beginning of block
    sys.stdout.write("\033[F" * 3)

    percent = int((value / max_value) * 100)
    spin = spinner[value % len(spinner)]

    filled = int(bar_length * percent / 100)
    bar = "=" * filled + "-" * (bar_length - filled)

    elapsed = time.time() - start_time
    speed = value / elapsed if elapsed > 0 else 0.0
    eta = (max_value - value) / speed if speed > 0 else 0.0

    print(f" $ Operating {spin}")
    print(f"  - {percent:02d}% [{bar}]")
    print(f"  - Speed : {speed:.2f}/s, ETA : {int(eta):02d}s")

    sys.stdout.write("\033[F" * 3)


# ---------------------------------------------------------------------------
# Structured printing
# ---------------------------------------------------------------------------

def print_dict(data: Dict[Any, Any], index = -1, limit: int = COLS) -> None:
    """
    Pretty-print a dictionary or a sub-dictionary.

    Parameters
    ----------
    data : dict
        Dictionary to display.
    index : any, optional
        If not -1, attempts to access data[index].
    limit : int, optional
        Maximum line width before truncation.

    Notes
    -----
    Empty values are replaced with '!ERR_NO_VALUE!'.
    """

    target = data if index == -1 else data.get(index, {})

    processed = {
        str(k): (v if str(v) else "!ERR_NO_VALUE!")
        for k, v in target.items()
    }

    max_key_len = max((len(k) for k in processed), default=0)

    for key, value in processed.items():
        line = f"  - {key:<{max_key_len}} | {value}"

        if len(line) > limit:
            line = line[: limit - 3] + "..."

        print(line)


def print_list(data: List[Any], index: int = -1, limit: int = COLS) -> None:
    """
    Pretty-print a list or a nested list.

    Parameters
    ----------
    data : list
        List to display.
    index : int, optional
        If not -1, prints data[index] assuming nested structure.
    limit : int, optional
        Maximum line width before truncation.
    """

    target = data if index == -1 else data[index]

    for element in target:

        line = "  - " + str(element)
        
        if len(line) > limit:
            line = line[: limit - 3] + "..."
            
        print(line)

# ---------------------------------------------------------------------------
# Structured string
# ---------------------------------------------------------------------------

def string_dict(data: Dict[Any, Any], index = -1, limit: int = COLS) -> str:
    """
    Pretty-print a dictionary or a sub-dictionary.

    Parameters
    ----------
    data : dict
        Dictionary to display.
    index : any, optional
        If not -1, attempts to access data[index].
    limit : int, optional
        Maximum line width before truncation.

    Notes
    -----
    Empty values are replaced with '!ERR_NO_VALUE!'.
    """
    string = ""
    
    target = data if index == -1 else data.get(index, {})

    processed = {
        str(k): (v if str(v) else "!ERR_NO_VALUE!")
        for k, v in target.items()
    }

    max_key_len = max((len(k) for k in processed), default=0)

    for key, value in processed.items():
        line = f"  - {key:<{max_key_len}} | {value}"

        if len(line) > limit:
            line = line[: limit - 3] + "..."

        string = string + line + "\n"
    return string

def string_list(data: List[Any], index: int = -1, limit: int = COLS) -> str:
    """
    Pretty-print a list or a nested list.

    Parameters
    ----------
    data : list
        List to display.
    index : int, optional
        If not -1, prints data[index] assuming nested structure.
    limit : int, optional
        Maximum line width before truncation.
    """

    string = ""

    target = data if index == -1 else data[index]

    for element in target:

        line = "  - " + str(element)
        
        if len(line) > limit:
            line = line[: limit - 3] + "..."
            
        string = string + line + "\n"
    return string

