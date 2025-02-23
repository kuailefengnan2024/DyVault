
from torch.utils.data import Dataset

help(Dataset)

foo = 6
a = 1

from PIL import Image
img_path = r"D:\BaiduSyncdisk\DyVault\LearnPytorch\dataset\val\ants\800px-Meat_eater_ant_qeen_excavating_hole.jpg"
img = Image.open(img_path)
print(img.size)

b = img.size
# img.show()

import os # win下文件管理的库
img_path_dict = os.listdir(r"D:\BaiduSyncdisk\DyVault\LearnPytorch\dataset\val\ants")
specific_img_path = img_path_dict[3]





