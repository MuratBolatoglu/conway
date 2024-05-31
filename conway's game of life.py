import pygame
import random
import copy 
black=(255,255,255)
gray=(128,128,128)
yellow=(2,193,149)

width,height=800,800
tile_size=20
fps=60

grid_width=width//tile_size
grid_height=height//tile_size

screen=pygame.display.set_mode((width,height))

clock=pygame.time.Clock()


def neighbor(grid,row,col):
    try:
        return grid[row][col]==1
    except IndexError:
        return 0
def update(cells):
    x=copy.deepcopy(cells)
    r=[-1,0,1]
    for i in range(0,len(cells)):
        for j in range(0,len(cells[0])):
            n=0
            for row in r:
                for col in r:
                    if not(i+row==-1 or j+col==-1):
                        n+=neighbor(cells,i+row,j+col)
            if cells[i][j]==1:n-=1
            if cells[i][j]==1 and n!=2 and n!=3:x[i][j]=0
            if cells[i][j]==0 and n==3: x[i][j]=1
    return x

def generate(num,grid):
    for i in range(num):
        row=random.randrange(0,len(grid))
        col=random.randrange(0,len(grid[0]))
        if grid[row][col]==0:grid[row][col]=1
    return grid

def draw_grid(lst):
    for i in range(0,len(lst)):
        for j in range(0,len(lst[0])):
            if lst[i][j]==1:
                top_left=(tile_size * j , tile_size * i)
                pygame.draw.rect(screen,yellow,(*top_left,tile_size,tile_size))
    for row in range(height):
        pygame.draw.line(screen,black,(0,row*tile_size),(width,row*tile_size))
    for col in range(width):
        pygame.draw.line(screen,black,(col*tile_size,0),(col*tile_size,height))



def main():
    holdrow,holdcol=-1,-1
    grid=[[0 for i in range(grid_height)] for j in range(grid_width)]
    running=True
    play=False
    freq=30
    count=0
    while running:
        if play:count+=1
        if count>=freq:
            grid=update(grid)
            count=0
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False

            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    play=False
                    x,y=pygame.mouse.get_pos()
                    col=x // tile_size
                    row = y // tile_size
                    if grid[row][col]==0:grid[row][col]=1
                    else:grid[row][col]=0
            elif pygame.mouse.get_pressed()[0]==True:
                play=False
                x,y=pygame.mouse.get_pos()
                col=x // tile_size
                row = y // tile_size
                if pygame.mouse.get_pressed()[0]==True and (holdrow!=row or holdcol!=col):
                        if grid[row][col]==0:
                            grid[row][col]=1
                            holdrow,holdcol=row,col
                        else:
                            grid[row][col]=0
                            holdrow,holdcol=row,col

                            
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    play=not play
                if event.key== pygame.K_c:
                    grid=[[0 for i in range(grid_height)] for j in range(grid_width)]
                    play=False
                if event.key==pygame.K_g:
                    play=False
                    grid=[[0 for i in range(grid_height)] for j in range(grid_width)]
                    num=random.randrange(100,200)
                    grid=generate(num,grid)

            
        screen.fill(gray)
        draw_grid(grid)
        pygame.display.update()
    pygame.quit()

main()