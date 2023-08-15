import libvgl as vgl

print("... Start Test Plot ...")

print("... Cardioid ...")
vgl.test.cardioid.save()

print("... Cycloid ...")
vgl.test.cycloid.save()

print("... Cycloid Animation ...")
vgl.test.cycloid_mov.save()

print("... Epicycloid ...")
vgl.test.epicycloid.save()

print("... Epicycloid Animation ...")
vgl.test.epicycloid_mov.save()

print("... Limacon ...")
vgl.test.limacon.save()

print("... Parabola ...")
vgl.test.parabola.save()

print("... Parabola_mov ...")
vgl.test.parabola_mov.save()

print("... Line Pattern ...")
vgl.test.pattern.save()

print("... Petal ...")
vgl.test.petal.save()

print("... Poly1 ...")
vgl.test.poly1.save()

print("... Poly2 ...")
vgl.test.poly2.save()

print("... Potential Flow ...")
vgl.test.potflow.save()

print("... Prametric Cruve ...")
vgl.test.pramsym.save()

print("... Print Fonts ...")
vgl.test.print_font.save()

print("... X^2 ...")
vgl.test.x2.save()

print("... Fractal Tree (skip PPT device ) ...")
print("... If you want pptx, vgl.test.fractree.save(ppt=True) ...")
vgl.test.fractree.save()

print("... End Test Plot ...")

print("... Pixel Grid ...")
vgl.pixel_grid()
