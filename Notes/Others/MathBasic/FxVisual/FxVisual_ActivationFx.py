# 激活函数的主要目的是引入非线性，使得神经网络能够学习复杂的、非线性的模式
# 激活函数将线性函数转换为非线性 能够更好的拟合现实世界

import numpy as np
import matplotlib.pyplot as plt

# 定义 x 的范围
x = np.linspace(-5, 5, 500)

# 定义一个简单的线性输入
linear_input = 2 * x + 1  # y = 2x + 1

# 定义激活函数
def relu(x):
    return np.maximum(0, x)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# 计算激活后的输出
y_linear = linear_input
y_relu = relu(linear_input)
y_sigmoid = sigmoid(linear_input)

# 创建图形
plt.figure(figsize=(10, 6))

# 绘制曲线
plt.plot(x, y_linear, label='Linear Input: y = 2x + 1', color='green', linestyle='--')
plt.plot(x, y_relu, label='ReLU(2x + 1)', color='blue', linewidth=2)
plt.plot(x, y_sigmoid, label='Sigmoid(2x + 1)', color='red', linewidth=2)

# 添加标题和标签
plt.title("Linear Input vs After Activation Functions", fontsize=16)
plt.xlabel("x", fontsize=14)
plt.ylabel("y", fontsize=14)

# 设置网格和刻度
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(np.arange(-5, 6, 1))
plt.yticks(np.arange(-10, 11, 2))

# 使坐标轴更清晰
ax = plt.gca()
ax.spines['bottom'].set_position('zero')
ax.spines['left'].set_position('zero')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 设置显示范围
plt.xlim(-5, 5)
plt.ylim(-10, 10)

# 添加图例
plt.legend(fontsize=12)

# 显示图形
plt.show()