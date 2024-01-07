from classes.window import Window
import pygame as pg
from random import randint, choice
import numpy as np

class GOL(Window):
    
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
    
    
    
    def __init__(self, rules: tuple, size: int, boundary: str, fps_cap: int, grid_lines=True) -> None:
        super().__init__()
        
        self.rules = rules
        self.size = size
        self.boundary = boundary
        self.fps_cap = fps_cap
        
        self.grid_lines = 1 if grid_lines else 0
        
        self.grid_width = self.width // self.size
        self.grid_height = self.height // self.size
    
    
    
    def update_grid(self, cells, paused=False):
        
        # store next generation
        updated_cells = np.zeros((cells.shape[0], cells.shape[1]), dtype=int)
        
        # apply boundary condition
        match self.boundary:
            
            case "periodic": padded_cells = np.pad(cells, 1, "wrap")
            case "dirichlet 0": padded_cells = np.pad(cells, 1, "constant", constant_values=0)
            case "dirichlet 1": padded_cells = np.pad(cells, 1, "constant", constant_values=1)
            case "neumann": padded_cells = np.pad(cells, 1, "edge")
        
        # get neighbourhood of each cell
        neighbourhoods = np.lib.stride_tricks.sliding_window_view(padded_cells, (3, 3)).sum(axis=(2, 3)) - cells
            
            
        
        # loop through all cells in the grid
        for row, col in np.ndindex(cells.shape):
            
            # count number of alive neighbours and determine current colour
            alive_count = neighbourhoods[row, col]
            colour = self.con if cells[row, col] else self.coff
            
            # apply rules
            if cells[row, col]:   # cell is alive
                
                if self.rules[0] <= alive_count <= self.rules[1]:                   # survival rule
                    updated_cells[row, col] = 1
                    if not paused: colour = self.con
                
                elif not paused:                                                    # death rule
                    colour = self.coff_next      
            
            else:    # cell is dead:
                
                if alive_count == self.rules[2]:                                    # birth rule
                    updated_cells[row, col] = 1
                    if not paused: colour = self.con
            
            # draw cell
            pg.draw.rect(self.screen, colour, (col * self.size,
                                               row * self.size,
                                               self.size - self.grid_lines,
                                               self.size - self.grid_lines))
            
            
            
        return updated_cells
    
    
    
    def fill_rnd(self, grid):
        
        # turn on rougly a sixth of the cells in the grid
        for _ in range(self.grid_width * self.grid_height // 6):
            
            # get random position
            row = randint(0, self.grid_height - 1)
            col = randint(0, self.grid_width - 1)
            
            grid[row, col] = 1
            
        return grid
    
    
    
    def run(self):
        
        # check for random variables or mystery box
        if self.mb or self.rule_rnd: self.rules = (a := randint(0,8),randint(a,8),randint(0,8))                          # rule
        if self.mb or self.size_rnd: self.size = randint(5,100)                                                          # size
        if self.mb or self.boundary_rnd: self.boundary = choice(["periodic", "dirichlet 0", "dirichlet 1", "neumann"])   # boundary                     
        if self.mb or self.cgrid_rnd: self.cgrid = (randint(0,255), randint(0,255), randint(0,255))                      # colour grid
        if self.mb or self.coff_rnd: self.coff = (randint(0,255), randint(0,255), randint(0,255))                        # colour off
        if self.mb or self.coff_next_rnd: self.coff_next = (randint(0,255), randint(0,255), randint(0,255))              # colour off next gen
        if self.mb or self.con_rnd: self.con = (randint(0,255), randint(0,255), randint(0,255))                          # colour on
        
        
        
        # create grid
        cells = np.zeros((self.grid_height, self.grid_width), dtype=int)
        
        
        
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
                    
                    
                # place cell in grid (left mousebutton)
                if pg.mouse.get_pressed()[0]:
                    pos = pg.mouse.get_pos()
                    cells[pos[1] // self.size, pos[0] // self.size] = 1
                
                # remove cell from grid (right mousebutton)
                elif pg.mouse.get_pressed()[2]:
                    pos = pg.mouse.get_pos()
                    cells[pos[1] // self.size, pos[0] // self.size] = 0
            
            
            
            # refresh screen
            self.screen.fill(self.cgrid)
            
            # if simulation is paused
            if paused:
                self.update_grid(cells, paused=True)               # draw grid but dont compute next generation
                self.update(fps=60)                                # raise fps to get mouse pos more effeciently
            
            # if simulation is not paused
            else:
                cells = self.update_grid(cells)                    # draw grid and compute next generation
                self.update()                                      # use user set fps