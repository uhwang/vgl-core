import numpy as np
import libvgl as vgl

r = 1.0
fmm = vgl.FrameManager()
frm = fmm.create(0,0,5,5, vgl.Data(-r,r,-r,r))
star5 = vgl.basicshape.StarPolygon( 0.5, 0.5,5, r*0.5)
star6 = vgl.basicshape.StarPolygon(-0.5, 0.5,6, r*0.5)
star7 = vgl.basicshape.StarPolygon(-0.5,-0.5,7, r*0.5)
star8 = vgl.basicshape.StarPolygon( 0.5,-0.5,8, r*0.5)
uu, max_u = 1, r/star5.u_radius
fps, duration= 10, 20
total_frame = fps*duration
du = max_u/total_frame
f0 = star5.u_radius/du
gbox = fmm.get_gbbox()

def draw(t):
    global dev, uu
    dev.fill_white()
    vgl.draw_center_axis(dev)
    dev.polygon(star5.xss, star5.yss, vgl.color.teal  , 0.004)
    dev.polygon(star6.xss, star6.yss, vgl.color.orchid, 0.004)
    dev.polygon(star7.xss, star7.yss, vgl.color.BLUE  , 0.004)
    dev.polygon(star8.xss, star8.yss, vgl.color.crimson, 0.004)

    if t*fps < f0:
        uu -= du
        if uu <= 0: uu = 0
    else:
        uu += du
        if uu > max_u: uu = max_u

    star5.u_param = uu
    star6.u_param = uu
    star7.u_param = uu
    star8.u_param = uu

def plot(dev):
    dev.set_device(frm)
    
    star5.reset()
    star6.reset()
    star7.reset()
    star8.reset()
    
    dev.polygon(star5.xss, star5.yss, vgl.color.BLACK, 0.003)
    dev.polygon(star6.xss, star6.yss, vgl.color.BLACK, 0.003)
    dev.polygon(star7.xss, star7.yss, vgl.color.BLACK, 0.003)
    dev.polygon(star8.xss, star8.yss, vgl.color.BLACK, 0.003)
    
    uu = np.linspace(0.4, 1.5, 10)
    for u in uu:
        star5.u_param = u
        star6.u_param = u
        star7.u_param = u
        star8.u_param = u
        dev.polygon(star5.xss, star5.yss, vgl.color.teal)
        dev.polygon(star6.xss, star6.yss, vgl.color.orchid)
        dev.polygon(star7.xss, star7.yss, vgl.color.BLUE)
        dev.polygon(star8.xss, star8.yss, vgl.color.crimson)

    vgl.draw_center_axis(dev)
    dev.close()
    
def plot_all():
    dev_img = vgl.DeviceIMG("./starpolygon/star5678.jpg", gbox, 300)
    dev_pdf = vgl.DevicePDF("./starpolygon/star5678.pdf", gbox)
    dev_wmf = vgl.DeviceWMF("./starpolygon/star5678.wmf", gbox)
    dev_emf = vgl.DeviceEMF("./starpolygon/star5678.emf", gbox)
    dev_svg = vgl.DeviceSVG("./starpolygon/star5678.svg", gbox, 300)
    dev_ppt = vgl.DevicePPT("./starpolygon/star5678.pptx",gbox)

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
    dev_mov = vgl.DeviceCairoAnimation("./starpolygon/starpolygon5678.mp4", 
    dev, draw, fps=fps, duration=duration)
    dev_mov.save_video()

    plot_all()
    
if __name__ == "__main__":
    save()
