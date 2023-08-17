# sierpinski.py

import libvgl as vgl

tri = vgl.geom.EquiTriangle(0,0,1)
xs = tri.get_xs()
ys = tri.get_ys()
fmm = vgl.FrameManager()
frm = fmm.create(1,1,4,4, vgl.Data(-0.5, 0.5, -0.5, 0.5))

def draw(dev, xs, ys, level):

    dev.set_device(frm)
    dev.polyline(xs, ys, closed=True)
    
    if level > 0:
        x1, x2, x3 = (xs[0]+xs[1])*0.5, (xs[1]+xs[2])*0.5, (xs[2]+xs[0])*0.5 
        y1, y2, y3 = (ys[0]+ys[1])*0.5, (ys[1]+ys[2])*0.5, (ys[2]+ys[0])*0.5 

        draw(dev, [xs[0], x1, x3], [ys[0], y1, y3], level-1)
        draw(dev, [xs[1], x2, x1], [ys[1], y2, y1], level-1)
        draw(dev, [xs[2], x3, x2], [ys[2], y3, y2], level-1)
    
def save(level=5):
    from . import chkfld
    
    if not chkfld.create_folder("./sierpinski"):
        return
            
    dev_img = vgl.DeviceIMG("./sierpinski/sierpinski.jpg", fmm.get_gbbox(), 300)
    dev_pdf = vgl.DevicePDF("./sierpinski/sierpinski.pdf", fmm.get_gbbox())
    dev_wmf = vgl.DeviceWMF("./sierpinski/sierpinski.wmf", fmm.get_gbbox())
    dev_emf = vgl.DeviceEMF("./sierpinski/sierpinski.emf", fmm.get_gbbox())
    dev_svg = vgl.DeviceSVG("./sierpinski/sierpinski.svg", fmm.get_gbbox(), 300)
    dev_ppt = vgl.DevicePPT("./sierpinski/sierpinski.pptx", fmm.get_gbbox())
    
    draw(dev_img, xs, ys, level)
    dev_img.close()

    draw(dev_pdf, xs, ys, level)
    dev_pdf.close()

    draw(dev_wmf, xs, ys, level)
    dev_wmf.close()
    
    draw(dev_emf, xs, ys, level)
    dev_emf.close()
    
    draw(dev_svg, xs, ys, level)
    dev_svg.close()
    
    draw(dev_ppt, xs, ys, level)
    dev_ppt.close()
    
if __name__ == "__main__":
    save()