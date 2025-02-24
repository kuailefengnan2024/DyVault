
from PIL import Image
import os


class MyDataDataset:  # 定义自定义数据集类
    def __init__(self, root_dir, label_dir):  # 初始化，设置根目录和标签目录
        self.root_dir = root_dir  # 存储根目录路径
        self.label_dir = label_dir  # 存储标签目录路径
        self.path = os.path.join(self.root_dir, self.label_dir)  # 组合根目录、标签目录和图像文件名，生成完整的图像文件路径
        self.img_path = os.listdir(self.path)   # 列出 image_path 目录下的所有文件（通常是图像文件），存储到 self.img_path 列表中

    def __getitem__(self, idx):  # 根据索引获取数据项
        img_name = self.img_path[idx]  # 获取对应图像文件名
        img_path = os.path.join(self.root_dir, self.label_dir, img_name)   # 组合根目录、标签目录和图像文件名，生成完整的图像文件路径
        image = Image.open(img_path)  # 打开图像
        label = self.label_dir  # 将标签目录名作为标签（可能需优化）
        return image, label  # 返回图像和标签

    def __len__(self):  # 返回数据集大小
        return len(self.img_path)  # 返回图像数量