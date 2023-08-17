# fractal_star.py

import libvgl as vgl

xx, yy = 2.2,2.2
scale = 0.4
fmm = vgl.FrameManager()
frm = fmm.create(1,1,4,4, vgl.Data(-xx, xx, -yy, yy))

def draw(dev, xc, yc, edge, level):
    global ctbl, dlevel

    p = vgl.geom.Polygon(xc, yc, 5, edge, deg_shift=18)
    xs, ys = p.get_xs(), p.get_ys()
    dev.line(xc,yc,xs[0],ys[0], ctbl[level])#, lthk=level*dlevel*0.01)
    dev.line(xc,yc,xs[1],ys[1], ctbl[level])#, lthk=level*dlevel*0.01)
    dev.line(xc,yc,xs[2],ys[2], ctbl[level])#, lthk=level*dlevel*0.01)
    dev.line(xc,yc,xs[3],ys[3], ctbl[level])#, lthk=level*dlevel*0.01)
    dev.line(xc,yc,xs[4],ys[4], ctbl[level])#, lthk=level*dlevel*0.01)

    if level > 0:
        new_edge = edge*scale
        level -= 1
        for x1, y1 in zip(xs, ys):
            draw(dev, x1, y1, new_edge, level)

def save(level=5, ppt=False):
    from . import chkfld
    #import chkfld
    global ctbl, dlevel
    
    if not chkfld.create_folder("./fractal_star"):
        return
            
    dev_img = vgl.DeviceIMG("./fractal_star/fractal_star.jpg", fmm.get_gbbox(), 300)
    dev_pdf = vgl.DevicePDF("./fractal_star/fractal_star.pdf", fmm.get_gbbox())
    dev_wmf = vgl.DeviceWMF("./fractal_star/fractal_star.wmf", fmm.get_gbbox())
    dev_emf = vgl.DeviceEMF("./fractal_star/fractal_star.emf", fmm.get_gbbox())
    dev_svg = vgl.DeviceSVG("./fractal_star/fractal_star.svg", fmm.get_gbbox(), 300)
    dev_ppt = vgl.DevicePPT("./fractal_star/fractal_star.pptx", fmm.get_gbbox())
    
    edge = 1.3
    xc, yc = 0, 0
    dlevel = 1./(level-1)*0.5
    ctbl = vgl.create_color_table(0,240, 0.8, 1, level+1)    
    
    dev_img.set_device(frm)    
    draw(dev_img, xc, yc, edge, level)
    vgl.draw_axis(dev_img)
    dev_img.close()

    dev_pdf.set_device(frm)
    draw(dev_pdf, xc, yc, edge, level)
    vgl.draw_axis(dev_pdf)
    dev_pdf.close()
    
    dev_wmf.set_device(frm)
    draw(dev_wmf, xc, yc, edge, level)
    vgl.draw_axis(dev_wmf)
    dev_wmf.close()
    
    dev_emf.set_device(frm)
    draw(dev_emf, xc, yc, edge, level)
    vgl.draw_axis(dev_emf)
    dev_emf.close()
    
    dev_svg.set_device(frm)
    draw(dev_svg, xc, yc, edge, level)
    vgl.draw_axis(dev_svg)
    dev_svg.close()
    
    if ppt:
        dev_ppt.set_device(frm)
        draw(dev_ppt, xc, yc, edge, level)
        vgl.draw_axis(dev_ppt)
        dev_ppt.close()
    
if __name__ == "__main__":
    save()    