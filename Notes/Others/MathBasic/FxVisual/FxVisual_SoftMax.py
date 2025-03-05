import numpy as np
import matplotlib.pyplot as plt

# 可以理解为输入和输出都是数组 并且输出概率加起来为1

# 定义 SoftMax 函数 
def softmax(z):
    exp_z = np.exp(z)  # 计算指数
    return exp_z / np.sum(exp_z)  # 归一化

# 定义输入范围
x = np.linspace(-5, 5, 500)  # 输入范围，模拟 logits

# 创建一组输入向量（这里用三个值模拟多分类输入）
z1 = x  # 第一个输入，随 x 变化
z2 = np.full_like(x, 1)  # 第二个输入，固定为 1
z3 = np.full_like(x, -1)  # 第三个输入，固定为 -1

# 计算 SoftMax 输出
softmax_input = np.vstack([z1, z2, z3]).T  # 组合成 (500, 3) 的矩阵
softmax_output = np.array([softmax(z) for z in softmax_input])  # 对每组输入计算 SoftMax

# 创建图形
plt.figure(figsize=(8, 6))

# 绘制 SoftMax 后的概率曲线
plt.plot(x, softmax_output[:, 0], label='SoftMax(z1)', color='red', linewidth=2)
plt.plot(x, softmax_output[:, 1], label='SoftMax(z2=1)', color='blue', linewidth=2)
plt.plot(x, softmax_output[:, 2], label='SoftMax(z3=-1)', color='green', linewidth=2)

# 添加标题和标签
plt.title("SoftMax Function Behavior", fontsize=16)
plt.xlabel("z1 (varying input)", fontsize=14)
plt.ylabel("Probability", fontsize=14)

# 设置坐标轴和网格
plt.grid(True)
plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
plt.axvline(x=0, color='k', linestyle='-', linewidth=0.5)

# 设置显示范围
plt.xlim(-5, 5)
plt.ylim(0, 1)  # 概率值在 0 到 1 之间

# 添加图例
plt.legend(fontsize=12)

# 显示图形
plt.show()