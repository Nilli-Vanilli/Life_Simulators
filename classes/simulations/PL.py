from classes.window import Window
import pygame as pg
import numpy as np
from random import random, randint, uniform
from quads import QuadTree, BoundingBox
from math import hypot



# function to calculate force between two particles
def force(beta, r, a):
    
    # repel if particles get to close, else force depends on r and a
    return r / beta - 1 if r < beta else a * (1 - abs(2 * r - 1 - beta) / (1 - beta))
    


# function to create random n x n matrix with coefficients between -1 and 1
def rnd_matrix(n):
    
    matrix = np.random.rand(n,n)
    
    for row, col in np.ndindex(n,n):
        matrix[row, col] = matrix[row, col] * 2 - 1
    
    return matrix
    


class PL():
    
    # background colour
    cbg = (10,10,10)
    
    # random variables
    mb = False
    num_particles_rnd = False
    size_rnd = False
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
      
    
    
    def get_neighbours(self, x, y):
        
        # find all particles in range of the specified position
        bb = BoundingBox(x - self.r_max, y - self.r_max,
                         x + self.r_max, y + self.r_max)
        
        neighbours = self.tree.within_bb(bb)
        
        # apply periodic boundary condition
        if x < self.r_max: # left wrap
            bb = BoundingBox(1 - self.r_max + x, y - self.r_max,
                             1, y + self.r_max)

            neighbours += self.tree.within_bb(bb)
        
        elif x > 1 - self.r_max: # right wrap
            bb = BoundingBox(0, y - self.r_max,
                             self.r_max - 1 + x, y + self.r_max)
            
            neighbours += self.tree.within_bb(bb)
        
        if y < self.r_max: # down wrap
            bb = BoundingBox(x - self.r_max, 1 - self.r_max + y,
                             x + self.r_max, 1)
            
            neighbours += self.tree.within_bb(bb)
        
        elif y > 1 - self.r_max: # up wrap
            bb = BoundingBox(x - self.r_max,0,
                                x + self.r_max, self.r_max - 1 + y)
            
            neighbours += self.tree.within_bb(bb)
        
        return neighbours
            
            
    
    def particles_effect(self, i, points):
        
        # return values
        fx = 0
        fy = 0
        
        # loop through the neighbouring particles
        for point in points:
            
            # find the index value of the particle
            j = np.where((self.positions_x == point.x) & (self.positions_y == point.y))[0][0]
            
            if j == i: continue # ignore the original particle itself
            
            # find euclidean distance between the original particle and the neighbour
            rx = self.positions_x[j] - self.positions_x[i]
            ry = self.positions_y[j] - self.positions_y[i]
            
            # periodic boundary
            if rx > 0.5: rx -= 1
            elif rx < -0.5: rx += 1
            if ry > 0.5: ry -= 1
            elif ry < -0.5: ry += 1
            
            r = hypot(rx, ry)
            
            # if the particle is within the specified range, calculate the force between them, dependent on the rule matrix
            if r < self.r_max:
                f = force(self.beta, r / self.r_max, self.matrix[self.colours[i], self.colours[j]])
                
                # add force to total force acting on the original particle
                fx += rx / r * f
                fy += ry / r * f
        
        return fx, fy
    
    
    
    def mouse_effect(self, i, click):
    
        # return values
        add_x = 0
        add_y = 0
        
        # get mouse position
        pos = pg.mouse.get_pos()
                
        # calculate euclidean distance between original particle and the mouse
        rx = self.positions_x[i] - pos[0] / self.window.width
        ry = self.positions_y[i] - pos[1] / self.window.height
        
        # periodic boundary
        if rx > 0.5: rx -= 1
        elif rx < -0.5: rx += 1
        if ry > 0.5: ry -= 1
        elif ry < -0.5: ry += 1
        
        r = hypot(rx, ry)
        
        # if mouse in range, create a force between particle and mouse
        if r < self.r_max: # attract if left click, else repel
            f = force(self.beta, r / self.r_max, -3 if click[0] else 5)
        
        # if mouse not in range, don't add force
        else: return 0, 0

        # add force to total force
        add_x += rx / r * f
        add_y += ry / r * f
        
        return add_x, add_y
    
    
    
    def calculate_velocity(self, i, fx, fy):
        
        # rescale force by r_max (we normalise r when we calculate the force)
        # and apply bonus force
        fx *= self.r_max * self.forcefactor
        fy *= self.r_max * self.forcefactor
        
        # apply friction
        self.velocities_x[i] *= self.friction
        self.velocities_y[i] *= self.friction
        
        # calculate dv and add to velocities
        self.velocities_x[i] += fx * self.dt
        self.velocities_y[i] += fy * self.dt
        
    
    
    def update_velocities(self):
        
        # loop through all particles
        for i in range(self.num_particles):
            
            # store particle position
            x = self.positions_x[i]
            y = self.positions_y[i]
            
            # find all particles in range of the particle
            neighbours = self.get_neighbours(x, y)
                    
            # calculate effect of neighbouring particles on particle
            fx, fy = self.particles_effect(i, neighbours)
            
            # detect if mouse is clicked and store which button
            if any(click := pg.mouse.get_pressed()):
                
                # calculate effect of mouse on particle
                add_x, add_y = self.mouse_effect(i, click)
                fx += add_x
                fy += add_y
                
            # calculate velocity
            self.calculate_velocity(i, fx, fy)
            
    
    
    def update_positions(self):
        
        # loop through all particles
        for i in range(self.num_particles):
            
            # calculate dx and dy and add to positions
            self.positions_x[i] += self.velocities_x[i] * self.dt
            self.positions_y[i] += self.velocities_y[i] * self.dt
            
            # periodic boundary
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
        
        # loop through all particles
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
        if self.mb or self.r_max_rnd: self.r_max = uniform(0.05,0.15)
        if self.mb or self.forcefactor_rnd: self.forcefactor = randint(5,40)
        
        
        
    def run(self):
        
        # check for random variables or mystery box
        self.check_rnd()
        
        # update friction and number of colours (particle types)
        self.friction = 0.5 ** (self.dt / self.fric_hl)
        self.num_colours = self.matrix.shape[0]
        
        # create quadtree
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
                self.update_velocities()
                self.update_positions()
                
            # reset tree
            self.tree = QuadTree((0.5, 0.5), 1, 1)
            
            # draw particles
            self.draw_particles()
            
            # update screen
            self.window.update(self.fps_cap)

        