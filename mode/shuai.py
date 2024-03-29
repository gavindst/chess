from mode.chess import Chess

class Shuai(Chess):
    # 如果使用父类的构造函数,这里会自动调用不需要重写
    def __init__(self, x, y, red=True, selected=False):
        super(Shuai, self).__init__(x, y, red=True, selected=False)
        self.name = '帅'
        self.red = red

    def picture(self):
        if self.red:
            pic = self.redpic()
        else:
            pic = self.blackpic()
        return pic

    def redpic(self):
        pic = 'red_king.gif'
        if self.selected:
            return pic
        else:
            return pic
    def blackpic(self):
        pic = 'black_king.gif'
        if self.selected:
            return pic
        else:
            return pic

    def rule(self, dx, dy):
        if abs(dx) + abs(dy) == 1:
            return True
        return False
 
    def can_move(self, start_position, end_position, chessboard):
        dx = end_position[0] - start_position[0]
        dy = end_position[1] - start_position[1]
        x, y = end_position
        if self.rule(dx, dy):
            # 移动
            if not self.position_has_chess(end_position, chessboard):
                if not self.is_out_range(x, y):
                    return False
                return True
            else:
                # 吃子
                # 是否本方棋子
                if self.chess_is_my(self.red, chessboard[x][y]):
                    return False
                else:
                    # 吃子
                    if not self.is_out_range(x, y):
                        return False
                    return True
        else:
            return False

    # 判断是否过界
    # 过界 返回 False
    def is_out_range(self, x, y):
        if self.red and 2 < x < 6 and 6 < y < 10:
            return True
        if not self.red and 2 < x < 6 and -1 < y < 3:
            return True
        return False


    # 检查是否越界,越界则返回False
    def checkp(self, pos):
        x,y = pos
        if x < 0 or y < 0 or x > 8 or y > 9:
            return False
        return True
    # 返回棋子能够移动的所有位置
    # position 棋子位置, chessboard棋盘二维列表
    # 返回列表,列表元素为元组
    def try_move(self, position, chessboard):
        x,y = position
        a = [(x+1,y),(x-1,y),(x,y-1),(x,y+1)]
        b = []

        for i in a:
            if not self.checkp(i):
                continue
            if self.can_move(position, i, chessboard):
                b.append(i)
        return b
