
'''
    devps.py
    
    # setlinejoin   : 0, 1, 2
    # setlinewidth
    newpath
    #1 #2 moveto
    #1 #2 lineto
    
    closepath : don need that start pnt
    stroke
    
    #1 #2 #3 setrgbcolor : 0-1, 0-1, 0-1 
    
    
    newpath
    moveto
    lineto
    rmoveto
    rlineto
    closepath
    stroke
    fill
    
    [] 0 setdash
    
    setlinewidth
    setrgbcolor
    setgray
    setlinejoin
    setlinecap
    
    
    Ex 1. fill a square with one color and stroke with another
        newpath
        144 144 moveto
        144 0 rlineto
        0 144 rlineto
        -144 0 rlineto
        closepath
        gsave
        1 0 0 setrgbcolor
        fill
        grestore
        0 setgray
        stroke
    
'''

from . import device
from . import color
from . import linepat
from . import patline

_PS_HEADER = ""
_EPS_HEADER = "%%!PS-Adobe-3.0 EPSF-3.0\n%%%%BoundingBox: %d %d %d %d"
_
_PS_LINE = "/L0 { newpath moveto lineto "
_PS_LINE_DASH = "L1 { newpath "
_PS_POLYGON = ""

class DevicePS(device.DeviceVector):
    def __init__(self):
        pass
    
        
    
    