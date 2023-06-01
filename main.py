import pygame
import math
import color_values
from algorithms import heuristic, algorithm

DIM = 800
WIN = pygame.display.set_mode((DIM, DIM))
pygame.display.set_caption('A*')

class Cell:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = color_values.WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        
    def position(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == color_values.CYAN
    
    def is_open(self):
        return self.color == color_values.CYAN
    
    def is_barrier(self):
        return self.color == color_values.BLACK
    
    def is_start(self):
        return self.color == color_values.BROWN
    
    def is_end(self):
        return self.color == color_values.FORESTGREEN
    
    def reset(self):
        self.color = color_values.WHITE
        
    def make_closed(self):
        self.color = color_values.DARKCYAN
        
    def make_open(self):
        self.color = color_values.LIGHTCHARCOAL
        
    def make_barrier(self):
        self.color = color_values.BLACK
        
    def make_start(self):
        self.color = color_values.BROWN
        
    def make_end(self):
        self.color = color_values.FORESTGREEN
        
    def make_path(self):
        self.color = color_values.YELLOW
        
    def make_gold(self):
        self.color = color_values.GOLD
        
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))
        
    def update_neighbors(self, grid): 
        self.neighbors = []
        
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col]) # down
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col]) # up
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1]) # right
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1]) # left 
    
    def __lt__(self, other):
        return False
    
def make_grid(total_rows, dim):
    grid = []
    dim_per_node = dim // total_rows
    for i in range(total_rows):
        grid.append([])
        for j in range(total_rows):
            cell = Cell(i, j, dim_per_node, total_rows)
            grid[i].append(cell)

    return grid

def draw_grid(window, total_rows, dim):
    dim_per_node = dim // total_rows
    
    for i in range(total_rows):
        pygame.draw.line(window, color_values.GRAY, (0, i * dim_per_node), (dim, i * dim_per_node))
        for j in range(total_rows):
            pygame.draw.line(window, color_values.GRAY, (j * dim_per_node, 0), (j * dim_per_node, dim))
            
def draw(window, grid, total_rows, dim):
    window.fill(color_values.WHITE)
    
    for row in grid:
        for cell in row:
            cell.draw(window)
            
    draw_grid(window, total_rows, dim)
    pygame.display.update()
    
def getPositionFromClick(mouse_position, total_rows, dim):
    dim_per_node = dim // total_rows
    y, x = mouse_position
    
    row = y // dim_per_node
    col = x // dim_per_node
    
    return row, col
    
def main(window, dim):
    TOTAL_ROWS = 40
    grid = make_grid(TOTAL_ROWS, dim)
    
    start, end = None, None
    run, started = True, False
    
    while run:
        draw(window, grid, TOTAL_ROWS, dim)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if started: continue
            
            if pygame.mouse.get_pressed()[0]: # left mouse button
                pos = pygame.mouse.get_pos()
                row, col = getPositionFromClick(pos, total_rows=TOTAL_ROWS, dim=dim)
                cell = grid[row][col]
                if not start:
                    start = cell
                    start.make_start()
                    
                elif not end and cell is not start:
                    end = cell
                    end.make_end()
                    
                elif cell != end and cell != start:
                    cell.make_barrier()
                
            elif pygame.mouse.get_pressed()[2]: # right mouse button
                pos = pygame.mouse.get_pos()
                row, col = getPositionFromClick(pos, total_rows=TOTAL_ROWS, dim=dim)
                cell = grid[row][col]
                cell.reset()
                if cell == start:
                    start = None
                    
                if cell == end:
                    end = None
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)
                    algorithm(lambda : draw(window=window, grid=grid, total_rows=TOTAL_ROWS, dim=dim), grid, start, end)
                    
            
    pygame.quit()
                
if __name__ == '__main__':
    pygame.init()
    main(WIN, DIM)