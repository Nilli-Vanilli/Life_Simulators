from classes.window import Window
import pygame as pg
import numpy as np
from random import randint

class Input_Matrix:
    
    # state and variable to store matrix
    locked = False
    locked_matrix = None
    
    def __init__(self, matrix: np.ndarray, rect: tuple) -> None:
        
        self.matrix = matrix
        
        self.dim = matrix.shape[0]
        
        self.rect = pg.Rect(rect)
        x, y, width, height = rect
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.size = self.width / self.dim
    
    
    
    def toggle_lock(self):
        
        # if in locked state, unlock and get stored matrix
        if self.locked:
            self.matrix = self.locked_matrix
            self.dim = self.matrix.shape[0] # reset dim
            self.size = self.width / self.dim # reset size
            self.locked = False
        
        # if in unlocked state, lock and store current matrix 
        else:
            self.locked_matrix = self.matrix
            self.matrix = np.zeros((10,10)) # initialise empty matrix for animation
            self.dim = 10 # set dim
            self.size = self.width / 10 # set size
            self.locked = True
            
            
    
    def add_dim(self):
        
        # add a new column and row to increase dim
        if self.dim < 10 and not self.locked: # cap dim at 10
            self.matrix = np.column_stack((self.matrix, np.zeros(self.dim)))
            self.matrix = np.row_stack((self.matrix, np.zeros(self.dim + 1)))
            self.dim += 1
            
            # decrease cell size
            self.size = self.width / self.dim
        
    
    
    def remove_dim(self):
        
        # remove column and row to decrease dim
        if self.dim > 1 and not self.locked: # make sure dim cant go below 1
            self.matrix = np.delete(self.matrix, -1, 0)
            self.matrix = np.delete(self.matrix, -1, 1)
            self.dim -= 1
            
            # increase cell size
            self.size = self.width / self.dim
    
    
    
    def draw_hover(self, window: Window, relative_pos: tuple):
        
        # unpack position of mouse relative to the matrix
        row, col = relative_pos
        
        # draw a box around cell where the mouse is hovering
        pg.draw.line(window.screen, window.colours.input_hover, (self.x + col * self.size, self.y + row * self.size), (self.x + col * self.size + self.size, self.y + row * self.size), 2)
        pg.draw.line(window.screen, window.colours.input_hover, (self.x + col * self.size, self.y + row * self.size), (self.x + col * self.size, self.y + row * self.size + self.size), 2)
        pg.draw.line(window.screen, window.colours.input_hover, (self.x + col * self.size, self.y + row * self.size + self.size), (self.x + col * self.size + self.size, self.y + row * self.size + self.size), 2)
        pg.draw.line(window.screen, window.colours.input_hover, (self.x + col * self.size + self.size, self.y + row * self.size), (self.x + col * self.size + self.size, self.y + row * self.size + self.size), 2)
            
            
    
    def check_mouseover(self, window: Window):
        
        # get position of mouse relative to the matrix, as well as button press
        pos = pg.mouse.get_pos() # relative pos will be stored as (row, column)
        relative_pos = (int((pos[1] - self.y) / self.size), int((pos[0] - self.x) / self.size))
        leftclick,_,rightclick = pg.mouse.get_pressed()
        
        # if mouse is hovering over matrix
        if self.rect.collidepoint(pos):
            
            # draw box around cell where the mouse is hovering
            self.draw_hover(window, relative_pos)
            
            # if left click, increase cell's value if possible
            if leftclick and self.matrix[relative_pos] < 0.98:
                    self.matrix[relative_pos] += 0.02
            
            # if right click, decrease cell's value if possible
            elif rightclick and self.matrix[relative_pos] > -0.98:
                    self.matrix[relative_pos] -= 0.02
        
    
    
    def draw_cells(self, screen: pg.Surface):
        
        # loop through all cells
        for row, col in np.ndindex(self.matrix.shape):
            
            # determine colour
            strength = abs(self.matrix[row, col]) * 255 # strength of colour depends on cell's value
            colour = (0,strength,0) if self.matrix[row, col] > 0 else (strength,0,0) # green if positive, red if negative
            
            # draw cell
            pg.draw.rect(screen, colour, (self.x + col * self.size + 1, # the 1's are the amount of pixels between cells
                                          self.y + row * self.size + 1, # and the border of the grid
                                          self.size - (self.dim + 1) / self.dim,
                                          self.size - (self.dim + 1) / self.dim))
            
    
    
    def draw_colourballs(self, screen: pg.Surface):
        
        # loop through all the different particle types
        for i in range(self.dim):
            
            # determine colour
            # evenly distribute over colour wheel
            colour = pg.Color(0,0,0); colour.hsla = (360 * i / self.dim, 100, 50, 100)
            
            # draw horizontal balls
            pg.draw.circle(screen, colour,
                           (self.x + i * self.size + self.size / 2,
                            self.y - self.height / 20),
                            self.height / 40)
            
            # draw vertical balls
            pg.draw.circle(screen, colour,
                           (self.x - self.width / 20,
                            self.y + i * self.size + self.size / 2),
                            self.width / 40)
        
    
    
    def animate_rnd_matrix(self):
        
        # get random matrix element
        coord = (randint(0, 9), randint(0, 9))
        
        # if number of elapsed seconds is uneven, increase element if possible
        if (pg.time.get_ticks()//1000) % 2 and self.matrix[coord] <= 0.8:
            self.matrix[coord] += 0.2
        
        # if number of elapsed seconds is even, decrease if possible
        elif self.matrix[coord] >= -0.8:
            self.matrix[coord] -= 0.2
    
    
    
    def draw(self, window: Window):
        
        # draw grid
        pg.draw.rect(window.screen, window.colours.underline,(self.x, self.y, self.width, self.height))
        
        # draw cells
        self.draw_cells(window.screen)
        
        # draw coloured balls
        self.draw_colourballs(window.screen)
        
        # if matrix not locked, allow user input
        if not self.locked:
            self.check_mouseover(window)
        
        # if matrix is locked, animate 'randomisation' of matrix (it's not real)
        else: self.animate_rnd_matrix()
        
        return self.matrix