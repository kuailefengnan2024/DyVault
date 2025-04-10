# -*- coding: utf-8 -*-
# 导入所有需要的库
import numpy as np # 提供高效的多维数组操作和数学计算功能，是数据处理的基础。
import torch
import torchvision # 为计算机视觉任务提供数据集、模型和图像变换工具。
import torchvision.transforms as transforms # 提供图像变换功能，如标准化、裁剪等。
import matplotlib.pyplot as plt  # 用于绘制图表和可视化数据，如训练过程中的损失曲线。
import pandas as pd # 处理和分析结构化数据，如表格或 CSV 文件。
from sklearn.model_selection import train_test_split # 提供数据拆分、评估指标和传统机器学习算法。
from sklearn.metrics import accuracy_score
import cv2 # 处理图像和视频，支持实时计算机视觉任务和复杂变换。





# === NumPy 示例 ===
print("=== NumPy 示例 ===")
# 创建数组
array = np.array([1, 2, 3, 4, 5])  # 从列表创建一维数组
matrix = np.array([[1, 2], [3, 4]])  # 创建二维数组
zeros = np.zeros((2, 3))  # 创建 2x3 的全零数组
ones = np.ones((3, 2))  # 创建 3x2 的全一数组
rng = np.random.rand(2, 2)  # 创建 2x2 的随机数组（0到1之间）

# 常用操作
print("一维数组:", array)
print("二维数组:\n", matrix)
print("数组加法:", array + 2)  # 数组元素逐个加2
print("矩阵乘法:\n", np.dot(matrix, matrix))  # 矩阵点乘
print("数组切片:", array[1:4])  # 取索引1到3的元素
print("数组形状:", matrix.shape)  # 获取数组形状
print("数组重塑:\n", array.reshape(5, 1))  # 改变形状为5x1
print("随机数组:\n", rng)





# === Torchvision 示例 ===
print("\n=== Torchvision 示例 ===")
# 定义图像变换
transform = transforms.Compose([
    transforms.ToTensor(),  # 将 PIL 图像或 NumPy 数组转为张量
    transforms.Normalize((0.5,), (0.5,))  # 标准化（均值0.5，标准差0.5）
])

# 加载 MNIST 数据集
trainset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=4, shuffle=True)

# 获取并展示一个批次的数据
images, labels = next(iter(trainloader))
print("图像张量形状:", images.shape)  # 打印张量形状 [batch_size, channels, height, width]
print("标签:", labels)

# 使用预训练模型
model = torchvision.models.resnet18(pretrained=True)
print("ResNet18 模型结构:", model)




# === Matplotlib 示例 ===
print("\n=== Matplotlib 示例 ===")
# 绘制简单折线图
x = np.array([1, 2, 3, 4])
y = np.array([10, 20, 25, 30])
plt.plot(x, y, marker='o', label='数据')  # 绘制折线图，带标记点
plt.xlabel("X轴")  # 设置X轴标签
plt.ylabel("Y轴")  # 设置Y轴标签
plt.title("简单折线图")  # 设置标题
plt.legend()  # 显示图例
plt.grid(True)  # 显示网格
# plt.show()  # 取消注释以显示图形

# 绘制图像
plt.figure()  # 创建新图形
plt.imshow(images[0].permute(1, 2, 0).numpy())  # 显示第一张 MNIST 图像（需调整张量维度）
plt.title(f"标签: {labels[0].item()}")
# plt.show()  # 取消注释以显示图形





# === Pandas 示例 ===
print("\n=== Pandas 示例 ===")
# 创建 DataFrame
data = {'名字': ['小明', '小红', '小刚'], '年龄': [20, 22, 19], '分数': [95, 88, 92]}
df = pd.DataFrame(data)
print("数据框:\n", df)

# 常用操作
print("选择列:\n", df['年龄'])  # 选择单列
print("筛选数据:\n", df[df['分数'] > 90])  # 筛选分数大于90的行
print("描述统计:\n", df.describe())  # 显示统计信息
print("排序:\n", df.sort_values('分数', ascending=False))  # 按分数降序排序
print("添加列:\n", df.assign(等级=['A', 'B', 'A']))  # 添加新列

# 保存和读取 CSV
df.to_csv('example.csv', index=False)  # 保存到 CSV 文件
df_read = pd.read_csv('example.csv')  # 从 CSV 读取
print("读取的 CSV:\n", df_read)

# === scikit-learn 示例 ===
print("\n=== scikit-learn 示例 ===")
# 数据拆分
X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
y = np.array([0, 1, 0, 1])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
print("训练集:\n", X_train)
print("测试集:\n", X_test)

# 评估指标
y_pred = [0, 1, 0, 1]  # 假设预测结果
acc = accuracy_score(y_test, y_pred[:len(y_test)])  # 计算准确率
print("准确率:", acc)





# === OpenCV 示例 ===
print("\n=== OpenCV 示例 ===")
# 读取图像
img = cv2.imread('example.jpg')  # 假设有一个 example.jpg 文件
if img is None:
    print("请提供一个图像文件（如 example.jpg），这里用随机数组替代")
    img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)

# 常用操作
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
print("灰度图形状:", gray.shape)
resized = cv2.resize(img, (50, 50))  # 调整图像大小
print("调整后形状:", resized.shape)
blurred = cv2.GaussianBlur(img, (5, 5), 0)  # 高斯模糊
edges = cv2.Canny(gray, 100, 200)  # 边缘检测

# 显示图像（注释掉以避免运行时弹出窗口）
# cv2.imshow('原始图像', img)
# cv2.imshow('灰度图', gray)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# 保存图像
cv2.imwrite('output.jpg', resized)  # 保存调整后的图像
print("已保存调整后的图像为 output.jpg")