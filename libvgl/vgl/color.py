# Vector Graphic Library (VGL) for Python
#
# color.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#
def get_rgb(c): return c.r/255., c.r/255., c.r/255.
def get_style(c): return "#%02x%02x%02x"%(c.r, c.g, c.b)
def normalize(c): return Color(c.r/255., c.g/255., c.b/255.)

class Color():
    def __init__(self,r=255,g=255,b=255):
        #self.conv(col)
        self.r = r
        self.g = g
        self.b = b
        
    def __eq__(self, c):
        return self.r == c.r and self.g == c.g and self.b == c.b
        
    def __str__(self):
        format = "%3.3f, %03.3f, %03.3f" if isinstance(self.r, float) else\
                 "%03d, %03d, %03d"
        return format%(self.r, self.g, self.b)
        
    def get_tuple(self) : return (self.r, self.g, self.b)
        
BLACK   = Color(0  ,  0,  0)
WHITE   = Color(255,255,255)
RED     = Color(255,  0,  0)
GREEN   = Color(0  ,255,  0)
BLUE    = Color(0  ,  0,255)
YELLOW  = Color(255,255,  0)
MAGENTA = Color(255,  0,255)
CYAN    = Color(0  ,255,255)
PURPLE  = Color(255,  0,255)
CUSTOM1 = Color(255,127,  0)
CUSTOM2 = Color(127,255,  0)
CUSTOM3 = Color(0  ,255,127)
CUSTOM4 = Color(127,  0,255)
CUSTOM5 = Color(255,  0,127)
GRAY20  = Color( 20, 20, 20)
GRAY30  = Color( 30, 30, 30)
GRAY40  = Color( 40, 40, 40)
GRAY50  = Color( 50, 50, 50)
GRAY60  = Color( 60, 60, 60)
GRAY70  = Color( 70, 70, 70)
GRAY80  = Color( 80, 80, 80)
GRAY90  = Color( 90, 90, 90)
GRAY100 = Color(100,100,100)

# SVG Color Codes
# https://johndecember.com/html/spec/colorsvghex.html

aliceblue         = Color(0xF0,0xF8,0xFF)
antiquewhite      = Color(0xFA,0xEB,0xD7)
aqua              = Color(0x00,0xFF,0xFF)
aquamarine        = Color(0x7F,0xFF,0xD4)
azure             = Color(0xF0,0xFF,0xFF)
beige             = Color(0xF5,0xF5,0xDC)
bisque            = Color(0xFF,0xE4,0xC4)
blanchedalmond    = Color(0xFF,0xEB,0xCD)
blueviolet        = Color(0x8A,0x2B,0xE2)
brown             = Color(0xA5,0x2A,0x2A)
burlywood         = Color(0xDE,0xB8,0x87)
cadetblue         = Color(0x5F,0x9E,0xA0)
chartreuse        = Color(0x7F,0xFF,0x00)
chocolate         = Color(0xD2,0x69,0x1E)
coral             = Color(0xFF,0x7F,0x50)
cornflowerblue    = Color(0x64,0x95,0xED)
cornsilk          = Color(0xFF,0xF8,0xDC)
crimson           = Color(0xDC,0x14,0x3C)
darkcyan          = Color(0x00,0x8B,0x8B)
darkgoldenrod     = Color(0xB8,0x86,0x0B)
darkgray          = Color(0xA9,0xA9,0xA9)
darkgreen         = Color(0x00,0x64,0x00)
darkgrey          = Color(0xA9,0xA9,0xA9)
darkkhaki         = Color(0xBD,0xB7,0x6B)
darkmagenta       = Color(0x8B,0x00,0x8B)
darkolivegreen    = Color(0x55,0x6B,0x2F)
darkorange        = Color(0xFF,0x8C,0x00)
darkorchid        = Color(0x99,0x32,0xCC)
darkred           = Color(0x8B,0x00,0x00)
darksalmon        = Color(0xE9,0x96,0x7A)
darkseagreen      = Color(0x8F,0xBC,0x8F)
darkslateblue     = Color(0x48,0x3D,0x8B)
darkslategray     = Color(0x2F,0x4F,0x4F)
darkslategrey     = Color(0x2F,0x4F,0x4F)
darkturquoise     = Color(0x00,0xCE,0xD1)
darkviolet        = Color(0x94,0x00,0xD3)
deeppink          = Color(0xFF,0x14,0x93)
deepskyblue       = Color(0x00,0xBF,0xFF)
dimgray           = Color(0x69,0x69,0x69)
dimgrey           = Color(0x69,0x69,0x69)
dodgerblue        = Color(0x1E,0x90,0xFF)
firebrick         = Color(0xB2,0x22,0x22)
floralwhite       = Color(0xFF,0xFA,0xF0)
forestgreen       = Color(0x22,0x8B,0x22)
fuchsia           = Color(0xFF,0x00,0xFF)
gainsboro         = Color(0xDC,0xDC,0xDC)
ghostwhite        = Color(0xF8,0xF8,0xFF)
gold              = Color(0xFF,0xD7,0x00)
goldenrod         = Color(0xDA,0xA5,0x20)
gray              = Color(0x80,0x80,0x80)
green16           = Color(0x00,0x80,0x00)
greenyellow       = Color(0xAD,0xFF,0x2F)
honeydew          = Color(0xF0,0xFF,0xF0)
hotpink           = Color(0xFF,0x69,0xB4)
indianred         = Color(0xCD,0x5C,0x5C)
indigo            = Color(0x4B,0x00,0x82)
ivory             = Color(0xFF,0xFF,0xF0)
khaki             = Color(0xF0,0xE6,0x8C)
lavender          = Color(0xE6,0xE6,0xFA)
lavenderblush     = Color(0xFF,0xF0,0xF5)
lawngreen         = Color(0x7C,0xFC,0x00)
lemonchiffon      = Color(0xFF,0xFA,0xCD)
lightblue         = Color(0xAD,0xD8,0xE6)
lightcoral        = Color(0xF0,0x80,0x80)
lightcyan         = Color(0xE0,0xFF,0xFF)
lightgray         = Color(0xD3,0xD3,0xD3)
lightgreen        = Color(0x90,0xEE,0x90)
lightpink         = Color(0xFF,0xB6,0xC1)
lightsalmon       = Color(0xFF,0xA0,0x7A)
lightseagreen     = Color(0x20,0xB2,0xAA)
lightskyblue      = Color(0x87,0xCE,0xFA)
lightslategrey    = Color(0x77,0x88,0x99)
lightsteelblue    = Color(0xB0,0xC4,0xDE)
lightyellow       = Color(0xFF,0xFF,0xE0)
lime              = Color(0x00,0xFF,0x00)
limegreen         = Color(0x32,0xCD,0x32)
linen             = Color(0xFA,0xF0,0xE6)
maroon            = Color(0x80,0x00,0x00)
mediumaquamarine  = Color(0x66,0xCD,0xAA)
mediumblue        = Color(0x00,0x00,0xCD)
mediumorchid      = Color(0xBA,0x55,0xD3)
mediumpurple      = Color(0x93,0x70,0xDB)
mediumseagreen    = Color(0x3C,0xB3,0x71)
mediumslateblue   = Color(0x7B,0x68,0xEE)
mediumspringgreen = Color(0x00,0xFA,0x9A)
mediumturquoise   = Color(0x48,0xD1,0xCC)
mediumvioletred   = Color(0xC7,0x15,0x85)
midnightblue      = Color(0x19,0x19,0x70)
mintcream         = Color(0xF5,0xFF,0xFA)
mistyrose         = Color(0xFF,0xE4,0xE1)
moccasin          = Color(0xFF,0xE4,0xB5)
navajowhite       = Color(0xFF,0xDE,0xAD)
oldlace           = Color(0xFD,0xF5,0xE6)
olive             = Color(0x80,0x80,0x00)
olivedrab         = Color(0x6B,0x8E,0x23)
orange            = Color(0xFF,0xA5,0x00)
orangered         = Color(0xFF,0x45,0x00)
orchid            = Color(0xDA,0x70,0xD6)
palegoldenrod     = Color(0xEE,0xE8,0xAA)
palegreen         = Color(0x98,0xFB,0x98)
paleturquoise     = Color(0xAF,0xEE,0xEE)
palevioletred     = Color(0xDB,0x70,0x93)
papayawhip        = Color(0xFF,0xEF,0xD5)
peachpuff         = Color(0xFF,0xDA,0xB9)
peru              = Color(0xCD,0x85,0x3F)
pink              = Color(0xFF,0xC0,0xCB)
plum              = Color(0xDD,0xA0,0xDD)
powderblue        = Color(0xB0,0xE0,0xE6)
purple            = Color(0x80,0x00,0x80)
rosybrown         = Color(0xBC,0x8F,0x8F)
royalblue         = Color(0x41,0x69,0xE1)
saddlebrown       = Color(0x8B,0x45,0x13)
salmon            = Color(0xFA,0x80,0x72)
sandybrown        = Color(0xF4,0xA4,0x60)
seagreen          = Color(0x2E,0x8B,0x57)
seashell          = Color(0xFF,0xF5,0xEE)
sienna            = Color(0xA0,0x52,0x2D)
silver            = Color(0xC0,0xC0,0xC0)
skyblue           = Color(0x87,0xCE,0xEB)
slateblue         = Color(0x6A,0x5A,0xCD)
slategrey         = Color(0x70,0x80,0x90)
snow              = Color(0xFF,0xFA,0xFA)
springgreen       = Color(0x00,0xFF,0x7F)
steelblue         = Color(0x46,0x82,0xB4)
tan               = Color(0xD2,0xB4,0x8C)
teal16            = Color(0x00,0x80,0x80)
thistle           = Color(0xD8,0xBF,0xD8)
tomato            = Color(0xFF,0x63,0x47)
turquoise         = Color(0x40,0xE0,0xD0)
violet            = Color(0xEE,0x82,0xEE)
wheat             = Color(0xF5,0xDE,0xB3)
whitesmoke        = Color(0xF5,0xF5,0xF5)
yellowgreen       = Color(0x9A,0xCD,0x32)
aliceblue         = Color(0xF0,0xF8,0xFF)
antiquewhite      = Color(0xFA,0xEB,0xD7)
aqua              = Color(0x00,0xFF,0xFF)
aquamarine        = Color(0x7F,0xFF,0xD4)
azure             = Color(0xF0,0xFF,0xFF)
beige             = Color(0xF5,0xF5,0xDC)
bisque            = Color(0xFF,0xE4,0xC4)
blanchedalmond    = Color(0xFF,0xEB,0xCD)
blueviolet        = Color(0x8A,0x2B,0xE2)
brown             = Color(0xA5,0x2A,0x2A)
burlywood         = Color(0xDE,0xB8,0x87)
cadetblue         = Color(0x5F,0x9E,0xA0)
chartreuse        = Color(0x7F,0xFF,0x00)
chocolate         = Color(0xD2,0x69,0x1E)
coral             = Color(0xFF,0x7F,0x50)
cornflowerblue    = Color(0x64,0x95,0xED)
cornsilk          = Color(0xFF,0xF8,0xDC)
crimson           = Color(0xDC,0x14,0x3C)
darkcyan          = Color(0x00,0x8B,0x8B)
darkgoldenrod     = Color(0xB8,0x86,0x0B)
darkgray          = Color(0xA9,0xA9,0xA9)
darkgreen         = Color(0x00,0x64,0x00)
darkgrey          = Color(0xA9,0xA9,0xA9)
darkkhaki         = Color(0xBD,0xB7,0x6B)
darkmagenta       = Color(0x8B,0x00,0x8B)
darkolivegreen    = Color(0x55,0x6B,0x2F)
darkorange        = Color(0xFF,0x8C,0x00)
darkorchid        = Color(0x99,0x32,0xCC)
darkred           = Color(0x8B,0x00,0x00)
darksalmon        = Color(0xE9,0x96,0x7A)
darkseagreen      = Color(0x8F,0xBC,0x8F)
darkslateblue     = Color(0x48,0x3D,0x8B)
darkslategray     = Color(0x2F,0x4F,0x4F)
darkslategrey     = Color(0x2F,0x4F,0x4F)
darkturquoise     = Color(0x00,0xCE,0xD1)
darkviolet        = Color(0x94,0x00,0xD3)
deeppink          = Color(0xFF,0x14,0x93)
deepskyblue       = Color(0x00,0xBF,0xFF)
dimgray           = Color(0x69,0x69,0x69)
dimgrey           = Color(0x69,0x69,0x69)
dodgerblue        = Color(0x1E,0x90,0xFF)
firebrick         = Color(0xB2,0x22,0x22)
floralwhite       = Color(0xFF,0xFA,0xF0)
forestgreen       = Color(0x22,0x8B,0x22)
fuchsia           = Color(0xFF,0x00,0xFF)
gainsboro         = Color(0xDC,0xDC,0xDC)
ghostwhite        = Color(0xF8,0xF8,0xFF)
gold              = Color(0xFF,0xD7,0x00)
goldenrod         = Color(0xDA,0xA5,0x20)
gray              = Color(0x80,0x80,0x80)
green16           = Color(0x00,0x80,0x00)
greenyellow       = Color(0xAD,0xFF,0x2F)
honeydew          = Color(0xF0,0xFF,0xF0)
hotpink           = Color(0xFF,0x69,0xB4)
indianred         = Color(0xCD,0x5C,0x5C)
indigo            = Color(0x4B,0x00,0x82)
ivory             = Color(0xFF,0xFF,0xF0)
khaki             = Color(0xF0,0xE6,0x8C)
lavender          = Color(0xE6,0xE6,0xFA)
lavenderblush     = Color(0xFF,0xF0,0xF5)
lawngreen         = Color(0x7C,0xFC,0x00)
lemonchiffon      = Color(0xFF,0xFA,0xCD)
lightblue         = Color(0xAD,0xD8,0xE6)
lightcoral        = Color(0xF0,0x80,0x80)
lightcyan         = Color(0xE0,0xFF,0xFF)
lightgray         = Color(0xD3,0xD3,0xD3)
lightgreen        = Color(0x90,0xEE,0x90)
lightpink         = Color(0xFF,0xB6,0xC1)
lightsalmon       = Color(0xFF,0xA0,0x7A)
lightseagreen     = Color(0x20,0xB2,0xAA)
lightskyblue      = Color(0x87,0xCE,0xFA)
lightslategrey    = Color(0x77,0x88,0x99)
lightsteelblue    = Color(0xB0,0xC4,0xDE)
lightyellow       = Color(0xFF,0xFF,0xE0)
lime              = Color(0x00,0xFF,0x00)
limegreen         = Color(0x32,0xCD,0x32)
linen             = Color(0xFA,0xF0,0xE6)
maroon            = Color(0x80,0x00,0x00)
mediumaquamarine  = Color(0x66,0xCD,0xAA)
mediumblue        = Color(0x00,0x00,0xCD)
mediumorchid      = Color(0xBA,0x55,0xD3)
mediumpurple      = Color(0x93,0x70,0xDB)
mediumseagreen    = Color(0x3C,0xB3,0x71)
mediumslateblue   = Color(0x7B,0x68,0xEE)
mediumspringgreen = Color(0x00,0xFA,0x9A)
mediumturquoise   = Color(0x48,0xD1,0xCC)
mediumvioletred   = Color(0xC7,0x15,0x85)
midnightblue      = Color(0x19,0x19,0x70)
mintcream         = Color(0xF5,0xFF,0xFA)
mistyrose         = Color(0xFF,0xE4,0xE1)
moccasin          = Color(0xFF,0xE4,0xB5)
navajowhite       = Color(0xFF,0xDE,0xAD)
oldlace           = Color(0xFD,0xF5,0xE6)
olive             = Color(0x80,0x80,0x00)
olivedrab         = Color(0x6B,0x8E,0x23)
orange            = Color(0xFF,0xA5,0x00)
orangered         = Color(0xFF,0x45,0x00)
orchid            = Color(0xDA,0x70,0xD6)
palegoldenrod     = Color(0xEE,0xE8,0xAA)
palegreen         = Color(0x98,0xFB,0x98)
paleturquoise     = Color(0xAF,0xEE,0xEE)
palevioletred     = Color(0xDB,0x70,0x93)
papayawhip        = Color(0xFF,0xEF,0xD5)
peachpuff         = Color(0xFF,0xDA,0xB9)
peru              = Color(0xCD,0x85,0x3F)
pink              = Color(0xFF,0xC0,0xCB)
plum              = Color(0xDD,0xA0,0xDD)
powderblue        = Color(0xB0,0xE0,0xE6)
purple            = Color(0x80,0x00,0x80)
rosybrown         = Color(0xBC,0x8F,0x8F)
royalblue         = Color(0x41,0x69,0xE1)
saddlebrown       = Color(0x8B,0x45,0x13)
salmon            = Color(0xFA,0x80,0x72)
sandybrown        = Color(0xF4,0xA4,0x60)
seagreen          = Color(0x2E,0x8B,0x57)
seashell          = Color(0xFF,0xF5,0xEE)
sienna            = Color(0xA0,0x52,0x2D)
silver            = Color(0xC0,0xC0,0xC0)
skyblue           = Color(0x87,0xCE,0xEB)
slateblue         = Color(0x6A,0x5A,0xCD)
slategrey         = Color(0x70,0x80,0x90)
snow              = Color(0xFF,0xFA,0xFA)
springgreen       = Color(0x00,0xFF,0x7F)
steelblue         = Color(0x46,0x82,0xB4)
tan               = Color(0xD2,0xB4,0x8C)
teal16            = Color(0x00,0x80,0x80)
thistle           = Color(0xD8,0xBF,0xD8)
tomato            = Color(0xFF,0x63,0x47)
turquoise         = Color(0x40,0xE0,0xD0)
violet            = Color(0xEE,0x82,0xEE)
wheat             = Color(0xF5,0xDE,0xB3)
whitesmoke        = Color(0xF5,0xF5,0xF5)
yellowgreen       = Color(0x9A,0xCD,0x32)
lightgoldenrodyellow = Color(0xFA,0xFA,0xD2)

    
agg_color = lambda x: (0,x[2],x[1],x[0])
get_gray  = lambda x: (int(x*255), int(x*255), int(x*255))

# level : 0~1
_gray = lambda level: Color(int(level*255), int(level*255), int(level*255))

#class rgb():
#    def __init__(self,col=WHITE):
#        self.conv(col)
#        
#    def conv(self,col):
#        self.r, self.g, self.b = get_rgb(col)
#        
#    def __str__(self):
#        return "RGB: %03d, %03d, %03d"%(self.r, self.g, self.b)

#inv_255 = 0.00392156862745

def hsv(H, S, V):
	import math
	I = 0.0
	F = 0.0
	P = 0.0
	Q = 0.0
	T = 0.0
	R1 = 0.0
	G1 = 0.0
	B1 = 0.0
	
	if S == 0:
		if H <= 0 or H > 360 :
			return color(int(V*255),int(V*255),int(V*255))

	if H==360: H=0

	H = H/60;
	I = math.floor(H)
	F = H-I
	P = V*(1-S)
	Q = V*(1-S*F)
	T = V*(1-S*(1-F))
	
	int_I = int(I)
	
	if   int_I == 0: 
		R1 = V
		G1 = T
		B1 = P
	elif int_I == 1: 
		R1 = Q
		G1 = V
		B1 = P
	elif int_I == 2: 
		R1 = P
		G1 = V
		B1 = T
	elif int_I == 3: 
		R1 = P
		G1 = Q
		B1 = V
	elif int_I == 4: 
		R1 = T
		G1 = P
		B1 = V
	else           : 
		R1 = V
		G1 = P
		B1 = Q
	
	R = int(R1 * 255)
	G = int(G1 * 255)
	B = int(B1 * 255)

	return Color(R,G,B)
    
    
def hsv_table_by_saturation(H, S1, S2, V, order):
    ctbl = []
    
    ds = (S2-S1)/order
    for i in range(order):
        S = S1 + ds*i
        ctbl.append(hsv(H, S, V))
    return ctbl
    
def create_color_table(H1, H2, S, V, order):
	cbtl = [(0,0,0)]*order
	dH, tempH=0,0
	
	if H1 > H2:
		H1, H2 = H2, H1

	dH = (H2 - H1)/order
	tempH = H1

	for i in range(order):
		cbtl[i] = hsv(tempH, S, V)
		tempH += dH;

	return cbtl    