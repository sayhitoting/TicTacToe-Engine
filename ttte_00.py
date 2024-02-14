def CreateBoard (board_size):
	for y in range(board_size):
		board_y = []
		for x in range(board_size):
			board_y.append('_')
		board_pieces.append(board_y)
	return board_size
		
def ShowBoard ():
	if board_size > len(char_string):
		print("Board is too big to display properly.")
	
	display_columns_id = [] 
	for column in range(board_size):
		display_columns_id.append(char_string[column])
	print (" ", display_columns_id)

	for row in range(board_size): # display board
		print (row + 1, board_pieces[row])


def LegalMove(user_input, game_history):
	legality = True

	# find column value
	column_chars = [] # total list of column labels
	for column_index in range(board_size):
		column_chars.append(char_string[column_index])
	
	column_value = []
	for input_char in user_input: # compare input chars to labeled columns
		if input_char in column_chars:
			column_value.append(input_char)
	
	if len(column_value) < 1: # existence check
		print ("Your move, [", user_input, "], does not have a column value within the board.")
		legality = False
		
	if len(column_value) > 1: # duplicity check
		print ("Your move, [", user_input, "], contains more than one column.")
		legality = False
			
	# find row value
	row_value = [] 
	for entry in user_input:  # compare entry with valid ints
		if entry.isdigit():
			row_value.append(int(entry))
	
	if len(row_value) < 1: # existence check
		print ("Your move, [", user_input, "], does not have a row value within the board.")
		legality = False
		
	if len(row_value) > 1: # duplicity check
		print ("Your move, [", user_input, "], contains more than one row.")
		legality = False

	#resulting move indices
	if legality:
		move_row_index = row_value[0] - 1 # row index
	
		for i in range(len(char_string)): # compare valid chars to entry
			if 	column_value[0] == char_string[i]:
				move_column_index = i # column index
		print ("Move indices(R,C):", move_row_index, move_column_index)

	# check if square is already occupied
	if [move_row_index, move_column_index] in game_history:
		print ("Your move, [", user_input, "], has already been played before.")
		legality = False
	
	if not legality:
		print ("not a legal move")
	else:
		print ("legal move")
	
	return legality, move_row_index, move_column_index

def MoveInput(game_history):
	player_input = str(input("Please input coordinate for your next move:"))
	legal_check = LegalMove(player_input, game_history)
	while not legal_check[0]:
		# True is legal
		MoveInput(game_history)	
	game_history.append([legal_check[1], legal_check[2]])
	return player_input, legal_check[1], legal_check[2]

def PlayMove(player_symbol, move_column, move_row):
	board_pieces[move_column][move_row] = player_symbol

def WinCheck ():
	column = []
	for row in range (board_size): # column check
		piece = board_pieces[row]
			
			
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

		ShowBoard()

		# Player 2's move
		print ("Turn {}".format(turns), "for Player 2")
		move_p2 = MoveInput(game_history)		
		print ("Your move was:", move_p2)
		PlayMove("X", move_p2[1], move_p2[2])
	
		if turns > board_size ** 2 + 1:
			game_status = False # failsafe
			game_result = "Too Many Turns", turns

	print (game_result)

char_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
board_pieces = []
board_size = 4

CreateBoard (board_size)
PlayGame()




