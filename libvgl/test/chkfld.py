from pathlib import Path, PurePath

def create_folder(path):
    global f_path
    f_path = PurePath(path)
    p = Path(path)
    if p.exists() == False:
        try:
            p.mkdir()
        except Exception as e:
            print("... Error: %s\n... Fail to create %s"%
                 (e,path))
            return False
            
    return True
    
def f_jpg():
    return str(PurePath(f_path, "%s.jpg"%f_path))
    
def f_png():
    return str(PurePath(f_path, "%s.png"%f_path))
    
def f_wmf():
    return str(PurePath(f_path, "%s.wmf"%f_path))
    
def f_emf():
    return str(PurePath(f_path, "%s.emf"%f_path))

def f_pdf():
    return str(PurePath(f_path, "%s.pdf"%f_path))

def f_svg():
    return str(PurePath(f_path, "%s.svg"%f_path))

def f_aps():
    return str(PurePath(f_path, "%s.ps"%f_path))
 
def f_ppt():
    return str(PurePath(f_path, "%s.pptx"%f_path))
 
def f_mp4():
    return str(PurePath(f_path, "%s.mp4"%f_path))

def f_gif():
    return str(PurePath(f_path, "%s.gif"%f_path))
    
if __name__ == "__main__":
    create_folder("./dummy")
    print(f_jpg())
    print(f_png())
    print(f_wmf())
    print(f_emf())
    print(f_pdf())
    print(f_svg())
    print(f_aps())
    print(f_ppt())
