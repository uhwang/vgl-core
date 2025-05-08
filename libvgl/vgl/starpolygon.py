import numpy as np

def create_star_polygon(xc, yc, nvert, radius, vertex=None, param_u=None):
    
    if isinstance(vertex, np.ndarray):
        vs = vertex
    else:
        vs = np.zeros(nvert*2*2+2)

    for k in range(nvert):
        angle = 0.5*(4*k+nvert)*np.pi/nvert
        vs[k*4] = xc+radius*np.cos(angle) 
        vs[k*4+1] = yc+radius*np.sin(angle)
        
    if not isinstance(vertex, np.ndarray):        
        vs[-1] = vs[1]
        vs[-2] = vs[0]

    xx = vs[0::4]
    yy = vs[1::4]

    if nvert == 3 or nvert == 4:
        default_u = nvert*0.1
        for i in range(nvert):
            angle = 2*np.pi*(i+1)/nvert+0.5*(nvert-2)*np.pi/nvert
            px = xc+default_u*radius*np.cos(angle)
            py = yc+default_u*radius*np.sin(angle)
            vs[2+i*4] = px
            vs[2+i*4+1] = py
    else:
        for i in range(nvert):
            i1 = i
            i2 = (i+2)%nvert
            i3 = (i+1)%nvert
            i4 = (nvert-1+i)%nvert

            x1, y1 = xx[i1], yy[i1]
            x2, y2 = xx[i2], yy[i2]
            x3, y3 = xx[i3], yy[i3]
            x4, y4 = xx[i4], yy[i4]

            if abs(x2-x1) < 1e-10:
                m = (y4-y3)/(x4-x3)
                px= x1
                py= m*(px-x3)+y3

            elif abs(x3-x4) < 1e-10:
                m = (y2-y1)/(x2-x1)
                px= x3
                py= m*(px-x1)+y1
            else:
                m1 = (y2-y1)/(x2-x1)
                m2 = (y4-y3)/(x4-x3)
                px = (m1*x1-y1-m2*x3+y3)/(m1-m2)
                py = m1*(px-x1)+y1

            vs[2+i*4] = px
            vs[2+i*4+1] = py
            
    if isinstance(param_u, float) or isinstance(param_u, int):
        for i in range(nvert):
            vs[2+i*4]   = xc+(vs[2+i*4]-xc)*param_u
            vs[2+i*4+1] = yc+(vs[2+i*4+1]-yc)*param_u
            
    return vs