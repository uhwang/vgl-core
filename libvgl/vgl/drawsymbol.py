'''
    draw symbol
    05-06-2025
    Star symbol: "*n:u"
                n = 3, 4, 5, ...
                u = (0, Inf) Ex: 0.1, 0.3, 0.4, 0.5, 1.0, 
                "*5:0.2", "*7:0.7"
    Plus/Cross : "+:0.5", "x:0.3", ...
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
    param_u = None
    sym_str.replace(' ','')

    if not sym_str in symbol.symbol_string:
        if ':' in sym_str:
            if re.search(r"\*\d", sym_str):
                nu = sym_str.split(':')
                nvert = int(nu[0][1:])
                if len(nu) > 1: # param_u exist
                    if re.match(r'^[-+]?(\d+(\.\d*)?|\.\d+)$', nu[1]):
                        param_u = float(nu[1])
                star_symbol = True
                sym_str = nu[0][0:1]
            else:
                nu = sym_str.split(':')
                sym_str = nu[0]
                if len(nu) > 1: 
                    if re.match(r'^[-+]?(\d+(\.\d*)?|\.\d+)$', nu[1]):
                        param_u = float(nu[1])
        else:
            print('Error: invalid symbol')
            return
    
    symbol_name = symbol.get_symbol_name[sym_str]
    sym_obj = symbol.stock_symbol[symbol_name]
    sym_obj.hgt = dev.frm.hgt()
    sym_obj.size = size
    if param_u is not None: 
        sym_obj.param_u = param_u

    sym_obj.update(0,0)
    
    # in case lpolygon, reverse y coord
    sym_obj.vertex[1::2] *= -1
    
    if deg != 0:
        sym_obj.rotate(deg)
    xss, yss = sym_obj.update_xy(dev._x_viewport(x),dev._y_viewport(y))
    
    # the shape of symbols is deformed under dev.polygon
    # the shape will be shrinked in x direction if the limits 
    # of x axis is bigger than y limit
    
    #dev.polygon(xss, yss, lcol, lthk, lpat, fcol)
    
    dev.lpolygon(xss, yss, lcol, lthk, lpat, fcol)

    
    
    
    