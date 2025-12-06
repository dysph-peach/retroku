"""
Grace Cox & Alex Chesin
Curses Test for RETROKU
Prints Sudoku board and given digits
"""
import curses
from curses import wrapper
from flask import *
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
import os, random


ROWS = 9
COLS = 9
VALID_NUMS = "123456789"

tiny_num = {"1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"}
board = {}
row = {}
for r in range(1, ROWS + 1):
    row[r] = set([])
col = {}
for c in range(1, COLS + 1):
    col[c] = set([])
box = {}
for b in range(1, 10):
    box[b] = set([])

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.getcwd() + "/instance/db.sqlite"
db = SQLAlchemy(app)


class Puzzle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puzz_disp = db.Column(db.String(81), nullable=False)
    puzz_answ = db.Column(db.String(81), nullable=False)
    board = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False) # 1 for easy, 2 for medium, 3 for hard
    puzzle_type = db.Column(db.Integer, nullable=False) # each number will be a different type of puzzle
    puzzle_name = db.Column(db.String, unique=True, nullable=False)
    puzzle_rules = db.Column(db.String)


class Cell:
    def __init__(self, pos, type, val, bg_col):
        self.pos = pos #position of cell on the board as a tuple: (r, c)
        self.type = type #"normal", "given", or "pencil"
        if not val:
            self.val = []
        else:
            self.val = [val] #list containing 1 or more numbers. if type == "pencil", will display last 3 numbers in the list
        self.bg_col = bg_col
    

    def set_type(self, new_type):
        if self.type == "normal":
            self.val = []
        self.type = new_type


    def add_val(self, new_val):
        if self.type == "pencil":
            if new_val not in self.val:
                self.val.append(new_val)
        else:
            self.val = [new_val]

    
    def del_val(self):
        if self.type != "given" and self.val:
            self.val.pop(-1)

    
    def set_bg(self, scr, new_bg):
        self.bg_col = new_bg
        scr.refresh()


    def scroll(self, scr, dir):
        if self.val:
            if dir == "r":
                self.val.append(self.val.pop(0))
            elif dir == "l":
                self.val.insert(0, self.val.pop(-1))
            self.update(scr)

    
    def update(self, scr):
        pair_num = (ROWS * (self.pos[0] - 1)) + self.pos[1] + 2
        curses.init_pair(pair_num, curses.COLOR_WHITE, self.bg_col)
        shading = curses.color_pair(pair_num)
        if self.val:
            if self.type == "normal":
                scr.addch(*cell_l(*self.pos), " ", shading)
                scr.addch(*cell_c(*self.pos), self.val[0], shading)
                scr.addch(*cell_r(*self.pos), " ", shading)
            elif self.type == "given":
                scr.addch(*cell_l(*self.pos), " ", shading)
                scr.addch(*cell_c(*self.pos), self.val[0], curses.A_BOLD | shading)
                scr.addch(*cell_r(*self.pos), " ", shading)
            elif self.type == "pencil":
                if len(self.val) == 1:
                    scr.addch(*cell_l(*self.pos), " ", shading)
                    scr.addch(*cell_c(*self.pos), tiny_num[self.val[0]], shading)
                    scr.addch(*cell_r(*self.pos), " ", shading)
                elif len(self.val) == 2:
                    scr.addch(*cell_l(*self.pos), tiny_num[self.val[0]], shading)
                    scr.addch(*cell_c(*self.pos), " ", shading)
                    scr.addch(*cell_r(*self.pos), tiny_num[self.val[1]], shading)
                else:
                    scr.addch(*cell_l(*self.pos), tiny_num[self.val[-3]], shading)
                    scr.addch(*cell_c(*self.pos), tiny_num[self.val[-2]], shading)
                    scr.addch(*cell_r(*self.pos), tiny_num[self.val[-1]], shading)
        else:
            scr.addch(*cell_l(*self.pos), " ", shading)
            scr.addch(*cell_c(*self.pos), " ", shading)
            scr.addch(*cell_r(*self.pos), " ", shading)
        scr.refresh()


def highlight(scr, r, c, color):
    board[(r, c)].set_bg(scr, color)
    board[(r, c)].update(scr)


def select(scr, r, c):
    scr.chgat(*cell_l(r, c), 3, curses.A_REVERSE)


def h_color(val):
    if val == 1:
        return curses.COLOR_CYAN
    
    if val == 2:
        return curses.COLOR_YELLOW
    
def l_color(val):
    if val == 1:
        return curses.COLOR_GREEN
    
    if val == 2:
        return curses.COLOR_MAGENTA


def cell_l(r, c):
    if r not in range(1, ROWS + 1) or c not in range(1, COLS + 1):
        raise ValueError
    return 2 * r, 4 * c - 1


def cell_c(r, c):
    if r not in range(1, ROWS + 1) or c not in range(1, COLS + 1):
        raise ValueError
    return 2 * r, 4 * c


def cell_r(r, c):
    if r not in range(1, ROWS + 1) or c not in range(1, COLS + 1):
        raise ValueError
    return 2 * r, 4 * c + 1


def rc_to_box(r, c):
    return ((r-1) // 3) * 3 + (c-1) // 3 + 1


def seen_cells(r, c):
    return row[r] | col[c] | box[rc_to_box(r, c)]


def print_template(scr, template):
    with open(template, "r", encoding="utf-8") as f:
        i = 0 #y position
        for line in f:
            scr.addstr(i, 0, line.strip("\n")) #print each line of template sans '\n'
            i += 1


def board_setup(scr, givens):
    if len(givens) > ROWS * COLS:
        raise ValueError
    givens = str(givens)
    i = 0 #index of number in givens
    for r in range(1, ROWS + 1):
        for c in range(1, COLS + 1):
            board[(r, c)] = Cell((r, c), "normal", None, -1)
            if i >= len(givens): #break if index too high
                pass
            elif givens[i] in "123456789":
                board[(r, c)].set_type("given")
                board[(r, c)].add_val(givens[i])
            box[rc_to_box(r, c)].add(board[r, c])
            row[r].add(board[(r, c)])
            col[c].add(board[(r, c)])
            board[(r, c)].update(scr)
            i += 1


def main(stdscr, puzzle):
    with app.app_context():
        curses.use_default_colors()
        curses.start_color()
        # Clear screen
        stdscr.clear()
        print_template(stdscr, puzzle.board)
        board_setup(stdscr, puzzle.puzz_disp)
        mode = "normal"
        color = 1
        r = 5
        c = 3
        lr = 5
        lc = 3
        curr_puzz = puzzle.puzz_disp
        select(stdscr, r, c)
        while curr_puzz != puzzle.puzz_answ:
            stdscr.refresh()
            key = stdscr.getkey()
            if key == "KEY_UP" or key == "l":
                lr = r
                lc = c
                if r > 1:
                    r -= 1
                else:
                    r = ROWS

            elif key == "KEY_DOWN" or key == "k":
                lr = r
                lc = c
                if r < ROWS:
                    r += 1
                else:
                    r = 1

            elif key == "KEY_LEFT" or key == "j":
                lc = c
                lr = r
                if c > 1:
                    c -= 1
                else:
                    c = COLS

            elif key == "KEY_RIGHT" or key == ";":
                lc = c
                lr = r
                if c < COLS:
                    c += 1
                else:
                    c = 1

            elif key == ",":
                board[(r, c)].scroll(stdscr, "l")

            elif key == ".":
                board[(r, c)].scroll(stdscr, "r")

            elif key == "n":
                mode = "normal"
            elif key == "p":
                mode = "pencil"
            elif key == "h":
                mode = "highlight"
            elif key == "c":
                if color == 1:
                    color = 2
                else:
                    color = 1

            elif key in VALID_NUMS:
                if mode == "normal" or mode == "pencil":
                    if board[(r, c)].type != "given":
                        board[(r, c)].set_type(mode)
                        board[(r, c)].add_val(key)
                        board[(r, c)].update(stdscr)

            elif key == "KEY_BACKSPACE":
                board[(r, c)].del_val()
                board[(r, c)].update(stdscr)

            elif key == " ":
                if mode == "highlight":
                    hcol = h_color(color)
                    if hcol == board[(r, c)].bg_col:
                        board[(r, c)].set_bg(stdscr, -1)
                    else:
                        board[(r, c)].set_bg(stdscr, hcol)

                board[(r, c)].update(stdscr)

            elif key == "s":
                puz_str = ""
                for y in range(1, ROWS + 1):
                    for x in range (1, COLS + 1):
                        if board[(y, x)].type != "pencil" and board[(y, x)].val:
                            puz_str += board[(y, x)].val[0]
                        else:
                            puz_str += "x"
                
                curr_puzz = puz_str

            else:
                curr_puzz = puzzle.puzz_answ

            board[(lr, lc)].update(stdscr)
            select(stdscr, r, c)
        
        stdscr.refresh()
        print("Looks good to me!")


def menu(stdscr):
    with app.app_context():
        stdscr.clear()
        position = 0
        posid = 1
        puzzles = Puzzle.query.all()
        i = 0
        puzzle_selected = False
        for pzl in puzzles:
            if pzl.difficulty == 1:
                difficulty = "n easy"
            elif pzl.difficulty == 2:
                difficulty = " medium"
            elif pzl.difficulty == 3:
                difficulty = " hard"
            
            if pzl.puzzle_type == 1:
                puzz_type = "Sudoku"

            if pzl.id == 1:
                stdscr.attron(curses.A_STANDOUT)
            stdscr.addstr(i, 0, f"{pzl.puzzle_name} (a{difficulty} {puzz_type} puzzle)")
            if pzl.id == 1:
                stdscr.attroff(curses.A_STANDOUT)
            i += 2
        while puzzle_selected == False:
            stdscr.refresh()
            key = stdscr.getkey()
            if key == "KEY_UP" or key == "l":
                if position > 0:
                    position -= 2
                    posid = position / 2
                    posid += 1
            elif key == "KEY_DOWN" or key == "k":
                if position < 2 * (len(puzzles) - 1):
                    position += 2
                    posid = position / 2
                    posid += 1
            elif key == " ":
                puzzle_selected = True
            
            if key == "KEY_DOWN" or key == "KEY_UP" or key == "k" or key == "l":
                stdscr.clear()
                i = 0
                for pzl in puzzles:
                    if pzl.difficulty == 1:
                        difficulty = "n easy"
                    elif pzl.difficulty == 2:
                        difficulty = " medium"
                    elif pzl.difficulty == 3:
                        difficulty = " hard"
                    
                    if pzl.puzzle_type == 1:
                        puzz_type = "Sudoku"

                    if pzl.id == posid:
                        stdscr.attron(curses.A_STANDOUT)
                    stdscr.addstr(i, 0, f"{pzl.puzzle_name} (a{difficulty} {puzz_type} puzzle)")
                    if pzl.id == posid:
                        stdscr.attroff(curses.A_STANDOUT)
                    i += 2
        if stdscr.getmaxyx()[0] < 30 or stdscr.getmaxyx()[1] < 50:
            raise Exception('Window too small. Please resize and try again.')
        else:
            wrapper(main, Puzzle.query.filter_by(id=posid).first())


wrapper(menu)