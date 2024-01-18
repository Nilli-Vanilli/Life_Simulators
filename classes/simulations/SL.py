import pygame as pg
import numpy as np
from math import log
from random import randint, choice, uniform




'''threshold / interval functions'''

def logistic_threshold(x, x0, alpha):
    
    return 1.0 / (1.0 + np.exp(-4.0 / alpha * (x - x0)))



def hard_threshold(x, x0):

    return np.greater(x, x0)



def linearized_threshold(x, x0, alpha):

    return np.clip((x - x0) / alpha + 0.5, 0, 1)



def logistic_interval(x, a, b, alpha):

    return logistic_threshold(x, a, alpha) * (1.0 - logistic_threshold(x, b, alpha))



def linearized_interval(x, a, b, alpha):

    return linearized_threshold(x, a, alpha) * (1.0 - linearized_threshold(x, b, alpha))



def lerp(a, b, t):

    return (1.0 - t) * a + t * b



'''other functions'''

def antialiased_circle(size, radius):
    
    y, x = size
    
    # get coordinates of each cell in the grid
    yy, xx = np.mgrid[:y, :x]
    
    # get euclidean distance between each cell and the middle cell
    radii = np.sqrt((xx - x / 2) ** 2 + (yy - y / 2) ** 2) # use np.sqrt because xx and yy are arrays
    
    
    
    # apply logistic function (type of smoothstep to blur circle)
    
    logres = log(min(*size), 2) # steepness of smoothstep
    
    with np.errstate(over="ignore"): # if cell is far away from origin, exp can overflow, so just leave as 0
        logistic = 1 / (1 + np.exp(logres * (radii - radius)))
    
    # center circle at extremes of matrix
    v_shift = np.roll(logistic, y // 2, axis=0)
    h_shift = np.roll(v_shift, x // 2, axis=1)
    
    return h_shift





'''main'''

class SL():
    
    # colour background
    cgrid = (10,10,10)
    
    # initial ranges
    birth_range = (0.278, 0.365)    # birth
    survival_range = (0.267, 0.445) # survival
    sigmoid_widths = (0.028, 0.147) # smoothstep
    
    # multipliers
    M = 0
    N = 0
    
    # RGB channels
    red = True
    green = True
    blue = True
    
    # random variables
    mb = False
    modes_rnd = True
    types_rnd = False
    size_rnd = False
    ra_rnd = False
    birth_rnd = False
    survival_rnd = False
    widths_rnd = False
    
    
    
    def __init__(self, window, size: int, outer_radius: float, sigmode: int, sigtype: int, mixtype: int, stepmode: int, dt: float, fps_cap: int) -> None:
        
        self.window = window
        
        self.size = size
        self.width = self.window.width // self.size
        self.height = self.window.height // self.size
        
        self.ra = outer_radius
        self.ri = outer_radius / 3
        
        self.sigmode = sigmode
        self.sigtype = sigtype
        self.mixtype = mixtype
        self.stepmode = stepmode
        
        self.dt = dt
        self.fps_cap = fps_cap
        
    
    
    def sigmoid_ab(self, x, a, b):
        
        if self.sigtype == 0:
            return hard_threshold(x, a) * (1 - hard_threshold(x, b))
        
        elif self.sigtype == 1:
            return linearized_interval(x, a, b, self.sigmoid_widths[0])
        
        else: # sigtype == 4
            return logistic_interval(x, a, b, self.sigmoid_widths[0])
    
    
    
    def sigmoid_mix(self, x, y, m):
        
        if self.mixtype == 0:
            intermediate = hard_threshold(m, 0.5)
            
        elif self.mixtype == 1:
            intermediate = linearized_threshold(m, 0.5, self.sigmoid_widths[1])
            
        else: # mixtype == 4
            intermediate = logistic_threshold(m, 0.5, self.sigmoid_widths[1])

        return lerp(x, y, intermediate)
    
    
    
    def s(self, n, m, grid):
        
        B1, B2 = self.birth_range
        D1, D2 = self.survival_range
        
        # determine next state for every "pixel" in the grid
        if self.sigmode == 1:
            b_thresh = self.sigmoid_ab(n, B1, B2)
            d_thresh = self.sigmoid_ab(n, D1, D2)
            transition = lerp(b_thresh, d_thresh, m)
            
        elif self.sigmode == 2:
            b_thresh = self.sigmoid_ab(n, B1, B2)
            d_thresh = self.sigmoid_ab(n, D1, D2)
            transition = self.sigmoid_mix(b_thresh, d_thresh, m)
            
        elif self.sigmode == 3:
            threshold1 = lerp(B1, D1, m)
            threshold2 = lerp(B2, D2, m)
            transition = self.sigmoid_ab(n, threshold1, threshold2)
            
        else: # sigmode == 4
            threshold1 = self.sigmoid_mix(B1, D1, m)
            threshold2 = self.sigmoid_mix(B2, D2, m)
            transition = self.sigmoid_ab(n, threshold1, threshold2)



        # apply transition to next state
        if self.stepmode == 0:
            nextgrid = transition
            
        elif self.stepmode == 1:
            nextgrid = grid + self.dt * (2 * transition - 1)
            
        elif self.stepmode == 2:
            nextgrid = grid + self.dt * (transition - grid)
            
        elif self.stepmode == 3:
            nextgrid = m + self.dt * (2 * transition - 1)
            
        else: #stepmode == 4
            nextgrid = m + self.dt * (transition - m)
            
        
        
        # clip state of every pixel between 0 and 1
        nextgrid = np.clip(nextgrid, 0, 1)
        
        return nextgrid
    
    
    
    def get_multipliers(self):
        
        # get kernels
        inner = antialiased_circle((self.height, self.width), self.ri)
        outer = antialiased_circle((self.height, self.width), self.ra)
        annulus = outer - inner
        
        # normalise kernels
        inner /= np.sum(inner)
        annulus /= np.sum(annulus)
        
        # get multipliers for kernel convolution
        M = np.fft.fft2(inner)
        N = np.fft.fft2(annulus)
        
        return M, N


    
    def step(self, grid, M, N):

        # convert grid to frequency domain
        grid_ = np.fft.fft2(grid)
        
        # multiply with kernel multipliers to apply convolution
        M_ = grid_ * M
        N_ = grid_ * N
        
        # convert back to spacial domain
        m = np.real(np.fft.ifft2(M_))
        n = np.real(np.fft.ifft2(N_))

        # Apply transition rules
        grid = self.s(n, m, grid)
        
        return grid
    
    
    
    def fill_rnd(self, grid):
        
        # create a few live cells in the grid, dependent on how large cells should be according to outer radius
        for _ in range(int(self.width * self.height / ((self.ra * 2) ** 2))):
            radius = int(self.ra)
            
            # get random position
            row = np.random.randint(0, self.height - radius) # make sure cells cannot spawn out of bounds
            col = np.random.randint(0, self.width - radius)
            
            grid[row : row + radius, col : col + radius] = 1
        
        
    
    def draw_cell(self, grid):
        
        # get pixel at mouse position
        pos = pg.mouse.get_pos()
        row = pos[1] // self.size
        col = pos[0] // self.size
        
        # get half of radius of cell
        radius = int(self.ra / 2)
        
        grid[row - radius : row + radius, col - radius : col + radius] = 1
        
    
    
    def draw_grid(self, grid):
        
        # loop through every "pixel" in grid
        for row, col in np.ndindex(grid.shape):
            
            # determine brightness and apply to rgb channels
            a = 255 * grid[row, col]
            colour = (a * self.red, a * self.green, a * self.blue)
            
            # draw pixel
            pg.draw.rect(self.window.screen, colour, (col * self.size,
                                                      row * self.size,
                                                      self.size,
                                                      self.size))
    
    
    
    def check_rnd(self):
        
        # check for random variables
        if self.mb or self.modes_rnd: self.sigmode = randint(1,4); self.stepmode = randint(0,4)          # modes
        if self.mb or self.types_rnd: self.sigtype = choice((0,1,4)); self.mixtype = choice((0,1,4))     # types
        if self.mb or self.size_rnd: self.size = randint(5, 20)                                          # size
        if self.mb or self.ra_rnd: self.ra = randint(5, 50 - 2 * self.size); self.ri = self.ra / 3       # outer radius
        if self.mb or self.birth_rnd: self.birth_range = (a := uniform(0.1, 0.3), uniform(a, 1))         # birth range
        if self.mb or self.survival_rnd: self.survival_range = (a := uniform(0.1, 0.3), uniform(a, 1))   # survival range
        if self.mb or self.widths_rnd: self.sigmoid_widths = (uniform(0.025, 0.05), uniform(0.05, 0.3))  # sigmoid widths
        
    
    
    def run(self):
        
        # check for random variables
        self.check_rnd()
        
        # update width and height
        self.width = self.window.width // self.size
        self.height = self.window.height // self.size
        
        # get multipliers
        M, N = self.get_multipliers()
        
        # create grid
        grid = np.zeros((self.height, self.width))
        
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
                    
                    # fill grid with random cells (R)
                    elif event.key == pg.K_r:
                        self.fill_rnd(grid)
                        
                        
                # place cell in grid (hold left mousebutton)
                if pg.mouse.get_pressed()[0]:
                    self.draw_cell(grid)
                    
                     
            
            # refresh screen
            self.window.screen.fill(self.cgrid)
            
            # compute next step
            if not paused:
                grid = self.step(grid, M, N)
            
            # draw grid
            self.draw_grid(grid)
            
            # update screen
            self.window.update(self.fps_cap)         
            
        
    

        
        