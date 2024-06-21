import random
import cv2
import os
import numpy as np
from ballState import AI_Board  # 导入AI_Board类
from collections import deque  # 用于高效地添加和删除元素
from keras.models import Sequential  # 导入Sequential模型
from keras.layers.convolutional import Conv2D  # 导入卷积层
from keras.layers.core import Dense, Activation, Flatten  # 导入全连接层、激活层和展平层
from keras.optimizers import Adam  # 导入Adam优化器

# 建立神经网络
def build_network(num_actions):
    print("Initializing model ....")
    model = Sequential()
    # 添加第一层卷积层，使用32个8x8的过滤器，步幅为4，输入形状为80x160x3
    model.add(Conv2D(32, (8, 8), padding='same', strides=(4, 4), input_shape=(80, 160, 3)))
    model.add(Activation('relu'))  # 添加ReLU激活函数
    # 添加第二层卷积层，使用64个4x4的过滤器，步幅为2
    model.add(Conv2D(64, (4, 4), padding='same', strides=(2, 2)))
    model.add(Activation('relu'))  # 添加ReLU激活函数
    # 添加第三层卷积层，使用64个3x3的过滤器，步幅为1
    model.add(Conv2D(64, (3, 3), padding='same', strides=(1, 1)))
    model.add(Activation('relu'))  # 添加ReLU激活函数
    # 添加第四层卷积层，使用64个4x4的过滤器，步幅为2
    model.add(Conv2D(64, (4, 4), padding='same', strides=(2, 2)))
    model.add(Activation('relu'))  # 添加ReLU激活函数
    # 添加第五层卷积层，使用64个3x3的过滤器，步幅为1
    model.add(Conv2D(64, (3, 3), padding='same', strides=(1, 1)))
    model.add(Activation('relu'))  # 添加ReLU激活函数
    model.add(Flatten())  # 将多维输入展平成一维
    # 添加全连接层，512个神经元
    model.add(Dense(512))
    model.add(Activation('relu'))  # 添加ReLU激活函数
    # 添加输出层，神经元数量等于动作数
    model.add(Dense(num_actions))
    model.add(Activation('softmax'))  # 添加softmax激活函数

    # 如果有已经训练出的模型文件.h5，先读取其文件再进行训练
    if os.path.exists("trainDQN.h5"):
        print("Loading weights from trainDQN.h5 .....")
        model.load_weights("trainDQN.h5")
        print("Weights loaded successfully.")
    # 使用Adam优化器编译模型，学习率为1e-4，损失函数为均方误差
    adam = Adam(learning_rate=1e-4)
    model.compile(loss='mse', optimizer=adam)
    print("Finished building model.")

    return model

# 处理游戏中每种水果的图片
def process(input):
    # 将图像从288x404调整大小到160x80
    image = cv2.resize(input, (160, 80))
    # 将像素值缩放到(0,1)范围内
    image = image / 255.0
    return image

# 训练神经网络
def train_network():
    game = AI_Board()  # 初始化游戏实例
    model = build_network(game.action_num)  # 构建神经网络模型
    num_actions = game.action_num  # 获取有效动作的数量
    FINAL_EPSILON = 0.0001  # ε的最终值，用于探索与利用的平衡
    INITIAL_EPSILON = 0.1  # ε的起始值
    replay_memory = 500  # 记忆库的容量
    discount = 0.99  # 折扣因子，用于未来奖励的衰减
    observe = 200  # 训练前观察的时间步骤
    explore = 3000000  # 在这个时间步数内逐渐减少epsilon

    epsilon = INITIAL_EPSILON  # 初始化epsilon
    timestep = 0  # 初始化时间步数
    loss = 0  # 初始化损失
    replay = deque()  # 初始化记忆库

    image, _, reward, alive = game.next(0)  # 获取初始状态图像
    input_image = process(image)  # 对图像进行预处理
    input_image = input_image.reshape(1, input_image.shape[0], input_image.shape[1], input_image.shape[2])  # 调整图像形状

    while True:  # 开始训练循环
        if random.random() <= epsilon:  # 以epsilon概率选择随机动作
            action = random.randint(0, num_actions)
        else:  # 否则选择Q值最大的动作
            q = model.predict(input_image)
            action = np.argmax(q)

        if epsilon > FINAL_EPSILON and timestep > observe:  # 线性衰减epsilon
            epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / explore

        image1, _, reward, alive = game.next(action)  # 执行动作并获取新的状态
        image1 = process(image1)  # 对新的状态图像进行预处理
        input_image1 = image1.reshape(1, image1.shape[0], image1.shape[1], image1.shape[2])  # 调整图像形状

        replay.append((input_image, action, reward, input_image1, alive))  # 将新经验存入记忆库
        if len(replay) > replay_memory:  # 如果记忆库超过容量，则删除最旧的经验
            replay.popleft()

        if timestep > observe:  # 如果步骤大于观察步骤，则从记忆库中取样本训练
            try:
                minibatch = random.sample(replay, 16)  # 从记忆库中随机取样16个经验
                s, a, r, s1, alive = zip(*minibatch)  # 解压经验
                s = np.concatenate(s)  # 将样本状态拼接在一起
                s1 = np.concatenate(s1)  # 将样本下一个状态拼接在一起
                targets = model.predict(s)  # 预测当前状态的Q值
                targets[range(16), a] = r + discount * np.max(model.predict(s1), axis=1) * alive  # 更新Q值
                loss += model.train_on_batch(s, targets)  # 使用小批次训练模型
            except Exception as e:
                print(e)  # 捕捉并打印异常，继续训练
                continue

        input_image = input_image1  # 更新当前状态
        timestep += 1  # 增加时间步数

        if timestep % 300 == 0:  # 每300步保存一次模型权重
            model.save_weights("trainDQN.h5", overwrite=True)

        print("TIMESTEP: " + str(timestep) + ", EPSILON: " + str(epsilon) + ", ACTION: " + str(action) + ", REWARD: " + str(reward) + ", Loss: " + str(loss))
        loss = 0  # 重置损失

if __name__ == "__main__":
    train_network()  # 运行训练函数