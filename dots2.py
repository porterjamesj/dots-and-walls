import sys
from graphics import *

class Board:
	def __init__(self, board_size):
		self.board_size = board_size
		self.empty_lines = []
		self.chosen_lines = []
		self.win = None
		self.LINE_WIDTH = 6
		self.create_board()
		return

	def get_win(self):
		return self.win

	def get_line_from_click(self, click, line_array):
		x = click.getX()
		y = click.getY()
		x_range = False
		y_range = False

		for line in line_array:
			# Check vertical lines in array
			if line.getP1().getX() == line.getP2().getX():
				# Check if click matches range in line's horizontal width (gives some padding)
				#print("x is greater than ", line.getP1().getX() - 2, "and less than ", line.getP1().getX() + 2)
				if (x >= (line.getP1().getX() - 4)) and (x <= (line.getP1().getX() + 4)):
					x_range = True
				#print("y is greater than ", line.getP1().getY(), "and less than ", line.getP2().getY())
				if y >= line.getP1().getY() and y <= line.getP2().getY():
					y_range = True
				if x_range and y_range:
					return line

			# Check horizontal lines in array
			elif line.getP1().getY() == line.getP2().getY():
				# Check if click matches range in line's vertical width
				if (y >= (line.getP1().getY() - 4)) and (y <= (line.getP1().getY() + 4)):
					y_range = True
				if x >= line.getP1().getX() and x <= line.getP2().getX():
					x_range = True
				if x_range and y_range:
					return line

			# Reset checks at end of each loop
			x_range = False
			y_range = False

		# Click does not match within any line range
		print("No line found.")
		return None

	def get_line(self, clicked_line):
		x1 = clicked_line.getP1().getX()
		y1 = clicked_line.getP1().getY()
		x2 = clicked_line.getP2().getX()
		y2 = clicked_line.getP2().getY()
		x_range = False
		y_range = False

		for line in self.chosen_lines:
			if x1 == line.getP1().getX() and y1 == line.getP1().getY() and x2 == line.getP2().getX() and y2 == line.getP2().getY():
				if line.getP1().getX() == line.getP2().getX():
					print("It's a match! Neighbor line matches vertical line in chosen_lines")
				elif line.getP1().getY() == line.getP2().getY():
					print("It's a match! Neighbor line matches horizontal line in chosen_lines")
				return line

		print("No line found.")
		return None

	# Completely wacky, beware
	def get_a_line(self, clicked_line):
		x = clicked_line.getP1().getX()
		y = clicked_line.getP1().getY()
		x_range = False
		y_range = False

		for line in self.chosen_lines:
			# Check vertical lines in array
			if line.getP1().getX() == line.getP2().getX():
				# Check if click matches range in line's horizontal width (gives some padding)
				#print("x is greater than ", line.getP1().getX() - 2, "and less than ", line.getP1().getX() + 2)
				if (x >= (line.getP1().getX() - 4)) and (x <= (line.getP1().getX() + 4)):
					x_range = True
				#print("y is greater than ", line.getP1().getY(), "and less than ", line.getP2().getY())
				if y >= line.getP1().getY() and y <= line.getP2().getY():
					y_range = True
				if x_range and y_range:
					print("Neighbor line matches vertical line in chosen_lines")
					return line

			# Check horizontal lines in array
			elif line.getP1().getY() == line.getP2().getY():
				# Check if click matches range in line's vertical width
				if (y >= (line.getP1().getY() - 4)) and (y <= (line.getP1().getY() + 4)):
					y_range = True
				if x >= line.getP1().getX() and x <= line.getP2().getX():
					x_range = True
				if x_range and y_range:
					print("Neighbor line matches horizontal line in chosen_lines")
					return line

			# Reset checks at end of each loop
			x_range = False
			y_range = False

		# Click does not match within any line range
		print("No line found.")
		return None

	def get_num_empty_lines(self):
		return len(self.empty_lines)

	def get_num_chosen_lines(self):
		return len(self.chosen_lines)

	def get_empty_lines(self):
		return self.empty_lines

	def get_chosen_liens(self):
		return self.chosen_lines

	def get_chosen_lines(self):
		return self.chosen_lines

	def get_board_size(self):
		return self.board_size

	def create_board(self):
		self.win = GraphWin("Dots and Walls", self.board_size * 100, self.board_size * 100)
		self.win.setBackground(color_rgb(255, 255, 255))
		point = None
		circles = []

		for x in range(self.board_size):
			for y in range(self.board_size):

				current_x = self.calculate_current_coordinate(x)
				current_y = self.calculate_current_coordinate(y)
				print("Current x, y = ", current_x, current_y)

				# Draw points (circles) on screen
				prev_point = point
				point = Point(current_x, current_y)
				c = Circle(point, 5)
				c.setFill(color_rgb(50, 50, 50))
				circles.append(c)

				# Draw lines on screen
				if (prev_point != None):
					# Draw vertical lines
					if y < self.board_size and point.getY() >= prev_point.getY():
						v_line = Line(prev_point, point)
						v_line.setOutline(color_rgb(225, 225, 225))
						v_line.setWidth(self.LINE_WIDTH)
						v_line.draw(self.get_win())
						# Add to array of empty lines
						self.empty_lines.append(v_line)

					# Draw horizontal lines
					if x < self.board_size - 1 and point.getX() >= prev_point.getX():
						h_end = Point(self.calculate_current_coordinate(x+1), prev_point.getY())
						h_line = Line(prev_point, h_end)
						h_line.setOutline(color_rgb(225, 225, 225))
						h_line.setWidth(self.LINE_WIDTH)
						h_line.draw(self.get_win())
						# Add to array of empty lines
						self.empty_lines.append(h_line)

		# Draw circles on screen
		# (Keeps circle on top of lines by drawing until the end)
		for c in circles:
			c.draw(self.get_win())

		# TODO: Remove or move to other fn:
		self.print_empty_lines()
		return

	def update_board(self, clicked_line, player_id):
		# Update arrays
		self.chosen_lines.append(clicked_line)
		self.empty_lines.remove(clicked_line)

		# Print initial line counts
		empty_line_count = self.get_num_empty_lines()
		print("Arrays updated.")
		print("# Empty lines:",empty_line_count)
		chosen_line_count = self.get_num_chosen_lines()
		print("# Chosen lines",chosen_line_count)

		# Update screen
		line = Line(clicked_line.getP1(), clicked_line.getP2())
		if player_id == 0:
			line.setOutline(color_rgb(38, 181, 172))
		elif player_id == 1:
			line.setOutline(color_rgb(119, 181, 38))
		line.setWidth(self.LINE_WIDTH)
		line.draw(self.get_win())

		print("\n")
		self.print_chosen_lines()
		print("\n")

		return

	def calculate_current_coordinate(self, coordinate_point):
		return self.board_size * 10 + coordinate_point * 50

	def calculate_original_coordinate(self, graph_coordinate):
		return int((graph_coordinate - (self.board_size * 10)) / 50)

	def print_empty_lines(self):
		for line in self.get_empty_lines():
			print("Line start = ", line.getP1().getX(), line.getP1().getY(), "End = ", line.getP2().getX(), line.getP2().getY())
		return

	def print_chosen_lines(self):
		print("Chosen lines tracker:")
		for line in self.get_chosen_lines():
			print("Line start = ", line.getP1().getX(), line.getP1().getY(), "End = ", line.getP2().getX(), line.getP2().getY())
		return

class Player:
	def __init__(self, player_id):
		self.score = 0
		self.id = player_id

	def add_score(self, score_increment):
		self.score = self.score + score_increment

class Game:
	def __init__(self, board_size):
		self.board = Board(board_size)
		self.player1 = Player(0)
		self.player2 = Player(1)
		self.start_game()
		return

	def start_game(self):
		print("Let's begin!")

		# Print initial line counts
		empty_line_count = self.board.get_num_empty_lines()
		print("# Empty:",empty_line_count)
		chosen_line_count = self.board.get_num_chosen_lines()
		print("# Chosen:",chosen_line_count)

		# Begin game until all board lines chosen
		while chosen_line_count <= self.board.get_board_size() * self.board.get_board_size():
			print("\nPlayer 1: Click on an empty line.")
			click = self.board.get_win().getMouse()
			print("x, y:", click.getX(), click.getY())
			clicked_line = self.board.get_line_from_click(click, self.board.empty_lines)
			if clicked_line != None:
				isValid = self.check_chosen_lines(clicked_line)
				if isValid:
					print("This line has not been clicked. Proceed.")
					self.board.update_board(clicked_line, 0)
					isSquare = self.check_complete_square(clicked_line, 0)
				else:
					print("Line has already been clicked.")

	def check_chosen_lines(self, clicked_line):
		if clicked_line in self.board.get_chosen_lines():
			return False
		return True

	def check_complete_square(self, clicked_line, player_id):
		# Grab original coordinate points for x, then
		# Recalculate to get next x/y neighbor
		this_x1 = clicked_line.getP1().getX()
		this_x2 = clicked_line.getP2().getX()
		orig_x1_coordinate = self.board.calculate_original_coordinate(this_x1)
		orig_x2_coordinate = self.board.calculate_original_coordinate(this_x2)

		print("this_x1:", this_x1)
		print("this_x2:", this_x2)

		print("original_x1 coordinate:", orig_x1_coordinate)
		print("original_x2 coordinate:", orig_x2_coordinate)
		print("\n")
		
		# Do same for y
		this_y1 = clicked_line.getP1().getY()
		this_y2 = clicked_line.getP2().getY()
		orig_y1_coordinate = self.board.calculate_original_coordinate(this_y1)
		orig_y2_coordinate = self.board.calculate_original_coordinate(this_y2)

		print("this_y1:", this_y1)
		print("this_y2:", this_y2)

		print("original_y1 coordinate:", orig_y1_coordinate)
		print("original_y2 coordinate:", orig_y2_coordinate)
		print("\n")
		
		# If vertical line:
		if this_x1 == this_x2:
			print("This is a VERTICAL line. Gathering neighbors...\n")

			# Left
			left_neighbor_x1 = self.board.calculate_current_coordinate(orig_x1_coordinate - 1)
			left_pt1 = Point(left_neighbor_x1, this_y1)
			left_pt2 = Point(left_neighbor_x1, this_y2)
			left = self.board.get_line(Line(left_pt1, left_pt2))
			print("Left neighbor line start: ", left_neighbor_x1, this_y1, " | end: ", left_neighbor_x1, this_y2)
				
			# Right
			right_neighbor_x1 = self.board.calculate_current_coordinate(orig_x1_coordinate + 1)
			right_pt1 = Point(right_neighbor_x1, this_y1)
			right_pt2 = Point(right_neighbor_x1, this_y2)
			right = self.board.get_line(Line(right_pt1, right_pt2))
			print("Right neighbor line start: ", right_neighbor_x1, this_y1, " | end: ", right_neighbor_x1, this_y2)

			# Top-left (a horizontal line)
			top_left_neighbor_x1 = self.board.calculate_current_coordinate(orig_x1_coordinate - 1)
			top_left_pt1 = Point(top_left_neighbor_x1, this_y1)
			top_left_pt2 = Point(this_x1, this_y1)
			top_left = self.board.get_line(Line(top_left_pt1, top_left_pt2))
			print("Top-left neighbor line start: ", top_left_neighbor_x1, this_y1, " | end: ", this_x1, this_y1)

			# Top-right (a horizontal line)
			top_right_neighbor_x2 = self.board.calculate_current_coordinate(orig_x1_coordinate + 1)
			top_right_pt1 = Point(this_x1, this_y1)
			top_right_pt2 = Point(top_right_neighbor_x2, this_y1)
			top_right = self.board.get_line(Line(top_right_pt1, top_right_pt2))
			print("Top-right neighbor line start: ", this_x1, this_y1, " | end: ", top_right_neighbor_x2, this_y1)

			# Bottom-left (a horizontal line)
			bottom_left_neighbor_x2 = self.board.calculate_current_coordinate(orig_x1_coordinate - 1)
			bottom_left_pt1 = Point(bottom_left_neighbor_x2, this_y2)
			bottom_left_pt2 = Point(this_x2, this_y2)
			bottom_left = self.board.get_line(Line(bottom_left_pt1, bottom_left_pt2))
			print("Bottom-left neighbor line start: ", bottom_left_neighbor_x2, this_y2, " | end: ", this_x2, this_y2)

			# Bottom-right (a horizontal line)
			bottom_right_neighbor_x2 = self.board.calculate_current_coordinate(orig_x1_coordinate + 1)
			bottom_right_pt1 = Point(this_x2, this_y2)
			bottom_right_pt2 = Point(bottom_right_neighbor_x2, this_y2)
			bottom_right = self.board.get_line(Line(bottom_right_pt1, bottom_right_pt2))
			print("Bottom-right neighbor line start: ", this_x2, this_y2, " | end: ", bottom_right_neighbor_x2, this_y2)

			print("\nThe following are lines already in chosen_lines:")
			if right in self.board.chosen_lines:
				print("Vertical right")
			if left in self.board.chosen_lines:
				print("Vertical left")
			if top_right in self.board.chosen_lines:
				print("Horizontal top right")
			if top_left in self.board.chosen_lines:
				print("Horizontal top left")
			if bottom_right in self.board.chosen_lines:
				print("Horizontal bottom right")
			if bottom_left in self.board.chosen_lines:
				print("Horizontal bottom left")

			# Check for completed squares
			if right in self.board.chosen_lines and top_right in self.board.chosen_lines and bottom_right in self.board.chosen_lines:
				print("SQUARE!")
			if left in self.board.chosen_lines and top_left in self.board.chosen_lines and bottom_left in self.board.chosen_lines:
				print("BOTTOM SQUARE!")

		# Horizontal lines
		elif this_y1 == this_y2:
			print("This is a HORIZONTAL line. Gathering neighbors...\n")

			# Top
			top_neighbor_y1 = self.board.calculate_current_coordinate(orig_y1_coordinate - 1)
			top_pt1 = Point(this_x1, top_neighbor_y1)
			top_pt2 = Point(this_x2, top_neighbor_y1)
			top = self.board.get_line(Line(top_pt1, top_pt2))
			print("Top neighbor line start: ", this_x1, top_neighbor_y1, " | end: ", this_x2, top_neighbor_y1)
		
			# Bottom
			bottom_neighbor_y1 = self.board.calculate_current_coordinate(orig_y1_coordinate + 1)
			bottom_pt1 = Point(this_x1, bottom_neighbor_y1)
			bottom_pt2 = Point(this_x2, bottom_neighbor_y1)
			bottom = self.board.get_line(Line(bottom_pt1, bottom_pt2))
			print("Bottom neighbor line start: ", this_x1, bottom_neighbor_y1, " | end: ", this_x2, bottom_neighbor_y1)
			
			# Top-left (a vertical line)
			top_left_neighbor_y1 = self.board.calculate_current_coordinate(orig_y1_coordinate - 1)
			top_left_pt1 = Point(this_x1, top_left_neighbor_y1)
			top_left_pt2 = Point(this_x1, this_y1)
			top_left = self.board.get_line(Line(top_left_pt1, top_left_pt2))
			print("Top-left neighbor line start: ", this_x1, top_left_neighbor_y1, " | end: ", this_x1, this_y1)
			
			# Top-right (a vertical line)
			top_right_neighbor_y1 = self.board.calculate_current_coordinate(orig_y1_coordinate - 1)
			top_right_pt1 = Point(this_x2, top_right_neighbor_y1)
			top_right_pt2 = Point(this_x2, this_y1)
			top_right = self.board.get_line(Line(top_right_pt1, top_right_pt2))
			print("Top-right neighbor line start: ", this_x2, top_right_neighbor_y1, " | end: ", this_x2, this_y1)
			
			# Bottom-left (a vertical line)
			bottom_left_neighbor_y2 = self.board.calculate_current_coordinate(orig_y1_coordinate + 1)
			bottom_left_pt1 = Point(this_x1, this_y1)
			bottom_left_pt2 = Point(this_x1, bottom_left_neighbor_y2)
			bottom_left = self.board.get_line(Line(bottom_left_pt1, bottom_left_pt2))
			print("Bottom-left neighbor line start: ", this_x1, this_y1, " | end: ", this_x1, bottom_left_neighbor_y2)
			
			# Bottom-right (a vertical line)
			bottom_right_neighbor_y2 = self.board.calculate_current_coordinate(orig_y1_coordinate + 1)
			bottom_right_pt1 = Point(this_x2, this_y2)
			bottom_right_pt2 = Point(this_x2, bottom_right_neighbor_y2)
			bottom_right = self.board.get_line(Line(bottom_right_pt1, bottom_right_pt2))
			print("Bottom-right neighbor line start: ", this_x2, this_y2, " | end: ", this_x2, bottom_right_neighbor_y2)
			
			# Check for either square pairing in chosen_line array
			#top_right_line = self.board.get_line(top_right)
			# fetched_line = self.board.get_line(clicked_line.getP1(), self.board.chosen_lines)
			# if (top_left in chosen_lines) and (top in chosen_lines) and (top_right in chosen_lines):
			# 	print("Your vertical line yielded a square! 1")
			# if (bottom_left in chosen_lines) and (bottom in chosen_lines) and (bottom_right in chosen_lines):
			# 	print("Your vertical line yielded a square! 2")


			print("\nThe following are lines already in chosen_lines:")
			if top in self.board.chosen_lines:
				print("Horizontal top")
			if bottom in self.board.chosen_lines:
				print("Horizontal bottom")
			if top_right in self.board.chosen_lines:
				print("Vertical top right")
			if top_left in self.board.chosen_lines:
				print("Vertical top left")
			if bottom_right in self.board.chosen_lines:
				print("Vertical bottom right")
			if bottom_left in self.board.chosen_lines:
				print("Vertical bottom left")

			# Check for complete square
			if top in self.board.chosen_lines and top_right in self.board.chosen_lines and top_left in self.board.chosen_lines:
				print("SQUARE!")
			if bottom in self.board.chosen_lines and bottom_right in self.board.chosen_lines and bottom_left in self.board.chosen_lines:
				print("BOTTOM SQUARE!")

		return 


def main():
	board_size = input("Enter board size (between 2-10):")
	while (int(board_size) <= 2) or (int(board_size) >= 10):
		print("Invalid number. Try again, or press 'q' to quit game.")
		board_size = input("Enter board size (between 2-10):")
		if board_size == 'q':
			exit()
	game = Game(int(board_size))

if __name__ == '__main__':
	main()