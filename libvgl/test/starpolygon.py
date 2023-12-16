import numpy as np
import libvgl as vgl

r = 1.0
fmm = vgl.FrameManager()
frm = fmm.create(0,0,4,4, vgl.Data(-r,r,-r,r))
dev = vgl.DeviceIMG("./starpolygon/star.jpg", fmm.get_gbbox(), 300)
dev.set_device(frm)
star = vgl.basicshape.StarPolygon(0,0,5)
uu, max_u = 1, r/star.u_radius
fps, duration= 10, 20
total_frame = fps*duration
du = max_u/total_frame
f0 = star.u_radius/du

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

def plot():
    dev.fill_white()
    uu = np.linspace(0.2, 1.3, 10)
    for u in uu:
        star.u_param = u
        dev.polygon(star.xss, star.yss, vgl.color.BLUE)
    dev.close()
    
def save():
    from . import chkfld
    global dev
    
    if not chkfld.create_folder("./starpolygon"):
        return

    dev_mov = vgl.DeviceCairoAnimation("./starpolygon/starpolygon.mp4", dev, draw, fps=fps, 
                                       duration=duration)
    dev_mov.save_video()

    plot()
    
if __name__ == "__main__":
    save()
