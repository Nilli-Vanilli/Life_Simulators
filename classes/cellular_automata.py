from classes.simulations import *
from classes.window import Window

# these are all the preset configurations of the simulations
class Cellular_Automata:
    
    def __init__(self, window: Window) -> None:
        
        # Elementary Cellular Automata
        self.eca = ECA(window=window,
                       rule="01101110", 
                       size=10, 
                       start_indices=[],      # set to middle cell on default
                       boundary="periodic",
                       fps_cap=60)
        
        # Game of Life
        self.gol = GOL(window=window,
                       rules=(3,4,3),
                       size=20,
                       boundary="periodic",
                       fps_cap=10)
        
        # Particle Life
        self.pl = PL(window=window,
                     matrix=rnd_matrix(6),
                     num_particles=200,
                     size=3,
                     fric_hl=0.04,
                     r_max=0.1,
                     beta=0.3,
                     forcefactor=20,
                     dt=0.02,
                     fps_cap=60)
        
        # Smooth Life
        self.sl = SL(window=window,
                     size=5,
                     outer_radius=21,
                     sigmode=4,
                     sigtype=4,
                     mixtype=4,
                     stepmode=0,
                     dt=0.3,
                     fps_cap=60)
        
        
        
        

