import pygame as pg
from random import randint, choice
import numpy as np



class ECA():
    
    # colours
    cgrid = (40, 40, 40)
    coff = (170, 170, 170)
    con = (255, 255, 255)
    
    # random variables
    mb = False
    rule_rnd = False
    size_rnd = False
    start_indices_rnd = False
    boundary_rnd = False
    cgrid_rnd = False
    coff_rnd = False
    con_rnd = False
        
        
        
    def __init__(self, window, rule: str, size: int, start_indices: list, boundary: str, fps_cap: int, middle=True, grid_lines=True) -> None:
        
        self.window = window
        
        self.rule = rule
        self.size = size
        self.start_indices = start_indices
        self.boundary = boundary
        self.fps_cap = fps_cap
        
        self.start_indices_middle = middle
        
        self.grid_lines = 1 if grid_lines else 0
        
        self.width = window.width // self.size
        self.height = window.height // self.size
        
        
        
    # update grid
    def update_grid(self, full_grid):
    
        # consider last row of grid as current generation
        cells = full_grid[-1]
        
        # store next generation
        updated_cells = np.zeros(len(cells), dtype=int)
        
        # apply boundary condition
        match self.boundary:
            
            case "periodic": left = -1; right = 0
            case "dirichlet 0": left = right = 0
            case "dirichlet 1": left = right = 1
            case "neumann": left = 0; right = -1
        
        
        
        # loop through cells and get neighbourhood
        for i in range(len(cells)):
            
            if i == 0:
                neighbourhood = str(cells[left]) + str(cells[0]) + str(cells[1])      # left edge
            
            elif i == len(cells) - 1:
                neighbourhood = str(cells[-2]) + str(cells[-1]) + str(cells[right])   # right edge
                
            else:
                neighbourhood = str(cells[i - 1]) + str(cells[i]) + str(cells[i + 1]) # remaining cells  
                
            # update state
            updated_cells[i] = self.rule[7 - int(neighbourhood, base=2)]
            
        
        
        # update grid
        updated_full_grid = np.delete(full_grid, 0, 0)
        updated_full_grid = np.vstack([updated_full_grid, updated_cells])
            
        return updated_full_grid
    
    
    
    def draw_grid(self, grid):
        
        # loop through all cells in grid
        for row, col in np.ndindex(grid.shape):
            
            # determine colour and draw cell
            colour = self.con if grid[row, col] == 1 else self.coff
            pg.draw.rect(self.window.screen, colour, (col * self.size,
                                                      row * self.size,
                                                      self.size - self.grid_lines,
                                                      self.size - self.grid_lines))
            
    
    
    def check_rnd(self):
        
        # check for random variables or mystery box
        if self.mb or self.rule_rnd: self.rule = f"{randint(0,255):08b}"                                                       # rule
        if self.mb or self.size_rnd: self.size = randint(5,100)                                                                # size
        if self.mb or self.boundary_rnd: self.boundary = choice(["periodic", "dirichlet 0", "dirichlet 1", "neumann"])         # boundary
        if self.mb or self.cgrid_rnd: self.cgrid = (randint(0,255), randint(0,255), randint(0,255))                            # colour grid
        if self.mb or self.coff_rnd: self.coff = (randint(0,255), randint(0,255), randint(0,255))                              # colour off
        if self.mb or self.con_rnd: self.con = (randint(0,255), randint(0,255), randint(0,255))                                # colour on
        if self.mb or self.start_indices_rnd: self.start_indices = [randint(0, self.width - 1) for _ in range(randint(1,4))]   # start indices
        
        # if start index not random, check if middle is set to true
        elif self.start_indices_middle: self.start_indices = [self.width // 2]
    
    
    
    # run simulation
    def run(self):
        
        # check for random variables or mystery box
        self.check_rnd()
        
        # update width and height
        self.width = self.window.width // self.size
        self.height = self.window.height // self.size
        
        # create grid
        cells = np.zeros((self.height, self.width), dtype=int)
        
        # turn on cells with start indices
        for index in self.start_indices:
            cells[-1][index] = 1
                

        
        #running loop
        paused = False
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
                    
                    # randomise rule (r)
                    elif event.key == pg.K_r:
                        self.rule = f"{randint(0,255):08b}"


 
            # refresh screen
            self.window.screen.fill(self.cgrid)
            
            # if simulation is not paused, compute next generation
            if not paused:
                cells = self.update_grid(cells)
            
            # draw grid
            self.draw_grid(cells)
                
            # update screen
            self.window.update(self.fps_cap)