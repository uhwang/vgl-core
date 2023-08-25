# uplate.py
import numpy as np
import libvgl as vgl

PI    = 3.141592653589793239
U     = 1.0
#X2(x) = ((x)*(x))
TUPI  = (2.0*PI)
FOPI  = (2*TUPI)
R2PI  = (1/TUPI)
R4PI  = (1/FOPI)
ALPHA = 0.0

# ----------------- Lumpted Vortex Method -------------------------

def solveMatrix(A, x, b, nx):
    
    n = nx
    for i in range(n-1):
        for j in range(i+1,n):
            ratio = A[j][i] / A[i][i]
            for count in range(i, n): 
                A[j][count] -= (ratio * A[i][count])
            b[j] -= (ratio * b[i])
    
    # Back substitution 
    x[n-1] = b[n-1] / A[n-1][n-1]
    
    i=n-2
    while i>=0:
        temp = b[i]
        for j in range(i+1, n):
            temp -= (A[i][j] * x[j])
        x[i] = temp / A[i][i]
        i -= 1

def getVelocity_UPlate(gam, xv, uu, vv, xs, ys, npan):
    
    j=0
    r2=0
    velu, velv = 0,0
    
    for j in range(npan):
        r2 = (xs-xv[j])*(xs-xv[j])+ys*ys
        velu += -gam[j]*ys/r2
        velv += -gam[j]*(xs-xv[j])/r2
    
    velu = uu + velu*R2PI
    velv = vv - velv*R2PI
    
    return velu, velv

def Euler_UPlate(gam, xv,  uu,  vv,  xs,  ys, npan,  dell):
    
    um,vm,qm,ump,vmp,qmp=0,0,0,0,0,0
    xm1p, ym1p = 0,0
    um = vm = 0
    um, vm = getVelocity_UPlate(gam, xv, uu, vv, xs, ys, npan)
    qm = np.sqrt(um*um + vm*vm)
    
    # 1st order forward difference
    xm1p = xs + um/qm * dell
    ym1p = ys + vm/qm * dell
    
    ump = vmp = 0
    ump, vmp = getVelocity_UPlate(gam, xv, uu, vv, xm1p, ym1p, npan)
    qmp = np.sqrt(ump*ump + vmp*vmp)
    
    # central difference method : improved method
    xm1p = (xs + 0.5 * ( um / qm + ump / qmp ) * dell)
    ym1p = (ys + 0.5 * ( vm / qm + vmp / qmp ) * dell)
    
    return xm1p, ym1p
    
def U_Plate(alpha, minx, miny, maxx, maxy, nsgx, nsgy):
    
    npan = 20
    chord = 1.0
    alrad = vgl.util.deg_to_rad(alpha)
    rhs,i,j=0,0,0
    xs, ys, uu, vv=0,0,0,0
    delx = (maxx - minx)/(nsgx-1)
    dely = (maxy - miny)/(nsgy-1)
    dell = delx
    xm1p, ym1p=0,0
    
    xv = np.zeros(npan)
    xc = np.zeros(npan)
    A = np.zeros([npan, npan])
    b = np.zeros(npan)
    gam = np.zeros(npan)
    gridy = np.zeros(nsgy)
    rhs = -2*PI*U*np.sin(alrad)
    
    for i in range(npan): 
        xv[i] = (1+4*i)*chord/(npan*4)
        xc[i] = (3+4*i)*chord/(npan*4)
        b[i]  = rhs
    
    for i in range(npan):
        for j in range(npan):
            A[i][j] = 1.0/(xc[i]-xv[j])     
    
    solveMatrix(A, gam, b, npan)
    
    for i in range(nsgy):
        gridy[i] = miny+dely*i
    
    uu = (U*np.cos(alrad))
    vv = (U*np.sin(alrad))
    stream_lines = list()
    
    for j in range(nsgy): 
        sub_lines = list()
        xs = minx
        ys = gridy[j]
        sub_lines.append((xs,ys))
        while True: 
            xm1p, ym1p = Euler_UPlate(gam, xv, uu, vv, xs, ys, npan, dell)
            if( xm1p < minx or\
                xm1p > maxx or\
                ym1p < miny or\
                ym1p > maxy):
                break
            sub_lines.append((xm1p,ym1p))
            xs, ys = xm1p, ym1p
        stream_lines.append(sub_lines)
        
    return stream_lines
    
minx, maxx, miny, maxy = -1,1,-1,1
data = vgl.Data(minx, maxx, miny, maxy)
fmm = vgl.FrameManager()
frm1 = fmm.create(1,1,4,4, data)
frm2 = fmm.create(1.5,1.5,1.3,1.3, vgl.Data(-0.1,0.2,-0.1,0.2))
frm2.set_bk_show(True)

def plot(dev, frm, lines, lthk1=0.004, lthk2=0.002, axis=True):

    dev.set_device(frm)
    vgl.draw_frame(dev)
    if axis: vgl.draw_axis(dev)
    
    clip = dev.frm.get_clip()
    dev.create_clip(clip[0],clip[1],clip[2],clip[3])
    
    # draw plate
    dev.polyline([0,1], [0,0], vgl.color.RED, lthk1)
    
    # draw stream lines around the plate
    for line in lines:
        xs = [l[0] for l in line]
        ys = [l[1] for l in line]
        dev.polyline(xs, ys, vgl.color.BLUE, lthk2)
    dev.delete_clip()
    
def save():
    from . import chkfld
    #import chkfld
    
    if not chkfld.create_folder("./uplate"):
        return
                 
    lines = U_Plate(10, -1,miny,maxx,maxy, 100, 50)
    
    dev_img = vgl.DeviceIMG("./uplate/uplate.jpg", fmm.get_gbbox(), 200)
    #dev_pdf = vgl.DevicePDF("./uplate/uplate.pdf", fmm.get_gbbox())
    #dev_wmf = vgl.DeviceWMF("./uplate/uplate.wmf", fmm.get_gbbox())
    #dev_emf = vgl.DeviceEMF("./uplate/uplate.emf", fmm.get_gbbox())
    #dev_svg = vgl.DeviceSVG("./uplate/uplate.svg", fmm.get_gbbox(), 300)
    #dev_ppt = vgl.DevicePPT("./uplate/uplate.pptx", fmm.get_gbbox())
    
    plot(dev_img, frm1, lines)
    plot(dev_img, frm2, lines, 0.01, 0.008, False)
    dev_img.close()
    
    #plot(dev_pdf)
    #plot(dev_wmf)
    #plot(dev_emf)
    #plot(dev_svg)
    #plot(dev_ppt)
    
if __name__ == "__main__":
    save()
    
