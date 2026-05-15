import numpy as np

class Body:

    # The Body class is not to be used by the user, but is used by the Simulation class to create, store, and do operations with the bodies in the simulation. 

    def __init__(self, name, mass, colour, orbital_radius, num_steps, mass_sun, gravitational_constant):
        self.name = name
        self.mass = mass
        self.colour = colour

        self.position_record = np.zeros((num_steps+1, 2)) # If we include initial state as a timestep, then n timesteps would result in (n+1) states
        self.position_record[0] = np.array([orbital_radius, 0])

        self.angle_record = np.zeros(num_steps+1) # Will store record of angle of the body relative to to the sun upon implementation of compute_angle method
        
        self.velocity_record = np.zeros((num_steps+1, 2))
        
        if orbital_radius != 0: # Avoid the ZeroDivisionError
            self.velocity_record[0] = np.array([0, np.sqrt((gravitational_constant*mass_sun)/orbital_radius)]) # Set the initial velocity of the body. Else it remains zero.

        self.current_acceleration = np.zeros(2)
        self.next_acceleration = np.zeros(2)
        self.previous_acceleration = np.zeros(2)

        self.orbital_cycles = 0 # To be changed after computing cycles
        self.num_steps = num_steps


    def get_force(self, other, step, G):
        r21 = other.position_record[step] - self.position_record[step] # Force vector from body 1 (self) to body 2 (other)
        force = (G*self.mass*other.mass)*(r21)/((np.linalg.norm(r21))**3)
        return force


    def get_kinetic_energy(self, step):
        # returns kinetic energy of th 
        speed = np.linalg.norm(self.velocity_record[step])
        kinetic_energy = (self.mass*speed**2)/2
        return kinetic_energy
    
    
    def get_potential_energy(self, other, step, G):
        # returns potential energy relative to other body
        distance = np.linalg.norm(self.position_record[step] - other.position_record[step])
        potential_energy = -G*self.mass*other.mass/distance
        return potential_energy
    

    def compute_cycles(self, position_record_sun):
        # Method not applicable for sun, sun filtered out in Simulation class
        
        # Compute the number of full cycles at first
        for step in range(1, self.num_steps+1): # Not considering the (0)th step
            current_y_relative = self.position_record[step, 1] - position_record_sun[step, 1]
            previous_y_relative = self.position_record[step-1, 1] - position_record_sun[step-1, 1]
            
            if previous_y_relative < 0 and current_y_relative >= 0: # A full cycle is completed (relative y position of the body changed from - to +)
                self.orbital_cycles += 1 # Increment the number of cycles
            
        final_position_relative = self.position_record[self.num_steps] - position_record_sun[self.num_steps]
        final_angle = np.arctan2(final_position_relative[1], final_position_relative[0])
        
        if final_angle < 0: # Ensures the final angle is between 0 and 2 pi
            final_angle += 2*np.pi
        
        self.orbital_cycles = self.orbital_cycles + final_angle/(2*np.pi)
    

    def compute_angle(self, position_record_sun):
        position_relative = self.position_record - position_record_sun
        angle_rad = np.arctan2(position_relative[:, 1], position_relative[:, 0]) # for every y-value and x-value of the position calculate angle from pi to -pi
        self.angle_record = np.mod(np.degrees(angle_rad), 360) # Converts from radians to degrees and then normalizes to 0-360 range


    def beeman_calculate_position(self, step, dt):
        self.position_record[step+1] = self.position_record[step] + self.velocity_record[step]*dt + (1/6)*(4*self.current_acceleration - self.previous_acceleration)*(dt**2)


    def beeman_calculate_velocity(self, step, dt):
        self.velocity_record[step+1] = self.velocity_record[step] + (1/6)*(2*self.next_acceleration + 5*self.current_acceleration - self.previous_acceleration)*dt


    def euler_cromer_calculate_position(self, step, dt):
        self.position_record[step+1] = self.position_record[step] + self.velocity_record[step+1]*dt


    def euler_cromer_calculate_velocity(self, step, dt):
        self.velocity_record[step+1] = self.velocity_record[step] + self.current_acceleration*dt


    def direct_euler_calculate_position(self, step, dt):
        self.position_record[step+1] = self.position_record[step] + self.velocity_record[step]*dt


    def direct_euler_calculate_velocity(self, step, dt):
        self.velocity_record[step+1] = self.velocity_record[step] + self.current_acceleration*dt