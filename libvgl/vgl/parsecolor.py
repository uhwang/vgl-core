'''
 parse color
 
'''
import re
from . import color
from . import util
from . import colordict

class ColorParseError(Exception):
    pass

hex_color = r"^((?:0x)?[0-9a-fA-F]{2}),((?:0x)?[0-9a-fA-F]{2}),((?:0x)?[0-9a-fA-F]{2})$"
int_color = r'^(\d{1,3}),(\d{1,3}),(\d{1,3})$'
str_color = r'^[a-zA-Z0-9]+$'

def parse_color(s, raw=False, default=None):

    if isinstance(s, color.Color):
        return s
    elif s is None:
        return s
        
    s = s.strip()
    g1 = re.match(int_color, s)
    g2 = re.match(hex_color, s)
    g3 = re.match(str_color, s)
    
    if not s:
        raise ColorParseError("Empty color value")
        
    if g1:
        c_ = (int(g1[1]), int(g1[2]), int(g1[3])) if raw else \
             color.Color(int(g1[1]), int(g1[2]), int(g1[3]))
    elif g2:
        h_r = util.hex_to_int(g1[1])
        h_g = util.hex_to_int(g1[2])
        h_b = util.hex_to_int(g1[3])
        c_  = (h_r, h_g, h_b) if raw else \
               color.Color(h_r,h_g,h_b)
    elif g3:
        c_ = color.default_color.get(s, None)
        if c_ is None:
            c_ = colordict.svg_colors.get(s, None)
            if c_ is None:
                c_ = colordict.turtle_colors.get(s, None)
                if c_ is None:
                    raise ColorParseError(f"Invalid color value {s}")
    else:
        if default is not None: 
            c_ = default
        else: 
            raise ColorParseError(f"Invalid color value {s}")
            
    return c_
