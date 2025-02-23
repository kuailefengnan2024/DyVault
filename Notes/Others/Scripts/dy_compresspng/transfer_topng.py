import os
from PIL import Image  # 导入PIL库来处理图像
from tqdm import tqdm
import subprocess  # 导入subprocess库来调用外部命令

# 原图片文件夹路径
source_folder = r"D:\BaiduSyncdisk\Proceduralization\default\4comfyui\FINAL\official_5"

# 创建一个新的文件夹来存储转换后的png图片
export_folder = os.path.join(os.path.dirname(source_folder), 'official_5_png')
if not os.path.exists(export_folder):
    os.makedirs(export_folder)

# 获取源文件夹中的所有JPEG和PNG图片文件
image_files = [f for f in os.listdir(source_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

# pngquant的完整路径
pngquant_path = r"D:\BaiduSyncdisk\Proceduralization\default\dy_compresspng\pngquant\pngquant.exe"

# 遍历源文件夹中的所有文件并显示进度条
for filename in tqdm(image_files, desc="Processing Images"):
    try:
        # 构建文件路径
        file_path = os.path.join(source_folder, filename)
        
        # 打开图片
        with Image.open(file_path) as img:
            # 如果是JPEG文件，转换为PNG格式
            if file_path.lower().endswith(('.jpg', '.jpeg')):
                png_path = os.path.join(export_folder, os.path.splitext(filename)[0] + '.png')
                # 使用quantize方法减少颜色数量
                img = img.convert('P', palette=Image.ADAPTIVE, colors=128)
                img.save(png_path, format='PNG', optimize=True)
            else:
                # 如果是PNG文件，直接压缩
                png_path = os.path.join(export_folder, filename)
                img = img.convert('P', palette=Image.ADAPTIVE, colors=128)
                img.save(png_path, format='PNG', optimize=True)
        
        # 使用pngquant进行二次压缩
        subprocess.run([pngquant_path, '--force', '--ext', '.png', '--quality', '10-30', '--speed', '1', png_path])
        
        print(f"Processed {filename} to PNG format: {png_path}")
    except Exception as e:
        print(f"Error processing {filename}: {e}")

print("All images have been processed and saved to the 'official_5_png' folder in the same directory as the source folder.")