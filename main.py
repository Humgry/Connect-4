import sys
import time
import pygame
from pygame.locals import *
pygame.init()

# set up
FPS = pygame.time.Clock()
frames = 30
screen = pygame.display.set_mode((640,550))
screen.fill((255,255,255))
pygame.display.set_caption("Connect 4 V1")
bkg_img = pygame.image.load('Connect4Board.png')

big_font = pygame.font.SysFont("Verdana", 60)
game_tie = big_font.render("Tie Game", True, (0,0,0))
game_r = big_font.render("Red Wins", True, (0,0,0))
game_b = big_font.render("Black Wins", True, (0,0,0))
small_font = pygame.font.SysFont("Verdana", 20)
close_msg = small_font.render("Closing in 5 seconds...", True, (0,0,0))

board = []
for i in range(7):
    board.append([''] * 6)
board_coord = []
for i, row in enumerate(board):
    x_pos = 50 + (90 * i)
    list_ = []
    for ii, checker in enumerate(row):
        y_pos = 111 + (80 * ii)
        list_.append((x_pos, y_pos))
    board_coord.append(list_)

def win_cond():
    # vertical
    for column in board:
        for i in range(3):
            if column[i] == column[i+1] and column[i] == column[i+2] and column[i] == column[i+3] and column[i] != '':
                return True, column[i]
    # horizontal
    for i in range(6):
        for ii in range(4):
            if board[ii][i] == board[ii+1][i] and board[ii][i] == board[ii+2][i] and board[ii][i] == board[ii+3][i] and board[ii][i] != '':
                return True, board[ii][i]
    # diagonal up
    for i in range(4):
        for ii in range(1,4):
            if board[i][-ii] == board[i+1][-(ii+1)] and board[i][-ii] == board[i+2][-(ii+2)] and board[i][-ii] == board[i+3][-(ii+3)] and board[i][-ii] != '':
                return True, board[i][-ii]
    # diagonal down
    for i in range(3):
        for ii in range(4):
            if board[ii][i] == board[ii+1][i+1] and board[ii][i] == board[ii+2][i+2] and board[ii][i] == board[ii+3][i+3] and board[ii][i] != '':
                return True, board[ii][i]
    return False, 0

def get_ind(x):
    center = 50
    for i in range(7):
        if x>(center-50) and x<(center+50):
            return i
        center += 90

def center(x,y):
    center = 50
    cond = False
    for i in range(7):
        if x>(center-50) and x<(center+50):
            cond = True
            break
        center += 90
    
    if cond == False:
        return False, 0
    
    column = board[i]
    for ii in range(1,7):
        if column[-ii] == '':
            return i, -ii

class Chip(pygame.sprite.Sprite):
    def __init__(self,x,y,color):
        super().__init__()
        if color == 'R':
            self.image = pygame.image.load('red.png')
        else:
            self.image = pygame.image.load('black.png')
        self.surf = pygame.Surface((75,75))
        self.rect = self.surf.get_rect(center=(x,y))

all_sprites = pygame.sprite.Group()

count = 0

while True:
    screen.fill((255,255,255))
    game_over = False
    
    if count%2 == 0:
        color = 'R'
        color_t = (255,0,0)
    elif count%2 == 1:
        color = 'B'
        color_t = (0,0,0)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            raw_x,raw_y = event.pos
            i, ii = center(raw_x, raw_y)
            x, y = board_coord[i][ii]
            c1 = Chip(x,y,color)
            all_sprites.add(c1)
            board[i][ii] = color
            count += 1
            game_over, winner = win_cond()

    if game_over == True or count == 42:
        if winner:
            if winner == 'R':
                screen.blit(game_r, (30,30))
            elif winner == 'B':
                screen.blit(game_b, (30,30))
        else:
            screen.blit(game_tie, (30,30))
        screen.blit(close_msg, (30,100))
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        sys.exit()
    
    x,y = pygame.mouse.get_pos()
    if x:
        ind = get_ind(x)
        x_pos = board_coord[ind][0][0]
        pygame.draw.circle(screen, color_t, (x_pos,35), 35)
        
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
    
    screen.blit(bkg_img, (0,70))
    FPS.tick(frames)
    pygame.display.update()