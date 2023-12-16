import numpy as np
import libvgl as vgl

r = 1.0
fmm = vgl.FrameManager()
frm = fmm.create(0,0,4,4, vgl.Data(-r,r,-r,r))
star = vgl.basicshape.StarPolygon(0, 0, 8, r)
uu, max_u = 1, r/star.u_radius
fps, duration= 10, 20
total_frame = fps*duration
du = max_u/total_frame
f0 = star.u_radius/du
gbox = fmm.get_gbbox()

def draw(t):
    global dev, uu
    dev.fill_white()
    vgl.draw_center_axis(dev)
    dev.polygon(star.xss, star.yss, vgl.color.BLUE, 0.005)

    if t*fps < f0:
        uu -= du
        if uu <= 0: uu = 0
    else:
        uu += du
        if uu > max_u: uu = max_u

    star.u_param = uu
    
def plot(dev):
    dev.set_device(frm)
    star.reset()
    dev.polygon(star.xss, star.yss, vgl.color.RED, 0.004)
    
    uu = np.linspace(0.4, 1.5, 10)
    for u in uu:
        star.u_param = u
        dev.polygon(star.xss, star.yss, vgl.color.BLUE  )
    dev.close()
    
def draw_star():
    dev_img = vgl.DeviceIMG("./starpolygon/star.jpg", gbox, 300)
    dev_pdf = vgl.DevicePDF("./starpolygon/star.pdf", gbox)
    dev_wmf = vgl.DeviceWMF("./starpolygon/star.wmf", gbox)
    dev_emf = vgl.DeviceEMF("./starpolygon/star.emf", gbox)
    dev_svg = vgl.DeviceSVG("./starpolygon/star.svg", gbox, 300)
    dev_ppt = vgl.DevicePPT("./starpolygon/star.pptx",gbox)

    plot(dev_img)
    plot(dev_pdf)
    plot(dev_wmf)
    plot(dev_emf)
    plot(dev_svg)
    plot(dev_ppt)
    
def save():
    from . import chkfld
    #import chkfld
    global dev
    
    if not chkfld.create_folder("./starpolygon"):
        return

    dev = vgl.DeviceIMG("", gbox, 300)
    dev.set_device(frm)
    dev_mov = vgl.DeviceCairoAnimation("./starpolygon/starpolygon.mp4", dev, draw, fps=fps, 
                                       duration=duration)
    dev_mov.save_video()

    draw_star()
    
if __name__ == "__main__":
    save()
