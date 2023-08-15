# ex_x2.py
import numpy as np
import libvgl as vgl

x = np.arange(-3,3.2,0.2)
y = x**2

data = vgl.Data(-3,3,-1,10)
fmm = vgl.FrameManager()
frm = fmm.create(1,1,5,6, data)
gbox = fmm.get_gbbox()

def draw(dev):
    dev.set_device(frm)
    vgl.draw_axis(dev)
    dev.polyline(x, y, vgl.color.BLUE, 0.001)
    vgl.plot_circle_symbol(dev,x,y)
    dev.close()

def save():
    from . import chkfld
    
    if not chkfld.create_folder("./x2"):
        return
    
    dev_wmf = vgl.DeviceWMF("./x2/x2.wmf", gbox)
    dev_emf = vgl.DeviceEMF("./x2/x2.emf", gbox)
    dev_pdf = vgl.DevicePDF("./x2/x2.pdf", gbox)
    dev_svg = vgl.DeviceSVG("./x2/x2.svg", gbox, 200)
    dev_img = vgl.DeviceIMG("./x2/x2.jpg", gbox, 200)
    dev_ppt = vgl.DevicePPT("./x2/x2.pptx",gbox)
    
    draw(dev_wmf)
    draw(dev_emf)
    draw(dev_pdf)
    draw(dev_svg)
    draw(dev_ppt)
    draw(dev_img)
    
if __name__ == "__main__":
    save()
