import copy
from itertools import permutations

class Eval_Line:
	def __init__(self, line, line_length, win_state):
		self.line = line
		self.line_length = line_length
		self.win_state = win_state	# -1 = lose, 1 = win, 0 = draw

def CreateBoard (board_size):
	board_clear = []
	for y in range(board_size):
		board_y = []
		for x in range(board_size):
			board_y.append('_')
		board_clear.append(board_y)
	return board_clear
		
def ShowBoard (board_display):
	if board_size > len(char_string):
		print("Board is too big to display properly.")
	
	display_columns_id = [] 
	for column in range(board_size):
		display_columns_id.append(char_string[column])
	print (" ", display_columns_id)

	for row in range(board_size): # display board
		print (row + 1, board_display[row])

def InputParse(user_input):
	# element parsing
	parse_result = True

	if len(str(user_input)) > 2:
		parse_result = False
		parse_note = "Too many characters were input."
		row_value = parse_note
		column_value = parse_note
	elif len(str(user_input)) < 2:
		parse_result = False
		parse_note = "Too few characters were input."
		row_value = parse_note
		column_value = parse_note
	else:
		input_char = []
		input_value = []
		for element in user_input: # search for letters and numbers
			if element in char_string:
				input_char.append(element)
			elif element.isdigit():
				input_value.append(int(element))
		
		if len(input_char) < 1: # too few letters
			parse_result = False
			parse_note = "No acceptable column letter (e.g. A) found."
			row_value = parse_note
			column_value = parse_note
		if len(input_char) > 1: # too many letters
			parse_result = False
			parse_note = "Multiple column letter (e.g. A) found."
			row_value = parse_note
			column_value = parse_note
		if len(input_value) < 1: # too few numbers
			parse_result = False
			parse_note = "No acceptable row number (e.g. 1) found."
			row_value = parse_note
			column_value = parse_note
		if len(input_value) > 1: # too many numbers
			parse_result = False
			parse_note = "Multiple row numbers (e.g. 1) found."
			row_value = parse_note
			column_value = parse_note

	if parse_result: # no error is thrown, character conversion to index
		for i in range(len(char_string)):
			if char_string[i] == input_char[0]:
				column_value = i
		row_value = input_value[0] - 1
	
	return parse_result, row_value, column_value

def LegalMove(user_input, game_history):
	legality = True

	input_parsing = InputParse(user_input)
	move_row_index = input_parsing[1]
	move_column_index = input_parsing[2]
	if not input_parsing[0]:
		print (str(input_parsing[1]))	
	else:
		print ("Input, [", user_input,"] accepted. Row ", move_row_index, ", Column ", move_column_index)

	# check if square is already occupied
	if [move_row_index, move_column_index] in game_history:
		print ("Your move, [", user_input, "], has already been played.")
		legality = False
	
	if not legality:
		print ("Not a legal move.")
	else:
		print ("Legal move.")
	
	return legality, move_row_index, move_column_index

def MoveInput(game_history):
	player_input = str(input("Please input coordinate for your next move:"))
	legal_check = LegalMove(player_input, game_history)

	while not legal_check[0]:
		# True is legal
		player_input = str(input("Please input coordinate for your next move:"))
		legal_check = LegalMove(player_input, game_history)	
	game_history.append([legal_check[1], legal_check[2]]) #stores game history as [index_row, index_column]

	return player_input, legal_check[1], legal_check[2]

def PlayMove(board_display, player_symbol, move_column, move_row):
	board_display[move_column][move_row] = player_symbol

def WinCheck_V2_Checks(moves):
	"""
	Written for checking wins after moves have been sorted by player.
	The variable "moves" refers to a list of moves made only by one player.
	"""

	win = False

	# rows wincheck
	for index_test_row in range(board_size):
		matches_row = [move for move in moves if move[0] == index_test_row]
		if len(matches_row) == board_size:
			win = True
			

	# columns wincheck
	for index_test_column in range(board_size):
		matches_column = [move for move in moves if move[1] == index_test_column]
		if len(matches_column) == board_size:
			win = True

	# diagonals wincheck
	## first diagonal, index_row == 0, index_column == 0
	if [0,0] in moves:
		win_squares_dia1 = []
		for i in range(board_size):
			win_square = [i, i]
			win_squares_dia1.append(win_square)
		if all(square in moves for square in win_squares_dia1): # check if all squares in win_squares_dia1 are in moves
			win = True
	
	## second diagonal, index_row == board_size - 1, index_column == 0
	if [board_size - 1, 0] in moves:
		win_squares_dia2 = []
		for i in range(board_size):
			win_square = [board_size - 1 - i, i]
			win_squares_dia2.append(win_square)
		if all(square in moves for square in win_squares_dia2):
			win = True
	
	
	
	return win

def WinCheck_V2(game_history):
	# 0 is no win, 1 is a win, 2 is a draw

	# split moves into player one and two
	moves_p1 = []
	moves_p2 = []

	for i in range(len(game_history)):
		if i % 2 == 0: # i is even, and thus player 1's move
			moves_p1.append(game_history[i])
		else: # i is odd, and thus player 2's move
			moves_p2.append(game_history[i])
	
	# check if either player has wins
	win_p1 = WinCheck_V2_Checks(moves_p1)
	win_p2 = WinCheck_V2_Checks(moves_p2)

	if win_p1: 
		return 1, 1 # Player One wins (win, player 1)
	
	elif win_p2:
		return 1, 2 # Player Two wins (win, player 2)
			
	# check for draws
	elif len(game_history) == board_size ** 2:
		if not win_p1 or not win_p2:
			return 2, 0 # draw (draw, no winner)

	return 0, 0 # no win or winner, game continues
		
def Eval_FindEmptySquares (game_history):
	empty_squares = []
	used_squares = []

	# check if each square is featured in the game history
	for column_val in range(board_size): 
		for row_val in range(board_size):
			test_square = [column_val, row_val]
			if test_square not in game_history:
				empty_squares.append(test_square)
			else:
				used_squares.append(test_square)

	return empty_squares, used_squares

def Eval_CalculateLines (game_history, empty_squares):
	empty_squares_permutations = list(permutations(empty_squares))
	p1_win_lines = []
	p2_win_lines = []
	draw_lines = []

	for permutation in empty_squares_permutations:
		# simulated game line to completion
		line = game_history + list(permutation) 
		
		# check for wins at every move
		line_test = []
		for move in line:
			line_test.append(move)
			wincheck_line = WinCheck_V2(line_test)

			if wincheck_line[0] == 1: # win detected, save and terminate line
				if wincheck_line[1] == 1: # player 1 win
					p1_win_lines.append(line_test.copy())
				elif wincheck_line[1] == 2: # player 2 win
					p2_win_lines.append(line_test.copy())
				break

			elif wincheck_line[0] == 2: # draw
				draw_lines.append(line_test.copy())
				break

	return p1_win_lines, p2_win_lines, draw_lines

def Eval_Evaluation (game_history):
	print ("Evaluating...")

	# calculate win percentage
	empty_squares = Eval_FindEmptySquares(game_history)[0]
	evaluation = Eval_CalculateLines (game_history, empty_squares)

	total_lines = len(evaluation[0]) + len(evaluation[1]) + len(evaluation[2])
	if total_lines == 0:
		win_percentage_p1 = 0.5
		win_percentage_p2 = 0.5
	else:
		win_percentage_p1 = round(100 * (len(evaluation[0]) / total_lines))
		win_percentage_p2 = round(100 * (len(evaluation[1]) / total_lines))
		draw_percentage = round(100 * (len(evaluation[2]) / total_lines))
	print (total_lines, " lines were evaluated.")
	print ("P1 - ", win_percentage_p1, "% | ", draw_percentage, "% |",  win_percentage_p2, "% - P2")

	# find shortest mate
	p1_win_lines_sorted = sorted(evaluation[0], key=len)
	p2_win_lines_sorted = sorted(evaluation[1], key=len)

	# announce closest mate
	mate_tolerance = 1
	if p1_win_lines_sorted and len(game_history) % 2 == 0:
		if len(p1_win_lines_sorted[0]) == len(game_history) + mate_tolerance:
			print("Mate in ", mate_tolerance, "by Player 1.")
	if p2_win_lines_sorted and len(game_history) % 2 != 0:
		if len(p1_win_lines_sorted[0]) == len(game_history) + mate_tolerance:
			print("Mate in ", mate_tolerance, "by Player 2.")

	return win_percentage_p1, win_percentage_p2


					
def PlayGame():
	
	print ("Michael's TicTacToe is loading...")

	play_with_eval = str(input("Would you like to see the evaluation during play? Y/N:"))
	if play_with_eval == "Y":
		eval_bool = True
	else:
		eval_bool = False

	game_status = True # if True, game is still in play
	game_result = "Game In Progress"
	game_history = []
	turns = 0

	board_display = CreateBoard (board_size)
	ShowBoard(board_display)
	if eval_bool:
		Eval_Evaluation (game_history)

	while game_status:
		player_name = "1"
		player_symbol = "O"

		if game_history:
			if len(game_history) % 2 == 0: # even number of moves, P1
				turns += 1
				player_name = "1"
				player_symbol = "O"
			else: # odd number of moves, P2
				player_name = "2"
				player_symbol = "X"

		# Plays a move
		print ("Turn {}".format(turns + 1), "for Player", player_name)
		move = MoveInput(game_history)		
		print ("Your move was:", move)
		PlayMove(board_display, player_symbol, move[1], move[2])

		# Check move for wins
		win_check = WinCheck_V2 (game_history)

		if win_check[0] == 1:
			game_status = False
			win_message = "Player {} Wins!"
			game_result = win_message.format(str(player_name))
			ShowBoard(board_display)
			continue
		elif win_check[0] == 2:
			game_status = False
			game_result = "Draw!"
			ShowBoard(board_display)
			continue
		
		ShowBoard(board_display)
		if eval_bool:
			Eval_Evaluation (game_history)

	print (game_result)

char_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
board_size = 3
eval_depth = board_size ** 3

PlayGame()




