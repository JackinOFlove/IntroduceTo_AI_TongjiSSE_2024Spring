import pygame as pg
#生成球
def createBall(type, x, y):
    ball = None
    if type == 1:
        ball = Marble(x, y)
    elif type == 2:
        ball = Crystalball(x, y)
    elif type == 3:
        ball = Golf(x, y)
    elif type == 4:
        ball = Poolball(x, y)
    elif type == 5:
        ball = Tennis(x, y)
    elif type == 6:
        ball = Baseball(x, y)
    elif type == 7:
        ball = Bowling(x, y)
    elif type == 8:
        ball = Volleyball(x, y)
    elif type == 9:
        ball = Football(x, y)
    elif type == 10:
        ball = Basketball(x, y)
    elif type == 11:
        ball = Beachball(x, y)
    return ball
#球类
class Ball():
    def __init__(self, x, y):
        self.load_images()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle_degree = 0

    def load_images(self):
        pass

    def update_position(self, x, y, angle_degree=0):
        self.rect.x = x - self.r
        self.rect.y = y - self.r
        self.angle_degree = angle_degree

    def draw(self, surface):
        surface.blit(self.image, self.rect)
#弹珠
class Marble(Ball):
    def __init__(self, x, y):
        self.r = 2 * 10
        self.type = 1
        self.size = (self.r*2, self.r*2)
        Ball.__init__(self, x - self.r, y - self.r)

    def load_images(self):
        self.image = pg.image.load('image/marble.png')
        self.image = pg.transform.smoothscale(self.image, self.size)
#蓝色球
class Crystalball(Ball):
    def __init__(self, x, y):
        self.r = 2 * 15
        self.type = 2
        self.size = (self.r*2, self.r*2)
        Ball.__init__(self, x - self.r, y - self.r)

    def load_images(self):
        self.image = pg.image.load('image/crystalball.png')
        self.image = pg.transform.smoothscale(self.image, self.size)
#高尔夫球
class Golf(Ball):
    def __init__(self, x, y):
        self.r = 2 * 21
        self.type = 3
        self.size = (self.r*2, self.r*2)
        Ball.__init__(self, x - self.r, y - self.r)

    def load_images(self):
        self.image = pg.image.load('image/golf.png')
        self.image = pg.transform.smoothscale(self.image, self.size)
#台球
class Poolball(Ball):
    def __init__(self, x, y):
        self.r = 2 * 23
        self.type = 4
        self.size = (self.r*2, self.r*2)
        Ball.__init__(self, x - self.r, y - self.r)

    def load_images(self):
        self.image = pg.image.load('image/poolball.png')
        self.image = pg.transform.smoothscale(self.image, self.size)
#网球
class Tennis(Ball):
    def __init__(self, x, y):
        self.r = 2 * 29
        self.type = 5
        self.size = (self.r*2, self.r*2)
        Ball.__init__(self, x - self.r, y - self.r)

    def load_images(self):
        self.image = pg.image.load('image/tennis.png')
        self.image = pg.transform.smoothscale(self.image, self.size)
#棒球
class Baseball(Ball):
    def __init__(self, x, y):
        self.r = 2 * 35
        self.type = 6
        self.size = (self.r*2, self.r*2)
        Ball.__init__(self, x - self.r, y - self.r)

    def load_images(self):
        self.image = pg.image.load('image/baseball.png')
        self.image = pg.transform.smoothscale(self.image, self.size)
#保龄球
class Bowling(Ball):
    def __init__(self, x, y):
        self.r = 2 * 37
        self.type = 7
        self.size = (self.r*2, self.r*2)
        Ball.__init__(self, x - self.r, y - self.r)

    def load_images(self):
        self.image = pg.image.load('image/bowling.png')
        self.image = pg.transform.smoothscale(self.image, self.size)
#排球
class Volleyball(Ball):
    def __init__(self, x, y):
        self.r = 2 * 50
        self.type = 8
        self.size = (self.r*2, self.r*2)
        Ball.__init__(self, x - self.r, y - self.r)

    def load_images(self):
        self.image = pg.image.load('image/volleyball.png')
        self.image = pg.transform.smoothscale(self.image, self.size)
#足球
class Football(Ball):
    def __init__(self, x, y):
        self.r = 2 * 59
        self.type = 9
        self.size = (self.r*2, self.r*2)
        Ball.__init__(self, x - self.r, y - self.r)

    def load_images(self):
        self.image = pg.image.load('image/football.png')
        self.image = pg.transform.smoothscale(self.image, self.size)
#篮球
class Basketball(Ball):
    def __init__(self, x, y):
        self.r = 2 * 60
        self.type = 10
        self.size = (self.r*2, self.r*2)
        Ball.__init__(self, x - self.r, y - self.r)

    def load_images(self):
        self.image = pg.image.load('image/basketball.png')
        self.image = pg.transform.smoothscale(self.image, self.size)
#沙滩球
class Beachball(Ball):
    def __init__(self, x, y):
        self.r = 2 * 78
        self.type = 11
        self.size = (self.r*2, self.r*2)
        Ball.__init__(self, x - self.r, y - self.r)

    def load_images(self):
        self.image = pg.image.load('image/beachball.png')
        self.image = pg.transform.smoothscale(self.image, self.size)