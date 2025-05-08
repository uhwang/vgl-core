'''
affine.py


'''
import copy
import numpy as np
import libvgl as vgl

_shear_dir_x = 0
_shear_dir_y = 1
_shear_dir_xy = 2

_mirror_dir_x = 3
_mirror_dir_y = 4
_mirror_dir_o = 5 # mirror around origin (0,0)

def scale(x, y, sfx, sfy):
    if isinstance(x, np.ndarray):
        x[:] *= sfx
        y[:] *= sfy
    elif isinstance(x, list) or\
         isinstance(x, tuple):
        for i in range(len(x)):
            x[i] *= sfx
            y[i] *= sfy
    
# Shear in x direction
# 1 tan(p) 0
# 0   1    0
# 0   1    1

# Shear in y direction
# 1      0  0
# tan(s) 1  0
# 0      0  1

def shear(x, y, sfx, sfy, shear_dir=_shear_dir_x, rad=False, keep_src=True):

    sfx = vgl.util.deg_to_rad(sfx) if sfx != 0 and rad==False else 0
    sfy = vgl.util.deg_to_rad(sfy) if sfy != 0 and rad==False else 0

    m = np.array([[1, np.tan(sfx)], [np.tan(sfy), 1]])

    if isinstance(x, np.ndarray):
        p = np.matmul(m, np.vstack((x,y)))
        x1 = p[:][0]
        y1 = p[:][1]
        if keep_src == False:
            x[:] = p[:][0]
            y[:] = p[:][1]
    else:
        if keep_src:
            nn = len(x)
            x1, y1 = np.zeros(nn), np.zeros(nn)
        else:
            x1, y1 = x, y

        for i in range(len(x)):
            p = np.matmul(m, np.array([x[i],y[i]]))
            x1[i], y1[i] = p[0], [1]

    return x1, y1

def shearx(x, y, sfx, rad=False, keep_src=True):
    return shear(x, y, sfx, 0, _shear_dir_x, rad, keep_src)

def sheary(x, y, sfy, rad=False, keep_src=True):
    return shear(x, y, 0, sfy, _shear_dir_y, rad, keep_src)    

def shearxy(x, y, sfx, sfy, rad=False, keep_src=True):
    return shear(x, y, sfx, sfy, _shear_dir_xy, rad, keep_src)


# Reflection about origin
# -1  0  0
#  0 -1  0
#  0  0  1

# Reflection about x-axis
#  1  0  0
#  0 -1  0
#  0  0  1

# Reflection about y-axis
# -1  0  0
#  0  1  0
#  0  0  1
    
def mirror_(xx, keep_src):

    if isinstance(xx, np.ndarray):
        if keep_src:
            x_ = np.copy(xx)
        else:
            x_ = xx
        x_ *= -1
    elif isinstance(xx, list):
        if keep_src:
            x_ = copy.deepcopy(xx)
        else:
            x_ = xx
        x_[:] = [-x for x in xx]
    else:
        if keep_src:
            x_ = copy.deepcopy(xx)
        else:
            x_ = xx
        x_ *= -1
        
    return x_
    
def mirror(xx,yy,mirror_dir, keep_src):    
    x_, y_ = xx, yy
    
    if mirror_dir == _mirror_dir_x:
        y_ = mirror_(yy, keep_src)
        
    elif mirror_dir == _mirror_dir_y:
        x_ = mirror_(xx, keep_src)
        
    elif mirror_dir == _mirror_dir_o:
        x_ = mirror_(xx, keep_src)
        y_ = mirror_(yy, keep_src)
    
    return x_, y_
    
def mirror_x(y,keep_src=True):
    x_, y_ = mirror(None,y,_mirror_dir_x,keep_src)
    return y_
    
def mirror_y(x,keep_src=True):
    x_, y_ = mirror(x,None,_mirror_dir_y,keep_src)
    return x_

def mirror_o(x,y,keep_src=True):
    x_, y_ = mirror(x,y,_mirror_dir_o,keep_src)
    return x_, y_

