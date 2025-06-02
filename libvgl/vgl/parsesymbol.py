'''
    initial version by Gemini
    edited by Uisang Hwang
    5/30/2025
'''

import re
from typing import Optional, Dict, Any, Tuple

if __name__ == "__main__":
    from libvgl import color, symbol
else:
    from . import color, symbol

# Reverse map for quick lookup
symbol_map = {code: name for name, code in symbol.symbol_name}

symbol_name = 'symbol'
symbol_lcol = 'line_color'
symbol_fcol = 'fill_color'
symbol_lthk = 'line_thickness'
symbol_size = 'size'
symbol_u    = 'u'
symbol_rot  = 'rotation'

# Default values
DEFAULTS = {
   symbol_lcol : 'k',
   symbol_fcol : 'r',
   symbol_lthk : 0.001,
   symbol_size : 0.05,
   symbol_u    : 0.6,
   symbol_rot  : 0.0
}

# Regex patterns
MODIFIER_RE = re.compile(r'(lc|fc|lt|sz|u|r)\(([^()]*)\)')
hex_color = r"^((?:0x)?[0-9a-fA-F]{2}),((?:0x)?[0-9a-fA-F]{2}),((?:0x)?[0-9a-fA-F]{2})$"

def parse_color(value: str) -> str:
    if isinstance(value, color.Color):
        return value

    value = value.strip()
    hex_match = re.search(hex_color, value)
    
    if hex_match:
        hex_r_str = hex_match.group(1)
        hex_g_str = hex_match.group(2)
        hex_b_str = hex_match.group(3)
        
        r_int = int(hex_r_str, 16)
        g_int = int(hex_g_str, 16)
        b_int = int(hex_b_str, 16)
        
        return color.Color(r_int, g_int, b_int)
    
    elif re.match(r'^\d{1,3},\d{1,3},\d{1,3}$', value):
        return color.Color(value[0],value[1],value[2])   # RGB triplet
        
    elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', value):
        c_ = color.default_color[value]
        if c_ is None:
            print("Error: invalid color name (%s). Default color(Black) will be returned"%value)
            return color.BLACK
        return c_  # Named color (e.g. 'r', 'blue', 'lightblue')
        
    elif re.match(r'^[\?]', value):
        return None
        
    else:
        raise ValueError(f"Invalid color value: {value}")

def parse_symbol_string(symbol_str: str) -> Dict[str, Any]:
    if ':' in symbol_str:
        shape_part, mod_part = symbol_str.split(':', 1)
    else:
        shape_part = symbol_str
        mod_part = ''

    symbol_type: Optional[str] = symbol_map.get(shape_part)

    # Handle star polygons like '*7'
    if symbol_type is None and shape_part.startswith('*') and shape_part[1:].isdigit():
        symbol_type = f'*{shape_part[1:]}'
    elif symbol_type is None:
        raise ValueError(f"Unknown symbol type: {shape_part}")

    # Start with default values
    result: Dict[str, Any] = {
        symbol_name : symbol_type,
        symbol_lcol : color.default_color[DEFAULTS[symbol_lcol]],
        symbol_fcol : color.default_color[DEFAULTS[symbol_fcol]],
        symbol_lthk : DEFAULTS[symbol_lthk],
        symbol_size : DEFAULTS[symbol_size],
        symbol_u    : DEFAULTS[symbol_u],
        symbol_rot  : DEFAULTS[symbol_rot]
    }

    for key, value in MODIFIER_RE.findall(mod_part):
        if key in ('lc', 'fc'):
            parsed = parse_color(value)
            if key == 'lc':
                result[symbol_lcol] = parsed
            else:
                result[symbol_fcol] = parsed
        elif key == 'lt':
            result[symbol_lthk] = float(value.strip())
        elif key == 'sz':
            result[symbol_size] = float(value.strip())
        elif key == 'u':
            result[symbol_u] = float(value)
        elif key == 'r':
            result[symbol_rot] = float(value)
                        
    return result

if __name__ == "__main__":    
    print(parse_symbol_string('<:lc(c)fc(k)'))
    print(parse_symbol_string('+:lc(g)'))
    print(parse_symbol_string('+'))
    # {'symbol': 'plus', 'line_color': 'black', 'fill_color': 'red', 'line_thickness': 0.001, 'size': 0.05}
    
    print(parse_symbol_string('*8:lc(g)fc(k)lt(0.003)'))
    # {'symbol': 'star_8', 'line_color': 'g', 'fill_color': 'k', 'line_thickness': 0.003, 'size': 0.05}
    
    print(parse_symbol_string('D:sz(0.06)fc(123,200,45)'))
    # {'symbol': 'diamond', 'line_color': 'black', 'fill_color': '123,200,45', 'line_thickness': 0.001, 'size': 0.06}
    