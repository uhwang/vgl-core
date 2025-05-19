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

_find_rgb = re.compile("(\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})")

def get_color(c):
    c1 = _find_rgb.search(c)
    
    if c1:
        r = int(c1.group(1))
        g = int(c1.group(2))
        b = int(c1.group(3))
    else:
        i1_c = c.find('(')
        i2_c = c.find(')')
        if i1_c >= 0 and i2_c >= 0:
            c_name = c[i1_c+1:i2_c]
            return color.default_color[c_name]
        else:
            return None
        
    try:
        assert 0 <= r <=255    
        assert 0 <= g <=255
        assert 0 <= b <=255
    except Exception as e:
        return None
    return color.Color(r, g, b)
    
STYLE_OPEN_RIGHT = '->'
STYLE_OPEN_LEFT  = '<-'
STYLE_OPEN       = '<->'

# Filled or Blank : f or b
#   '-|>'           : arrow body line inside arrow head
#   '-|>b'          : no line inside arrow head
#   '-|>f'          : fill the arrow head w/ line color
#   '-|>f(10,55,1)' : fill the arrow head w/ given color
STYLE_CLOSED_RIGHT = '-|>'   
STYLE_CLOSED_LEFT  = '<|-'
STYLE_CLOSED       = '<|-|>'

STYLE_CLOSEDBLANK_LEFT  = '<|-'
STYLE_CLOSEDBLANK_RIGHT = '-|>'
STYLE_CLOSEDBLANK       = '<|-|>'

STYLE_VIKING_RIGHT = '->>'
STYLE_VIKING_LEFT  = '<<-'
STYLE_VIKING       = '<<->>' 


STYLE_OPEN_STRING   = [STYLE_OPEN_LEFT  , STYLE_OPEN_RIGHT  , STYLE_OPEN]
STYLE_CLOSED_STRING = [STYLE_CLOSED_LEFT, STYLE_CLOSED_RIGHT, STYLE_CLOSED]
STYLE_VIKING_STRING = [STYLE_VIKING_LEFT, STYLE_VIKING_RIGHT, STYLE_VIKING]

_ARROW_HEAD_ANGLE    = 15   # degree
_ARROW_HEAD_LENGTH_0 = 0.01 # 
_ARROW_HEAD_LENGTH_1 = 0.05 # 
_VIKING_XPOS_SCALE   = 0.7

_ARROW_HEAD_TYPE_OPEN         = 0x0001
_ARROW_HEAD_TYPE_CLOSED       = 0x0002
_ARROW_HEAD_TYPE_VIKING       = 0x0003
_ARROW_DIR_LEFT               = 0x0004
_ARROW_DIR_RIGHT              = 0x0005

def find_arrow_type(style):
    
    head_lt, line_, head_rt = None, None, None
    i, s, s_len = 0, style, len(style)
    
    try:
        while i < s_len:
            if s[i] == '<':
                head_lt = _ARROW_HEAD_TYPE_OPEN
                if i+1 >= s_len: break
                if s[i+1] == '<':
                    head_lt = _ARROW_HEAD_TYPE_VIKING
                    i += 1
                elif s[i+1] == '|':
                    head_lt =_ARROW_HEAD_TYPE_CLOSED
                    i += 1
            elif s[i] == '-':
                line_ = True
            elif s[i] == '|':
                if i+1 >= s_len: break
                if s[i+1] == '>':
                    head_rt = _ARROW_HEAD_TYPE_CLOSED
                    i += 1
                else:
                    print('Error (find_arrow_type @ drawarrow.py): invalid right arrow headtype')
                    return head_lt, line_, head_rt
            elif s[i] == '>':
                head_rt = _ARROW_HEAD_TYPE_OPEN
                if i+1 >= s_len: break
                if s[i+1] == '>':
                    head_rt = _ARROW_HEAD_TYPE_VIKING
                    i += 1
            i += 1
    except Exception as e:
        print('Error (find_arrow_type @ drawarrow.py): %s'%str(e))
        head_lt, line_, head_rt = None, None, None
        
    return head_lt, line_, head_rt

def draw_arrow_head(dev, head_type, direction, lcol, lthk, fcol, xs_l, ys_l, xs_r, ys_r, xs_vl, ys_vl, xs_vr, ys_vr, style):   
 
    if head_type == _ARROW_HEAD_TYPE_VIKING:
        f_col = get_color(style)
           
        # Closed blank head + Fill head w/ given color or line color + No line in head
        if f_col is None and style.find('bf') >= 0:
            f_col = color.WHITE
            
        # Closed blank head + No line in head
        elif f_col is None and style.find('b') >= 0:
            f_col = color.WHITE
            
        # Closed blank head + fill head w/ given color or line color + arrow line in head
        elif f_col is None and style.find('f') >= 0:
            f_col = color.WHITE

        if direction == _ARROW_DIR_LEFT:
            dev.lpolygon(xs_vl, ys_vl, lcol=lcol, lthk=lthk, fcol=f_col)
            
        elif direction == _ARROW_DIR_RIGHT:
            dev.lpolygon(xs_vr, ys_vr, lcol=lcol, lthk=lthk, fcol=f_col)
                
    # Arrow style open
    elif head_type == _ARROW_HEAD_TYPE_OPEN:
        
        if direction == _ARROW_DIR_LEFT:
        
            # draw left arrow head
            dev.lpolyline(xs_l[:-1], ys_l[:-1], lcol=lcol, lthk=lthk)
        
        elif direction == _ARROW_DIR_RIGHT:
            
            # draw left arrow head
            dev.lpolyline(xs_r[:-1], ys_r[:-1], lcol=lcol, lthk=lthk)
            
    # Arrow style closed
    elif head_type == _ARROW_HEAD_TYPE_CLOSED:
        f_col = get_color(style)
    
        # Closed blank head + Fill head w/ given color or line color + No line in head
        if style.find('bf') >= 0:
            if f_col is None:
                f_col = color.WHITE
            
        # Closed blank head + No line in head
        elif f_col is None and style.find('b') >= 0:
            f_col = color.WHITE
            
        # Closed blank head + fill head w/ given color or line color + arrow line in head
        elif f_col is None and style.find('f') >= 0:
            f_col = color.WHITE
   
        if direction == _ARROW_DIR_LEFT:
            dev.lpolygon(xs_l, ys_l, lcol=lcol, lthk=lthk, fcol=f_col)
            
        elif direction == _ARROW_DIR_RIGHT:
            dev.lpolygon(xs_r, ys_r, lcol=lcol, lthk=lthk, fcol=f_col)
    
    
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

    htype_l, line_, htype_r = find_arrow_type(style)
        
    if line_:
        dev.line(sx, sy, ex, ey, lcol, lthk, lpat)
 
    if htype_l:
        draw_arrow_head(dev,
                        htype_l, 
                        _ARROW_DIR_LEFT, 
                        lcol, lthk, fcol,
                        xs_open_left, 
                        ys_open_left, 
                        xs_open_right, 
                        ys_open_right, 
                        xs_vk_left,
                        ys_vk_left,
                        xs_vk_right,
                        ys_vk_right,
                        style)

    if htype_r:
        draw_arrow_head(dev, 
                        htype_r, 
                        _ARROW_DIR_RIGHT, 
                        lcol, lthk, fcol,
                        xs_open_left, 
                        ys_open_left, 
                        xs_open_right, 
                        ys_open_right, 
                        xs_vk_left,
                        ys_vk_left,
                        xs_vk_right,
                        ys_vk_right,
                        style)
                        
    '''
    if any(sub in style for sub in STYLE_VIKING_STRING):
        f_col = get_color(style)
        print('viking')
        if style.find('-'):
            # draw arrow body line
            dev.line(sx, sy, ex, ey, lcol, lthk, lpat)
            
        # Closed blank head + Fill head w/ given color or line color + No line in head
        if style.find('bf') >= 0:
            if f_col is None:
                f_col = color.WHITE
            
        # Closed blank head + No line in head
        elif style.find('b') >= 0:
            f_col = color.WHITE
            
        # Closed blank head + fill head w/ given color or line color + arrow line in head
        elif style.find('f') >= 0:
            if f_col is None:
                f_col = color.WHITE
            
        if re.search(re.escape(STYLE_VIKING), style):
            dev.lpolygon(xs_vk_left , ys_vk_left, lcol=lcol, lthk=lthk, fcol=f_col)
            dev.lpolygon(xs_vk_right, ys_vk_right, lcol=lcol, lthk=lthk, fcol=f_col)
            
        elif re.search(re.escape(STYLE_VIKING_LEFT), style):
            dev.lpolygon(xs_vk_left, ys_vk_left, lcol=lcol, lthk=lthk, fcol=f_col)
            
        elif re.search(re.escape(STYLE_VIKING_RIGHT), style):
            dev.lpolygon(xs_vk_right, ys_vk_right, lcol=lcol, lthk=lthk, fcol=f_col)
            
    # Arrow style open
    elif any(sub in style for sub in STYLE_OPEN_STRING):
        if style.find('-'):
            # draw arrow body line
            dev.line(sx, sy, ex, ey, lcol, lthk, lpat)
        
        if style.find(STYLE_OPEN) >= 0:
            
            # draw left arrow head
            dev.lpolyline(xs_open_left[:-1], ys_open_left[:-1], lcol=color.RED, lthk=lthk)
            
            # draw right arrow head
            dev.lpolyline(xs_open_right[:-1], ys_open_right[:-1], lcol=lcol, lthk=lthk)
            
        elif style.find(STYLE_OPEN_LEFT):
           
            # draw left arrow head
            dev.lpolyline(xs_open_left[:-1], ys_open_left[:-1], lcol=color.RED, lthk=lthk)
        
        elif style.find(STYLE_OPEN_RIGHT):
            
            # draw left arrow head
            dev.lpolyline(xs_open_right[:-1], ys_open_right[:-1], lcol=color.RED, lthk=lthk)
            
    # Arrow style closed
    elif any(sub in style for sub in STYLE_CLOSED_STRING):
        f_col = get_color(style)
        
        if style.find('-'):
            # draw arrow body line
            dev.line(sx, sy, ex, ey, lcol, lthk, lpat)
            
        # Closed blank head + Fill head w/ given color or line color + No line in head
        if style.find('bf') >= 0:
            if f_col is None:
                f_col = color.WHITE
            
        # Closed blank head + No line in head
        elif style.find('b') >= 0:
            f_col = color.WHITE
            
        # Closed blank head + fill head w/ given color or line color + arrow line in head
        elif style.find('f') >= 0:
            if f_col is None:
                f_col = color.WHITE
            
        if re.search(re.escape(STYLE_CLOSED), style):
            dev.lpolygon(xs_open_left, ys_open_left, lcol=lcol, lthk=lthk, fcol=f_col)
            dev.lpolygon(xs_open_right, ys_open_right, lcol=lcol, lthk=lthk, fcol=f_col)
            
        elif re.search(re.escape(STYLE_CLOSED_LEFT), style):
            dev.lpolygon(xs_open_left, ys_open_left, lcol=lcol, lthk=lthk, fcol=f_col)
            
        elif re.search(re.escape(STYLE_CLOSED_RIGHT), style):
            dev.lpolygon(xs_open_right, ys_open_right, lcol=lcol, lthk=lthk, fcol=f_col)

        '''
    
    
    
    
    
    
    
    
    