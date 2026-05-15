import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import json
from body import Body

class Simulation:

    def __init__(self, params_file, num_steps, total_time):

        """
        Initializes the Simulation class by parsing the params_file and creating Body objects for each body in the simulation. Only one computation method (Beeman, Euler-Cromer, or Direct Euler) should be called after initialization. A body named "sun" to be included in the params_file for the correct functioning of the simulation.
        Parameters:
        params_file (str): The path to the JSON file containing the parameters of the simulation (to include keys: name, mass, orbital_radius, colour for each body),
        num_steps (int): The number of time steps to simulate,
        total_time (float): The total time to simulate in Earth years.
        """
        
        self.G = 6.6743e-11 * (5.9722e24 * (3.15576e7**2)) / (1.4959787e11**3)
        self.bodies = []
        self.num_steps = num_steps
        self.total_time = total_time
        self.dt = total_time/num_steps
        
        self.energy_record = np.zeros(num_steps+1)
        self.alignment_steps = [] # Stores steps (including 0) at which alignments occur after the implementation of determine_alingment method
        self.alignment_angle = [] # Stores corresponding mean alingment angle for each alignment step
        self.alignment_count = 0

        # Parse the params_file to add bodies to be simulated
        
        with open(params_file) as f:
            parameters = json.load(f)
        
        # Get the mass of the sun
        for body in parameters["bodies"]:
            if body['name'] == "sun":
                self.mass_sun = body['mass']
            
        # Create bodies and add them to the 'bodies' list
        for body in parameters["bodies"]:
            self.bodies.append(Body(body['name'], body['mass'], body['colour'], body['orbital_radius'], self.num_steps, self.mass_sun, self.G))

        # Calculate initial accelerations of bodies
        for i in range(len(self.bodies)):
                force = np.zeros(2)
                for k in range(len(self.bodies)):
                    if i != k: # If not itself
                        force = force + self.bodies[i].get_force(self.bodies[k], 0, self.G) # Calculate the vector force by body k on body i
                # Calculate acceleration based on force and mass (a = F/m)
                self.bodies[i].current_acceleration = force/self.bodies[i].mass
                self.bodies[i].previous_acceleration = self.bodies[i].current_acceleration.copy() # Needed for Beeman Method. Previous acceleration assumed to equal current acceleration since it does not exist at (0)th timestep



    def beeman_compute(self):
        """
        Computes the positions and velocities of the bodies in the simulation using the Beeman method.
        """
        for step in range(self.num_steps): # Iterate for each state starting from state 0 until the step 1 before the last one

            # Determine r(t+dt) for every body
            for i in range(len(self.bodies)):
                self.bodies[i].beeman_calculate_position(step, self.dt) # Calculates body's position at (step+1)th position using Beeman Method
            
            # After determining r(t+td) for every body, we can calculate a(t+dt) based on that
            for i in range(len(self.bodies)):
                force = np.zeros(2)
                for k in range(len(self.bodies)):
                    if i != k:
                        force = force + self.bodies[i].get_force(self.bodies[k], step+1, self.G)
                self.bodies[i].next_acceleration = force/self.bodies[i].mass

            for i in range(len(self.bodies)):  
                self.bodies[i].beeman_calculate_velocity(step, self.dt) # Calculate velocity at (step+1)th timestep based on the results above

                # Shift history for the next iteration
                self.bodies[i].previous_acceleration = self.bodies[i].current_acceleration.copy() # .copy() function used to prevent accidental synchronisation
                self.bodies[i].current_acceleration = self.bodies[i].next_acceleration.copy() # order of the operations considered not to overwrite variables



    def euler_cromer_compute(self):
        """
        Computes the positions and velocities of the bodies in the simulation using the Euler-Cromer method.
        """
        for step in range(self.num_steps): # Iterate for each state starting from state 0 until the step 1 before the last one

            # Determine r(t+dt) for every body
            for i in range(len(self.bodies)):
                self.bodies[i].euler_cromer_calculate_velocity(step, self.dt) # Calculates body's velocity at (step+1)th position
                self.bodies[i].euler_cromer_calculate_position(step, self.dt) # Calculates body's position at (step+1)th position, order matters, velocity calculation should come first since position calculation is based on that

            
            # After determining r(t+td) for every body, we can calculate the self.current_velocity for the next iteration
            for i in range(len(self.bodies)):
                force = np.zeros(2)
                for k in range(len(self.bodies)):
                    if i != k:
                        force = force + self.bodies[i].get_force(self.bodies[k], step+1, self.G)
                self.bodies[i].current_acceleration = force/self.bodies[i].mass


    def direct_euler_compute(self):
        """
        Computes the positions and velocities of the bodies in the simulation using the Direct Euler method.
        """
        for step in range(self.num_steps): # Iterate for each state starting from state 0 until the step 1 before the last one

            # Determine r(t+dt) and v(t+dt) for every body
            for i in range(len(self.bodies)):
                self.bodies[i].direct_euler_calculate_position(step, self.dt) # Calculates body's position at (step+1)th position
                self.bodies[i].direct_euler_calculate_velocity(step, self.dt)
            
            # After determining r(t+td) for every body, we can calculate the self.current_acceleration for the next iteration
            for i in range(len(self.bodies)):
                force = np.zeros(2)
                for k in range(len(self.bodies)):
                    if i != k:
                        force = force + self.bodies[i].get_force(self.bodies[k], step+1, self.G)
                self.bodies[i].current_acceleration = force/self.bodies[i].mass


    def compute_cycles(self):
        """
        Computes the number of orbital cycles completed by each body in the simulation. The result could be obtained by calling the return_cycles method after this method.
        """
        # Computes the number of orbital cycles of each body and assigns it to each body's orbital_cycles variable

        position_record_sun = None
        for body in self.bodies:
            if body.name == "sun":
                position_record_sun = body.position_record

        for body in self.bodies:
            if body.name == "sun":
                continue # Skip the sun
            body.compute_cycles(position_record_sun) # compute_cycles method of Simulation class uses that of Body class


    def compute_total_energy(self):
        """
        Computes the total energy of the system at each time step, The result could be obtained by calling the return_energy method after this method.
        """

        # Computes the total energy of the system at each time step and assigns it energy_record variable of Simulation class
        # Energy is in units of (Earth Mass)*(AU^2)/(Year^2)

        for step in range(self.num_steps+1): # for each step

            # Calculate total_potential_energy at step=step
            total_potential_energy = 0
            for i in range(len(self.bodies)-1): # Last element omitted
                for j in range(i+1, len(self.bodies)): # Iterate j from (the position of the current element + 1) until the last element in self.bodies
                    total_potential_energy += self.bodies[i].get_potential_energy(self.bodies[j], step, self.G) # Increment potantial energy
            
            # Calculate total_kinetic_energy at step=step
            total_kinetic_energy = 0
            for body in self.bodies:
                total_kinetic_energy += body.get_kinetic_energy(step)

            # Add them up to get the total energy and store the result
            self.energy_record[step] = total_potential_energy + total_kinetic_energy
    

    def determine_alignment(self, threshold=5):
        """
        Computes the timesteps and corresponding mean alignment angles at which the bodies in the simulation are aligned within a specified threshold. The result could be obtained by calling the return_alignment_count and return_alignment_data methods after this method. Alignment count is also calculated and can be accessed by calling the return_alignment_count method after this method.
        Parameters:
        threshold (float): The maximum allowed deviation from the mean alignment angle for the bodies to be considered aligned, in degrees. Default value is 5 degrees.
        """

        self.alignment_steps = [] # Reset alignment steps and count to allow for multiple calls to this method with different thresholds
        self.alignment_angle = []
        self.alignment_count = 0

        position_record_sun = None
        for body in self.bodies:
            if body.name == "sun":
                position_record_sun = body.position_record
        
        # Compute the angle record for each body with respect to the sun and set it to body's angle_record attirbute
        for body in self.bodies:
            body.compute_angle(position_record_sun)
        
        # Filter to only include planets for the alignment calculation
        planets = []

        for body in self.bodies:
            if body.name != "sun":
                planets.append(body)


        # Iterate for each step to check for alignment
        for step in range(self.num_steps+1):
            Aligned = True # Flag initially set to True
            
            # Shift planets[0].angle_record[step] to be at angle 0
            reference = planets[0].angle_record[step]
            differences = np.zeros(len(planets)) # array for storing difference from reference to the angle of each body [-180, 180]
            
            for i in range(len(planets)):
                difference = ((planets[i].angle_record[step] - reference + 180) % 360) - 180
                differences[i] = difference
            
            mean = np.mean(differences)
            actual_mean = ((reference +mean)% 360)

            for planet in planets:
                deviation = abs(planet.angle_record[step]- actual_mean)

                # Set the deviation to a shorter angle
                if deviation > 180:
                    deviation = 360 - deviation
                
                # Check
                if deviation > threshold:
                    Aligned = False # If for one body deviation exceeds threshold Aligned will be set to False
            
            if Aligned:
                self.alignment_steps.append(step) # If at this step the bodies are aligned, we add the step to list
                self.alignment_angle.append(actual_mean) # Add the alignment angle to list for possible plotting
        
        # After having a list of steps at which alingments occur alignment count can be calculated
        # Given steps are consecutive integers, they are part of a single alignment
        # Alignment in the beginning is counted

        previous_alignment_step = -2 
        for step in self.alignment_steps:
            if step != previous_alignment_step + 1: # If not concesutive, we increment 
                self.alignment_count += 1
            previous_alignment_step = step # Update previous_alignment_step



    # Output Methods

    def animate(self, interval=20, trail=False, show_alignment=False):
        """
        Animates the simulation using Matplotlib. determine_alignment method to be used before for show_alignment function to be functional.
        Parameters:
        trail (bool): If True, trails of the bodies will be shown in the animation. Default value is False.
        time (int): The total time of the animation in milliseconds. Default value is 10000 ms (10 seconds).
        """

        fig, ax = plt.subplots()

        # Determine the distance from the center fo the farthest body
        r_bodies = np.zeros(len(self.bodies))
        for i in range(len(self.bodies)):
            r_bodies[i] = np.linalg.norm(self.bodies[i].position_record[0])
        max_r = np.max(r_bodies)

        # Set the window limit to 1.2*max_r in both directions for both x and y
        ax.set_xlim(-max_r*1.2, max_r*1.2)
        ax.set_ylim(-max_r*1.2, max_r*1.2)
        ax.set_aspect('equal')

        body_patches = []
        trail_lines = []
        
        for body in self.bodies:
            patch = patches.Circle(body.position_record[0], max_r*0.02, color = body.colour, animated = True) # Radius of circles set to change depending on max_r so as to be seen
            ax.add_patch(patch)
            body_patches.append(patch)

            if trail:
                line, = ax.plot([], [], color=body.colour, linewidth=1, animated = True)
                trail_lines.append(line,)
        
        alignment_line, = ax.plot([], [], 'r-', linewidth=1.5, zorder=10) # zorder=10 ensure the line is put at the very front
        if show_alignment:
            alignment_dict = self.return_alignment_data()
        else:
            alignment_dict = {}
        
        def update(frame):
            
            for i in range(len(self.bodies)):
                body_patches[i].set_center(self.bodies[i].position_record[frame])

                if trail:
                    start_frame = max(0, frame - 500) # Fading for performance
                    history = self.bodies[i].position_record[start_frame:frame+1] # Line drawn from start frame until current
                    trail_lines[i].set_data(history[:, 0], history[:, 1]) # x position, y-position
            
            if show_alignment and alignment_dict: # Check if boolean is True and if the list is not empty
                if frame in alignment_dict: # If the current step is an alignment step
                    angle_rad = np.radians(alignment_dict[frame]) # Convert to rad for math
                    
                    # Calculate the end coordinates using your max_r limit
                    x_end = max_r * np.cos(angle_rad)
                    y_end = max_r * np.sin(angle_rad)
                    
                    # Draw the line from the center to the end (until (x_end; y_end))
                    alignment_line.set_data([0, x_end], [0, y_end])
                else:
                    # Hide the line on frames where there is no alignment
                    alignment_line.set_data([], [])
                
            return body_patches + trail_lines + [alignment_line] # Brackets used since alignment_line is not a list by itself

        self.animation = FuncAnimation(fig, update, frames=self.num_steps+1, interval=interval, blit=True, repeat=False)
        plt.show()

    def return_cycles(self):
        """
        Returns a dictionary containing the number of orbital cycles completed by each body in the simulation. The compute_cycles method should be called before this method to get the correct results.
        Returns:
        dict: A dictionary where the keys are the names of the bodies and the values are the number of orbital cycles completed by each body.
        """

        cycle_dictionary = dict()

        for body in self.bodies:
            cycle_dictionary[body.name] = body.orbital_cycles

        return cycle_dictionary.copy()

    def return_energy(self):
        """
        Returns the total energy of the system at each time step as a numpy array. The compute_total_energy method should be called before this method to get the correct results.
        Returns:
        numpy.ndarray: An array containing the total energy of the system at each time step.
        """
        return self.energy_record.copy()
    
    def return_alignment_count(self):
        """
        Returns the number of alignments that occurred in the simulation. The determine_alignment method should be called before this method to get the correct results.
        Returns:
        int: The number of alignments that occurred in the simulation.
        """
        return self.alignment_count

    def return_alignment_data(self):
        """
        Returns a dictionary containing the timesteps and corresponding mean alignment angles at which the bodies in the simulation are aligned within a specified threshold. The determine_alignment method should be called before this method to get the correct results.
        Returns:
        dict: A dictionary where the keys are the timesteps and the values are the corresponding mean alignment angles.
        """
        alignment_dictionary = {}

        for i in range(len(self.alignment_steps)):
            alignment_dictionary[self.alignment_steps[i]] = self.alignment_angle[i]
        return alignment_dictionary


