# rotation.py

import numpy as np
import libvgl as vgl

data = vgl.Data(-4,4,-4,4)
fmm = vgl.FrameManager()
frm = fmm.create(1,1,6,6, data)
gbox = fmm.get_gbbox()

box1 = vgl.basicshape.Box(-2,0,2,2,vgl.color.RED)
box2 = vgl.basicshape.Box(-2,0,2,2,vgl.color.BLUE)
box3 = vgl.basicshape.Box(1.5,1.5,2,2,vgl.color.GREEN)
box4 = vgl.basicshape.Box(1.5,1.5,2,2,vgl.color.MAGENTA)
box5 = vgl.basicshape.Box(2,-2,2,2,vgl.color.CYAN)
box6 = vgl.basicshape.Box(2,-2,2,2,vgl.color.CYAN).rotate(-45)

box2.rotate_about_point(-2,0,45)
box4.rotate_about_point(1.5,1.5,45)

def draw(dev):
    dev.set_device(frm)
    vgl.draw_center_axis(dev)
    box1.draw(dev)
    box2.draw(dev)
    box3.draw(dev)
    box4.draw(dev)
    box5.draw(dev)
    box6.draw(dev)
    dev.line(0,0,4,-4,vgl.color.BLACK, 0.002, vgl.linepat.get_dot(0.05))
    dev.close()

def save():
    from . import chkfld
    
    if not chkfld.create_folder("./rotation"):
        return
    
    dev_wmf = vgl.DeviceWMF("./rotation/rotation.wmf", gbox)
    dev_emf = vgl.DeviceEMF("./rotation/rotation.emf", gbox)
    dev_pdf = vgl.DevicePDF("./rotation/rotation.pdf", gbox)
    dev_svg = vgl.DeviceSVG("./rotation/rotation.svg", gbox, 200)
    dev_img = vgl.DeviceIMG("./rotation/rotation.jpg", gbox, 200)
    dev_ppt = vgl.DevicePPT("./rotation/rotation.pptx",gbox)
    
    draw(dev_wmf)
    draw(dev_emf)
    draw(dev_pdf)
    draw(dev_svg)
    draw(dev_ppt)
    draw(dev_img)
    
if __name__ == "__main__":
    save()
