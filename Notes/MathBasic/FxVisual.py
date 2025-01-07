import numpy as np
import matplotlib.pyplot as plt

# 定义 x 的范围
x = np.linspace(-10, 10, 500)  # 在 -10 到 10 之间均匀取 500 个点
x_positive = np.linspace(0, 10, 500)  # 0.5^x 只定义在 x >= 0 的范围

# 定义函数
y1 = x**2                 # y = x^2
y2 = 0.5**x_positive      # y = 0.5^x
y3 = x                    # y = x

# 创建图形
plt.figure(figsize=(8, 8))  # 调整图形尺寸为正方形

# 绘制三条曲线
plt.plot(x, y1, label='y = x^2', color='blue', linewidth=2)         # y = x^2 曲线
plt.plot(x_positive, y2, label='y = 0.5^x', color='red', linewidth=2)  # y = 0.5^x 曲线
plt.plot(x, y3, label='y = x', color='green', linewidth=2, linestyle='--')  # y = x 曲线 (虚线)

# 添加标题和标签
plt.title("Function Curves: y = x^2, y = 0.5^x, and y = x", fontsize=16)
plt.xlabel("x", fontsize=14)
plt.ylabel("y", fontsize=14)

# 设置横纵坐标步幅一致
plt.axis('equal')  # 设置坐标轴比例为1:1
plt.grid(alpha=0.3)  # 添加网格线

# 设置坐标范围（可选，根据需要调整范围）
plt.xlim(-10, 10)
plt.ylim(-10, 10)

# 添加图例
plt.legend(fontsize=12)

# 显示图形
plt.show()