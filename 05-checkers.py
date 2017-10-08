#!/Library/Frameworks/Python.framework/Versions/3.6/bin

import sys, pygame, time
from Board import Board, Piece, Square
assert sys.version_info >= (3,4), 'This script requires at least Python 3.4'

pygame.init()
font = pygame.font.SysFont("arial",30)
#easy to divide by sixteen
size = (width,height) = (600,600)
constraints = (cols,rows) = (8,8)


#----------------------------------------
# helper functions

def draw_board(board, alternate, pieces, draw, screen):
	board.draw(draw,screen,alternate)
	for p in pieces:
		p.draw(draw,screen)
	pygame.display.flip()
#----------------------------------------

def main():
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption("Checkers")

	moves = 0

	# feel free to come up with your own colors. They are in (R,G,B) tuples	
	red = (224,49,49)
	black = (33,37,41)
	board_colors = [(98,80,87),(222,226,230)]
	board_alternate = [(73,80,87),(222,226,230)]
	board_highlight = (255,224,102)

	board = Board(size,constraints,board_colors,board_alternate,board_highlight)
	

	red_pieces = []
	for p in board.red_starting_positions:
		piece = Piece(p, 'Red', red, board_highlight, board.dim,-1,font)
		red_pieces.append(piece)
	black_pieces = []
	for p in board.black_starting_positions:
		piece = Piece(p, 'Black', black, board_highlight, board.dim,1,font)
		black_pieces.append(piece)
	all_pieces = red_pieces + black_pieces

	draw_board(board, 0, all_pieces, pygame.draw, screen)
	
	selected = False
	jumping = None
	jumps = []
	playing = True
	winner = ''
	players = ["Red","Black"]
	
	
	while playing:
		time.sleep(0.1)	#a 100 ms delay, so we don't max out the CPU
		currentPlayer = players[moves % len(players)]
		if currentPlayer == "Red":
			pieces = red_pieces
			opponents = black_pieces
		else:
			pieces = black_pieces
			opponents = red_pieces

		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			# handle MOUSEBUTTONUP
			if event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()
				square = board.get_square(pos)
				if selected:
					if square.highlighted:
						for p in pieces:
							if p.alive and p.selected:
								p.move(square.col,square.row)
								p.check_king(rows)
								for j in jumps:
									if square.position == j['position']:
										j['piece'].alive = False
										jumping = p
										sq = board.get_squares()
										jumps = jumping.check_jump(all_pieces,sq)
										if not len(jumps):
											jumping = None
								if jumping is None:
									moves += 1
					for p in pieces:
						p.selected = False
					for s in board.get_squares():
						s.highlighted = False
					if jumping is not None:
						jumping.selected = True
						for j in jumps:
							for s in sq:
								if j['position'] == s.position:
									s.highlighted = True
						selected = True
					else:
						selected = False
						jumps = []
				else:
					for p in pieces:
						if p.alive and p.position == square.position:
							p.selected = True
							possibilities = p.get_possibilities(board.get_squares())
							for h in possibilities:
								c = board.get_square_coord(h)
								if c is not None:
									add = True
									for a in all_pieces:
										if a.alive and a.col == c.col and a.row == c.row:
											add = False
									if add:
										c.highlighted = True
									else:
										sq = board.get_squares()
										jumps = p.check_jump(all_pieces,sq)
										for j in jumps:
											for s in sq:
												if j['position'] == s.position:
													s.highlighted = True
							selected = True
				draw_board(board, moves % len(players), all_pieces, pygame.draw, screen)
				red_count = 0
				black_count = 0
				for p in all_pieces:
					if p.alive:
						if p.player == 'Red':
							red_count += 1
						if p.player == 'Black':
							black_count += 1
				if red_count == 0:
					winner = 'Black'
					playing = False
				if black_count == 0:
					winner = 'Red'
					playing = False

	print(winner + ' won in only ' + str(moves//2) + ' turns! Good job!')


if __name__ == "__main__":
	# execute only if run as a script
	main()