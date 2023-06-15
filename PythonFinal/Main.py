"""五子棋之人机对战"""

import sys  # 系统模块，用于与操作系统交互
import random  # 随机数模块，用于生成随机数
import pygame  # Pygame库，用于开发游戏和多媒体应用
from pygame.locals import *  # Pygame的本地模块，包含一些全局常量和变量
import pygame.gfxdraw  # Pygame的图形绘制模块，用于绘制图形
# 从checkerboard模块导入所需的类和函数
from checkerboard import Checkerboard, BLACK_CHESSMAN, WHITE_CHESSMAN, offset, Point

# 设置棋盘大小
SIZE = 30  # 棋盘每个点时间的间隔
Line_Points = 19  # 棋盘每行/每列点数
Outer_Width = 20  # 棋盘外宽度
Border_Width = 4  # 边框宽度
Inside_Width = 4  # 边框跟实际的棋盘之间的间隔
Border_Length = SIZE * (Line_Points - 1) + \
    Inside_Width * 2 + Border_Width  # 边框线的长度
Start_X = Start_Y = Outer_Width + \
    int(Border_Width / 2) + Inside_Width  # 网格线起点（左上角）坐标
SCREEN_HEIGHT = SIZE * (Line_Points - 1) + Outer_Width * \
    2 + Border_Width + Inside_Width * 2  # 游戏屏幕的高
SCREEN_WIDTH = SCREEN_HEIGHT + 200  # 游戏屏幕的宽

Stone_Radius = SIZE // 2 - 3  # 棋子半径
Stone_Radius2 = SIZE // 2 + 3
Checkerboard_Color = (0xE3, 0x92, 0x65)  # 棋盘颜色
BLACK_COLOR = (0, 0, 0)  # 设置黑色棋子颜色
WHITE_COLOR = (255, 255, 255)  # 设置白色棋子颜色
RED_COLOR = (200, 30, 30)
BLUE_COLOR = (30, 30, 200)

RIGHT_INFO_POS_X = SCREEN_HEIGHT + Stone_Radius2 * 2 + 10  # 设置右侧信息位置的X坐标(右下角)

# 在屏幕上绘制文本


def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)  # 字体和颜色
    screen.blit(imgText, (x, y))


def main():
    pygame.init()  # 初始化pygame库
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT))  # 创建一个窗口，设置窗口大小和标题
    pygame.display.set_caption('五子棋')

    font1 = pygame.font.SysFont('SimHei', 32)  # 加载字体1和字体2,用于显示文字
    font2 = pygame.font.SysFont('SimHei', 72)
    fwidth, fheight = font2.size('黑方获胜')  # 获取字体2中“黑方获胜”的宽度和高度

    checkerboard = Checkerboard(Line_Points)  # 创建一个棋盘对象，参数为行点数和列点数
    cur_runner = BLACK_CHESSMAN  # 将当前下棋者设为黑色棋子
    winner = None  # 将胜者设为空
    computer = AI(Line_Points, WHITE_CHESSMAN)  # 根据行点数和列点数创建一个电脑下棋对象

    black_win_count = 0  # 将黑方获胜计数器设为0
    white_win_count = 0  # 将白方获胜计数器设为0

# 当没有胜者时，程序会继续下棋，直到有一方获胜或者棋盘被下满。具体来说，它首先判断是否有胜者，如果没有则调用 _get_next() 函数获取下一个落子点，
# 并让电脑对手落子。然后再调用 checkerboard.drop() 函数来判断当前落子是否有效，如果有效则更新胜者计数器和当前落子点，否则提示“超出棋盘区域”。
# 如果已经有胜者，则直接增加胜利次数或平局次数。'''

    while True:
        for event in pygame.event.get():  # 遍历所有事件
            if event.type == QUIT:  # 如果收到退出事件，则退出程序
                sys.exit()
            elif event.type == KEYDOWN:  # 如果收到键盘按下事件，且按下的是回车键
                if event.key == K_RETURN:
                    if winner is not None:  # 如果已经有胜者，则重置棋盘和电脑对手
                        winner = None
                        cur_runner = BLACK_CHESSMAN
                        checkerboard = Checkerboard(Line_Points)
                        computer = AI(Line_Points, WHITE_CHESSMAN)
            elif event.type == MOUSEBUTTONDOWN:  # 如果还没有胜者，则处理鼠标点击事件
                if winner is None:
                    pressed_array = pygame.mouse.get_pressed()  # 获取当前鼠标状态
                    if pressed_array[0]:  # 如果鼠标左键被按下
                        mouse_pos = pygame.mouse.get_pos()  # 获取鼠标位置
                        click_point = _get_clickpoint(mouse_pos)  # 获取点击位置
                        if click_point is not None:  # 如果点击位置在棋盘内，则处理落子事件
                            if checkerboard.can_drop(click_point):
                                winner = checkerboard.drop(
                                    cur_runner, click_point)
                                if winner is None:  # 如果没有胜者，则继续下棋
                                    cur_runner = _get_next(cur_runner)
                                    computer.get_opponent_drop(click_point)
                                    AI_point = computer.AI_drop()
                                    winner = checkerboard.drop(
                                        cur_runner, AI_point)
                                    if winner is not None:  # 如果有胜者，则增加白方胜利次数或黑方胜利次数
                                        white_win_count += 1
                                    cur_runner = _get_next(cur_runner)
                                else:
                                    black_win_count += 1
                        else:
                            print('超出棋盘区域')

# 绘制棋盘和显示游戏信息的。具体来说，它首先遍历整个棋盘，根据每个格子上的棋子颜色来调用 _draw_chessman() 函数来绘制棋子。
# 然后调用 _draw_left_info() 函数来在屏幕左侧显示当前的下棋者、黑方胜利次数和白方胜利次数等信息。最后，如果有胜者，则在屏幕中央显示获胜者的姓名和颜色。

        # 画棋盘
        _draw_checkerboard(screen)

        # 画棋盘上已有的棋子
        for i, row in enumerate(checkerboard.checkerboard):
            for j, cell in enumerate(row):
                if cell == BLACK_CHESSMAN.Value:
                    _draw_chessman(screen, Point(j, i), BLACK_CHESSMAN.Color)
                elif cell == WHITE_CHESSMAN.Value:
                    _draw_chessman(screen, Point(j, i), WHITE_CHESSMAN.Color)

        _draw_left_info(screen, font1, cur_runner,
                        black_win_count, white_win_count)

# 在屏幕中央显示获胜者的姓名和颜色的。具体来说，它首先判断是否有胜者，如果有则调用 print_text() 函数来在屏幕中央显示获胜者的姓名和颜色。
# 其中，font2 是用于显示文本的字体对象，winner.Name 是获胜者的姓名，RED_COLOR 是红色的颜色值。最后，使用 pygame.display.flip() 函数更新屏幕显示。

        if winner:
            print_text(screen, font2, (SCREEN_WIDTH - fwidth)//2,
                       (SCREEN_HEIGHT - fheight)//2, winner.Name + '获胜', RED_COLOR)

        pygame.display.flip()

# 获取下一个落子点的。具体来说，它首先判断当前的棋子是黑方还是白方，如果是黑方则返回白方棋子，否则返回黑方棋子。这样可以保证每次下棋时都是交替进行的。


def _get_next(cur_runner):
    if cur_runner == BLACK_CHESSMAN:
        return WHITE_CHESSMAN
    else:
        return BLACK_CHESSMAN


# 画棋盘
def _draw_checkerboard(screen):
    # 填充棋盘背景色
    screen.fill(Checkerboard_Color)
    # 画棋盘网格线外的边框
    pygame.draw.rect(screen, BLACK_COLOR, (Outer_Width,
                     Outer_Width, Border_Length, Border_Length), Border_Width)
    # 画网格线
    for i in range(Line_Points):
        pygame.draw.line(screen, BLACK_COLOR,
                         (Start_Y, Start_Y + SIZE * i),
                         (Start_Y + SIZE * (Line_Points - 1), Start_Y + SIZE * i),
                         1)
    for j in range(Line_Points):
        pygame.draw.line(screen, BLACK_COLOR,
                         (Start_X + SIZE * j, Start_X),
                         (Start_X + SIZE * j, Start_X + SIZE * (Line_Points - 1)),
                         1)
    # 画星位和天元
    for i in (3, 9, 15):
        for j in (3, 9, 15):
            if i == j == 9:
                radius = 5
            else:
                radius = 3
            # pygame.draw.circle(screen, BLACK, (Start_X + SIZE * i, Start_Y + SIZE * j), radius)
            pygame.gfxdraw.aacircle(
                screen, Start_X + SIZE * i, Start_Y + SIZE * j, radius, BLACK_COLOR)
            pygame.gfxdraw.filled_circle(
                screen, Start_X + SIZE * i, Start_Y + SIZE * j, radius, BLACK_COLOR)


# 画棋子
def _draw_chessman(screen, point, stone_color):
    # pygame.draw.circle(screen, stone_color, (Start_X + SIZE * point.X, Start_Y + SIZE * point.Y), Stone_Radius)
    pygame.gfxdraw.aacircle(screen, Start_X + SIZE * point.X,
                            Start_Y + SIZE * point.Y, Stone_Radius, stone_color)
    pygame.gfxdraw.filled_circle(
        screen, Start_X + SIZE * point.X, Start_Y + SIZE * point.Y, Stone_Radius, stone_color)


# 画左侧信息显示,首先绘制当前的黑方和白方棋子的位置，然后分别在屏幕右侧和底部显示当前的玩家和电脑的信息。
# 接着在屏幕右侧显示当前的战况信息，包括黑方和白方的胜负情况。最后使用 print_text() 函数来在屏幕上显示文本信息。
def _draw_left_info(screen, font, cur_runner, black_win_count, white_win_count):
    _draw_chessman_pos(screen, (SCREEN_HEIGHT + Stone_Radius2,
                       Start_X + Stone_Radius2), BLACK_CHESSMAN.Color)
    _draw_chessman_pos(screen, (SCREEN_HEIGHT + Stone_Radius2,
                       Start_X + Stone_Radius2 * 4), WHITE_CHESSMAN.Color)

    print_text(screen, font, RIGHT_INFO_POS_X, Start_X + 3, '玩家', BLUE_COLOR)
    print_text(screen, font, RIGHT_INFO_POS_X, Start_X +
               Stone_Radius2 * 3 + 3, '电脑', BLUE_COLOR)

    print_text(screen, font, SCREEN_HEIGHT, SCREEN_HEIGHT -
               Stone_Radius2 * 8, '战况：', BLUE_COLOR)
    _draw_chessman_pos(screen, (SCREEN_HEIGHT + Stone_Radius2,
                       SCREEN_HEIGHT - int(Stone_Radius2 * 4.5)), BLACK_CHESSMAN.Color)
    _draw_chessman_pos(screen, (SCREEN_HEIGHT + Stone_Radius2,
                       SCREEN_HEIGHT - Stone_Radius2 * 2), WHITE_CHESSMAN.Color)
    print_text(screen, font, RIGHT_INFO_POS_X, SCREEN_HEIGHT -
               int(Stone_Radius2 * 5.5) + 3, f'{black_win_count} 胜', BLUE_COLOR)
    print_text(screen, font, RIGHT_INFO_POS_X, SCREEN_HEIGHT -
               Stone_Radius2 * 3 + 3, f'{white_win_count} 胜', BLUE_COLOR)

# 绘制棋子位置,首先使用 pygame.gfxdraw.aacircle() 函数来绘制圆圈的边缘，然后使用 pygame.gfxdraw.filled_circle() 函数来填充圆圈内部。
# 其中，pos[0] 和 pos[1] 分别表示棋子在屏幕上的横纵坐标位置，Stone_Radius2 表示棋子的半径。


def _draw_chessman_pos(screen, pos, stone_color):
    pygame.gfxdraw.aacircle(screen, pos[0], pos[1], Stone_Radius2, stone_color)
    pygame.gfxdraw.filled_circle(
        screen, pos[0], pos[1], Stone_Radius2, stone_color)


# 根据鼠标点击位置，返回游戏区坐标.
# 首先计算出点击位置相对于游戏区域左上角的偏移量，然后根据偏移量和棋盘大小计算出点击位置在棋盘上的横纵坐标。
# 接着判断该点是否在棋盘范围内，如果不在则返回 None。最后将该点的横纵坐标封装成一个 Point 对象并返回。
def _get_clickpoint(click_pos):
    pos_x = click_pos[0] - Start_X
    pos_y = click_pos[1] - Start_Y
    if pos_x < -Inside_Width or pos_y < -Inside_Width:
        return None
    x = pos_x // SIZE
    y = pos_y // SIZE
    if pos_x % SIZE > Stone_Radius:
        x += 1
    if pos_y % SIZE > Stone_Radius:
        y += 1
    if x >= Line_Points or y >= Line_Points:
        return None

    return Point(x, y)

# 定义一个 AI 类的构造函数。具体来说，它首先将传入的参数 line_points 和 chessman 分别赋值给实例变量 self._line_points、self._my 和 self._opponent,
# 其中 chessman 表示当前玩家(黑棋或白棋),self._opponent 则表示对手玩家。接着，创建一个大小为 line_points x line_points 的二维列表 self._checkerboard,
# 并将其所有元素初始化为 0。最后，定义了一个名为 get_opponent_drop 的方法，该方法接受一个点对象作为参数，并将该点的值设置为对手玩家的值。


class AI:
    def __init__(self, line_points, chessman):
        self._line_points = line_points
        self._my = chessman
        self._opponent = BLACK_CHESSMAN if chessman == WHITE_CHESSMAN else WHITE_CHESSMAN
        self._checkerboard = [[0] * line_points for _ in range(line_points)]

    def get_opponent_drop(self, point):
        self._checkerboard[point.Y][point.X] = self._opponent.Value

# 首先初始化 point 和 score 为 None,然后遍历整个棋盘，找到一个空点(即值为 0 的元素),计算该点的得分，并将其与当前最高得分进行比较。
# 如果该点的得分更高，则更新 score 和 point。如果两个点的得分相同但大于 0,则随机选择一个点作为落子位置。最后，将选中的点的位置赋值给当前玩家，并返回该点的位置。
    def AI_drop(self):
        point = None
        score = 0
        for i in range(self._line_points):
            for j in range(self._line_points):
                if self._checkerboard[j][i] == 0:
                    _score = self._get_point_score(Point(i, j))
                    if _score > score:
                        score = _score
                        point = Point(i, j)
                    elif _score == score and _score > 0:
                        r = random.randint(0, 100)
                        if r % 2 == 0:
                            point = Point(i, j)
        self._checkerboard[point.Y][point.X] = self._my.Value
        return point
# 计算一个点在棋盘上的价值得分。首先初始化 score 为 0,然后遍历所有可能的偏移量 offset,对于每个偏移量，
# 调用 _get_direction_score() 方法计算该点在该方向上的得分，并将其累加到 score 中。最后返回 score 作为该点的得分。

    def _get_point_score(self, point):
        score = 0
        for os in offset:
            score += self._get_direction_score(point, os[0], os[1])
        return score
# 计算一个点在棋盘上的价值得分,调用 _get_direction_score() 方法计算该点在该方向上的得分，并将其累加到相应的变量中。最后返回这些变量的值作为该点的得分。

    def _get_direction_score(self, point, x_offset, y_offset):
        count = 0   # 落子处我方连续子数
        _count = 0  # 落子处对方连续子数
        space = None   # 我方连续子中有无空格
        _space = None  # 对方连续子中有无空格
        both = 0    # 我方连续子两端有无阻挡
        _both = 0   # 对方连续子两端有无阻挡

        # 如果是 1 表示是边上是我方子，2 表示敌方子
        # 用来获取一个落子点的颜色的。具体来说,它首先调用 _get_stone_color() 方法来获取该点的颜色,并将结果存储在变量flag中。然后根据flag的值来判断该点属于哪一方，并进行相应的处理。
        # 如果 flag 等于 1,则表示该点属于当前玩家，需要继续向右下方向落子。在遍历的过程中，如果遇到空位，则将 space 设置为 True,以便后续判断是否存在连续的空位。
        # 如果遇到非空位，则根据当前玩家和对手的棋子颜色来更新计数器 count 和 _both,并根据是否存在连续的空位来更新变量 space。
        # 如果 flag 等于 2,则表示该点属于对方玩家，需要继续向右上方向落子。在遍历的过程中，如果遇到空位，则将 _space 设置为 True,以便后续判断是否存在连续的空位。
        # 如果遇到非空位，则根据当前玩家和对手的棋子颜色来更新计数器 _count 和 _both,并根据是否存在连续的空位来更新变量 _space。
        flag = self._get_stone_color(point, x_offset, y_offset, True)
        if flag != 0:
            for step in range(1, 6):
                x = point.X + step * x_offset
                y = point.Y + step * y_offset
                if 0 <= x < self._line_points and 0 <= y < self._line_points:
                    if flag == 1:
                        if self._checkerboard[y][x] == self._my.Value:
                            count += 1
                            if space is False:
                                space = True
                        elif self._checkerboard[y][x] == self._opponent.Value:
                            _both += 1
                            break
                        else:
                            if space is None:
                                space = False
                            else:
                                break   # 遇到第二个空格退出
                    elif flag == 2:
                        if self._checkerboard[y][x] == self._my.Value:
                            _both += 1
                            break
                        elif self._checkerboard[y][x] == self._opponent.Value:
                            _count += 1
                            if _space is False:
                                _space = True
                        else:
                            if _space is None:
                                _space = False
                            else:
                                break
                else:
                    # 遇到边也就是阻挡
                    if flag == 1:
                        both += 1
                    elif flag == 2:
                        _both += 1

        if space is False:
            space = None
        if _space is False:
            _space = None

        _flag = self._get_stone_color(point, -x_offset, -y_offset, True)
        if _flag != 0:
            for step in range(1, 6):
                x = point.X - step * x_offset
                y = point.Y - step * y_offset
                if 0 <= x < self._line_points and 0 <= y < self._line_points:
                    if _flag == 1:
                        if self._checkerboard[y][x] == self._my.Value:
                            count += 1
                            if space is False:
                                space = True
                        elif self._checkerboard[y][x] == self._opponent.Value:
                            _both += 1
                            break
                        else:
                            if space is None:
                                space = False
                            else:
                                break   # 遇到第二个空格退出
                    elif _flag == 2:
                        if self._checkerboard[y][x] == self._my.Value:
                            _both += 1
                            break
                        elif self._checkerboard[y][x] == self._opponent.Value:
                            _count += 1
                            if _space is False:
                                _space = True
                        else:
                            if _space is None:
                                _space = False
                            else:
                                break
                else:
                    # 遇到边也就是阻挡,具体来说，首先根据当前玩家和对手连续落子的次数来确定初始得分。
                    # 然后，根据落子的数量来逐步累加得分，并根据是否存在空位来调整得分。最后，返回最终得分。
                    if _flag == 1:
                        both += 1
                    elif _flag == 2:
                        _both += 1

        score = 0
        if count == 4:
            score = 10000
        elif _count == 4:
            score = 9000
        elif count == 3:
            if both == 0:
                score = 1000
            elif both == 1:
                score = 100
            else:
                score = 0
        elif _count == 3:
            if _both == 0:
                score = 900
            elif _both == 1:
                score = 90
            else:
                score = 0
        elif count == 2:
            if both == 0:
                score = 100
            elif both == 1:
                score = 10
            else:
                score = 0
        elif _count == 2:
            if _both == 0:
                score = 90
            elif _both == 1:
                score = 9
            else:
                score = 0
        elif count == 1:
            score = 10
        elif _count == 1:
            score = 9
        else:
            score = 0

        if space or _space:
            score /= 2

        return score

    # 判断指定位置处在指定方向上是我方子、对方子、空。首先计算出该点在棋盘上的坐标 (x, y),然后检查该点是否在棋盘范围内。
    # 如果在范围内，则根据该点的黑白值来判断该点属于哪一方，并返回相应的颜色值 1 或 2。如果不在范围内，则返回 0。
    def _get_stone_color(self, point, x_offset, y_offset, next):
        x = point.X + x_offset
        y = point.Y + y_offset
        if 0 <= x < self._line_points and 0 <= y < self._line_points:
            if self._checkerboard[y][x] == self._my.Value:
                return 1
            elif self._checkerboard[y][x] == self._opponent.Value:
                return 2
            else:
                if next:
                    return self._get_stone_color(Point(x, y), x_offset, y_offset, False)
                else:
                    return 0
        else:
            return 0


if __name__ == '__main__':
    main()
