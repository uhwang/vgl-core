import math
import libvgl as vgl

data = vgl.Data(-10,10,-10,10)
fmm = vgl.FrameManager()
frm = fmm.create(1,1,6,6, data)
gbox= fmm.get_gbbox()
lthk = 0.0001
deg_lbox = 45
deg_rbox = 45
lrat = 1/math.sqrt(2)

def pytha_tree(dev, v1, v2, up, angle, order):
    global ctbl
    
    l = math.sqrt((v2[0]-v1[0])**2 + (v2[1]-v1[1])**2)
    k = lrat * l
    m = lrat * l
    
    if up == True:
        ak= angle+deg_lbox
        am= angle-deg_rbox
        
        box1 = vgl.basicshape.Box(v1[0], v1[1],k,k,lthk=lthk,fcol=ctbl[order])
        box1.rotate_about_point(v1[0],v1[1], ak)
        box2 = vgl.basicshape.Box(v2[0], v2[1],m,m,
            pos_t=vgl.basicshape.BOX_POS_RIGHTBOTTOM,
            lthk=lthk,fcol=ctbl[order])
        box2.rotate_about_point(v2[0],v2[1], am)
    else:
        ak= angle-deg_lbox
        am= angle+deg_rbox
        
        box1 = vgl.basicshape.Box(v1[0], v1[1],k,k,
            pos_t=vgl.basicshape.BOX_POS_LEFTTOP, lthk=lthk,fcol=ctbl[order])
        box1.rotate_about_point(v1[0],v1[1], ak)
        box2 = vgl.basicshape.Box(v2[0], v2[1],m,m,
            pos_t=vgl.basicshape.BOX_POS_RIGHTTOP, lthk=lthk,fcol=ctbl[order])
        box2.rotate_about_point(v2[0],v2[1], am)
        
    box1.draw(dev)
    box2.draw(dev)
    
    if order > 0:
        if up == True:
            lp1 = box1.get_vertex(3)
            lp2 = box1.get_vertex(2)
            rp1 = box2.get_vertex(3)
            rp2 = box2.get_vertex(2)
        else:
            lp1 = box1.get_vertex(1)
            lp2 = box1.get_vertex(2)
            rp1 = box2.get_vertex(1)
            rp2 = box2.get_vertex(2)
        pytha_tree(dev, lp1, lp2, up, ak, order - 1)
        pytha_tree(dev, rp1, rp2, up, am, order - 1)
   
def draw(dev):
    global ctbl
    dev.set_device(frm)
    order = 10
    ctbl = vgl.hsv_table_by_saturation(260, 0, 0.8, 1, order)
    box = vgl.basicshape.Box(-1.5, -1.5, 3, 3, lthk=lthk, fcol=ctbl[order-1])
    box.draw(dev)
    pytha_tree(dev, box.get_vertex(3), box.get_vertex(2), True , 0, order-1)
    pytha_tree(dev, box.get_vertex(0), box.get_vertex(1), False, 0, order-1)
    vgl.draw_axis(dev)
    dev.close()

def save(ppt=False):
    from . import chkfld
    #import chkfld
    
    chkfld.create_folder("./pythatree45")
    
    dev_wmf = vgl.DeviceWMF("./pythatree45/pythatree45.wmf", gbox)
    dev_emf = vgl.DeviceEMF("./pythatree45/pythatree45.emf", gbox)
    dev_pdf = vgl.DevicePDF("./pythatree45/pythatree45.pdf", gbox)
    dev_svg = vgl.DeviceSVG("./pythatree45/pythatree45.svg", gbox, 200)
    dev_img = vgl.DeviceIMG("./pythatree45/pythatree45.jpg", gbox, 200)
    if ppt:
        dev_ppt = vgl.DevicePPT("./pythatree/pythatree.pptx",gbox)
    
    draw(dev_img)
    draw(dev_wmf)
    draw(dev_emf)
    draw(dev_pdf)
    draw(dev_svg)
    if ppt: draw(dev_ppt)
    
if __name__ == "__main__":
    save()
