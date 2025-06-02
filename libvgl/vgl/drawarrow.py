'''
    draw arrow
    05-06-2025

    Arrow style
        OPEN           '->'   or '<-'   or '<->'
        CLOSED         '-|>'  or '<|-'  or '<|-|>'
        CLOSEDFILLED   '-|>f' or '<|-f' or '<|-|>f'
        CLOSEDBLANK    '-|>b' or '<|-b' or '<|-|>b'
        VIKING         '->>'  or '<<-'  or '<<->>' 
        VIKINGFILLED   '->>f' or '<<-f' or '<<->>f' 
        VIKINGBLANK    '->>b' or '<<-b' or '<<->>b' 
        
        
        
'''
import re
import numpy as np
from . import util
from . import color
from . import parsearrow
from . import drawarrowhead

_ARROW_HEAD_ANGLE    = 15   # degree
_ARROW_HEAD_LENGTH_0 = 0.01 # 
_ARROW_HEAD_LENGTH_1 = 0.05 # 
_VIKING_XPOS_SCALE   = 0.7

def draw_arrow(dev, sx, sy, ex, ey, style, size, lcol, lthk, lpat, fcol):
    
    style.replace(' ','')
    style.lower()
    
    # find arrow head wing pos in local coord
    wing = size*dev.frm.hgt()
    wing_x = wing*np.cos(util.deg_to_rad(_ARROW_HEAD_ANGLE))
    wing_y = wing*np.sin(util.deg_to_rad(_ARROW_HEAD_ANGLE))
    vk_x   = wing_x*_VIKING_XPOS_SCALE
    vk_y   = 0
    theta = np.arctan2(ey-sy, ex-sx)
    if theta < 0:
        theta += np.pi*2
    
    # Left: (0,0)<
    left_wing_up = util.rad_rotation(-wing_x, wing_y, -theta)
    left_wing_dn = util.rad_rotation(-wing_x,-wing_y, -theta)
    left_vk      = util.rad_rotation(-vk_x  , 0, -theta)
    
    # Right: >(0,0)
    right_wing_up = util.rad_rotation(wing_x, wing_y, -theta)
    right_wing_dn = util.rad_rotation(wing_x,-wing_y, -theta)
    right_vk      = util.rad_rotation(vk_x  , 0, -theta)
    
    sx_ = dev._x_viewport(sx)
    sy_ = dev._y_viewport(sy)
    ex_ = dev._x_viewport(ex)
    ey_ = dev._y_viewport(ey)
    
    xs_open_right = np.array([ex_+left_wing_up[0], ex_, ex_+left_wing_dn[0], ex_+left_wing_up[0]])
    ys_open_right = np.array([ey_+left_wing_up[1], ey_, ey_+left_wing_dn[1], ey_+left_wing_up[1]])

    xs_open_left = np.array([sx_+right_wing_up[0], sx_, sx_+right_wing_dn[0], sx_+right_wing_up[0]])
    ys_open_left = np.array([sy_+right_wing_up[1], sy_, sy_+right_wing_dn[1], sy_+right_wing_up[1]])

    xs_vk_right = np.array([ex_+left_wing_up[0], ex_, ex_+left_wing_dn[0], ex_+left_vk[0], ex_+left_wing_up[0]])
    ys_vk_right = np.array([ey_+left_wing_up[1], ey_, ey_+left_wing_dn[1], ey_+left_vk[1], ey_+left_wing_up[1]])
    
    xs_vk_left= np.array([sx_+right_wing_up[0], sx_, sx_+right_wing_dn[0], sx_+right_vk[0], sx_+right_wing_up[0]])
    ys_vk_left= np.array([sy_+right_wing_up[1], sy_, sy_+right_wing_dn[1], sy_+right_vk[1], sy_+right_wing_up[1]])

    try:
        p = parsearrow.parse_arrow_pattern(style)
    except Exception as e:
        print(e)
        return
        
    p_l = p.get("left_head")
    p_r = p.get("right_head")
    p_b = p.get("body")
    p_f = p.get("fill")    
    p_fl= p.get("left_fill")    
    p_fr= p.get("right_fill")
    p_lp= p.get("lpat")
    
    def render_head(h_type):
        if   "open"   in h_type: return drawarrowhead._ARROW_HEAD_TYPE_OPEN
        elif "closed" in h_type: return drawarrowhead._ARROW_HEAD_TYPE_CLOSED
        elif "viking" in h_type: return drawarrowhead._ARROW_HEAD_TYPE_VIKING
        
    def color_value(c):
        if c.find(',') >= 0: 
            c_ = c.split(',')
            return color.Color(int(c_[0]), int(c_[1]), int(c_[2]))
        else:
            return color.default_color[c]
            
    def render_color(p):
        p_f, p_lf, p_rf = p.get("fill"), p.get("left_fill"), p.get("right_fill")
        
        if p_f:
            f_col = p_f["color"]
            return color_value(f_col), None, None
        else:
            return None, color_value(p_lf), color_value(p_rf)

    f_col, fl_col, fr_col, lpat_ = None, None, None, None
    if p_f or p_fl or p_fr:
        f_col, fl_col, fr_col = render_color(p)
    
    if p_b:
        if p_lp is not None: lpat = p_lp
        dev.line(sx, sy, ex, ey, lcol, lthk, lpat)

    if p_l:
        drawarrowhead.draw_arrow_head(
                        dev,
                        render_head(p_l['type']),
                        f_col if f_col else fl_col,
                        drawarrowhead._ARROW_DIR_LEFT, 
                        lcol, lthk, fcol,
                        xs_open_left, 
                        ys_open_left, 
                        xs_open_right, 
                        ys_open_right, 
                        xs_vk_left,
                        ys_vk_left,
                        xs_vk_right,
                        ys_vk_right)
    
    if p_r:
        drawarrowhead.draw_arrow_head(
                        dev, 
                        render_head(p_r['type']),
                        f_col if f_col else fr_col,
                        drawarrowhead._ARROW_DIR_RIGHT, 
                        lcol, lthk, fcol,
                        xs_open_left, 
                        ys_open_left, 
                        xs_open_right, 
                        ys_open_right, 
                        xs_vk_left,
                        ys_vk_left,
                        xs_vk_right,
                        ys_vk_right)
                        
