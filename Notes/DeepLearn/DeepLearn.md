
>**NumPy**：适合数值计算，尤其是多维数组和矩阵操作。
>**OpenCV**：专注于图像和视频处理，功能强大且实用。

矩阵是二维数据 张量可以是更多维度数据 所以RGB图象可以用张量表示


---
#### 魔术方法

##### __getitem__案例
```
import os
from PIL import Image

class SimpleImageDataset:
    def __init__(self, data_dir, label_dir):  # 初始化，接收数据目录和标签目录
        self.data_dir = data_dir  # 设置数据目录路径
        self.label_dir = label_dir  # 设置标签目录路径
        self.image_files = os.listdir(data_dir)  # 列出目录下所有图像文件

    def __getitem__(self, idx):  # 定义 __getitem__，根据索引返回数据
        img_name = self.image_files[idx]  # 根据索引获取图像文件名
        img_path = os.path.join(self.data_dir, img_name)  # 组合完整图像路径
        image = Image.open(img_path)  # 打开图像
        label = os.path.join(self.label_dir, img_name.replace(".jpg", ".txt"))  # 假设标签是同名 .txt 文件
        return image, label  # 返回图像和对应标签

# 使用示例
dataset = SimpleImageDataset("/path/to/images", "/path/to/labels")
image, label = dataset[0]  # 通过索引 0 获取第一个图像和标签
```

```
class NumberSequence:
    def __init__(self, numbers):  # 初始化，接收一个数字列表
        self.numbers = numbers  # 存储数字列表作为属性

    def __getitem__(self, idx):  # 定义 __getitem__，根据索引返回数字
        return self.numbers[idx]  # 返回列表中对应索引的数字

# 使用示例
sequence = NumberSequence([10, 20, 30, 40, 50])
print(sequence[2])  # 输出: 30
print(sequence[0])  # 输出: 10
```


__xxx__ 是魔术方法 本质就是函数 为了和普通函数区分开 所以加上了双下划线

| 特殊方法       | 用途                                      |
|----------------|-------------------------------------------|
| `__init__`     | 初始化对象，设置类属性（如数据集路径）        |
| `__len__`      | 返回数据集或对象的长度，用于 `len()`         |
| `__getitem__`  | 根据索引获取数据项，支持索引访问（如 `dataset[idx]`） |
| `__call__`     | 使对象可调用，如模型的前向传播               |
| `__repr__`     | 返回对象的字符串表示，用于调试和显示         |
| `__str__`      | 返回对象的简洁字符串描述，用于打印          |
| `__setattr__`  | 控制属性设置行为，用于自定义属性赋值逻辑      |
| `__getattr__`  | 控制属性访问行为，用于动态返回属性           |
| `__eq__`       | 定义对象相等性比较，用于 `==` 操作          |
| `__add__`      | 定义对象相加行为，用于 `+` 操作（如张量操作） |
| `__torch_function__` | 自定义张量操作行为，扩展 PyTorch 功能       |  
  



##### __init__定义案例

```
class SimpleImageDataset: #类本身
    def __init__(self, data_dir, label_dir):  # 定义 __init__，接收数据目录和标签目录作为参数
        self.data_dir = data_dir  # 设置数据目录路径作为实例属性
        self.label_dir = label_dir  # 设置标签目录路径作为实例属性
        self.image_files = os.listdir(data_dir)  # 列出数据目录下的所有图像文件，存储为列表

使用示例
dataset = SimpleImageDataset("/path/to/images", "/path/to/labels") #实例化一个具体的类
```

```
import torch
import torch.nn as nn

class SimpleNN: #类本身
    def __init__(self, input_size=10, hidden_size=20, output_size=2):  # 定义 __init__，接收网络层大小作为参数
        self.layer1 = nn.Linear(input_size, hidden_size)  # 初始化第一层线性层
        self.layer2 = nn.Linear(hidden_size, output_size)  # 初始化第二层线性层
        self.activation = nn.ReLU()  # 初始化激活函数

 使用示例
model = SimpleNN(input_size=10, hidden_size=20, output_size=2) #实例化一个具体的类
```

**def -init-(self, ...) self 总是第一个参数，表示当前实例(mydataset) 将类的实例（对象）和初始化时的参数关联起来，为新创建的类实例设置初始状态或属性**

---



Pytorch
1.使用anaconda prompt 输入 conda activate pytorch 打开pytorch环境
2.然后anaconda prompt 输入 jupyter notebook 打开jupyter notebook


|  类型        |  描述                   |
|-------------|------------------------|
|  ML（机器学习）分为以下三种 |  =  DL（深度学习）     |
|  CNN（卷积神经网络） |  主要处理图像        |
|  RNN（循环神经网络） |  主要处理文本        |
|  GAN（对抗神经网络） |  生成图片            |
|  Auto-Encoder（自编码器） |  生成            |
|  Transformer() |  chatgpt            |
| 原理示意| ![](d:/BaiduSyncdisk/DyVault/Notes/DeepLearn/images/2024-10-28-23-52-09p.png)|
|  此图对应上图 一个小圆 |![](d:/BaiduSyncdisk/DyVault/Notes/DeepLearn/images/2024-10-28-23-55-48p.png)  |

anaconda就是管理环境的工具
![](d:/BaiduSyncdisk/DyVault/Notes/DeepLearn/images/2024-10-28-23-44-05p.png)

conda和pip是并列概念 都是包的安装工具

>**梯度下降**是优化模型的核心算法，通过不断更新参数来最小化损失函数。
**收敛**是判断算法是否达到最佳状态的标准，确保训练过程的有效性。
**正态分布**在初始化、引入随机性和假设检验等方面发挥着重要作用，帮助模型更好地学习和泛化。

![](d:/BaiduSyncdisk/DyVault/Notes/DeepLearn/images/image-3p.png)
魔术方法===私有属性
示例-add- 来赋予Menu可加性👇
```
class Menu:
    def __init__(self, items):
        self.items = items

    def __add__(self, other):
        return Menu(self.items + other.items)

menu1 = Menu(["披萨"])
menu2 = Menu(["意大利面"])
combined_menu = menu1 + menu2
print(combined_menu.items)  # 输出: ['披萨', '意大利面']
```
```
class Restaurant:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Restaurant: {self.name}"

# 示例
rest = Restaurant("美味餐厅")
print(rest)  # 输出: Restaurant: 美味餐厅
```

>这里的__len__相当于给Menu赋予了长度属性 从而len可以识别其长度,👇
```
class Menu:
    def __init__(self, items):
        self.items = items

    def __len__(self):   
        return len(self.items)

# 示例
menu = Menu(["披萨", "意大利面", "沙拉"])
print(len(menu))  # 输出: 3
```

print()会自动调用--str--属性

>类 餐馆模板
对象 麦当劳连锁店
实例 海淀麦当劳1号店


![](d:/BaiduSyncdisk/DyVault/Notes/DeepLearn/images/image-2p.png)

>pip：Python 的包管理工具
conda: 包管理工具 但不限于python

![](d:/BaiduSyncdisk/DyVault/Notes/DeepLearn/images/imagep.png)
*不同的pytorch版本*

类是对象的蓝图，对象是类的实例
python面向对象编程，具有封装，继承，多态等特性，继承就是儿子获得爸爸属性，多态就是不同的人(对象)可以同一个妓女(方法，接口)
vex面向过程
AI相关
高精需求
- 生成贴图
- 生成背景和其他物件（喂精致的
- 先做精致然后扩图
vae编码~行李打包
vae解码~行李拆包
可以用大模型（搬家公司）的vae袋子也可以用自己找的vae
图像可以通过vae编码为latent潜在空间（行李空间）
采样器的降噪就是重绘幅度

latent直接缩放等同于ps放大图片，需要再采样重绘一次


```Python
# 定义class可以理解为在定义班长self，然后与班长对接，用.链接不同同学
class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower

class Car:
    def __init__(self, brand, engine):
        self.brand = brand
        self.engine = engine

# 创建Engine实例和Car实例
my_engine = Engine(250)
my_car = Car("Toyota", my_engine)

# 使用点号进行链式访问
print(my_car.engine.horsepower)  # 输出: 250
```

API python用法
1.在json和py存放目录输入powershell启动powershell 2.启动python 3.操作具体的那个py
注意：json是接口文件，py才是脚本文件



| **概念**        | **描述**                                           |
|-----------------|----------------------------------------------------|
| **cuDNN** **TensorRT**      | NVIDIA深度学习加速库，优化神经网络**工具本身**  |
| **CUDA**        | NVIDIA 利用 GPU 加速计算。 **工具箱**   |
| **TensorFlow** **PyTorch**  | 机器学习框架**建筑蓝图包含工具箱**    |
| **Conda**  **Chocolatey (choco)**     | 包管理和环境管理工具，用于创建和管理虚拟环境。 **工具箱架子**   |
| **环境变量**     | 指引系统找工具和库   **路线图** |




![](d:/BaiduSyncdisk/DyVault/Notes/DeepLearn/images/2024-12-31-15-14-44.png)


**卷积层**：提取输入数据特征的神经网络层。
**梯度**：描述损失函数变化率的数学工具，推动模型优化。
| 概念         | 比喻                                   | 作用                                      | 常用文件名称       | 文件格式说明       |
|--------------|----------------------------------------|-------------------------------------------|--------------------|--------------------|
| 权重         | 果汁中水果和水的比例                   | 决定最终的味道                            | weights.npy        | NumPy 数组文件，用于存储权重值 |
| 卷积层       | 制作果汁时使用的工具                   | 提取输入数据的不同特征                  | conv_layer.py      | Python 文件，定义卷积层的实现 |
| 潜在空间     | 所有果汁汇聚的大碗                     | 表示不同果汁的特征                       | latent_space.pkl    | Pickle 文件，存储潜在空间的特征 |
| 梯度         | 调整果汁味道的过程                     | 指导如何改进配方，以减少损失             | gradients.csv       | CSV 文件，记录梯度值和更新信息 |
