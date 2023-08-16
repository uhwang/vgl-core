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
   - Python console
   ```Python
   import libvgl as vgl
   vgl.pixel_grid()

<img width="354" alt="libvgl pixelgrid" src="https://github.com/uhwang/vgl-core/assets/43251090/77a783b5-44d0-473e-b09b-4659fb0fc8f4">

![libvgl pixelgrid screenshot-](https://github.com/uhwang/vgl-core/assets/43251090/af146b8e-e8e5-4fec-b195-a9cc972080ac)
   ```Python
  vgl.test.cardioid()


![cardioid](https://github.com/uhwang/vgl-core/assets/43251090/25ebb160-e8dc-4a6b-905a-4287c27b6c91)
