'''
    drawarrowhead.py
'''

_ARROW_HEAD_TYPE_OPEN         = 0x0001
_ARROW_HEAD_TYPE_CLOSED       = 0x0002
_ARROW_HEAD_TYPE_VIKING       = 0x0003
_ARROW_DIR_LEFT               = 0x0004
_ARROW_DIR_RIGHT              = 0x0005

def draw_arrow_head(dev, 
                    head_type, 
                    f_col,
                    direction, 
                    lcol, lthk, fcol, 
                    xs_l, ys_l, 
                    xs_r, ys_r, 
                    xs_vl, ys_vl, 
                    xs_vr, ys_vr):   
 
    if head_type == _ARROW_HEAD_TYPE_VIKING:
        
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
   
        if direction == _ARROW_DIR_LEFT:
            dev.lpolygon(xs_l, ys_l, lcol=lcol, lthk=lthk, fcol=f_col)
            
        elif direction == _ARROW_DIR_RIGHT:
            dev.lpolygon(xs_r, ys_r, lcol=lcol, lthk=lthk, fcol=f_col)
    
    