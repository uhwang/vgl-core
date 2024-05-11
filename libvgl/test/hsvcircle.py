'''
   hsvcircle.py
'''
import math as mp
import libvgl as vgl

fmm = vgl.FrameManager()
rad, nop = 1, 100
frm = fmm.create(0.5,0.5,4,4,vgl.Data(-rad,rad,-rad,rad))
clt  = vgl.create_color_table(0,360,1,1,nop)
dpi = np.pi*2/nop

def plot(dev):
    dev.set_device(frm)
    for i in range(nop):
        xx = [0, rad*mp.cos(i*dpi), rad*mp.cos((i+1)*dpi)]
        yy = [0, rad*mp.sin(i*dpi), rad*mp.sin((i+1)*dpi)]
        dev.polygon(xx, yy, lcol=None, fcol=clt[i])
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
