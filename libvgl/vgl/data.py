# Vector Graphic Library (VGL) for Python
#
# data.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

class Data():
    def __init__(self, xmin=1e7, xmax=-1e7, ymin=1e7, ymax=-1e7, zmin=1e7, zmax=-1e7):
        self.xmin=xmin
        self.xmax=xmax 
        self.ymin=ymin 
        self.ymax=ymax 
        self.zmin=zmin 
        self.zmax=zmax
        
        self.xmin_org=xmin
        self.xmax_org=xmax 
        self.ymin_org=ymin 
        self.ymax_org=ymax 
        self.zmin_org=zmin 
        self.zmax_org=zmax
	
        self.data_ptr = {}
        self.data_idx = 0
        
    def load(self, x,y):
        self.data_idx += 1
        self.data_ptr[self.data_idx] = (x,y)
        xmin = min(x)
        xmax = max(x)
        ymin = min(y)
        ymax = max(y)
        
        if xmin < self.xmin: self.xmin = xmin
        if xmax > self.xmax: self.xmax = xmax
        if ymin < self.ymin: self.ymin = ymin
        if ymax > self.ymax: self.ymax = ymax
        
    def reset(self):
        self.xmin=self.xmin_org
        self.xmax=self.xmax_org 
        self.ymin=self.ymin_org 
        self.ymax=self.ymax_org 
        self.zmin=self.zmin_org 
        self.zmax=self.zmax_org
    
    def trans(self, dx, dy, dz):
        self.xmin+=dx
        self.xmax+=dx 
        self.ymin+=dy 
        self.ymax+=dy 
        self.zmin+=dz 
        self.zmax+=dz
        
    def get_xrange(self): return self.xrange()
    def get_yrange(self): return self.yrange()
    def get_zrange(self): return self.zmax-self.zmin
    def set_yrange(self, ymin, ymax): 
        self.ymin = ymin
        self.ymax = ymax
        
    def xrange(self): return self.xmax-self.xmin
    def yrange(self): return self.ymax-self.ymin
    
    def xcenter(self): return self.xmin+(self.xmax-self.xmin)*0.5
    def ycenter(self): return self.ymin+(self.ymax-self.ymin)*0.5
   