import numpy as np
import matplotlib.pyplot as plt

# 定义 x 的范围
x = np.linspace(0.1, 5, 500)  # 从0.1开始避免对数为负

# 定义函数
y1 = np.log(x) / np.log(0.5)  # 底数为0.5的对数
y2 = np.log(x)  # 自然对数(底数为e)
y3 = np.log10(x)  # 底数为10的对数
y4 = np.log(x) / np.log(5)  # 底数为5的对数

# 创建图形
plt.figure(figsize=(8, 8))

# 绘制曲线
plt.plot(x, y1, label='y = log_0.5(x)', color='red', linewidth=2)
plt.plot(x, y2, label='y = ln(x)', color='blue', linewidth=2)
plt.plot(x, y3, label='y = log_10(x)', color='green', linewidth=2)
plt.plot(x, y4, label='y = log_5(x)', color='purple', linewidth=2)

# 添加标题和标签
plt.title("Different Base Logarithm Functions", fontsize=16)
plt.xlabel("x", fontsize=14)
plt.ylabel("y", fontsize=14)

# 设置坐标轴和网格
plt.grid(True)
plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
plt.axvline(x=0, color='k', linestyle='-', linewidth=0.5)

# 设置显示范围
plt.xlim(0, 5)
plt.ylim(-4, 4)

# 添加图例
plt.legend(fontsize=12)

# 显示图形
plt.show()
