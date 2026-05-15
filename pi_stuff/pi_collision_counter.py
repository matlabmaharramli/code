from block import Block

class PiCollisionCounter:
    
    def __init__(self, block1, block2):
        self.block1 = block1
        self.block2 = block2

        print(f"Number of collisions: {self.compute()}")

    
    def collide_blocks(self):
        """
        Collides the two blocks and updates their velocities according to the laws of elastic collisions.
        
        :param self:
        """

        v1 = ((self.block1.getMass()-self.block2.getMass())*self.block1.getVelocity()+2*self.block2.getMass()*self.block2.getVelocity())/(self.block1.getMass()+self.block2.getMass())
        v2 = ((self.block2.getMass()-self.block1.getMass())*self.block2.getVelocity()+2*self.block1.getMass()*self.block1.getVelocity())/(self.block1.getMass()+self.block2.getMass())
        self.block1.setVelocity((v1))
        self.block2.setVelocity((v2))
    
    def compute(self):
        """
        Computes the number of collisions that will occur between the two blocks and the wall.
        
        :param self:
        """

        collision_count = 0
        
        while(True):
            if ((self.block2.getVelocity()>=self.block1.getVelocity())):
                break

            self.collide_blocks()
            print("01")
            collision_count += 1

            if self.block1.getVelocity() >= 0:
                break
            
            self.block1.collide_wall()
            print("10")
            collision_count += 1
        
        return collision_count