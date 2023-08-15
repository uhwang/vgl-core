# print_font.py

import libvgl as vgl

def save():
    from . import chkfld
    
    path = "./vgl-fonts"
    if not chkfld.create_folder(path):
        return
    
    for fid in vgl.fontid._FONT_LIST:
        vgl.print_hershey_font(fid, vgl.devutil._dev_img, path)    
    
    # print font with all formats
    #for fid in vgl.fontid._FONT_LIST:
    #    for div in vgl.devutil._dev_list:
    #        vgl.print_hershey_font(fid, div)
    #    
    
    
if __name__ == "__main__":
    save()    