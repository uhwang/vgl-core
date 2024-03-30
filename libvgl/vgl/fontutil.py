'''
fontutil.py

7/30/2023

'''
from pathlib import Path, PurePath
import numpy as np

from . import paper
from . import size
from . import fontm
from . import devutil
from . import text
from . import linepat
from . import color
from . import fontid
from . import fontm

# single_char : digit or char
def glyp_line(glyp):
    return glyp_to_line(None, None, False, True, glyp)
    
def glyp_to_line(fontid, single_char, xflip=False, yflip=True, glyp_given=None):

    if fontid != None and single_char != None:
        font_map = fontm.font_manager.get_font_map(fontid)
        
        if isinstance(single_char, int):
            pass
        elif isinstance(single_char, str):
            if len(single_char) > 0: single_char = single_char[0]
            single_char = ord(single_char)
            
        glyp = font_map[single_char-ord(' ')]
    else:
        glyp = glyp_given
        
    xmin, xmax, ymin, ymax = 100, -100, 100, -100
    glyp_lines, line = [], []
    
    for p in glyp[1]:
        if p[0] == -1 and p[1] == -1:
            glyp_lines.append(line)
            line = []
        else:
            line.append(p)
    
    if len(line) > 0:
        glyp_lines.append(line)
        
    point_list = []
    y_flip = 1
    if yflip: y_flip = -1

    for gl in glyp_lines:
        npnt = len(gl)
        x = np.zeros(npnt)
        y = np.zeros(npnt)
        
        for i, p in enumerate(gl):
            x[i] = p[0]
            y[i] = p[1]*y_flip
            if x[i] < xmin : xmin = x[i]
            if x[i] > xmax : xmax = x[i]
            if y[i] < ymin : ymin = y[i]
            if y[i] > ymax : ymax = y[i]        
            
        point_list.append((x,y))
        
    return point_list, xmin, xmax, ymin, ymax

def print_hershey_font(font_id, dev_name, lthk=0.002, path=None):
 
    if fontid._valid_fid(font_id):
    
        font_name = fontm.get_font_name(font_id)
        fname = Path("%s/%s-table"%(path,font_name) if path else "%s-table"%font_name)
        
        dev = devutil.open_device(dev_name, str(fname))
        
        if dev:
            gbox = dev.frm.bbox
            fh= dev.frm.hgt()
            fw= dev.frm.wid()
            tx= text.Text()
            tx.lthk = lthk
            sx= gbox.sx
            sy= gbox.sy
            ex= gbox.ex
            ey= gbox.ey

            # number of character horizontal/vertical direction + index
            ncv = 6+1+1+1
            nch = 16+1
            dw  = fw/nch
            dh  = fh/ncv
            sy += dh
            
            tx.hv()
            tx.set_font(fontid.FONT_ROMANSIMPLEX)
            tx.set_text(sx+fw*0.5, sy, font_name)
            text.write_text(dev, tx, True)
            
            # draw horiz lines
            for i in range(nch+1):
                xx = sx + i*dw
                dev.lline(xx, sy+dh, xx, ey, color.BLACK, 0.001, linepat._PAT_SOLID)
            
            for i in range(ncv-1):
                yy = sy + (i+1)*dh
                dev.lline(sx, yy, ex, yy, color.BLACK, 0.001, linepat._PAT_SOLID)
            
            # write index in horizontal (0, 1, 2, ... F)
            tx.hv()
            for i in range(nch-1):
                tx.set_text(sx+dw*(i+1.5), sy+dh*1.5, "%0X"%i)
                text.write_text(dev, tx, True)
                
            # write index in vertical
            for i in range(ncv-3):
                tx.set_text(sx+dw*0.5, sy+dh*(i+2.5), "%dx"%(i+2))
                text.write_text(dev, tx, True)                

            tx.set_font(font_id)
            for i in range(6):
                for j in range(16):
                    idx = int("0x%x%x"%(i+2,j), 16)
                    if idx == 32: continue
                    if idx > 126: break
                    x1 = sx+dw*(j+1.5)
                    y1 = sy+dh*(i+2.5)
                    tx.set_text(x1, y1, chr(idx))
                    try:
                        text.write_text(dev, tx, True)
                    except Exception as e:
                        print("Error (%s): %d\n..... %s"%(font_name,idx,str(e)))
                        pass
                    
            devutil.close_device()