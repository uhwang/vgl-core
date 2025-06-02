'''
    draw symbol
    05-06-2025
    Star symbol: "*n:u"
                n = 3, 4, 5, ...
                u = (0, Inf) Ex: 0.1, 0.3, 0.4, 0.5, 1.0, 
                "*5:0.2", "*7:0.7"
    Plus/Cross : "+:0.5", "x:0.3", ...
'''
'''
    drawsymbol.py
    
    
'''

import re
from . import symbol
from . import linepat
from . import color
from . import parsesymbol

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
    param_u, deg, star_symbol = None, None, False
    res = parsesymbol.parse_symbol_string(sym_str)
    name  = res[parsesymbol.symbol_name]
    lcol_ = res[parsesymbol.symbol_lcol]
    lthk_ = res[parsesymbol.symbol_lthk]
    fcol_ = res[parsesymbol.symbol_fcol]
    size_ = res[parsesymbol.symbol_size]
    u_    = res[parsesymbol.symbol_u]
    r_    = res[parsesymbol.symbol_rot]
    
    s_lcol, s_lthk, s_fcol, s_size = lcol_, lthk_, fcol_, size_
    
    if lcol is not None:
        s_lcol = parsesymbol.parse_color(lcol)

    if lthk is not None:
        s_lthk = lthk
        
    if fcol is not None:
        s_fcol = parsesymbol.parse_color(fcol)
        
    if u_ is not None:
        param_u = u_
     
    if r_ is not None:
        deg = r_
        
    hgt = dev.frm.hgt()
    match = re.search(r"\*(\d+)", name)
    if match:
        star_symbol = True
        nvert = int(match.group(1))
        
    if star_symbol:
        sym_obj = symbol.Star(size, hgt, nvert=nvert)
    else:
        #symbol_name = symbol.get_symbol_name[name]
        #sym_obj = symbol.stock_symbol[symbol_name]
        sym_obj = symbol.stock_symbol[name]
        
    sym_obj.hgt = hgt
    sym_obj.size = size if size is not None else size_
    if param_u is not None: 
        sym_obj.param_u = param_u

    sym_obj.update(0,0) 
    # in case lpolygon, reverse y coord
    sym_obj.vertex[1::2] *= -1    
    xss, yss = sym_obj.update_xy(dev._x_viewport(x),dev._y_viewport(y))
    dev.lpolygon(xss, yss, s_lcol, s_lthk, lpat, s_fcol)
        
    '''
    param_u = None
    sym_str.replace(' ','')
    star_symbol = None
    if not sym_str in symbol.symbol_string:
        match = re.search(r"\*(\d+)", sym_str)
        if match:
            star_symbol = True
            nvert = int(match.group(1))
            
            if ':' in sym_str:
                nu = sym_str.split(':')
                if len(nu) > 1: # param_u exist
                    if re.match(r'^[-+]?(\d+(\.\d*)?|\.\d+)$', nu[1]):
                        param_u = float(nu[1])
        else:
            print('Error: invalid symbol')
            return
    hgt = dev.frm.hgt()
    
    if star_symbol is not None:
        sym_obj = symbol.Star(size, hgt, nvert=nvert)
    else:
        symbol_name = symbol.get_symbol_name[sym_str]
        sym_obj = symbol.stock_symbol[symbol_name]
    
    sym_obj.hgt = hgt
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
    '''
    #print(lcol, lthk, lpat, fcol)


    
    
    
    