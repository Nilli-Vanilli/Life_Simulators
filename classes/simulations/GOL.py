import pygame as pg
from random import randint, choice
import numpy as np

class GOL():
    
    # colours
    cgrid = (40,40,40)
    coff = (10,10,10)
    coff_next = (170,170,170)
    con = (255,255,255)
    
    # random variables
    mb = False
    rule_rnd = False
    size_rnd = False
    boundary_rnd = False
    coff_rnd = False
    cgrid_rnd = False
    coff_next_rnd = False
    con_rnd = False
    
    
    
    def __init__(self, window, rules: tuple, size: int, boundary: str, fps_cap: int, grid_lines=True) -> None:
        
        self.window = window
        
        self.rules = rules
        self.size = size
        self.boundary = boundary
        self.fps_cap = fps_cap
        self.grid_lines = grid_lines
        
        self.width = self.window.width // self.size
        self.height = self.window.height // self.size
    
    
    
    def get_totalistic_sums(self, cells):
        
        # apply boundary condition
        match self.boundary:
            
            case "periodic": padded_cells = np.pad(cells, 1, "wrap")
            case "dirichlet 0": padded_cells = np.pad(cells, 1, "constant", constant_values=0)
            case "dirichlet 1": padded_cells = np.pad(cells, 1, "constant", constant_values=1)
            case "neumann": padded_cells = np.pad(cells, 1, "edge")
        
        # get totalistic neighbourhood sum of each cell
        sums = np.lib.stride_tricks.sliding_window_view(padded_cells, (3, 3)).sum(axis=(2, 3))
        
        return sums
    
    
    
    def apply_rules(self, state, tot_sum):
        
        # apply rules
        if state == 1:   # cell is alive
            if self.rules[0] <= tot_sum <= self.rules[1]: # survival
                return 1, self.con

            else: return 0, self.coff_next                # death
        
        # cell is dead
        elif tot_sum == self.rules[2]:                   # birth                  
                return 1, self.con
        
        else: return 0, self.coff
                    
    
    def draw_grid(self, cells: np.ndarray, paused):
        
        # if not paused, get totalistic neighbourhood sums
        if not paused:
            tot_sums = self.get_totalistic_sums(cells)
            
        # loop through all cells in the grid
        for row, col in np.ndindex(cells.shape):
            
            # determine current colour
            colour = self.con if cells[row, col] else self.coff
            
            # if not paused, calculate new state and colour
            if not paused:
                cells[row, col], colour = self.apply_rules(cells[row, col], tot_sums[row, col])
            
            # draw cell
            pg.draw.rect(self.window.screen, colour, (col * self.size,
                                                      row * self.size,
                                                      self.size - self.grid_lines,
                                                      self.size - self.grid_lines))
            
        return cells
    
    
    
    def fill_rnd(self, grid: np.ndarray):
        
        # turn on rougly a sixth of the cells in the grid
        for _ in range(self.width * self.height // 6):
            
            # get random position
            row = randint(0, self.height - 1)
            col = randint(0, self.width - 1)
            
            grid[row, col] = 1
            
        return grid
    
    
    
    def check_rnd(self):
        
        # check for random variables or mystery box
        if self.mb or self.rule_rnd: self.rules = (a := randint(0,8),randint(a,8),randint(0,8))                          # rule
        if self.mb or self.size_rnd: self.size = randint(5,100)                                                          # size
        if self.mb or self.boundary_rnd: self.boundary = choice(["periodic", "dirichlet 0", "dirichlet 1", "neumann"])   # boundary                     
        if self.mb or self.cgrid_rnd: self.cgrid = (randint(0,255), randint(0,255), randint(0,255))                      # colour grid
        if self.mb or self.coff_rnd: self.coff = (randint(0,255), randint(0,255), randint(0,255))                        # colour off
        if self.mb or self.coff_next_rnd: self.coff_next = (randint(0,255), randint(0,255), randint(0,255))              # colour off next gen
        if self.mb or self.con_rnd: self.con = (randint(0,255), randint(0,255), randint(0,255))                          # colour on
    
    
    def run(self):
        
        # check for random variables or mystery box
        self.check_rnd()
        
        # update width and height
        self.width = self.window.width // self.size
        self.height = self.window.height // self.size
        
        # create grid
        cells = np.zeros((self.height, self.width), dtype=int)
        
        #running loop
        paused = True
        running = True
        while running:
            for event in pg.event.get():
                
                # window close button (when tabbed out)
                if event.type == pg.QUIT:
                    running = not running
                
                # get keypresses
                elif event.type == pg.KEYDOWN:
                    
                    # end simulation (escape)
                    if event.key == pg.K_ESCAPE:
                        running = not running
                    
                    # pause button (space)
                    elif event.key == pg.K_SPACE:
                        paused = not paused
                    
                    # fill grid with random cells (R)
                    elif event.key == pg.K_r:
                        cells = self.fill_rnd(cells)
                    
                # place or remove cell in grid
                elif any(click := pg.mouse.get_pressed()):
                    x, y = pg.mouse.get_pos() # left click to place, right click to remove
                    try: cells[y // self.size, x // self.size] = 1 if click[0] else 0
                    except: pass # if user clicks off screen
            
            # refresh screen
            self.window.screen.fill(self.cgrid)

            # draw grid and update cells if not paused
            cells = self.draw_grid(cells, paused)
            
            # update screen
            self.window.update(fps=(60 if paused else self.fps_cap))