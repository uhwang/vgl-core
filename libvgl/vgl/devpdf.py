'''

    devpdf.py

    03/23/2023  Initial versioin
    12/08/2024  Fix crop & compression
    
'''

import numpy as np
from . import color
from . import device
from . import drvpdf
from . import linepat
from . import patline
from . import devval
from . import drawsymbol
from . import drawarrow
from . import parselinepattern

class DevicePDF(device.DeviceVector):
    def __init__(
            self, 
            fname, 
            gbox, 
            size=(8.5,11.0), 
            pdir = "P",
            crop=False,
            compression=True):
        super().__init__()
        self.gbox =gbox
        self.wid = size[0]        
        self.hgt = size[1]

        if not pdir in "PpLl":
            pdir = devval.layout_dir_portrait
        else:
            pdir = devval.layout_dir_portrait if pdir in "Pp" else\
                   devval.layout_dir_landscape
        
        self.drv = drvpdf.PDFDriver(fname, 
                                    gbox, 
                                    size[0], 
                                    size[1], 
                                    pdir, 
                                    crop,
                                    compression)
        self.pen = False
        self.brush = device.Brush()

    def set_device(self, frm, extend=device._FIT_NONE):
        self.frm = frm
        self.set_plot(frm,extend)

    def stroke(self):
        pass
    def fill_white(self):
        return
        
    def make_pen(self, color, thk):
        self.drv.MakePen(color, thk*drvpdf._points_inch)
        self.pen = True
    
    def delete_pen(self):
        self.drv.DeletePen()
        self.pen = False
        
    def _line(self, sx, sy, ex, ey, lcol=None, lthk=None, lpat=linepat._PAT_SOLID, viewport=False):
        xx = [sx, ex]
        yy = [sy, ey]
            
        if viewport:
            sxp = sx*drvpdf._points_inch
            syp = sy*drvpdf._points_inch
            exp = ex*drvpdf._points_inch
            eyp = ey*drvpdf._points_inch
        else:
            sxp = self._x_viewport(sx)*drvpdf._points_inch
            syp = self._y_viewport(sy)*drvpdf._points_inch
            exp = self._x_viewport(ex)*drvpdf._points_inch
            eyp = self._y_viewport(ey)*drvpdf._points_inch
            
        if isinstance(lpat, linepat.LinePattern) or \
            (lpat is not None and lpat != linepat._PAT_SOLID):
            if isinstance(lpat, str):
                try:
                    p = parselinepattern.parse_line_pattern(lpat)
                    lpat = linepat.LinePattern(p[1], p[0])
                except Exception as e:
                    print(e)
                    return 
                    
            self.polyline(xx,yy,lcol,lthk,lpat,viewport)
        else:
            if self.pen:
                self.drv.MoveTo(sxp, syp)
                self.drv.LineTo(exp, eyp)
            else:
                self.polyline(xx,yy,lcol,lthk,linepat._PAT_SOLID,viewport=viewport)
        
    def _moveto(self, x, y, viewport=False):
        if viewport:
            sxp = x*drvpdf._points_inch, 
            syp = y*drvpdf._points_inch 
        else:
            sxp = self._x_viewport(x)*drvpdf._points_inch, 
            syp = self._y_viewport(y)*drvpdf._points_inch 
        self.drv.MoveTo(sxp, syp)

    def _lineto(self, x, y, viewport=False):
        if viewport:
            sxp = x*drvpdf._points_inch, 
            syp = y*drvpdf._points_inch 
        else:
            sxp = self._x_viewport(x)*drvpdf._points_inch, 
            syp = self._y_viewport(y)*drvpdf._points_inch 
        self.drv.LineTo(sxp, syp)
        
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
        
    # viewport(True) : lpolygon
    # viewport(False) : polygon
    
    def polygon(self, x, y, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, fcol=None, viewport=False):
        pat_inst = isinstance(lpat, linepat.LinePattern) or (lpat is not None and lpat != linepat._PAT_SOLID)

        #if lthk: 
        if not self.pen and lthk:
            _lthk = lthk*self.frm.hgt()*drvpdf._points_inch
            
        if (pat_inst ==False and lcol) or fcol:
            if viewport:
                px = [xx*drvpdf._points_inch for xx in x]
                py = [yy*drvpdf._points_inch for yy in y]
            else:
                px = [self._x_viewport(xx)*drvpdf._points_inch for xx in x]
                py = [self._y_viewport(yy)*drvpdf._points_inch for yy in y]
            if isinstance(lcol, color.Color) and lpat == linepat._PAT_SOLID:
                self.drv.Polygon(px,py,lcol,_lthk,fcol)
            elif fcol:
                self.drv.Polygon(px,py,None,None,fcol)
    
        if lcol and pat_inst:
            if isinstance(lpat, str):
                try:
                    p = parselinepattern.parse_line_pattern(lpat)
                    lpat = linepat.LinePattern(p[1], p[0])
                except Exception as e:
                    print(e)
                    return 
                    
            if isinstance(x, np.ndarray):
                xp = np.append(x, x[0])
                yp = np.append(y, y[0])
            elif isinstance(x, list):
                xp = x.copy()
                yp = y.copy()
                xp.append(x[0])
                yp.append(y[0])
            if viewport:
                pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t, viewport=True)
            else:
                pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t)
            #self.make_pen(lcol, lthk)
            for p1 in pat_seg:
                x2 = [p2[0]*drvpdf._points_inch for p2 in p1 ]
                y2 = [p2[1]*drvpdf._points_inch for p2 in p1 ]
                self.drv.Polyline(x2, y2, lcol, _lthk, fcol=None, closed=False)
            #self.delete_pen()
            
    def begin_symbol(self, sym):
        pass        
    def end_symbol(self):
        pass        
        
    #def symbol(self, x,y,sym,draw=False):
    #    cx = self._x_viewport(x)
    #    cy = self._y_viewport(y)
    #    px, py = sym.update_xy(cx,cy)
    #    ppx = [px1*drvpdf._points_inch for px1 in px]
    #    ppy = [py1*drvpdf._points_inch for py1 in py]
    #    self.drv.Polygon(ppx, ppy, sym.lcol, sym.lthk*drvpdf._points_inch, sym.fcol)
        
    def symbol(self, x,y, sym_str='o', size=0.02, deg=0,lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, fcol=color.RED):
        drawsymbol.draw_symbol(self,x,y,sym_str,size,deg,lcol,lthk,lpat,fcol)

    def arrow(self, sx, sy, ex, ey, style, size=0.02, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, fcol=None):
        drawarrow.draw_arrow(self, sx, sy, ex, ey, style, size, lcol, lthk, lpat, fcol)
            
    def circle(self, x,y, rad, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, fcol=None):
        rrad = np.linspace(0, np.pi*2, self._circle_point)
        x1 = x+rad*np.cos(rrad)
        y1 = y+rad*np.sin(rrad)
        self.polygon(x1, y1, lcol, lthk, lpat, fcol)
        
    def polyline(self, x, y, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, closed=False, viewport=False):
        pat_inst = isinstance(lpat, linepat.LinePattern) or (lpat is not None and lpat != linepat._PAT_SOLID)

        #if lthk: _lthk = lthk*drvpdf._points_inch
        #else: lthk = 0
        if not self.pen:
            _lthk = lthk*self.frm.hgt()*drvpdf._points_inch
            _lcol = lcol
        
        if pat_inst == False and lcol:
            if viewport:
                px = [xx*drvpdf._points_inch for xx in x]
                py = [yy*drvpdf._points_inch for yy in y]
                if closed:
                    px.append(x[0]*drvpdf._points_inch)
                    py.append(y[0]*drvpdf._points_inch)
            else:
                px = [self._x_viewport(xx)*drvpdf._points_inch for xx in x]
                py = [self._y_viewport(yy)*drvpdf._points_inch for yy in y]
                if closed:
                    px.append(self._x_viewport(x[0])*drvpdf._points_inch)
                    py.append(self._y_viewport(y[0])*drvpdf._points_inch)
            self.drv.Polyline(px,py,_lcol,_lthk,fcol=None,closed=False)
    
        #if lcol and pat_inst:
        if not self.pen and lcol and pat_inst:
            if isinstance(lpat, str):
                try:
                    p = parselinepattern.parse_line_pattern(lpat)
                    lpat = linepat.LinePattern(p[1], p[0])
                except Exception as e:
                    print(e)
                    return 
                    
            if closed: 
                if isinstance(x, np.ndarray):
                    xp = np.append(x, x[0])
                    yp = np.append(y, y[0])
                elif isinstance(x, list):
                    xp = x.copy()
                    yp = y.copy()
                    xp.append(x[0])
                    yp.append(y[0])
            else:
                xp, yp = x, y
                
            if viewport:
                pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t, viewport=True)
            else:
                pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t)

            for p1 in pat_seg:
                x2 = [p2[0]*drvpdf._points_inch for p2 in p1 ]
                y2 = [p2[1]*drvpdf._points_inch for p2 in p1 ]
                self.drv.Polyline(x2, y2, _lcol, _lthk, fcol=None, closed=False)
        
        
    def lpolygon(self, x, y, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, fcol=None):
        self.polygon(x,y,lcol,lthk,lpat,fcol,viewport=True)

    def lpolyline(self, x, y, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, closed=False):
        self.polyline(x,y,lcol,lthk,lpat,closed,viewport=True)
        
    def create_clip(self, sx, sy, ex, ey):
        self.drv.CreateClip(sx*drvpdf._points_inch, 
                            sy*drvpdf._points_inch, 
                            ex*drvpdf._points_inch, 
                            ey*drvpdf._points_inch)
        
    def delete_clip(self):
        self.drv.DeleteClip()
        
    def close(self):
        self.drv.Close()