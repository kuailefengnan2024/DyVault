import numpy as np
import matplotlib.pyplot as plt

# 定义 x 的范围（指数范围）
x = np.linspace(-5, 5, 500)  # x从-5到5

# 定义不同的基础color值（模拟Unity中[0,1]的颜色值）
color1 = 0.0  # 添加0（用极小值近似处理）
color2 = 0.2  # 较暗的颜色值
color3 = 0.5  # 中间值
color4 = 0.8  # 较亮的颜色值
color5 = 1.0  # 添加1

# 计算幂函数 y = pow(color, x)
# 对于color=0，数学上未定义，使用极小值1e-10代替以避免错误
y1 = np.power(1e-10 if color1 == 0 else color1, x)  # color = 0时的幂函数（近似）
y2 = np.power(color2, x)  # color = 0.2时的幂函数
y3 = np.power(color3, x)  # color = 0.5时的幂函数
y4 = np.power(color4, x)  # color = 0.8时的幂函数
y5 = np.power(color5, x)  # color = 1时的幂函数

# 创建图形
plt.figure(figsize=(8, 8))

# 绘制曲线
plt.plot(x, y1, label=f'y = pow({color1}, x)', color='black', linewidth=2)
plt.plot(x, y2, label=f'y = pow({color2}, x)', color='red', linewidth=2)
plt.plot(x, y3, label=f'y = pow({color3}, x)', color='blue', linewidth=2)
plt.plot(x, y4, label=f'y = pow({color4}, x)', color='green', linewidth=2)
plt.plot(x, y5, label=f'y = pow({color5}, x)', color='purple', linewidth=2)

# 添加标题和标签
plt.title("Power Function with Different Base Colors", fontsize=16)
plt.xlabel("x (Exponent)", fontsize=14)
plt.ylabel("y (Result)", fontsize=14)

# 设置坐标轴和网格
plt.grid(True)
plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
plt.axvline(x=0, color='k', linestyle='-', linewidth=0.5)

# 设置显示范围为[-5, 5]
plt.xlim(-5, 5)
plt.ylim(-5, 5)

# 添加图例
plt.legend(fontsize=12)

# 显示图形
plt.show()