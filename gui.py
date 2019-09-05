import os

import pygame
from pygame.locals import *

from control import Chessboard

if not pygame.font: print('fonts disable')
if not pygame.mixer: print('mixer disable')

# 主路径
main_dir = os.path.split(os.path.abspath(__file__))[0]
# 资源文件路径
data_dir = os.path.join(main_dir, 'source')

def load_image(name):
    "loads an image, prepares it for play"
    filename = os.path.join(data_dir, name)
    try:
        surface = pygame.image.load(filename)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(filename, pygame.get_error()))
    return surface.convert(), surface.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        raise SystemExit('Could not load sound "%s" %s'%(name, pygame.get_error()))
        

class ChessBoard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image, self.rect = load_image('boardchess.gif')

# 棋子类,position为棋子坐标
class Piece(pygame.sprite.Sprite):
    def __init__(self, name, position, *groups):
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = load_image(name)

        self.position = position
        x, y = self.position
        # 通过改变矩形的中心来改变位置
        self.rect.center = (x * 80 + 40, y * 80 + 40)

    def move(self, position):
        x, y = position
        self.rect.center = (x * 80 + 40, y * 80 + 40)
        self.position = position


# 鼠标相对于棋盘的位置
# 返回位置坐标x,y
def mouse_pos(position):
    x,y = position
    ex = x // 80
    ey = y // 80
    return ex,ey

def chess_main():
    pygame.init()

    screen = pygame.display.set_mode((720,800))
    pygame.display.set_caption('chess')

    clock = pygame.time.Clock()

    chessboard = ChessBoard()

    # init group
    board = pygame.sprite.Group()
    chesses = pygame.sprite.Group()

    board.add((chessboard, ))
    # add chess
    chess = Chessboard()
    for i in chess.chessboard:
        for y in i:
            if not y == 0:
                temp = Piece(y.picture(), y.position())
                chesses.add((temp,))
    

    going = True
    # 一会要测试一下这里
    global start_pos
    global end_pos
    start_pos = end_pos = (-1,-1)
    while going:
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == KEYDOWN:
                if event.key == pygame.K_s:
                    chess.save()
            elif event.type == MOUSEBUTTONDOWN:
                # 鼠标按下
                pos = pygame.mouse.get_pos()
                end_pos = mouse_pos(pos)

                if chess.move(start_pos,end_pos):
                    for spr in chesses:
                        if spr.position == end_pos:
                            spr.kill()
                        if spr.position == start_pos:
                            spr.move(end_pos)
                    end_pos = start_pos = (-1,-1)
                else:
                    start_pos = end_pos

        board.draw(screen)
        chesses.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    chess_main()
