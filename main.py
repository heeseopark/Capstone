from meshclass import *

hand = Mesh('hand.stl')

hand.get_wrist()

print(hand.width)

scale_factor = 68 / (hand.width)



hand.scale(scale_factor).save('newhand.stl')


newhand = Mesh('newhand.stl')
newhand.get_wrist()
print(newhand.width)

