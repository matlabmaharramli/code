from block import Block
from pi_collision_counter import PiCollisionCounter

block1 = Block(1, 0)
block2 = Block(1000000, -1)

simulation = PiCollisionCounter(block1, block2)