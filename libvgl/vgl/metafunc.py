'''
metafunc.py


typedef unsigned short svc_u16; // WIN16 : WORD
typedef unsigned int   svc_u32; // WIN16 : DWORD
typedef int            svc_32;  // WIN16 : LONG (Signed Integer)
typedef unsigned char  svc_u8;  // WIN16 : BYTE
typedef unsigned int   svc_uint;
typedef svc_u16  svc_word;
typedef svc_u32  svc_dword;

'''

import struct

LF_FACESIZE = 32

BYTE = 1
WORD = 2
DWORD= 4
WORD_SIZE = WORD
DWORD_SIZE = DWORD
BYTE_SIZE = BYTE

MetaRecordSize = WORD+DWORD 

unpack_word_f  = "=H"
unpack_dword_f = "=I"
unpack_byte_f  = "=B"

boolean = lambda f : f == 1

u8_bin     = lambda x : bin(x)[2:].zfill(8)
u8low_bin  = lambda x : bin(x&0x0f)[2:].zfill(8)
u8high_bin = lambda x : bin(x&0xf0)[2:].zfill(8)

GET_R = lambda v: ( (v)&0x000000ff)
GET_G = lambda v: (((v)&0x0000ff00)>>8)
GET_B = lambda v: (((v)&0x00ff0000)>>16)

def buf_to_record(self, buf):
    #size = struct.pack('=L', self.Size)
    #func = struct.pack('=h', self.Function)
    h = struct.unpack("=L=h", buf[:MetaRecordSize])
    size, func = h[0], h[1]
    return size, func

def get_format_size(format):
    f_size = 0
    for f in format:
        if f == "L" or f == 'i': f_size += 4
        elif f == "h": f_size += 2
    return f_size

