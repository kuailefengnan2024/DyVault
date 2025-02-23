
from torch.utils.data import Dataset
help(Dataset)

from PIL import Image
img_path = r"LearnPytorch\dataset\val\ants\800px-Meat_eater_ant_qeen_excavating_hole.jpg"
img = Image.open(img_path)
print(img.size)