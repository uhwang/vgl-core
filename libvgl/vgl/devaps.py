
'''
    devaps.py 
    
    device Adobe Postscript
'''
import numpy as np

from . import device
from . import color
from . import linepat
from . import patline
from . import drvaps
from . import devval

class DeviceAPS(device.DeviceVector):
    def __init__(
        self,
        fname,
        gbox, 
        size=(8.5,11.0), 
        dev_type = devval.DEV_PS, 
        layout_dir=devval.layout_dir_portrait):
        
        super().__init__()
        self.dev = drvps.PSDrive(fname, gbox, size[0], size[1],
                                 dev_type, layout_dir)
        self.pen = False

    def close(self):
        self.dev.Close()
        
    def set_device(self, frm, extend=device._FIT_NONE):
        self.frm = frm
        self.set_plot(frm,extend)        
    
    def make_pen(self, lcol, lthk, lpat = linepat._PAT_SOLID):
        self.dev.MakePen(lcol, lthk, lpat)
        self.pen = True
    
    def delete_pen(self):
        self.dev.DeletePen()
        self.pen = False
        
    def _line(self, sx, sy, ex, ey, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, viewport=False):
        _lthk = lthk
        if not self.pen:
            _lthk = lthk*self.frm.hgt()
        self.dev.Line(self, sx, sy, ex, ey, lcol, _lthk, lpat, viewport)
        
    def _moveto(self, x, y, viewport=False):
        self.dev.MoveTo(self, x, y, viewport)

    def _lineto(self, x, y, viewport=False):
        self.dev.LineTo(self, x, y, viewport)
        
    def moveto(self, x, y):
        self._moveto(x,y,False)
        
    def lmoveto(self, x, y):
        self._moveto(x,y,True)
        
    def lineto(self, x, y):
        self._lineto(x,y,False)

    def llineto(self, x, y):
        self._lineto(x,y,True)
        
    def lline(self, x1, y1, x2, y2, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID):
        self._line(x1, y1, x2, y2, lcol, lthk, lpat, True)
        
    def line(self, x1, y1, x2, y2, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID):
        self._line(x1, y1, x2, y2, lcol, lthk, lpat, False)
        
    def polyline(self, x, y, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, closed=False):
        _lthk = lthk
        if not self.pen:
            _lthk = lthk*self.frm.hgt()
        self.dev.Polyline(self, x, y, lcol, _lthk, lpat, None, closed, False)
        
    def lpolyline(self, x, y, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, closed=False):
        _lthk = lthk
        if not self.pen:
            _lthk = lthk*self.frm.hgt()
        self.dev.Polyline(self, x, y, lcol, _lthk, lpat, None, closed, True)
        
    def polygon(self, x, y, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, fcol=None):
        _lthk = lthk
        if not self.pen:
            _lthk = lthk*self.frm.hgt()
        self.dev.Polyline(self, x, y, lcol, _lthk, lpat, fcol, True, False)
    
    def lpolygon(self, x, y, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, fcol=None):
        _lthk = lthk
        if not self.pen:
            _lthk = lthk*self.frm.hgt()
        self.dev.Polyline(self, x, y, lcol, _lthk, lpat, fcol, True, True)
        
    def symbol(self, x,y,sym,draw=False):
        cx = self._x_viewport(x)
        cy = self._y_viewport(y)
        px, py = sym.update_xy(cx,cy)
        self.dev.Polyline(self, px, py, sym.lcol, sym.lthk, linepat._PAT_SOLID, 
        sym.fcol if sym.fill else None, True, True)
    
    def circle(self, x,y, rad, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, fcol=None):
        if not self.pen:
            _lthk = lthk*self.frm.hgt()
        rrad = np.linspace(0, np.pi*2, self._circle_point)
        x1 = x+rad*np.cos(rrad)
        y1 = y+rad*np.sin(rrad)
        self.dev.Polyline(self, x1, y1, lcol, _lthk, lpat, fcol, True, False)
