import pygame

#define the grid / playing field

grid = [
    [5, 0, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0,1 , 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 6, 0, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

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

        updateScreen()
        solve()
        updateScreen()

        pygame.display.update()



Main()

pygame.quit()