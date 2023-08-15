# limacon.py
import numpy as np
import libvgl as vgl

theta = np.linspace(0, 2*np.pi, 300, endpoint=True)
rho = 1+2*np.cos(theta)
rmin = np.min(rho)
rmax = np.max(rho)
fmm = vgl.FrameManager()
#frm = fmm.create(1,1,4,4, vgl.Data(rmin, rmax, -2, 2))
frm = fmm.create(1,1,4,4, vgl.Data(-rmax, rmax, -rmax, rmax))

def plot(dev):
    dev.set_device(frm, vgl.device._FIT_EXTEND_Y)
    vgl.polarplot(dev, theta, rho)
    dev.close()

def save():
    from . import chkfld
    
    if not chkfld.create_folder("./limacon"):
        return
            
    dev_img = vgl.DeviceIMG("./limacon/limacon.jpg", fmm.get_gbbox(), 300)
    dev_pdf = vgl.DevicePDF("./limacon/limacon.pdf", fmm.get_gbbox())
    dev_wmf = vgl.DeviceWMF("./limacon/limacon.wmf", fmm.get_gbbox())
    dev_emf = vgl.DeviceEMF("./limacon/limacon.emf", fmm.get_gbbox())
    dev_svg = vgl.DeviceSVG("./limacon/limacon.svg", fmm.get_gbbox(), 300)
    dev_ppt = vgl.DevicePPT("./limacon/limacon.pptx", fmm.get_gbbox())
    
    plot(dev_img)
    plot(dev_pdf)
    plot(dev_wmf)
    plot(dev_emf)
    plot(dev_svg)
    plot(dev_ppt)
    
if __name__ == "__main__":
    save()
    
