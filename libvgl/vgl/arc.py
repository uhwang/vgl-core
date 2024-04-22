'''
arc.py

4/20/2024

'''
import numpy as np

from . import util
from . import color
from . import linepat

def _arc(dev,
         xc           ,  # the x coord of the center
         yc           ,  # the y coord of the center
         radius       ,  # radius of the Arc
         start_angle  ,  # (degree)
         end_angle    ,  # (degree)
         line_in      ,  # Draw line from center to start/end pnt (T/F)
         lcol_in      ,  # line color
         lthk_in      ,  # line thickness
         lpat_in      ,  # line pattern
         line_out     ,  # Draw perimeter (T/F)
         lcol_out     ,  # line color
         lthk_out     ,  # line thickness
         lpat_out     ,  # line pattern perimeter
         fcol         ,  # fill color (Color obj or None:default)
         viewport     ,
         ):
    
    ang1_rad = util.deg_to_rad(start_angle)
    ang2_rad = util.deg_to_rad(end_angle)
    
    ang3 = np.linspace(ang1_rad, ang2_rad, dev._circle_point, endpoint=True)
    xx = xc + radius*np.cos(ang3) 
    yy = yc + radius*np.sin(ang3) 
    
    if isinstance(fcol, color.Color):
        if viewport:
            dev.lpolygon(xx,yy,lcol=None,fcol=fcol)
        else:
            dev.polygon(xx,yy,lcol=None,fcol=fcol)
    
    if line_in:
        xx1 = [xx[0], xc, xx[-1]]
        yy1 = [yy[0], yc, yy[-1]]
        if viewport:
            dev.lpolyline(xx1,yy1,lcol_in,lthk_in,lpat_in)
        else:
            dev.polyline(xx1,yy1,lcol_in,lthk_in,lpat_in)
            
    if line_out:
        if viewport:
            dev.lpolyline(xx,yy,lcol_out,lthk_out,lpat_out)
        else:
            dev.polyline(xx,yy,lcol_out,lthk_out,lpat_out)
        
def arc(dev,
        xc            = 0,            # the x coord of the center
        yc            = 0,            # the y coord of the center
        radius        = 1,            # radius of the Arc
        start_angle   = 0,            # (degree)
        end_angle     = 45,           # (degree)
        line_in       = False,        # Draw line from center to start/end pnt (T/F)
        lcol_in       = color.BLACK , # line color
        lthk_in       = 0.001,        # line thickness
        lpat_in       = linepat._PAT_SOLID, # line pattern ()
                                            # _PAT_SOLID is string, others are class obj
        line_out      = True,         # Draw perimeter (T/F)
        lcol_out      = color.BLACK , # line color
        lthk_out      = 0.001,        # line thickness
        lpat_out      = linepat._PAT_SOLID, # line pattern perimeter
                                            # _PAT_SOLID is string, others are class obj
        fcol          = None          # fill color
        ):
            
    _arc(
        dev,
        xc,
        yc,
        radius,
        start_angle,
        end_angle,
        line_in,
        lcol_in,
        lthk_in,
        lpat_in,
        line_out,
        lcol_out,
        lthk_out,
        lpat_out,
        fcol,
        viewport = False)
            
def arc(dev,
        xc            = 0,            # the x coord of the center
        yc            = 0,            # the y coord of the center
        radius        = 1,            # radius of the Arc
        start_angle   = 0,            # (degree)
        end_angle     = 45,           # (degree)
        line_in       = False,        # Draw line from center to start/end pnt (T/F)
        lcol_in       = color.BLACK , # line color
        lthk_in       = 0.001,        # line thickness
        lpat_in       = linepat._PAT_SOLID, # line pattern ()
                                            # _PAT_SOLID is string, others are class obj
        line_out      = True,         # Draw perimeter (T/F)
        lcol_out      = color.BLACK , # line color
        lthk_out      = 0.001,        # line thickness
        lpat_out      = linepat._PAT_SOLID, # line pattern perimeter
                                            # _PAT_SOLID is string, others are class obj
        fcol          = None          # fill color
        ):
            
    _arc(dev,
         xc,
         yc,
         radius,
         start_angle,
         end_angle,
         line_in,
         line_out,
         lcol_in,
         lthk_in,
         lcol_out,
         lthk_out,
         lpat_in,
         lpat_out,
         fcol,
         viewport = True)            