from torchvision import transforms
from PIL import Image
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt

# 加载图片
image = Image.open(r'LearnPytorch\dataset\train\ants\5650366_e22b7e1065.jpg')

# 使用 transforms.ToTensor() 转换图像为张量
transform = transforms.ToTensor()
image_tensor = transform(image)

# 打印原始张量的形状 (C, H, W)
print("原始图像张量形状:", image_tensor.shape)

# 添加批次维度，因为池化函数需要 (N, C, H, W) 格式
image_tensor_batch = image_tensor.unsqueeze(0)

# 应用最大池化 (kernel_size=2, stride=2)
pooled_tensor = F.max_pool2d(image_tensor_batch, kernel_size=8, stride=8)

# 移除批次维度以便显示
pooled_tensor = pooled_tensor.squeeze(0)

print("池化后图像张量形状:", pooled_tensor.shape)

# 显示原始图像和池化后的图像
plt.figure(figsize=(10, 5))

# 显示原始图像
plt.subplot(1, 2, 1)
plt.imshow(image_tensor.permute(1, 2, 0))  # 转换为 (H, W, C) 格式用于显示
plt.title("原始图像")
plt.axis('off')

# 显示池化后的图像
plt.subplot(1, 2, 2)
plt.imshow(pooled_tensor.permute(1, 2, 0))  # 转换为 (H, W, C) 格式用于显示
plt.title("池化后图像")
plt.axis('off')

plt.tight_layout()
plt.show()
