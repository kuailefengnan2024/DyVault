import os
from PIL import Image

def extract_hue_ranges(image_name_or_path, output_prefix, percentages):
    # 获取当前脚本的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 如果只提供了图片名称，则从当前目录读取图片
    if not os.path.isabs(image_name_or_path):
        image_path = os.path.join(current_dir, image_name_or_path)
    else:
        image_path = image_name_or_path
    
    # 打开图像
    image = Image.open(image_path).convert('RGB')  # 转换为RGB图像
    pixels = image.load()

    # 创建HSV图像
    hsv_image = image.convert('HSV')
    hsv_pixels = hsv_image.load()

    # 获取图像的最小和最大色相值
    min_hue = 360
    max_hue = 0
    for i in range(hsv_image.width):
        for j in range(hsv_image.height):
            hue, _, _ = hsv_pixels[i, j]
            if hue < min_hue:
                min_hue = hue
            if hue > max_hue:
                max_hue = hue

    # 计算切分色相值
    hue_ranges = [min_hue] + [min_hue + int(p * (max_hue - min_hue) / 100) for p in percentages] + [max_hue]

    # 遍历色相范围，生成对应的图像
    for idx in range(len(hue_ranges) - 1):
        lower_bound = hue_ranges[idx]
        upper_bound = hue_ranges[idx + 1]
        output_filename = f"{output_prefix}_{lower_bound}_{upper_bound}.png"
        output_path = os.path.join(current_dir, output_filename)
        
        # 创建新的图像
        new_image = Image.new('L', image.size)
        new_pixels = new_image.load()

        # 遍历所有像素
        for i in range(hsv_image.width):
            for j in range(hsv_image.height):
                hue, _, _ = hsv_pixels[i, j]
                if lower_bound <= hue < upper_bound:
                    new_pixels[i, j] = 255  # 白色
                else:
                    new_pixels[i, j] = 0  # 黑色

        # 保存新图像
        new_image.save(output_path)

# 示例用法
extract_hue_ranges('input.png', 'output', [25, 75])