# util.py

import numpy as np

vgl_pi = 3.141592653589793238
vgl_dtr= 0.0174532925199433
vgl_rtd= 57.29577951308233

deg_to_rad = lambda d: d*vgl_dtr
rad_to_deg = lambda r: r*vgl_rtd
distance = lambda sx,sy,ex,ey: np.sqrt((ex-sx)**2+(ey-sy)**2)

_c = lambda angle, rad: np.cos(angle) if rad==True else np.cos(vgl_dtr*angle)
_s = lambda angle, rad: np.sin(angle) if rad==True else np.sin(vgl_dtr*angle)


def rot_matrix(angle, rad=True):

    if rad:
        c, s = np.cos(angle), np.sin(angle)
    else:
        c, s = np.cos(vgl_dtr*angle), np.sin(vgl_dtr*angle)    
        
    return np.array([[c, -s], [s, c]])
    
def deg_rot_matrix(angle):

    return rot_matrix(angle, rad=False)
    
def rad_rot_matrix(angle):

    return rot_matrix(angle)
    
# angle in degree
def rotation(x,y,angle,rad=True):

    return np.matmul(rot_matrix(angle, rad),[x,y])
        
def deg_rotation(x, y, angle):

    return rotation(x,y,angle,rad=False)
    
def rad_rotation(x, y, angle):

    return rotation(x,y,angle)

def translate_points(x, y, x_shift, y_shift):
    for i in len(x):
        x[i] += x_shift
        y[i] += y_shift
        
# x, y : nd array, list, set, ...
def rotation_points(x, y, angle, rad = True, new_copy = False):
    rr = rot_matrix(angle, rad)
    
    if new_copy: 
        xx = np.zeros(len(x))
        yy = np.zeros(len(y))
    else:
        xx = x
        yy = y
        
    for i, (x_, y_) in enumerate(zip(xx,yy)):
        rp = np.matmul(rr, [x_,y_])
        xx[i] = rp[0]
        yy[i] = rp[1]
        
    return xx, yy
    
def deg_rotation_points(x, y, angle, new_copy=False):
    return rotation_points(x, y, angle, False, new_copy)
    
def rad_rotation_points(x, y, angle, new_copy=False):
    return rotation_points(x, y, angle, True, new_copy)

'''
    Ref: Mathematics for Computer Graphics by John Vince. p75
    
    |1 0 px| |cos(a) -sin(a)| |1 0 -px|
    |0 1 py|x|sin(a)  cos(a)|x|0 1 -py|
    |0 0  1| |  0       0   | |0 0   1|
    
    | cos(a)  -sin(a)  px*(1-cos(a))+py*sin(a)| |x|
    | sin(a)   cos(a)  py*(1-cos(a))-px*sin(a)|x|y|
    |   0        0                1           | |1|
    
'''
def rot_about_points(px, py, xs, ys, angle, rad=True, dim=2):
    c, s = _c(angle, rad), _s(angle, rad)
    rm   = np.array([
                [c, -s, px*(1-c)+py*s],  
                [s,  c, py*(1-c)-px*s],
                [0,  0,     1        ]
            ])
            
    pnt=np.array([np.dot(rm,(v1,v2,1))[0:dim] for v1,v2 in zip(xs,ys)]).flatten()
    x= pnt[::dim]
    y= pnt[1::dim]
    
    if dim == 2:
        return x,y
    else:
        return x, y, pnt[2::dim]
            
def deg_rot_about_points(px, py, xs, ys, angle, dim=2):
    return rot_about_points(px, py, xs, ys, angle, False, dim)
    
def rad_rot_about_points(px, py, xs, ys, angle, dim=2):
    return rot_about_points(px, py, xs, ys, angle, True, dim)    
    
def deg_rot_about_point(px, py, x, y, angle, dim=2):
    res = rot_about_points(px, py, [x], [y], angle, False, dim)
    return res[0][0], res[1][0]
    
def rad_rot_about_point(px, py, x, y, angle, dim=2):
    res = rot_about_points(px, py, [x], [y], angle, True, dim)
    return res[0][0], res[1][0]