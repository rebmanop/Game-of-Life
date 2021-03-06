import pygame
from cell import Cell

GRID_FRAME_COLOR = (64, 64, 64)
LINE_COLOR = (153, 153, 153)

GRID_FRAME_WIDTH = 5

class Grid:
    def __init__(self, win, grid_size, grid_dimensions, grid_position):
        self.win = win 
        self.grid_size = grid_size
        self.total_rows, self.total_columns = grid_size
        self.width, self.height  = grid_dimensions
        self.gap = self.width // self.total_columns
        self.line_color = LINE_COLOR
        self.grid_position = grid_position
        self.x, self.y = self.grid_position
        self.raw_grid  = self.init_cells()
        

    def init_cells(self):

        """Populates grid with cell objects"""

        raw_grid = []

        for i in range(self.total_rows):
            raw_grid.append([])
            for j in range(self.total_columns):
                raw_grid[i].append(Cell(i, j, self.gap, self.grid_size, self.grid_position))

        return raw_grid
        

    def draw_grid_lines(self) -> None:

        """Draws horizontal and vertical grid lines"""

        for i in range(self.total_rows + 1):
            pygame.draw.line(self.win, self.line_color, (self.x, self.y + i * self.gap), (self.x + self.width, self.y + i * self.gap))
            for j in range(self.total_columns + 1):
                pygame.draw.line(self.win, self.line_color, (self.x + j * self.gap, self.y), (self.x + j * self.gap, self.y + self.height))

 
    def update_alive_neighbors_list_for_every_cell(self) -> None:
        for row in self.raw_grid:
            for cell in row:
                cell.update_list_of_alive_neighbors(self.raw_grid)


    def draw_all_cells(self) -> None:

        for row in self.raw_grid:
            for cell in row:
                cell.draw(self.win)


    def get_cell(self, row: int, col: int) -> Cell:

        """Returns cell object based on row and column"""

        return self.raw_grid[row][col]
    

    def get_rc_of_under_mouse_cell(self, mpos) -> tuple:
        
        """Returns row and column of under the mouse cell based on mouse position"""
        
        x, y = mpos

        row =  (y - self.y) // self.gap
        col = (x - self.x) // self.gap
        
        return int(row), int(col) 
    
    
    def clear(self) -> None:
        for row in self.raw_grid:
            for  cell in row: 
                    cell.kill()


    def draw_grid_frame(self) -> None:
        pygame.draw.line(self.win, GRID_FRAME_COLOR, ((self.x - 3, self.y)), (self.x - 3, self.y + self.height), width=GRID_FRAME_WIDTH)
        pygame.draw.line(self.win, GRID_FRAME_COLOR, ((self.x + self.width + 3, self.y)), (self.x + self.width + 3, self.y + self.height), width=GRID_FRAME_WIDTH)
        pygame.draw.line(self.win, GRID_FRAME_COLOR, ((0,self.y - 2)), (self.win.get_width(), self.y - 2), width=GRID_FRAME_WIDTH)
        pygame.draw.line(self.win, GRID_FRAME_COLOR, ((0, self.y + self.height + 2)), (self.win.get_width(), self.y + self.height + 2), width=GRID_FRAME_WIDTH)


    def mouse_on_the_grid(self) -> bool:

        """Checks if mouse on the grid"""
        
        mpos = pygame.mouse.get_pos()
        if (mpos[0] > self.x and mpos[0] < (self.x + self.width) 
        and mpos[1] > self.y and mpos[1] < (self.y + self.height)):
            return True
        else:
            return False


    def __getitem__(self, row):
        return self.raw_grid[row]


