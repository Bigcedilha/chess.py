from pathlib import Path
import tkinter as tk
parent_directory = Path(__file__).parent

root = tk.Tk()
root.title('Chess')

#size of the window
Canvas = tk.Canvas(root, width=680, height=680)
Canvas.pack()

#size of the square
cell_size = 80
#numero de linhas e colunas
rows, cols = 8, 8

images = {}

def position_notation(file, rank):
    columns = 'abcdefgh'
    column = columns[file] 
    row = 8 - rank
    return f"{column}{row}"

def load_images():
    images['white_pawn'] = tk.PhotoImage(file=str(parent_directory / 'images' / 'white_pawn.png'))
    images['white_rook'] = tk.PhotoImage(file=str(parent_directory / 'images' / 'white_rook.png'))
    images['white_knight'] = tk.PhotoImage(file=str(parent_directory / 'images' / 'white_knight.png'))
    images['white_bishop'] = tk.PhotoImage(file=str(parent_directory / 'images' / 'white_bishop.png'))
    images['white_queen'] = tk.PhotoImage(file=str(parent_directory / 'images' / 'white_queen.png'))
    images['white_king'] = tk.PhotoImage(file=str(parent_directory / 'images' / 'white_king.png'))
    images['black_pawn'] = tk.PhotoImage(file=str(parent_directory / 'images' / 'black_pawn.png'))
    images['black_rook'] = tk.PhotoImage(file=str(parent_directory / 'images' / 'black_rook.png'))
    images['black_knight'] = tk.PhotoImage(file=str(parent_directory / 'images' / 'black_knight.png'))
    images['black_bishop'] = tk.PhotoImage(file=str(parent_directory / 'images' / 'black_bishop.png'))
    images['black_queen'] = tk.PhotoImage(file=str(parent_directory / 'images' / 'black_queen.png'))
    images['black_king'] = tk.PhotoImage(file=str(parent_directory / 'images' / 'black_king.png'))
    return images
        
def initial_position():
    return[
        ['black_rook', 'black_knight','black_bishop','black_queen', 'black_king','black_bishop', 'black_knight', 'black_rook'],
        ['black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn'],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        ['white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn'],
        ['white_rook', 'white_knight','white_bishop','white_queen', 'white_king','white_bishop', 'white_knight', 'white_rook']
        
    ]
    
def board(Canvas, images, board_state):
    
    for row in range(rows):
        for col in range(cols):
            x1 = col * cell_size + 40
            y1 = row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            
            if(row + col) % 2 == 0:
                color = 'white'
            else:
                color = 'slategray'
            
            Canvas.create_rectangle(x1, y1, x2, y2, fill=color)
            peça = board_state[row][col]
            if peça:
                Canvas.create_image(x1 + cell_size / 2, y1 + cell_size / 2, image=images[peça])

def start():
    images = load_images()
    board_state = initial_position()
    board(Canvas, images, board_state)
    
def on_click(event):
    file = (event.x-40) // cell_size
    rank = event.y // cell_size
    notation = position_notation(file, rank)
    print(notation)

Canvas.bind("<Button-1>", on_click)
start()


root.mainloop()