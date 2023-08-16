# vgl-core
VGL package for distribution  
> [!NOTE]
> Wheel package was created with Python version: 3.11.4

1. How to create libvgl package
   - pip install wheel
   - python setup.py bdist_wheel

2. Install libvgl package
   - pip install dist\libvgl-0.1-py3-none-any.whl

3. Usage
   ```Python
   import libvgl as vgl
   vgl.pixel_grid()

<img width="354" alt="libvgl pixelgrid" src="https://github.com/uhwang/vgl-core/assets/43251090/77a783b5-44d0-473e-b09b-4659fb0fc8f4">

![libvgl pixelgrid screenshot-](https://github.com/uhwang/vgl-core/assets/43251090/af146b8e-e8e5-4fec-b195-a9cc972080ac)

4. Plot example #1
   ```Python
   import libvgl as vgl
   vgl.test.cardioid.save()


![cardioid](https://github.com/uhwang/vgl-core/assets/43251090/25ebb160-e8dc-4a6b-905a-4287c27b6c91)

5. Plot example #2
   ```Python
   import libvgal as vgl
   vgl.test.fractree.save()

![fractree](https://github.com/uhwang/vgl-core/assets/43251090/634bfe5a-1678-470f-94ce-e729d0626e6f)

6. Plot example #3
   ```Python
   import libvga as vgl
   vgl.test.epicyloid.save()

![epicycloid](https://github.com/uhwang/vgl-core/assets/43251090/15e35fb7-d78d-4d82-9695-e5b8e89e10f5)

7. Plot example #4
   ```Python
   import libvgl as vgl
   vgl.test.potflow.save()
   
![potflow](https://github.com/uhwang/vgl-core/assets/43251090/bc4172ff-68dc-43e3-9de5-f5fc78cbf1b2)   

8. Plot example #5
   ```Python
   import libvgl as vgl
   vgl.test.pramsym.save()
![pramsym](https://github.com/uhwang/vgl-core/assets/43251090/de515f75-5f42-4921-9fa9-84d25ddf8d4b)  

10. Plot example #6
    ```Python
    import libvgl as vgl
    vgl.test.x2.save()
![x2](https://github.com/uhwang/vgl-core/assets/43251090/2e66c6af-0b21-4034-b823-2324c7b45ea0)    
