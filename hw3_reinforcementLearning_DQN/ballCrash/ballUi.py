import pygame as pg  # 导入pygame库，用于游戏开发
import pymunk.pygame_util  # 导入pymunk.pygame_util模块，用于在pygame中绘制pymunk物理引擎的形状
from ballType import createBall  # 导入createBall函数，用于创建小球对象

class GameBoard(object):
    def __init__(self, create_time, gravity):
        self.RES = self.WIDTH, self.HEIGHT = 400, 800  # 设置游戏窗口的尺寸
        self.FPS = 50  # 设置游戏的帧率

        # 初始化游戏中的小球列表
        self.balls = []
        self.fruits = []

        self.reset()  # 调用reset方法，初始化游戏状态

        self.init_y = int(0.15 * self.HEIGHT)  # 设置初始小球生成的y坐标
        self.init_x = int(self.WIDTH / 2)  # 设置初始小球生成的x坐标（屏幕中心）

        pg.init()  # 初始化pygame模块
        self.surface = pg.display.set_mode(self.RES)  # 创建游戏窗口表面
        self.clock = pg.time.Clock()  # 创建游戏时钟对象
        self.draw_options = pymunk.pygame_util.DrawOptions(self.surface)  # 创建绘制选项对象，用于在游戏窗口中绘制物理形状

        self.space = pymunk.Space()  # 创建pymunk空间对象，用于模拟物理世界
        self.space.gravity = gravity  # 设置物理空间的重力
        self.create_time = create_time  # 设置小球生成的时间间隔

    def reset(self):
        # 移除之前的小球
        for ball in self.balls:
            self.space.remove(ball, ball.body)
        del self.fruits
        del self.balls
        # 初始化小球以及游戏得分等状态
        self.fruits = []
        self.balls = []
        self.score = 0
        self.last_score = 0
        self.count = 1
        self.lock = False
        self.waiting = False
        self.current_fruit = None
        self.i = None
        self.fail_count = 0
        self.alive = True

    def init_segment(self):
        # 初始化游戏边界
        B1, B2, B3, B4 = (0, 0), (0, self.HEIGHT), (self.WIDTH, self.HEIGHT), (self.WIDTH, 0)  # 左上、左下、右下、右上
        borders = (B1, B2), (B2, B3), (B3, B4)  # 边界线段的起点和终点坐标
        # 遍历每一条边界线段，并调用create_segment方法创建并添加到pymunk空间中
        for border in borders:
            self.create_segment(*border, 20, self.space, 'lightblue')

    def setup_collision_handler(self):
        # 设置碰撞处理程序
        def post_solve_bird_line(arbiter, space, data):
            if not self.lock:
                self.lock = True
                b1, b2 = None, None
                i = arbiter.shapes[0].collision_type + 1
                x1, y1 = arbiter.shapes[0].body.position
                x2, y2 = arbiter.shapes[1].body.position
                if y1 > y2:
                    x, y = x1, y1
                else:
                    x, y = x2, y2
                if arbiter.shapes[0] in self.balls:
                    b1 = self.balls.index(arbiter.shapes[0])
                    space.remove(arbiter.shapes[0], arbiter.shapes[0].body)
                    self.balls.remove(arbiter.shapes[0])
                    fruit1 = self.fruits[b1]
                    self.fruits.remove(fruit1)
                if arbiter.shapes[1] in self.balls:
                    b2 = self.balls.index(arbiter.shapes[1])
                    space.remove(arbiter.shapes[1], arbiter.shapes[1].body)
                    self.balls.remove(arbiter.shapes[1])
                    fruit2 = self.fruits[b2]
                    self.fruits.remove(fruit2)

                ball = createBall(i, x, self.init_y)  # 创建新的小球对象
                self.fruits.append(ball)  # 将小球对象添加到小球列表中
                ball = self.create_ball(
                    self.space, x, y, m=ball.r//10, r=ball.r-1, i=i)  # 创建新的小球对象
                self.balls.append(ball)  # 将小球对象添加到小球列表中
                if i < 11:
                    self.last_score = self.score
                    self.score += i
                elif i == 11:
                    self.last_score = self.score
                    self.score += 100
                self.lock = False

        # 遍历小球的碰撞类型，并设置碰撞处理程序
        for i in range(1, 11):
            # 为碰撞类型为i的物体设置碰撞处理程序为post_solve_bird_line
            self.space.add_collision_handler(i, i).post_solve = post_solve_bird_line

    def create_ball(self, space, x, y, m=1, r=7, i=1):
        # 创建小球的方法
        ball_moment = pymunk.moment_for_circle(m, 0, r)  # 计算小球的惯性矩
        ball_body = pymunk.Body(m, ball_moment)  # 创建小球的物理体
        ball_body.position = x, y  # 设置小球的初始位置
        ball_shape = pymunk.Circle(ball_body, r)  # 创建小球的形状
        ball_shape.elasticity = 0.3  # 设置小球的弹性
        ball_shape.friction = 0.6  # 设置小球的摩擦系数
        ball_shape.collision_type = i  # 设置小球的碰撞类型
        space.add(ball_body, ball_shape)  # 将小球的物理体和形状添加到物理空间中
        return ball_shape

    def create_segment(self, from_, to_, thickness, space, color):
        # 创建线段的方法
        segment_shape = pymunk.Segment(space.static_body, from_, to_, thickness)  # 创建线段形状
        segment_shape.color = pg.color.THECOLORS[color]  # 设置线段的颜色
        segment_shape.friction = 0.6  # 设置线段的摩擦系数
        space.add(segment_shape)  # 将线段形状添加到物理空间中

    def show_score(self):
        # 在屏幕上显示得分
        score_font = pg.font.SysFont("Times New Roman", 30)  # 设置得分显示的字体和大小
        score_text = score_font.render('score: {}'.format(str(self.score)), True, (255, 0, 0))  # 渲染得分文本
        text_rect = score_text.get_rect()  # 获取文本的矩形区域
        text_rect.topleft = [160, 10]  # 设置文本左上角的位置
        self.surface.blit(score_text, text_rect)  # 在游戏窗口上绘制得分文本

    def check_fail(self):
        # 检查游戏失败条件
        exist = False  # 初始化标志变量，表示是否存在小球
        if len(self.balls):
            for i, ball in enumerate(self.balls[:-1]):
                if ball:
                    if int(ball.body.position[1]) < self.init_y:  # 如果小球掉出了屏幕
                        self.fail_count += 1  # 失败次数加1
                        exist = True  # 设置存在小球的标志为True
                        break
        if exist:
            if self.fail_count > self.FPS*self.create_time:  # 如果失败次数超过阈值
                self.alive = False  # 设置游戏状态为不活跃
                return True  # 返回游戏失败
            return False  # 否则返回游戏未失败
        else:
            self.fail_count = 0  # 重置失败次数为0
            return False  # 返回游戏未失败

    def run(self):
        pass  # 运行游戏的主循环，具体实现在子类中