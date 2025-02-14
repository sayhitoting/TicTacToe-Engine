import copy

def CreateBoard (board_size):
	board_clear = []
	for y in range(board_size):
		board_y = []
		for x in range(board_size):
			board_y.append('_')
		board_clear.append(board_y)
	return board_clear
		
def ShowBoard ():
	if board_size > len(char_string):
		print("Board is too big to display properly.")
	
	display_columns_id = [] 
	for column in range(board_size):
		display_columns_id.append(char_string[column])
	print (" ", display_columns_id)

	for row in range(board_size): # display board
		print (row + 1, board_pieces[row])

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
	game_history.append([legal_check[1], legal_check[2]])

	return player_input, legal_check[1], legal_check[2]

def PlayMove(player_symbol, move_column, move_row):
	board_pieces[move_column][move_row] = player_symbol

def WinCheck (game_history):
	# 0 is no win, 1 is a win, 2 is a draw

	for i in range(board_size): # column win check
		first_item = board_pieces[i][0]
		if first_item != "_":
			for j in range(board_size):
				if board_pieces[i][j] != first_item:
					break
				elif j == board_size - 1:
					return 1
	
	for j in range(board_size): # row win check
		first_item = board_pieces[0][j]
		if first_item != "_":
			for i in range(board_size):
				if board_pieces[i][j] != first_item:
					break
				elif i == board_size - 1:
					return 1
	
	first_item = board_pieces[0][0] # diagonal 1 check
	if first_item != "_":
		for i in range(board_size):
			if board_pieces[i][i] != first_item:
				break
			elif i == board_size - 1:
					return 1
	
	first_item = board_pieces[0][-1] # diagonal 2 check
	if first_item != "_":
		for i in range(board_size):
			index = board_size - i - 1
			if board_pieces[index][i] != first_item:
				break
			elif i == board_size - 1:
					return 1
	
	moves_max = (board_size ** 2) # draw check if no win
	if len(game_history) >=  moves_max:
		return 2
		
	

	return 0

def Engine (game_status, game_history):
	if game_status:
		board_eval = copy.deepcopy(game_history)
		
		if eval_depth:
			print ("Evaluating to set depth:")

		else:
			print ("Evaluating full game:")
			num_possible = 3 ** (board_size ** 2)
			eval_status = False # simulated game status: True means game ended.
			eval_counter = 0
			while not eval_status: 
				eval_counter += 1
				if eval_counter == num_possible:
					eval_status = True
				
				eval = Evaluation(board_eval)


	else:
		print ("Checkmate.")

def Evaluation (board_eval, game_status):
	win_percent_p1 = []
	win_percent_p2 = []
	mate_found = False

	


	# skip testing squares that are already played

	for y in range(len(eval_depth)):
		for x in range(len()):
			if [y, x] not in game_history:
				print("Move was played")
	
	print ("P1:", win_percent_p1, "P2:", win_percent_p2)
	if mate_found:
		print("Mate in:", mate_seq, "moves.")
	
	


def PlayGame():
	
	print ("Michael's TicTacToe is loading...")

	game_status = True # if True, game is still in play
	game_result = "Game In Progress"
	game_history = []
	turns = 0
	
	while game_status:
		turns += 1

		ShowBoard()

		# Player 1's move
		print ("Turn {}".format(turns), "for Player 1")
		move_p1 = MoveInput(game_history)		
		print ("Your move was:", move_p1)
		PlayMove("O", move_p1[1], move_p1[2])

		# Check Player 1's move for wins
		win_check = WinCheck (game_history)

		if win_check == 1:
			game_status = False
			game_result = "Player 1 Wins!"
			ShowBoard()
			continue
		elif win_check == 2:
			game_status = False
			game_result = "Draw!"
			ShowBoard()
			continue

		ShowBoard()

		# Player 2's move
		print ("Turn {}".format(turns), "for Player 2")
		move_p2 = MoveInput(game_history)		
		print ("Your move was:", move_p2)
		PlayMove("X", move_p2[1], move_p2[2])

		# Check Player 2's move for wins
		win_check = WinCheck (game_history)

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
eval_depth = 0 # 0 depth means full evaluation per move

board_pieces = CreateBoard (board_size)
PlayGame()




