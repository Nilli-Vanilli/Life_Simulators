from classes.window import Window
import pygame as pg
import numpy as np
from random import random, randint, uniform
from quads import QuadTree, BoundingBox
from math import hypot



# function to calculate force between two particles
def force(beta, r, a):
    
    if r < beta: # make sure particles dont get too close to one another
        return r / beta - 1
    
    elif beta < r < 1: # if particle in range, calculate force
        return a * (1 - abs(2 * r - 1 - beta) / (1 - beta))
    
    else: # if particle not in range, no force
        return 0
    


# function to create random n x n matrix with coefficients between -1 and 1
def rnd_matrix(n):
    
    matrix = np.random.rand(n,n)
    
    for row, col in np.ndindex(n,n):
        matrix[row, col] = matrix[row, col] * 2 - 1
    
    return matrix
    


class PL(Window):
    
    # background colour
    cbg = (10,10,10)
    
    # random variables
    mb = False
    num_particles_rnd = False
    size_rnd = False
    fric_hl_rnd = False # remove maybe???
    r_max_rnd = False
    forcefactor_rnd = False
    
    # other stuff
    tree = None
    friction = None
    colours = None
    num_colours = None
    positions_x = None
    positions_y = None
    velocities_x = None
    velocities_y = None
    
    
    
    def __init__(self, window, matrix: np.ndarray, num_particles: int, size: int, fric_hl: float, r_max: float, beta: float, forcefactor: int, dt: float, fps_cap: int) -> None:

        self.window = window
        
        self.matrix = matrix
        self.num_particles = num_particles
        self.size = size
        self.fric_hl = fric_hl
        self.r_max = r_max
        self.beta = beta
        self.forcefactor = forcefactor
        self.dt = dt
        self.fps_cap = fps_cap
      
    
    
    def update_particles(self):
        
        '''update velocities'''
        
        # loop through all particles
        for i in range(self.num_particles):
            
            total_fx = 0
            total_fy = 0
            
            # find all particles in range of the particle
            bb = BoundingBox(self.positions_x[i] - self.r_max,
                             self.positions_y[i] - self.r_max,
                             self.positions_x[i] + self.r_max,
                             self.positions_y[i] + self.r_max)
            
            # loop through the neighbouring particles
            for point in self.tree.within_bb(bb):
                
                # find the index value of the particle
                j = np.where((self.positions_x == point.x) & (self.positions_y == point.y))[0][0]
                
                if j == i: continue # ignore the original particle
                
                # find euclidean distance between the original particle and the neighbour
                rx = self.positions_x[j] - self.positions_x[i]
                ry = self.positions_y[j] - self.positions_y[i]
                r = hypot(rx, ry)
                
                # if the particle is within the specified range, calculate the force between them, dependent on the rule matrix
                if 0 < r < self.r_max:
                    
                    f = force(self.beta, r / self.r_max, self.matrix[self.colours[i], self.colours[j]])
                    
                    # add force to total force acting on the original particle
                    total_fx += rx / r * f
                    total_fy += ry / r * f
            
            
            
            # detect if mouse is clicked
            if any(click := pg.mouse.get_pressed()):
                pos = pg.mouse.get_pos()
                
                # calculate euclidean distance between original particle and the mouse
                rx = self.positions_x[i] - pos[0] / self.window.width
                ry = self.positions_y[i] - pos[1] / self.window.height
                r = hypot(rx, ry)
                
                # create a force between particle and mouse
                if click[0]: # left mousebutton
                    f = force(self.beta, r / self.r_max, -3)
                else:  # right mousebutton
                    f = force(self.beta, r / self.r_max, 5)

                # add force to total force
                total_fx += rx / r * f
                total_fy += ry / r * f
            
            
            # rescale total force by r_max (we normalise r when we calculate the force) and apply bonus force
            total_fx *= self.r_max * self.forcefactor
            total_fy *= self.r_max * self.forcefactor
            
            # apply friction
            self.velocities_x[i] *= self.friction
            self.velocities_y[i] *= self.friction
            
            # calculate dv and add to velocities
            self.velocities_x[i] += total_fx * self.dt
            self.velocities_y[i] += total_fy * self.dt
        
        
        
        '''calculate positions'''
        
        # loop through all particles
        for i in range(self.num_particles):
            
            # calculate dx and dy and add to positions
            self.positions_x[i] += self.velocities_x[i] * self.dt
            self.positions_y[i] += self.velocities_y[i] * self.dt
    
            # discourage cells from moving off screen
            if self.positions_x[i] < 0.01: self.velocities_x[i] += 10 / self.forcefactor
            elif self.positions_x[i] > 0.99: self.velocities_x[i] -= 10 / self.forcefactor
            if self.positions_y[i] < 0.01: self.velocities_y[i] += 10 / self.forcefactor
            elif self.positions_y[i] > 0.99: self.velocities_y[i] -= 10 / self.forcefactor
            
            # teleport cells that do move off screen
            self.positions_x[i] %= 1
            self.positions_y[i] %= 1
            


    
    def create_particles(self):
        
        # create arrays to store colour, position and velocity for all particles
        self.colours = np.zeros(self.num_particles, dtype=int)
        self.positions_x = np.zeros(self.num_particles)
        self.positions_y = np.zeros(self.num_particles)
        self.velocities_x = np.zeros(self.num_particles)
        self.velocities_y = np.zeros(self.num_particles)
        
        # initialise random colours and positions for all particles
        for i in range(self.num_particles):
            
            self.colours[i] = randint(0, self.num_colours - 1)
            self.positions_x[i] = random()
            self.positions_y[i] = random()
            
            
    
    def draw_particles(self):
        
       for i in range(self.num_particles):
            
            # get position on screen
            x = self.positions_x[i] * self.window.width
            y = self.positions_y[i] * self.window.height
            
            # determine colour, based on dim of matrix
            colour = pg.Color(0,0,0); colour.hsla = (360 * self.colours[i] / self.num_colours, 100, 50, 100)
            
            # draw particle
            pg.draw.circle(self.window.screen, colour,(x,y), self.size)
            
            # update tree
            self.tree.insert((self.positions_x[i], self.positions_y[i])) 
        
    
    
    def check_rnd(self):
        
        if self.mb: self.matrix = rnd_matrix(randint(1,10))
        if self.mb or self.num_particles_rnd: self.num_particles = randint(50,500)
        if self.mb or self.size_rnd: self.size = randint(1,10)
        if self.mb or self.fric_hl_rnd: self.fric_hl = uniform(0.001, 0.1)
        if self.mb or self.r_max_rnd: self.r_max = uniform(0.05,0.15)
        if self.mb or self.forcefactor_rnd: self.forcefactor = randint(5,40)
        
        
        
    def run(self):
        
        # check for random variables or mystery box
        self.check_rnd()
        
        # update friction and number of colours (particle types)
        self.friction = 0.5 ** (self.dt / self.fric_hl)
        self.num_colours = self.matrix.shape[0]
        
        # create quadtree and friction
        self.tree = QuadTree((0.5, 0.5), 1, 1)
        
        # create particles
        self.create_particles()
        
        # running loop
        paused = False
        running = True
        while running:
            for event in pg.event.get():
                
                # window close button (when tabbed out)
                if event.type == pg.QUIT:
                    running = not running
                
                
                # get keypresses
                if event.type == pg.KEYDOWN:
                    
                    # end simulation (escape)
                    if event.key == pg.K_ESCAPE:
                        running = not running
                    
                    # pause button (space)
                    elif event.key == pg.K_SPACE:
                        paused = not paused
                    
                    # randomise rule matrix (r)
                    elif event.key == pg.K_r:
                        self.matrix = rnd_matrix(self.num_colours)
                
                
                    
            # refresh screen
            self.window.screen.fill(self.cbg)
            
            # update particles
            if not paused:
                self.update_particles()
                
            # reset tree
            self.tree = QuadTree((0.5, 0.5), 1, 1)
            
            # draw particles
            self.draw_particles()
            
            # update screen
            self.window.update(self.fps_cap)

        