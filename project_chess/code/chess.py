from pathlib import Path
import tkinter as tk

parent_directory = Path(__file__).parent.parent

root = tk.Tk()
root.title('Chess')

Canvas = tk.Canvas(root, width=680, height=680)
Canvas.pack()

cell_size = 80
rows, cols = 8, 8

images = {}
board_state = []
selected = []
turn = "white"

white_king_moved = False
black_king_moved = False
white_rook_moved = {'left': False, 'right': False}
black_rook_moved = {'left': False, 'right': False}

def position_notation(file, rank):
    columns = 'abcdefgh'
    column = columns[file]
    row = 8 - rank
    return f"{column}{row}"

def load_images():
    imgs = {}
    for piece in [
        'white_pawn', 'white_rook', 'white_knight', 'white_bishop', 'white_queen', 'white_king',
        'black_pawn', 'black_rook', 'black_knight', 'black_bishop', 'black_queen', 'black_king'
    ]:
        imgs[piece] = tk.PhotoImage(file=str(parent_directory / 'images' / f'{piece}.png'))
    return imgs

def initial_position():
    return [
        ['black_rook', 'black_knight','black_bishop','black_queen', 'black_king','black_bishop', 'black_knight', 'black_rook'],
        ['black_pawn']*8,
        [None]*8,
        [None]*8,
        [None]*8,
        [None]*8,
        ['white_pawn']*8,
        ['white_rook', 'white_knight','white_bishop','white_queen', 'white_king','white_bishop', 'white_knight', 'white_rook']
    ]

def draw_board():
    Canvas.delete('all')
    for row in range(rows):
        for col in range(cols):
            x1 = col * cell_size + 40
            y1 = row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            color = 'white' if (row + col) % 2 == 0 else 'slategray'
            Canvas.create_rectangle(x1, y1, x2, y2, fill=color)

            if selected and selected[0] == (row, col):
                cx = x1 + cell_size / 2
                cy = y1 + cell_size / 2
                r = cell_size / 2 - 8
                Canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline='gray77', fill='gray77', width=3)

            piece = board_state[row][col]
            if piece:
                Canvas.create_image(x1 + cell_size/2, y1 + cell_size/2, image=images[piece])

def start():
    global images, board_state
    images = load_images()
    board_state = initial_position()
    draw_board()

def on_click(event):
    file = (event.x - 40) // cell_size
    rank = event.y // cell_size
    if 0 <= file < 8 and 0 <= rank < 8:
        selected.append((rank, file))
        if len(selected) == 2:
            move(selected[0], selected[1])
            selected.clear()
        draw_board()

def move(first_click, second_click):
    global board_state, turn, white_king_moved, black_king_moved
    piece = board_state[first_click[0]][first_click[1]]

    if piece is None:
        return

    square_state1 = piece.split('_')
    square_state2 = (board_state[second_click[0]][second_click[1]] or '').split('_')

    if square_state1[0] != turn:
        return

    if square_state2[0] == turn:
        return

    moved = False

    if square_state1[1] == 'king':
        moved = king_move(square_state1, piece, first_click, second_click)
        if piece == 'white_king':
            white_king_moved = True
        else:
            black_king_moved = True

    elif square_state1[1] == 'pawn':
        moved = pawn_move(square_state1, piece, first_click, second_click)

    elif square_state1[1] == 'knight':
        moved = knight_move(square_state1, piece, first_click, second_click)

    elif square_state1[1] == 'rook':
        moved = rook_move(square_state1, piece, first_click, second_click)
        if piece == 'white_rook':
            if first_click == (7, 0): white_rook_moved['left'] = True
            elif first_click == (7, 7): white_rook_moved['right'] = True
        elif piece == 'black_rook':
            if first_click == (0, 0): black_rook_moved['left'] = True
            elif first_click == (0, 7): black_rook_moved['right'] = True

    elif square_state1[1] == 'bishop':
        moved = bishop_move(square_state1, piece, first_click, second_click)

    elif square_state1[1] == 'queen':
        moved = queen_move(square_state1, piece, first_click, second_click)

    if moved:
        turn = 'white' if turn == 'black' else 'black'
        draw_board()

def king_move(square_state1, piece, first_click, second_click):
    global white_king_moved, black_king_moved
    r1, c1 = first_click
    r2, c2 = second_click
    if abs(r2 - r1) <= 1 and abs(c2 - c1) <= 1:
        board_state[r1][c1] = None
        board_state[r2][c2] = piece
        return True

    if square_state1[0] == 'white' and not white_king_moved:
        if second_click == (7, 6) and not white_rook_moved['right']:
            if board_state[7][5] is None and board_state[7][6] is None:
                board_state[7][4] = None
                board_state[7][6] = piece
                board_state[7][5] = board_state[7][7]
                board_state[7][7] = None
                white_king_moved = True
                white_rook_moved['right'] = True
                return True
        elif second_click == (7, 2) and not white_rook_moved['left']:
            if board_state[7][1] is None and board_state[7][2] is None and board_state[7][3] is None:
                board_state[7][4] = None
                board_state[7][2] = piece
                board_state[7][3] = board_state[7][0]
                board_state[7][0] = None
                white_king_moved = True
                white_rook_moved['left'] = True
                return True

    if square_state1[0] == 'black' and not black_king_moved:
        if second_click == (0, 6) and not black_rook_moved['right']:
            if board_state[0][5] is None and board_state[0][6] is None:
                board_state[0][4] = None
                board_state[0][6] = piece
                board_state[0][5] = board_state[0][7]
                board_state[0][7] = None
                black_king_moved = True
                black_rook_moved['right'] = True
                return True
        elif second_click == (0, 2) and not black_rook_moved['left']:
            if board_state[0][1] is None and board_state[0][2] is None and board_state[0][3] is None:
                board_state[0][4] = None
                board_state[0][2] = piece
                board_state[0][3] = board_state[0][0]
                board_state[0][0] = None
                black_king_moved = True
                black_rook_moved['left'] = True
                return True
    return False

def pawn_move(square_state1, piece, first_click, second_click):
    direction = -1 if square_state1[0] == 'white' else 1
    start_row = 6 if square_state1[0] == 'white' else 1
    r1, c1 = first_click
    r2, c2 = second_click

    target_piece = board_state[r2][c2]

    if c1 == c2 and r2 == r1 + direction and target_piece is None:
        board_state[r1][c1] = None
        board_state[r2][c2] = piece
        return True

    if c1 == c2 and r1 == start_row and r2 == r1 + 2 * direction:
        if board_state[r1 + direction][c1] is None and board_state[r2][c2] is None:
            board_state[r1][c1] = None
            board_state[r2][c2] = piece
            return True

    if abs(c2 - c1) == 1 and r2 == r1 + direction and target_piece is not None:
        if square_state1[0] != target_piece.split('_')[0]:
            board_state[r1][c1] = None
            board_state[r2][c2] = piece
            return True

    return False

def knight_move(square_state1, piece, first_click, second_click):
    r1, c1 = first_click
    r2, c2 = second_click
    dr, dc = abs(r1 - r2), abs(c1 - c2)
    if (dr, dc) in [(2, 1), (1, 2)]:
        target = board_state[r2][c2]
        if target is None or square_state1[0] != target.split('_')[0]:
            board_state[r1][c1] = None
            board_state[r2][c2] = piece
            return True
    return False

def bishop_move(square_state1, piece, first_click, second_click):
    r1, c1 = first_click
    r2, c2 = second_click
    if abs(r1 - r2) != abs(c1 - c2):
        return False
    dr = 1 if r2 > r1 else -1
    dc = 1 if c2 > c1 else -1
    r, c = r1 + dr, c1 + dc
    while r != r2 and c != c2:
        if board_state[r][c] is not None:
            return False
        r += dr
        c += dc
    target = board_state[r2][c2]
    if target is None or square_state1[0] != target.split('_')[0]:
        board_state[r1][c1] = None
        board_state[r2][c2] = piece
        return True
    return False

def rook_move(square_state1, piece, first_click, second_click):
    r1, c1 = first_click
    r2, c2 = second_click
    if r1 != r2 and c1 != c2:
        return False
    if r1 == r2:
        step = 1 if c2 > c1 else -1
        for c in range(c1 + step, c2, step):
            if board_state[r1][c] is not None:
                return False
    else:
        step = 1 if r2 > r1 else -1
        for r in range(r1 + step, r2, step):
            if board_state[r][c1] is not None:
                return False
    target = board_state[r2][c2]
    if target is None or square_state1[0] != target.split('_')[0]:
        board_state[r1][c1] = None
        board_state[r2][c2] = piece
        return True
    return False

def queen_move(square_state1, piece, first_click, second_click):
    return bishop_move(square_state1, piece, first_click, second_click) or \
           rook_move(square_state1, piece, first_click, second_click)

Canvas.bind("<Button-1>", on_click)
start()
root.mainloop()
