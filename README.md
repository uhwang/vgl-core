# vgl-core
vgl package for distribution  
> [!NOTE]
> Wheel package was created with Python version: 3.11.4

1. How to create libvgl package
   - pip install wheel
   - python setup.py bdist_wheel

2. Install libvgl package
   - pip install dist\libvgl-0.1-py3-none-any.whl

3. Libvgl Architecture
![VGL](https://github.com/uhwang/vgl-core/assets/43251090/c200106b-c1b2-4fdd-99b9-6ccf9364e019)

4. Usage
   ```Python
   import libvgl as vgl
   vgl.pixel_grid()

<img width="354" alt="libvgl pixelgrid" src="https://github.com/uhwang/vgl-core/assets/43251090/77a783b5-44d0-473e-b09b-4659fb0fc8f4">

![libvgl pixelgrid screenshot-](https://github.com/uhwang/vgl-core/assets/43251090/af146b8e-e8e5-4fec-b195-a9cc972080ac)

5. Plot example #1
![cardioid](https://github.com/uhwang/vgl-core/assets/43251090/25ebb160-e8dc-4a6b-905a-4287c27b6c91)
   ```Python
   import libvgl as vgl
   vgl.test.cardioid.save()

6. Plot example #2
![fractree](https://github.com/uhwang/vgl-core/assets/43251090/634bfe5a-1678-470f-94ce-e729d0626e6f)
   ```Python
   import libvgal as vgl
   vgl.test.fractree.save()

7. Plot example #3
![epicycloid](https://github.com/uhwang/vgl-core/assets/43251090/15e35fb7-d78d-4d82-9695-e5b8e89e10f5)
   ```Python
   import libvga as vgl
   vgl.test.epicyloid.save()

8. Plot example #4
![potflow](https://github.com/uhwang/vgl-core/assets/43251090/bc4172ff-68dc-43e3-9de5-f5fc78cbf1b2)   
   ```Python
   import libvgl as vgl
   vgl.test.potflow.save()
   
9. Plot example #5
![pramsym](https://github.com/uhwang/vgl-core/assets/43251090/de515f75-5f42-4921-9fa9-84d25ddf8d4b)  
   ```Python
   import libvgl as vgl
   vgl.test.pramsym.save()

10. Plot example #6
![x2](https://github.com/uhwang/vgl-core/assets/43251090/2e66c6af-0b21-4034-b823-2324c7b45ea0)   
    ```Python
    import libvgl as vgl
    vgl.test.x2.save()

11. Plot example #7
![fractal_star](https://github.com/uhwang/vgl-core/assets/43251090/7504c830-2b59-43d9-b2ba-6c3ce83e218a)
    ```Python
    import libvgl as vgl
    vgl.test.fractal_star.save()
12. Plot example #8
![rotation](https://github.com/uhwang/vgl-core/assets/43251090/f6409e67-5fce-4ccf-b9f0-c906febec3f1)
    ```Python
    import libvgl as vgl
    vgl.test.rotation.save()
13. Plot example #9
![uplate](https://github.com/uhwang/vgl-core/assets/43251090/230b1043-262d-4252-9ce3-677b0d930d21)
    ```Python
    import libvgl as vgl
    vgl.test.uplate.save()
14. Plot example #10
![pythatree](https://github.com/uhwang/vgl-core/assets/43251090/74c8ca1a-4734-404e-834c-9967a222c02d)
    ```Python
    import libvgl as vgl
    vgl.test.pythatree.save()

15. Plot example #11
![pythatree45](https://github.com/uhwang/vgl-core/assets/43251090/bc48b154-d4d5-4871-a5a4-4d3652dd3915)
    ```Python
    import libvgl as vgl
    vgl.test.pythatree45.save()
16.  Plot example #12
![star](https://github.com/uhwang/vgl-core/assets/43251090/fe877606-c22c-4cca-85a8-abd4a0bb7610)
     ```Python
     import libvgl as vgl
     vgl.test.starpolygon.save()
18. Cantor Plot
![cantor](https://github.com/uhwang/vgl-core/assets/43251090/b7f9c51b-a052-454a-9454-1724f3705892)
   ```Python
   import libvgl as vgl

   xmin,xmax,ymin,ymax=-10,10,-8,5.
   data = vgl.Data(xmin,xmax,ymin,ymax)
   fmm = vgl.FrameManager()
   frm = fmm.create(0,0,3,3, data)

   def cantor(dev, x, y, xrange, yshift, lthk):
       if xrange >= 0.01:
           dev.line(x, y, x+xrange, y, vgl.color.BLUE, lthk)
           y += yshift
           new_len = xrange/3.0
           cantor(dev, x, y, new_len, yshift, lthk)
           cantor(dev, x+new_len*2, y, new_len, yshift, lthk)
        
   def save_cairo(fname, gbox, dpi):
       dev = vgl.DeviceIMG(fname, gbox, dpi)
       dev.set_device(frm)
       cantor(dev, xmin, ymax*0.5, xmax-xmin, -1.5, 0.09)
       vgl.draw_axis(dev)
       dev.close()        
    
   save_cairo("cantor.jpg", fmm.get_gbbox(), 200)

