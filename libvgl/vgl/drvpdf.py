'''
    drvpdf.py
    
    12/06/2024 ... Fix landscape bug
    
    Newline sould be 0x0A. Windows CR(0x0D), LF(0x0A) ==> 0x0A
    Object: 
        obj number generation number obj ==> ex) 2 0 obj
        indirect object (Referenct to obj) ==> 2 0 R
        
        Drawing line
            1 0 obj <</Length ...>>
            stream
            
            path construction: m, l, c, v, y, re
            Path painting: S, s, F, f, f*, B, B*, b, b*, n
            Clipping: W, W*
            Color: CS, cs, SC, SCN, sc, scn, G, g, RG, rg, K, k
            
        q : save DC
        Q : restore DC
        w : line width (non-neg num in user spc)
        J : line cap (butt(0)/round(1)/projecting square(2) cap)
        j : line join (miter(0)/round(1)/bevel(2) join)
        M : miter limit
        
        Line
        =========================
        m : move to  ex) x, y m
        l : line to  ex) x, y l
        h : close the path  ex) h
        
        Painting
        =========================
        S : stroke
        s : close and stroke = h S
        f : fill the path
        B : fill + stroke
        b : close, fill and stroke = h B
        
        Color
        =========================
        RG : set color
            
        Clipping
        =========================
        n : end of path w/o stroke, fill = path painting no-op
        W : modify the cur clipping path by intersecting it w/ the cur path, non-zero winding
        W*: 
        ex) W n
'''
import zlib
import math

from . import size
from . import color
from . import gdiobj
from . import devval
from . import util

_pdf_header = "%PDF-1.7\n"
_points_inch = 72

'''
a b c d e f*

 a : scaling in the horizontal direction
 b : represent skewing (or shearing) in the horizontal
 c : represent skewing (or shearing) in the vertical
 d : scaling in the vertical directions
 e : translation in horizontal
 f : translation in vertical
 
 Ex: portrait layout (origin: left top, y grows downward)
     1 0 0 -1 0 hgt
     landscape layout (origin: left top, y gorws downward)
     0 -1 1 0 0 0 cm
     
  Tm = | a b|
       | c d|
       | e f|

  Tm = | cos(q) sin(q)|
       |-sin(q) cos(q)|
       |   e     f    |
       
Lanscape: 
    1. Move the origin(0,0) to upper left corner (0,11)
       Ex) translate(0,0, 11.0)
    2. Rotete the origin with 90 degree CCW
       Ex) rotate(90)
    3. Turn the y positive direction inverse
       Ex) _y_inverse(hgt)

'''
_default_nobj = 3

_translate = lambda x,y : "1.0000 0.0000 "\
                          "0.0000 1.0000 "\
                          "%3.4f %3.4f cm\n"%(x,y)

_rotate = lambda phi : "%3.4f %3.4f "\
                       "%3.4f %3.4f "\
                       "0.0000 0.0000 cm\n"%(
                        math.cos(phi), math.sin(phi),
                       -math.sin(phi), math.cos(phi)
                       )
_y_inverse = lambda hgt : "1.0000 0.0000 "\
                          "0.0000 -1.0000 "\
                          "0.0000 %3.4f cm\n"%(
                          hgt
                          )

_x_inverse = lambda wid : "-1.0000 0.0000 "\
                          "0.0000 1.0000 "\
                          "%3.4f 0.0000 cm\n"%(
                          wid
                          )
                       
class PDFDriver():
    def __init__(
            self, 
            fname,
            gbbox, 
            wid, 
            hgt, 
            layout_dir,
            plot_area_only=False,
            compression=False):
        self.wid = wid
        self.hgt = hgt
        self.obj_list = [bytes("stream\n", 'utf-8')]
        self.file_size = 0
        self.cur_pen_index = 0
        self.pen = None
        self.clip_region = None
        self.gbbox = gbbox
        self.layout_dir = layout_dir
        self.compression = compression
        self.obj_length = 0
        self.cur_obj_index = 0
        self.rotate = 0
        
        self.obj_length += len(self.obj_list[0])
        ex = self.wid*_points_inch
        ey = self.hgt*_points_inch
        
        if plot_area_only:
            self._sx = self.gbbox.sx
            self._sy = self.gbbox.sy
            self._ex = self.gbbox.ex
            self._ey = self.gbbox.ey
        else:
            self._sx = 0
            self._sy = 0
            self._ex = ex
            self._ey = ey
        
        if layout_dir == devval.layout_dir_landscape:
            self.rotate = 90
            obj_buffer_list = [ _translate(ex, 0), 
                                _rotate(util.deg_to_rad(90)),
                                _y_inverse(self._ex)]
        else:
            obj_buffer_list = [ _y_inverse(self._ey)]

        if self.compression:
            obj_buffer = zlib.compress(bytes(''.join(obj_buffer_list), 'utf-8'))
        else:
            obj_buffer = bytes(''.join(obj_buffer_list), 'utf-8')
                
        self.obj_list.append(obj_buffer)
        self.obj_length += len(obj_buffer)
        
        self.fp = open(fname, "wb")
        
    def MakePen(self, lcol, lthk):
        lc = color.normalize(lcol)
        self.pen = gdiobj.PDFPen()
        self.pen.set_pen(lc, lthk, self.cur_obj_index)

    def DeletePen(self):
        obj_buffer_list = ["q\n"] #saveDC
        obj_buffer_list.append("%1.4f %1.4f %1.4f RG\n"%(self.pen.lcol.r, self.pen.lcol.g, self.pen.lcol.b))
        obj_buffer_list.append("%3.3f w\n"% self.pen.lthk)
        
        for p in self.pen.buf:
            obj_buffer_list.append(p)
        obj_buffer_list.append("S\nQ\n")
        
        if self.compression:
            obj_buffer = zlib.compress(bytes(''.join(obj_buffer_list), 'utf-8'))
        else:
            obj_buffer = bytes(''.join(obj_buffer_list), 'utf-8')

        self.obj_list.append(obj_buffer)
        self.obj_length += len(obj_buffer)
        self.pen = None

    def MoveTo(self, x, y):
        self.pen.buf.append("%3.4f %3.4f m\n"%(x,y))
        
    def LineTo(self, x, y):
        self.pen.buf.append("%3.4f %3.4f l\n"% (x,y))
        
    def Line(self, sx, sy, ex, ey, lcol=None, lthk=None):
        xx = [sx, ex] 
        yy = [sy, ey]
        self.Polyline(xx,yy,lcol,lthk,None,False)

    def Polyline(self, x, y, lcol, lthk, fcol, closed=False):
        lc = color.normalize(lcol) if lcol else lcol
        fc = color.normalize(fcol) if fcol else fcol
        obj_buffer_list = ["q\n"] #saveDC
        
        if self.clip_region:
            obj_buffer_list.append("W\n%3.4f %3.4f %3.4f %3.4f re\nh\nn\nW\n"%\
                                (self.clip_region.sx,
                                 self.clip_region.sy,
                                 self.clip_region.ex,
                                 self.clip_region.ey))
        
        if lcol:
            obj_buffer_list.append("%1.4f %1.4f %1.4f RG\n"%(lc.r, lc.g, lc.b))
            obj_buffer_list.append("%3.3f w\n"%lthk)
        
        if fcol:
            obj_buffer_list.append("%1.4f %1.4f %1.4f rg\n"%(fc.r, fc.g, fc.b))
            
        obj_buffer_list.append("%3.3f %3.3f m\n"%(x[0],y[0]))
        
        for x1, y1 in zip(x[1:],y[1:]):
            obj_buffer_list.append("%3.3f %3.3f l\n"%(x1,y1))
        
        if closed:
            if lcol and fcol:
                obj_buffer_list.append("b\nQ\n") # close, fill, stroke and restore DC
            elif not isinstance(lcol, color.Color) and fcol:
                obj_buffer_list.append("f\nQ\n") # close, fill, and restore DC
            else:
                obj_buffer_list.append("s\nQ\n") # close, stroke and restore DC
        else:
            obj_buffer_list.append("S\nQ\n")     # stroke and restoreDC
            
        if self.compression:
            obj_buffer = zlib.compress(bytes(''.join(obj_buffer_list), 'utf-8'))
        else:
            obj_buffer = bytes(''.join(obj_buffer_list), 'utf-8')
            
        self.obj_list.append(obj_buffer)
        self.obj_length += len(obj_buffer)
        
    def Polygon(self, x, y, lcol, lthk, fcol):
        self.Polyline(x,y,lcol,lthk,fcol,True)
    
    # save    nq  ... save graphics state for remove clip
    # newpath n
    # rawRect "%.3f %.3f %.3f %.3f re\n", x, y, w, h
    # clip    W
    # newpath n
    def CreateClip(self, sx, sy, ex, ey):
        w, h = ex-sx, ey-sy
        obj_buffer = ["q\nn\n%3.4f %3.4f %3.4f %3.4f re\nW\nnWn"%(sx, sy, w, h)]
        
        if self.compression:
            obj_buffer = zlib.compress(bytes(''.join(buffer2), 'utf-8'))
        else:
            obj_buffer = bytes(''.join(obj_buffer), 'utf-8')
        
        self.obj_list.append(obj_buffer)
        self.obj_length += len(obj_buffer)

    # Q   Restore graphics state    
    # W	  Sets the clipping path to the path that is currently being constructed.
    # W*  Sets the clipping path to the intersection of the current clipping path 
    #     and the    path that is currently being constructed.
    
    # Create and delete clip must be inside one stream unit.
    # Ex:   
    #   6 0 obj
    #   <</Length 64>>
    #   stream
    #   0.0000 G
    #   0.2000 w
    #   q
    #   n
    #   108.000 288.000 432.000 288.000 re
    #   W
    #   n
    #   ...... Drawing ......   
    #   Q 
    #   endstream
    #   endobj
    
    def DeleteClip(self):
        obj_buffer = "Q\n"
        self.obj_list.append(bytes(obj_buffer,'utf-8'))
        self.obj_length += len(obj_buffer)
                
    #
    # Currently, the total number of ojb is 4. The first 3 objs are headers.
    # The 4th obj is the ploting commands. 
    #
    def Close(self):

        obj1 = "1 0 obj\n<< /Type /Catalog /Pages 2 0 R>>\nendobj\n"
        obj2 = "2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1>>\nendobj\n"
        obj3 = "3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n"\
                "/MediaBox [%3.4f %3.4f %3.4f %3.4f]\n"\
                "/Rotate %d\n"\
                "/Contents 4 0 R\n>>\nendobj\n"%\
                (self._sx, self._sy, self._ex, self._ey, self.rotate)
        
        # Write PDF Header
        self.file_size = 0
        self.fp.write(bytes(_pdf_header,'utf-8'))
        self.file_size += len(_pdf_header)
        obj_pos = [self.file_size]   
        
        # Write Obj 1
        self.fp.write(bytes(obj1,'utf-8'))
        self.file_size += len(obj1)
        obj_pos.append(self.file_size)
        
        # Write Obj 2
        self.fp.write(bytes(obj2,'utf-8'))
        self.file_size += len(obj2)
        obj_pos.append(self.file_size)
        
        # Write Obj 3
        self.fp.write(bytes(obj3,'utf-8'))
        self.file_size += len(obj3)
        obj_pos.append(self.file_size)        

        # Write Obj 4
        obj4 = bytes("4 0 obj\n<</Length %d>>\n"% self.obj_length, 'utf-8')
        self.file_size += len(obj4)
        self.fp.write(obj4)

        for o in self.obj_list:
            self.fp.write(o)
        self.file_size += self.obj_length
        
        obj4 = bytes("endstream\nendobj\n",'utf-8')
        self.file_size += len(obj4)
        self.fp.write(obj4)   
        obj_pos.append(self.file_size)
        
        start_xref = self.file_size
        nobj = len(obj_pos)+1
        self.fp.write(bytes("xref\n0 %d\n0000000000 65535 f\n"%nobj,'utf-8'))
        for v in obj_pos:
            self.fp.write(bytes("%010d 00000 n\n"%(v),'utf-8'))
            
        total_nobj = _default_nobj+1
        self.fp.write(bytes("trailer<</Size %d/Root 1 0 R>>\n"%total_nobj,'utf-8'))
        self.fp.write(bytes("startxref\n%d\n"%start_xref,'utf-8'))
        self.fp.write(bytes("%%EOF",'utf-8'))
        self.fp.close()
        
      
   