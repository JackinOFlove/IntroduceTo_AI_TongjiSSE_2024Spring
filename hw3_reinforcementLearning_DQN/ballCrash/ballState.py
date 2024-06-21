import pygame as pg  # 导入Pygame库
from random import randrange  # 导入randrange函数
from ballType import createBall  # 从ballType模块中导入createBall函数
from ballUi import GameBoard  # 从ballUi模块中导入GameBoard类

class AI_Board(GameBoard):  # AI_Board类继承自GameBoard类
    def __init__(self):
        # 初始化AI_Board对象
        self.create_time = 0.5  # 小球创建时间间隔
        self.gravity = (0, 4000)  # 重力
        GameBoard.__init__(self, self.create_time, self.gravity)  # 调用父类初始化方法
        self.action_num = 16  # 动作数量
        self.init_segment()  # 初始化边界线段
        self.setup_collision_handler()  # 设置碰撞处理器

    def decode_action(self, action):
        # 解码动作
        seg = (self.WIDTH - 40) // self.action_num  # 将窗口宽度分成16个部分
        x = action * seg + 20  # 计算小球下落的x坐标
        print('[information] Ball drop down at x =', x)  # 打印提示信息
        return x  # 返回x坐标

    def next_frame(self, action=None):
        try:
            reward = 0  # 初始化奖励为0
            if not self.waiting:
                self.count += 1  # 计数器加1
            self.surface.fill(pg.Color('white'))  # 填充白色背景

            self.space.step(1 / self.FPS)  # 让空间进行模拟
            self.space.debug_draw(self.draw_options)  # 绘制物理空间的调试图形
            if self.count % (self.FPS * self.create_time) == 0:  # 如果计数达到了小球创建时间
                self.i = randrange(1, 5)  # 随机生成1到4的整数
                self.current_fruit = createBall(  # 创建当前小球对象
                    self.i, int(self.WIDTH/2), self.init_y - 10)  # 小球的类型和位置
                self.count = 1  # 计数器重置为1
                self.waiting = True  # 设置等待状态为True

            for event in pg.event.get():  # 遍历所有事件
                if event.type == pg.QUIT:  # 如果事件是退出事件
                    exit()  # 退出游戏

            if not action is None and self.i and self.waiting:  # 如果动作不为空且存在当前小球且处于等待状态
                x = self.decode_action(action)  # 解码动作得到小球下落的x坐标
                fruit = createBall(self.i, x, self.init_y)  # 创建小球对象
                self.fruits.append(fruit)  # 将小球对象添加到小球列表中
                ball = self.create_ball(  # 创建小球对象
                    self.space, x, self.init_y, m=fruit.r//10, r=fruit.r-fruit.r % 5, i=self.i)  # 小球的位置和类型
                self.balls.append(ball)  # 将小球对象添加到小球列表中
                self.current_fruit = None  # 当前小球置为None
                self.i = None  # 变量i置为None
                self.waiting = False  # 设置等待状态为False

            reward = self.score - self.last_score  # 计算奖励值
            if reward > 0:  # 如果奖励大于0
                self.last_score = self.score  # 更新上一次得分为当前得分

            if not self.lock:  # 如果未锁定
                for i, ball in enumerate(self.balls):  # 遍历小球列表
                    if ball:  # 如果小球存在
                        angle = ball.body.angle  # 获取小球的旋转角度
                        x, y = (int(ball.body.position[0]), int(
                            ball.body.position[1]))  # 获取小球的坐标
                        self.fruits[i].update_position(x, y, angle)  # 更新小球的位置和旋转角度
                        self.fruits[i].draw(self.surface)  # 在表面上绘制小球

            if self.current_fruit:  # 如果有当前小球
                self.current_fruit.draw(self.surface)  # 在表面上绘制当前小球

            pg.draw.aaline(self.surface, (0, 0, 0), (0, self.init_y), (self.WIDTH, self.init_y), 5)  # 绘制辅助线

            self.show_score()  # 显示得分信息

            if self.check_fail():  # 检查是否失败
                self.score = 0  # 分数清零
                self.last_score = 0  # 上一次得分清零
                self.reset()  # 重置游戏状态

            pg.display.flip()  # 更新显示
            self.clock.tick(self.FPS)  # 控制帧率
            image = pg.surfarray.array3d(pg.display.get_surface())  # 获取当前表面的像素数组

        except Exception as e:  # 捕获异常
            print(e)  # 打印异常信息
            if len(self.fruits) > len(self.balls):  # 如果小球列表长度大于小球列表长度
                seg = len(self.fruits) - len(self.balls)  # 计算长度差
                self.fruits = self.fruits[:-seg]  # 将多出的小球对象从列表中删除
            elif len(self.balls) > len(self.fruits):  # 如果小球列表长度大于小球列表长度
                seg = len(self.balls) - len(self.fruits)  # 计算长度差
                self.balls = self.balls[:-seg]  # 将多出的小球对象从列表中删除

        return image, self.score, reward, self.alive  # 返回图像、得分、奖励、游戏状态

    def next(self, action=None):
        # 执行下一步操作
        _, _, reward, _ = self.next_frame(action=action)  # 获取当前帧的奖励值
        for _ in range(self.FPS * 3):  # 迭代进行三秒的帧更新
            _, _, nreward, _ = self.next_frame()  # 获取下一帧的奖励值
            reward += nreward  # 累加奖励值
        image, _, nreward, _ = self.next_frame()  # 获取下一帧的图像和奖励值
        reward += nreward  # 累加奖励值
        if reward == 0:  # 如果奖励为0
            reward = -self.i  # 奖励为-i
        return image, self.score, reward, self.alive  # 返回图像、得分、奖励、游戏状态

    def run(self):
        # 运行游戏循环
        while True:  # 无限循环
            action = randrange(0, self.action_num)  # 随机生成一个动作
            print('action:', action)  # 打印动作信息
            _, score, reward, alive = self.next(action=action)  # 执行下一步操作
            print('score:{} reward:{} alive:{}'.format(score, reward, alive))  # 打印得分、奖励、游戏状态信息

if __name__ == '__main__':
    game = AI_Board()  # 创建AI_Board对象
    game.run()  # 运行游戏循环
