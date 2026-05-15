class Block:

    def __init__(self, mass, velocity):
        self.mass = mass
        self.velocity = velocity

    def getMass(self):
        return self.mass
    
    def getVelocity(self):
        return self.velocity
    
    def setVelocity(self, velocity):
        self.velocity = velocity

    def collide_wall(self):
        self.velocity = -self.velocity