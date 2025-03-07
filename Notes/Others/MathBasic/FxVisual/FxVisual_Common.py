import numpy as np
import matplotlib.pyplot as plt

# 定义 x 的范围
x = np.linspace(-5, 5, 500)  # 在 -5 到 5 之间均匀取 500 个点

# 定义函数
y1 = x  # y = x
y3 = 1 / (1 + np.exp(-x))  # y = sigmoid(x)
y5 = np.exp(x)  # y = exp(x)
y6 = np.power(x, 2)  # y = x^2 (pow function, can be any base)

# 定义分段 smoothstep 函数
def smoothstep(x):
    return np.piecewise(x,
        [x < 0, (x >= 0) & (x <= 1), x > 1],   
        [0, lambda x: x**2 * (3 - 2 * x), 1])
y4 = smoothstep(x)

# 创建图形
plt.figure(figsize=(8, 8))  # 调整图形尺寸为正方形

# 绘制曲线
plt.plot(x, y1, label='y = x', color='green', linewidth=2, linestyle='--')  # y = x 曲线 (虚线)
plt.plot(x, y3, label='y = sigmoid(x)', color='blue', linewidth=2)  # sigmoid 曲线
plt.plot(x, y4, label='y = smoothstep(x)', color='red', linewidth=2)  # smoothstep 曲线
plt.plot(x, y5, label='y = exp(x)', color='purple', linewidth=2)  # exp 曲线
plt.plot(x, y6, label='y = pow(x, 2)', color='orange', linewidth=2)  # pow(x, 2) 曲线

# 添加标题和标签
plt.title("Function Curves: y = x, Sigmoid, Smoothstep, Exp and Pow", fontsize=16)
plt.xlabel("x", fontsize=14)
plt.ylabel("y", fontsize=14)

# 设置横纵坐标步幅一致
plt.axis('equal')  # 设置坐标轴比例为1:1

# 设置更明显的网格和刻度
plt.xticks(np.arange(-5, 6, 1))  # 整数刻度
plt.yticks(np.arange(-5, 30, 5))  # 整数刻度，扩展y值范围以便查看exp和pow函数
plt.grid(True, which='major', linestyle='-', linewidth=0.5, alpha=0.7)  # 主要网格线
plt.grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.3)  # 次要网格线
plt.minorticks_on()  # 启用次要刻度

# 使坐标轴居中并更明显
ax = plt.gca()

# 将x轴移到中间
ax.spines['bottom'].set_position('zero')
ax.spines['bottom'].set_linewidth(1.5)

# 将y轴移到中间
ax.spines['left'].set_position('zero')
ax.spines['left'].set_linewidth(1.5)

# 隐藏顶部和右侧的轴线
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 设置坐标范围，只显示 -5 到 5 的范围
plt.xlim(-5, 5)  # x 轴范围 [-5, 5]
plt.ylim(-5, 5)  # y 轴范围 [-5, 5]，限制视窗显示范围

# 添加图例
plt.legend(fontsize=12)

# 显示图形
plt.show()
