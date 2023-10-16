import math
import libvgl as vgl

data = vgl.Data(-10,10,0,20)
fmm = vgl.FrameManager()
frm = fmm.create(1,1,6,6, data)
gbox= fmm.get_gbbox()

deg_lbox = vgl.util.rad_to_deg(math.acos(4*0.2)) # 4/5
deg_rbox = vgl.util.rad_to_deg(math.acos(3*0.2)) # 3/5

def pytha_tree(dev, v1, v2, angle, length, order):
    global ctbl
    
    l = math.sqrt((v2[0]-v1[0])**2 + (v2[1]-v1[1])**2)
    k = 0.8 * l
    m = 0.6 * l
    ak= angle+deg_lbox
    am= angle-deg_rbox
    
    box1 = vgl.basicshape.Box(v1[0], v1[1],k,k, lcol=None, fcol=ctbl[int(length-1)])
    box1.rotate_about_point(v1[0],v1[1], ak)
    box2 = vgl.basicshape.Box(v2[0], v2[1],m,m,pos_t=vgl.basicshape.BOX_POS_RIGHTBOTTOM, lcol=None, fcol=ctbl[int(length-1)])
    box2.rotate_about_point(v2[0],v2[1], am)

    box1.draw(dev)
    box2.draw(dev)

    if order > 0:
        lp1 = box1.get_vertex(3)
        lp2 = box1.get_vertex(2)
        
        rp1 = box2.get_vertex(3)
        rp2 = box2.get_vertex(2)
        
        pytha_tree(dev, lp1, lp2, ak, length*0.8, order - 1)
        pytha_tree(dev, rp1, rp2, am, length*0.8, order - 1)
   
def draw(dev):
    global ctbl, length, dlength
    dev.set_device(frm)
    order = 11
    edge = 3
    yshift = 4
    length = 60
    dlength = 1./(length-1)*0.5
    ctbl = vgl.create_color_table(0,240, 0.8, 1, length)
    v1, v2 = (0,3+yshift), (3,3+yshift)
    box = vgl.basicshape.Box(0,yshift, 3, 3, lcol=None, fcol=ctbl[int(length-1)])
    box.draw(dev)
    pytha_tree(dev, box.get_vertex(3), box.get_vertex(2), 0, length*0.8, order)
    vgl.draw_axis(dev)
    dev.close()

def save(ppt=False):
    from . import chkfld
    #import chkfld
    
    chkfld.create_folder("./pythatree")
    
    dev_wmf = vgl.DeviceWMF("./pythatree/pythatree.wmf", gbox)
    dev_emf = vgl.DeviceEMF("./pythatree/pythatree.emf", gbox)
    dev_pdf = vgl.DevicePDF("./pythatree/pythatree.pdf", gbox)
    dev_svg = vgl.DeviceSVG("./pythatree/pythatree.svg", gbox, 200)
    dev_img = vgl.DeviceIMG("./pythatree/pythatree.jpg", gbox, 200)
    if ppt:
        dev_ppt = vgl.DevicePPT("./pythatree/pythatree.pptx",gbox)
    
    draw(dev_wmf)
    draw(dev_emf)
    draw(dev_pdf)
    draw(dev_svg)
    draw(dev_img)
    if ppt: draw(dev_ppt)
    
if __name__ == "__main__":
    save()
