# Bugs: If mouse not moved after click, thinks square still free if clicked again

import sys
from graphics import *

class Board:
	def __init__(self, board_size):
		self.board_size = board_size
		self.r_empty_board_lines = []			# horizontal lines
		self.d_empty_board_lines = []			# vertical lines
		self.r_chosen_board_lines = []
		self.d_chosen_board_lines = []
		self.win = None
		self.LINE_WIDTH = 4						# Constant
		self.create_board()
		return

	def create_board(self):
		board = [[0 for x in range(self.board_size)] for y in range(self.board_size)]
		board_lines = []
		self.win = GraphWin("GameBoard", self.board_size * 50, self.board_size * 50)
		self.win.setBackground(color_rgb(255, 255, 255))
		for x in range(self.board_size):
			for y in range(self.board_size):
				this_x = self.calculate_current_coordinate(x)
				this_y = self.calculate_current_coordinate(y)
				# Get next x,y circle coordinate to determine where to draw vertical/horizontal lines
				next_x = self.calculate_next_coordinate(x)
				next_y = self.calculate_next_coordinate(y)
				point = Point(this_x, this_y)
				c = Circle(point, 5)
				c.setFill(color_rgb(50, 50, 50))
				c.draw(self.get_win())
				# Right
				if x < self.board_size - 1:
					r_start = Point(this_x+8, this_y) 	# start at outer edge of first circle
					r_end = Point(next_x-8, this_y)
					r_line = Rectangle(r_start, r_end)
					r_line.setOutline(color_rgb(225, 225, 225))
					r_line.setWidth(self.LINE_WIDTH)
					self.r_empty_board_lines.append(r_line)
					r_line.draw(self.get_win())
				# Down
				if y < self.board_size - 1:
					d_start = Point(this_x, this_y+8)
					d_end = Point(this_x, next_y-8)
					d_line = Rectangle(d_start, d_end)
					d_line.setOutline(color_rgb(225, 225, 225))
					d_line.setWidth(self.LINE_WIDTH)
					self.d_empty_board_lines.append(d_line)
					d_line.draw(self.get_win())
		self.print_board_lines()
		#print("Hello?")
		return

	# Calculates current circle coordinate based on x/y input
	def calculate_current_coordinate(self, coordinate_point):
		return self.board_size*10 + coordinate_point*35

	# Calculates next circle coordinate using x/y input.
	# Differs from current_coordinate to account for graph edges (using % to wrap around)
	# and for slight shift in where line ends (+1)
	def calculate_next_coordinate(self, coordinate_point):
		return self.board_size*10 + ((coordinate_point+1)%(self.board_size))*35 # Mod to circle around number of circles in row

	def get_win(self):
		return self.win

	def get_board_size(self):
		return self.board_size

	# Returns Line object based on click input
	# Returns None if click does not match any lines
	def get_line(self, click):
		x = click.getX()
		y = click.getY()
		x_range = False
		y_range = False
		# Check if click touches any horizontal lines first
		for line in self.get_r_empty_board_lines():
			if x >= line.getP1().getX() and x <= line.getP2().getX():
				x_range = True	# within x range
			if y >= line.getP1().getY() and y <= line.getP2().getY() + self.LINE_WIDTH:
				y_range = True
			if x_range and y_range:
				return line
		# Now check if click touches vertical
		for line in self.get_d_empty_board_lines():
			if x >= line.getP1().getX() and x <= line.getP2().getX():
				x_range = True	# within x range
			if y >= line.getP1().getY() and y <= line.getP2().getY() + self.LINE_WIDTH:
				y_range = True
			if x_range and y_range:
				return line
		return None

	# Returns "h" for horizontal line, "v" for vertical line
	# Returns None if invalid line (diagonal)
	def get_line_orientation(self, line):
		# Y-coordinates same at either end, so horizontal
		if line.getP1().getY() == line.getP2().getY():
			return "h"
		elif line.getP1().getX() == line.getP2().getX():
			return "v"
		else:
			print("Invalid line. Unable to determine line orientation.")
			return None

	def get_r_empty_board_lines(self):
		return self.r_empty_board_lines

	def get_d_empty_board_lines(self):
		return self.d_empty_board_lines

	def get_r_chosen_board_lines(self):
		return self.r_chosen_board_lines

	def get_d_chosen_board_lines(self):
		return self.d_chosen_board_lines

	def get_num_empty_lines(self):
		return len(self.get_d_empty_board_lines()) + len(self.get_r_empty_board_lines())

	def get_num_chosen_lines(self):
		return len(self.get_d_chosen_board_lines()) + len(self.get_r_chosen_board_lines())

	# Updates line arrays (removes from empty and appends to chosen lines)
	# TODO: Draws chosen line on board
	def update_board(self, line, line_orientation, player_id):
		# Horizontal lines
		if line_orientation == "h":
			self.r_empty_board_lines.remove(line)
			self.r_chosen_board_lines.append(line)
		elif line_orientation == "v":
			self.d_empty_board_lines.remove(line)
			self.d_chosen_board_lines.append(line)
		# Update line drawing
		new_line = Rectangle(line.getP1(), line.getP2())
		if player_id == 0:
			new_line.setOutline(color_rgb(38, 181, 172))
		elif player_id == 1:
			r_line.setOutline(color_rgb(119, 181, 38))
		new_line.setWidth(self.LINE_WIDTH)
		new_line.draw(self.get_win())
		return

	def print_board_lines(self):
		for line in self.get_r_empty_board_lines():
			print("Line: Start = ", line.getP1().getX(), line.getP1().getY(), "End = ", line.getP2().getX(), line.getP2().getY())
		for line in self.get_d_empty_board_lines():
			print("Line: Start = ", line.getP1().getX(), line.getP1().getY(), "End = ", line.getP2().getX(), line.getP2().getY())
		return

	def print_chosen_board_lines(self):
		for line in self.get_r_chosen_board_lines():
			print("Line: Start = ", line.getP1().getX(), line.getP1().getY(), "End = ", line.getP2().getX(), line.getP2().getY())
		for line in self.get_d_chosen_board_lines():
			print("Line: Start = ", line.getP1().getX(), line.getP1().getY(), "End = ", line.getP2().getX(), line.getP2().getY())
		return

class Player:
	def __init__(self, player_id):
		self.score = 0
		self.plays = []
		self.id = player_id

	def add_score(self, score_increment):
		self.score = self.score + score_increment
		return

	def update_plays(self, new_line):
		self.plays.append(new_line)

class Game:
	def __init__(self, board_size):
		self.board = Board(board_size)
		self.player1 = Player(0)
		self.player2 = Player(1)
		self.start_game()

	def start_game(self):
		print("Let's begin!")

		empty_line_count = self.board.get_num_empty_lines()
		print(empty_line_count)
		chosen_line_count = self.board.get_num_chosen_lines()
		print(chosen_line_count)

		while chosen_line_count <= self.board.get_board_size() * self.board.get_board_size():
			print("Player 1: Click on an empty line.")
			click = self.board.get_win().getMouse()
			clicked_line = self.board.get_line(click)
			isValid = self.check_filled_lines(click)
			if clicked_line != None and isValid:
				print("This line has not been clicked.")
				line_orientation = self.board.get_line_orientation(clicked_line)
				self.board.update_board(clicked_line, line_orientation, 0)
				#if check_complete_square(click)
			empty_line_count = self.board.get_num_empty_lines()
			print(empty_line_count)
			chosen_line_count = self.board.get_num_chosen_lines()
			print(chosen_line_count)
			# print("Player 2: Click on an empty line.")
			# click = self.board.get_win().getMouse()
			# isWithinRange = self.check_line_range(click)
			# isValid = self.check_filled_lines(click)
			# if isWithinRange and isValid:
			# 	print("Yes.")

		print("Game finished! The winner is...")
		return

	# Check if that line has already been picked
	def check_filled_lines(self, click):
		if click in self.board.get_d_chosen_board_lines():
			return False
		elif click in self.board.get_r_chosen_board_lines():
			return False
		return True

	def check_complete_square(self, click):
		return

def main():
	board_size = input("Enter size of board (ranging between 2-10):")
	while (int(board_size) <= 2) or (int(board_size) >= 10):
		print("Invalid number. Try again, or press 'q' to quit game.")
		board_size = input("Enter size of board (ranging between 2-10):")
		if (board_size == "q"):
			exit()
	game = Game(int(board_size))

	#win.getMouse()
	#win.close()

if __name__ == '__main__':
	main()

