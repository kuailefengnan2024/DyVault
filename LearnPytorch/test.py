# import torch

# dir_data = dir(torch.utils.data)
# dir_data = dir(torch.utils.data.Dataset)
# dir_data = dir(torch.cuda)
# dir_data = dir(torch.cuda.is_available())
# help(torch.cuda.is_available)
# print(dir_data)

import numpy as np
import cv2

# NumPy 示例
array2 = np.array([[1, 2], [3, 4]])
print("NumPy 数组：\n", array)
print("数组转置：\n", array.T)

# OpenCV 示例
img = np.zeros((300, 300, 3), dtype=np.uint8)  # 创建黑色图像
cv2.rectangle(img, (50, 50), (250, 250), (0, 255, 0), 2)  # 画绿色矩形
cv2.imshow('Demo', img)
cv2.waitKey(0)
cv2.destroyAllWindows()




