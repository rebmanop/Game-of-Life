import pygame

DEAD_COLOR = (126, 126, 126)
ALIVE_COLOR = (255, 255, 0)


class Cell:
	def __init__(self, row, col, width, grid_size, grid_position):
		self.row = row
		self.col = col
		self.width = width
		self.total_rows, self.total_columns = grid_size
		self.color = DEAD_COLOR
		self.alive_neighbors = []
		self.x = grid_position[0] + self.col * self.width
		self.y = grid_position[1] + self.row * self.width
	

	def get_pos(self):
		return self.row, self.col


	def is_dead(self):
		return self.color == DEAD_COLOR
	
	def is_alive(self):
		return self.color == ALIVE_COLOR


	def resurrect(self):
		self.color = ALIVE_COLOR

	def kill(self):
		self.color = DEAD_COLOR


	def draw(self, win):
		"""Draws individual cell to the screen"""
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


	def number_of_alive_neighbors(self):
		return len(self.alive_neighbors)


	def update_list_of_alive_neighbors(self, grid):
		
		"""Updates list of alive neighbors for this cell"""
		
		self.alive_neighbors.clear()

		if self.row < self.total_rows - 1 and grid[self.row + 1][self.col].is_alive(): #down
			self.alive_neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and grid[self.row - 1][self.col].is_alive(): #up
			self.alive_neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_columns - 1 and grid[self.row][self.col + 1].is_alive(): #right
			self.alive_neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and  grid[self.row][self.col - 1].is_alive(): #left
			self.alive_neighbors.append(grid[self.row][self.col - 1])

		if self.col > 0 and self.row > 0 and grid[self.row - 1][self.col - 1].is_alive(): #up_left
			self.alive_neighbors.append(grid[self.row][self.col - 1])

		if self.col < self.total_columns - 1 and self.row > 0 and grid[self.row - 1][self.col + 1].is_alive(): #up_right
			self.alive_neighbors.append(grid[self.row][self.col + 1])

		if self.col < self.total_columns - 1 and self.row < self.total_rows - 1 and grid[self.row + 1][self.col + 1].is_alive(): #down_right
			self.alive_neighbors.append(grid[self.row + 1][self.col + 1])

		if self.col > 0 and self.row < self.total_rows - 1 and grid[self.row + 1][self.col - 1].is_alive(): #down_left
			self.alive_neighbors.append(grid[self.row + 1][self.col - 1])








	
	

