'''
   hsvcircle.py
   
'''

import numpy as np
import libvgl as vgl

fmm = vgl.FrameManager()
frm = fmm.create(0.5,0.5,4,4,vgl.Data(-1,1,-1,1))
r1  = 1
no  = 100
cl  = vgl.create_color_table(0,360,1,1,no)
dpi = np.pi*2/no

def plot(dev):
    dev.set_device(frm)
    for i in range(no):
        xx = [0, r1*np.cos(i*dpi), r1*np.cos((i+1)*dpi)]
        yy = [0, r1*np.sin(i*dpi), r1*np.sin((i+1)*dpi)]
        dev.polygon(xx, yy, lcol=None, fcol=cl[i])
    vgl.draw_axis(dev)
    dev.close()
    
def save():
    if __name__ == "__main__":
        import chkfld
    else:
        from . import chkfld
    
    if not chkfld.create_folder("./hsvcircle"):
        return
        
    dev_img = vgl.DeviceIMG(chkfld.f_jpg(), fmm.get_gbbox(), 200)
    dev_pdf = vgl.DevicePDF(chkfld.f_pdf(), fmm.get_gbbox())
    dev_wmf = vgl.DeviceWMF(chkfld.f_wmf(), fmm.get_gbbox())
    dev_emf = vgl.DeviceEMF(chkfld.f_emf(), fmm.get_gbbox())
    dev_svg = vgl.DeviceSVG(chkfld.f_svg(), fmm.get_gbbox(), 300)
    dev_ppt = vgl.DevicePPT(chkfld.f_ppt(), fmm.get_gbbox())
    dev_aps = vgl.DeviceAPS(chkfld.f_aps(), fmm.get_gbbox())

    plot(dev_ppt)
    plot(dev_pdf)
    plot(dev_wmf)
    plot(dev_emf)
    plot(dev_svg)
    plot(dev_img)
    plot(dev_aps)
    
if __name__ == "__main__":
    save()