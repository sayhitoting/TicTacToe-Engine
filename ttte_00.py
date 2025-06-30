import copy

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

def WinCheck (board_display, game_history):
	# 0 is no win, 1 is a win, 2 is a draw

	for i in range(board_size): # column win check
		first_item = board_display[i][0]
		if first_item != "_":
			for j in range(board_size):
				if board_display[i][j] != first_item:
					break
				elif j == board_size - 1:
					return 1
	
	for j in range(board_size): # row win check
		first_item = board_display[0][j]
		if first_item != "_":
			for i in range(board_size):
				if board_display[i][j] != first_item:
					break
				elif i == board_size - 1:
					return 1
	
	first_item = board_display[0][0] # diagonal 1 check
	if first_item != "_":
		for i in range(board_size):
			if board_display[i][i] != first_item:
				break
			elif i == board_size - 1:
					return 1
	
	first_item = board_display[0][-1] # diagonal 2 check
	if first_item != "_":
		for i in range(board_size):
			index = board_size - i - 1
			if board_display[index][i] != first_item:
				break
			elif i == board_size - 1:
					return 1
	
	moves_max = (board_size ** 2) # draw check if no win
	if len(game_history) >=  moves_max:
		return 2
		
	

	return 0

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
		win_squares = []
		for i in range(board_size):
			win_square = [i,i]
			win_squares.append(win_square)
		if all(square in win_squares for square in moves):
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
		return 1, 1 # Player One wins (win, winner 1)
	if win_p2:
		return 1, 2 # Player Two wins (win, winner 2)
			
	# check for draws
	if len(game_history) == board_size ** 2:
		if not win:
			return 2, 0 # draw (draw, no winner)

		

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

def Eval_PermutateEmptySquares (game_history, empty_squares):
	# for each iteration, perform wincheck
	for i in range(len(empty_squares)):
		



def Eval_Evaluation (game_status, game_history, player_id):
	if game_status:
		"""
		1. Make deepcopy of the game.
		2. Find unplayed squares and put into new list, "squares_empty".
		3. Create deepcopy of unplayed squares list, "squares_pool".
		4. Create new unplayed line until win condition met:
			Append square from "squares_empty" to 


		9. Play unplayed square on deepcopy.
		10. History check on any other lists in "eval_lines" for similarity
			If similar, break loop and start next unplayed square.
			If not similar, continue.
		11. Remove played square from "square_pool".
		12. Repeat
		13. Wincheck. 
			If win, check if list length is odd or even.
			If win and odd, append "current_line" to "p1_win_lines".
			If win and even, append "current_line" to "p2_win_lines".
			If draw, append "current_line" to "draw_lines".
			If no win, continue.
		
		
		5. If no win, play next unplayed square


		"""


		eval_board = copy.deepcopy(game_history)
		moves_possible = board_size ** 2

		squares_empty = Eval_FindEmptySquares(game_history)
		eval_lines = []






		

	else:
		print ("Game is over, nothing to evaluate.")

	return p1_chances, p2_chances, shortest_win, eval_notes

					
def PlayGame():
	
	print ("Michael's TicTacToe is loading...")

	game_status = True # if True, game is still in play
	game_result = "Game In Progress"
	game_history = []
	turns = 0

	board_display = CreateBoard (board_size)
	
	while game_status:
		turns += 1

		ShowBoard(board_display)

		# Player 1's move
		print ("Turn {}".format(turns), "for Player 1")
		move_p1 = MoveInput(game_history)		
		print ("Your move was:", move_p1)
		PlayMove(board_display, "O", move_p1[1], move_p1[2])

		# Check Player 1's move for wins
		win_check = WinCheck (board_display, game_history)

		if win_check == 1:
			game_status = False
			game_result = "Player 1 Wins!"
			ShowBoard(board_display)
			continue
		elif win_check == 2:
			game_status = False
			game_result = "Draw!"
			ShowBoard(board_display)
			continue

		ShowBoard(board_display)

		# Player 2's move
		print ("Turn {}".format(turns), "for Player 2")
		move_p2 = MoveInput(game_history)		
		print ("Your move was:", move_p2)
		PlayMove(board_display,"X", move_p2[1], move_p2[2])

		# Check Player 2's move for wins
		win_check = WinCheck (board_display, game_history)

		if win_check == 1:
			game_status = False
			game_result = "Player 2 Wins!"
			ShowBoard()
			continue
		elif win_check == 2:
			game_status = False
			game_result = "Draw!"
			ShowBoard()
			continue

	print (game_result)

char_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
board_size = 3
eval_depth = board_size ** 2

PlayGame()




