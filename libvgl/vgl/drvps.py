'''

    drvps.py
    
    3/8/24
    
    1 inch = 72 points.

'''

from . import paper
from . import color
from . import linepat
from . import gdiobj
from . import devval

_PS_HEADER = [
    "%!PS-Adobe-3.0 EPSF-3.0\n",
    "%%BeginProlog\n",
    "%%EndProlog\n",
]

_EPS_HEADER = "%%BoundingBox: %d %d %d %d\n"
_PS_SCALE_INCH = "72 72 scale\n"
_PS_SET_COORD_UPLEFT = "0 %3.4f translate\n1 -1 scale\n"
_END = "%%EOF"

_ps_points_inch = 72

class PSDrive():
    def __init__(
        self, 
        fname,
        gbbox, 
        wid, 
        hgt, 
        dev_type = devval.DEV_PS, 
        layout_dir=paper.paper_dir_portrait):
        
        try:
            self.fp = open(fname, "wt")
        except OSError as e:
            print(str(e))
            raise
            
        self.fp.write(_PS_HEADER[0])
        if dev_type == devval.DEV_EPS:
            self.fp.write(_EPS_HEADER%(gbbox.sx,
                                       gbbox.sy,
                                       gbbox.wid(),
                                       gbbox.hgt()))        
            
        self.fp.write(_PS_HEADER[1])
        self.fp.write(_PS_HEADER[2])
        self.fp.write(_PS_SCALE_INCH)
        self.fp.write(_PS_SET_COORD_UPLEFT%hgt)
        self.closed = False
        
    def MakePen(self, lcol, lthk, lpat):
        self.pen = gdiobj.PSPen(lcol, lthk, lpat)
        
    def DeletePen(self):
        lc = color.normalize(self.pen.lcol)
        self.fp.write("newpath\n")
        for s in self.pen.stream:
            self.fp.write(s)
        self.fp.write("closepath\n")
        self.fp.write("%1.4f %1.4f %1.4f setrgbcolor\n"
                      "%1.4f setlinewidth\n"
                      "stroke\n"%(lc.r, lc.g, lc.b, self.pen.lthk))
        self.pen = None
    
    def MoveTo(self, dev, x, y):
        self.pen.stream = "%3.4f %3.4f m\n"%\
                       (x if viewport else dev._x_viewport(x), 
                        y if viewport else dev._y_viewport(y))
    
    def LineTo(self, dev, x, y):
        self.pen.stream = "%3.4f %3.4f l\n"%\
                       (x if viewport else dev._x_viewport(x), 
                        y if viewport else dev._y_viewport(y))
    
    def Line(self, dev, sx, sy, ex, ey, lcol, lthk, lpat, viewport=False):
        self.Polyline(dev, [sx, ex], [sy, ey], lcol, lthk, lpat, None, False, viewport)
        
    def Polyline(self, dev, x, y, lcol, lthk, lpat, fcol, closed=False, viewport=False):
        
        pat_inst = isinstance(lpat, linepat.LinePattern)
        
        self.fp.write("newpath\n%3.4f %3.4f moveto\n"%\
                       (x[0] if viewport else dev._x_viewport(x[0]),
                        y[0] if viewport else dev._y_viewport(y[0])))
                        
        for x1, y1 in zip(x[1:], y[1:]):
            self.fp.write("%3.4f %3.4f lineto\n"%\
                       (x1 if viewport else dev._x_viewport(x1), 
                        y1 if viewport else dev._y_viewport(y1)))
        
        if closed:
            self.fp.write("closepath\n")
            
        if fcol and lcol:
            self.fp.write("gsave\n")

        if fcol:
            fc = color.normalize(fcol)
            self.fp.write("%1.4f %1.4f %1.4f setrgbcolor\nfill\n"%(fc.r, fc.g, fc.b))

        if lcol:
            lc = color.normalize(lcol)
            if fcol: self.fp.write("grestore\n")
            
            if pat_inst:
                if lpat.pat_t == _PAT_SOLID:
                    self.fp.write("[] 0 setdash\n")
                else:
                    pat_info = patline._get_pattern_info(lpat_t)
                    pat_mul = lpat.pat_len*lpat.pat_t*_ps_ps_points_inch*dev.frm.hgt()
    
                    if lpat.pat_t == _PAT_DASHE:
                        self.fp.write("[%d] 0 setdash\n"%pat_info[1][0]*pat_mul)
                    else:
                        self.fp.write("[");
                        for p in pat_info[1]:
                            welf.write("%d "% p*pat_mul)
                        self.fp.write("] 0 setdash\n")
                    
            self.fp.write("%1.4f %1.4f %1.4f setrgbcolor\n"
                          "%1.4f setlinewidth\n"
                          "stroke\n"%(lc.r, lc.g, lc.b, lthk))

    def Polygon(self, x, y, lcol, lthk, lpat, fcol):
        self.Polyline(x,y,lcol,lthk,lpat,fcol,True,False)
        
    def Close(self):
        if not self.closed:
            self.fp.write(_END)
            self.fp.close()
            self.closed = True