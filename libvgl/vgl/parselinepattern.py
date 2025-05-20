'''
    created by ChapGPT
'''

import re

def parse_line_pattern(pattern_str):
    """
    Parse a patterned line string into a tuple of (pattern_name, length).

    Valid formats:
        .        -> DOT
        -        -> DASH
        -.       -> DASHDOT
        -..      -> DASHDOTDOT
        --       -> LONGDASH
        Optionally followed by :<length>, e.g., '--:0.2'

    Returns:
        (pattern_name, length)

    Raises:
        ValueError for any invalid input
    """
    pattern_map = {
        '.': 'DOT',
        '-': 'DASH',
        '-.': 'DASHDOT',
        '-..': 'DASHDOTDOT',
        '--': 'LONGDASH'
    }

    default_length = 0.05

    try:
        # Match exactly the 5 valid patterns, optionally followed by :<float>
        match = re.fullmatch(r'(\.|-|-\.|-\.{2}|--)(?::(\d*\.?\d+))?', pattern_str)
        if not match:
            raise ValueError(f"Invalid pattern format: '{pattern_str}'")

        symbol, length_str = match.groups()

        if symbol not in pattern_map:
            raise ValueError(f"Unknown pattern symbol: '{symbol}'")

        pattern_name = pattern_map[symbol]
        length = float(length_str) if length_str else default_length

        if length <= 0:
            raise ValueError("Length must be a positive number.")

        return pattern_name, length

    except Exception as e:
        raise ValueError(f"Failed to parse pattern string '{pattern_str}': {e}")
