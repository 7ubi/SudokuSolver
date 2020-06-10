import pygame

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


grid = [[0 for x in range(9)] for y in range(9)] 


#delay before next number gets placed in milliseconds
delay = 100 

pygame.init()
screen = pygame.display.set_mode((630, 630))
pygame.display.set_caption("Sudoku Solver")
myfont = pygame.font.SysFont('Comic Sans MS', 30)

def canBePlaced(row, col, val):
    #check row
    for i in range(0, 9):
        if(grid[row][i] == val):
            return False
    
    #check column
    for i in range(0, 9):
        if(grid[i][col] == val):
            return False

    #check box
    r = row - row % 3
    c = col - col % 3

    for i in range(r, r + 3):
        for j in range(c, c + 3):
            if(grid[i][j] == val):
                return False

    return True
def updateScreen():
    #sets background white
    screen.fill(pygame.Color(255, 255, 255))

    #draw lines for Sudoku field
    for i in range(1, 9):
        if(i % 3 == 0):
            pygame.draw.rect(screen, pygame.Color(0, 0, 0), (0, i *70, 630, 4))
        else:
            pygame.draw.line(screen, pygame.Color(0, 0, 0), (0, i * 70), (630, i * 70))

    for i in range(1, 9):
        if(i % 3 == 0):
            pygame.draw.rect(screen, pygame.Color(0, 0, 0), (i *70, 0, 4, 630))
        else:
            pygame.draw.line(screen, pygame.Color(0, 0, 0), (i * 70, 0), (i * 70, 630))

    #draw numbers of the grid
    for i in range(0, 9):
        for j in range(0, 9):
            #only draw the number if it's not 0
            if(grid[j][i] == 0):
                continue

            textsurface = myfont.render(str(grid[j][i]), False, (0, 0, 0))
            screen.blit(textsurface,(i * 70 + 20, j * 70 + 15))
    pygame.display.update()

  

def solve():
    #go through every cell
    for i in range(0, 9):
        for j in range(0, 9):
            #check if it number is already filled in
            if(grid[i][j] != 0):
                continue
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            #check every number
            for num in range(1, 10):
                #check if it can be placed there
                if(not canBePlaced(i, j , num)):
                    continue
                
                #set the cell to the number
                grid[i][j] = num

                pygame.time.delay(delay)
                #update the screen with new grid
                updateScreen()
                #time delay 
                pygame.time.delay(5)

                #check if the number is correct in this place
                #if not try next on 
                if(solve()):
                    return True
                else:
                    grid[i][j] = 0
            #if no number works -> backtrack so that it gets right
            return False
    return True

def Main():
    run = True
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        updateScreen()
        solve()
        updateScreen()

        pygame.display.update()


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Sodoku Solver'
        self.left = 100
        self.top = 100
        self.width = 450
        self.height = 500
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create textbox
        self.textbox = []
        for i in range(9):
            for j in range(9):
                self.textboxi = QLineEdit(self)
                self.textboxi.move(i*50, j*50)
                self.textboxi.resize(50,50)
                f = self.textboxi.font()
                f.setPointSize(40) # sets the size to 27
                self.textboxi.setFont(f)
                self.textbox.append(self.textboxi)
        
        # Create a button in the window
        self.button = QPushButton('Solve Sodoku', self)
        self.button.move(225,450)
        
        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()
    
    @pyqtSlot()
    def on_click(self):
        for i in range(9):
            for j in range(9):
                if self.textbox[(j*9) + i].text() == "":
                    grid[i][j] = 0
                elif int(self.textbox[(j*9) + i].text()) < 0 or int(self.textbox[(j*9) + i].text()) > 9:
                    self.msg = QMessageBox(self)
                    self.msg.setWindowTitle('Error')
                    self.msg.setText("Numbers must be between 1 and 9!")
                    self.msg.setIcon(QMessageBox.Critical)
                    x = self.msg.exec_()
                    return
                else:
                    grid[i][j] = int(self.textbox[(j * 9) + i].text())
        
        Main()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
    
