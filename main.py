from meshclass import *

hand = Mesh('3DModel.stl').run_pca().smoothen().rotate('x',-90).rotate('z',180).print_values()

test = hand.scale(20).render()

scale_factor = 68 / float(hand.width)

print("scale factor: " + str(scale_factor))

hand.scale(scale_factor).translate('z', -hand.min_z_value).save('new3DModel.stl')

newhand = Mesh('new3DModel.stl').print_values().render()

base = Mesh('wristbase.stl')