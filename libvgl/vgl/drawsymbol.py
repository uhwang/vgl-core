'''
    draw symbol
    05-06-2025
    Star symbol: "*n:u"
                n = 3, 4, 5, ...
                u = (0, Inf) Ex: 0.1, 0.3, 0.4, 0.5, 1.0, 
                "*5:0.2", "*7:0.7"
'''
import re
from . import symbol
from . import linepat
from . import color

def draw_symbol(dev, 
                x, 
                y, 
                sym_str,
                size,
                deg,
                lcol,
                lthk,
                lpat,
                fcol):
    star_symbol=False
    if not sym_str in symbol.symbol_string:
        sym_str.replace(' ','')
        if re.search(r"\*\d", sym_str):
            param_u = None
            nu = sym_str.split(':')
            nvert = int(nu[0][1:])
            if ':' in sym_str: 
                param_u = float(nu[1])
            star_symbol = True
        else:    
            print('Error: invalid symbol')
            return
    
    if star_symbol:
        sym_obj = symbol.Star(size, dev.frm.hgt(), nvert, param_u=param_u)
    else:
        symbol_name = symbol.get_symbol_name[sym_str]
        sym_obj = symbol.stock_symbol[symbol_name]
        sym_obj.hgt = dev.frm.hgt()
        sym_obj.size = size

    sym_obj.update(0,0)
    if deg != 0:
        sym_obj.rotate(deg)
    xss, yss = sym_obj.update_xy(x,y)
    dev.polygon(xss, yss, lcol, lthk, lpat, fcol)

    
    
    
    