# Ali Mahmoud
# 2017

from tkinter import *
from random import randrange
import time

#
width, height = 400, 400
w = 40
rows, cols = int(height/w), int(width/w)
grid = [[[] for c in range(cols)] for r in range(rows)]  #using list comprehensions to declare 2d array
current = 0
stack = []
solve = []
#

window = Tk()
window.title('Maze Game!')
canvas = Canvas(window, width=width, height=height)
canvas.pack(fill='both')


class Cell():
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.walls = [True, True, True, True]  #[top, right, bottom, left]
        self.visited = False
        self.tl = self.rl = self.bl = self.ll = 0

    def show(self):
        x = self.i * w
        y = self.j * w
        #if self.walls[0]:
        self.tl = canvas.create_line(x,    y,    x+w,  y, fill='blue')     #draw top line
        #if self.walls[1]:
        self.rl = canvas.create_line(x+w, y,    x+w , y+w, fill='blue')  #draw right line
        #if self.walls[2]:
        self.bl = canvas.create_line(x+w, y+w, x,     y+w, fill='blue')  #draw bottom line
        #if self.walls[3]:
        self.ll = canvas.create_line(x,    y+w, x,     y, fill='blue')     #draw left line

    def draw_visited(self):
        x = self.i * w
        y = self.j * w
        if self.visited:
            canvas.create_rectangle(x+2, y+2, x+w-2, y+w-2, fill='white', outline='')
            window.update()
            time.sleep(0.05)

    def hightlight(self):
        x = self.i * w
        y = self.j * w
        canvas.create_rectangle(x+2, y+2, x+w-2, y+w-2, fill='red', outline='')
        window.update()
        time.sleep(0.05)

    def check_neighbors(self):
        neighbors = []

        if not edge(self.i-1, self.j):
            top = grid[self.i-1][self.j]
            if not top.visited:
                neighbors.append(top)
        if not edge(self.i, self.j+1):
            right = grid[self.i][self.j+1]
            if not right.visited:
                neighbors.append(right)
        if not edge(self.i+1, self.j):
            bottom = grid[self.i+1][self.j]
            if not bottom.visited:
                neighbors.append(bottom)
        if not edge(self.i, self.j-1):
            left = grid[self.i][self.j-1]
            if not left.visited:
                neighbors.append(left)

        if len(neighbors) > 0:
            return neighbors[randrange(len(neighbors))]
        else:
            return False


def edge(i, j):
    if i<0 or j<0 or i>= rows or j>= cols:
        return True
    return False


def setup():
    global current

    for i in range(rows):
        for j in range(cols):
            grid[i][j] = Cell(i, j)

    current = grid[0][0]
    current.visited = True


def draw():
    global current

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j].show()


    while True:
        current.hightlight()
        current.draw_visited()

        #STEP 1
        next_cell = current.check_neighbors()
        if next_cell:

            #STEP 2
            stack.append(current)

            #STEP 3
            if not next_cell.visited:
                remove_walls(current, next_cell) #######
                solve.append(current)

            #STEP 4
            current = next_cell
            current.visited = True

        elif len(stack) > 0:
            current = stack.pop()
        else:
            break


def remove_walls(c, n):
    y = c.i - n.i
    x = c.j - n.j
    if x == 0:
        if y == -1:
            canvas.delete(c.rl)
            canvas.delete(n.ll)
            window.update()
        elif y == 1:
            canvas.delete(c.ll)
            canvas.delete(n.rl)
            window.update()

    if y == 0:
        if x == -1:
            canvas.delete(c.bl)
            canvas.delete(n.tl)
            window.update()
        elif x == 1:
            canvas.delete(c.tl)
            canvas.delete(n.bl)
            window.update()
            #print(c.__dict__)

def draw_solve():
    global solve
    solve = grid[0][0]

if __name__ == '__main__':
    setup()
    draw()
    button = Button(window, text='Show Solve!', command=draw_solve).pack()
    window.mainloop()