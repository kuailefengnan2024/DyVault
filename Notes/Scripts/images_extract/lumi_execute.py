import os
from PIL import Image

def extract_luminance_ranges(image_name_or_path, output_prefix, percentages):
    # 获取当前脚本的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 如果只提供了图片名称，则从当前目录读取图片
    if not os.path.isabs(image_name_or_path):
        image_path = os.path.join(current_dir, image_name_or_path)
    else:
        image_path = image_name_or_path
    
    # 打开图像
    image = Image.open(image_path).convert('L')  # 转换为灰度图像
    pixels = image.load()

    # 获取图像的最小和最大明度值
    min_luminance = 255
    max_luminance = 0
    for i in range(image.width):
        for j in range(image.height):
            luminance = pixels[i, j]
            if luminance < min_luminance:
                min_luminance = luminance
            if luminance > max_luminance:
                max_luminance = luminance

    # 计算切分明度值
    luminance_ranges = [min_luminance] + [min_luminance + int(p * (max_luminance - min_luminance) / 100) for p in percentages] + [max_luminance]

    # 遍历明度范围，生成对应的图像
    for idx in range(len(luminance_ranges) - 1):
        lower_bound = luminance_ranges[idx]
        upper_bound = luminance_ranges[idx + 1]
        output_filename = f"{output_prefix}_{lower_bound}_{upper_bound}.png"
        output_path = os.path.join(current_dir, output_filename)
        
        # 创建新的图像
        new_image = Image.new('L', image.size)
        new_pixels = new_image.load()

        # 遍历所有像素
        for i in range(image.width):
            for j in range(image.height):
                luminance = pixels[i, j]
                if lower_bound <= luminance < upper_bound:
                    new_pixels[i, j] = 255  # 白色
                else:
                    new_pixels[i, j] = 0  # 黑色

        # 保存新图像
        new_image.save(output_path)

# 示例用法
extract_luminance_ranges('input.png', 'output', [25, 75])