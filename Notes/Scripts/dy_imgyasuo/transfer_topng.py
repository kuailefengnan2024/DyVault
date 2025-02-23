import os
from PIL import Image  # 导入PIL库来处理图像
from tqdm import tqdm
import subprocess  # 导入subprocess库来调用外部命令
import tkinter as tk
from tkinter import filedialog, messagebox
import sys

def process_images(source_folder, quality):
    # 创建一个新的文件夹来存储转换后的png图片
    export_folder = os.path.join(source_folder, 'Zip_png')
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
        print(f"Created export folder: {export_folder}")

    # 获取源文件夹中的所有JPEG和PNG图片文件
    image_files = [f for f in os.listdir(source_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    # pngquant的相对路径
    pngquant_path = os.path.join(os.path.dirname(sys.argv[0]), 'pngquant', 'pngquant.exe')

    # 检查标准输出流是否存在
    tqdm_output = sys.stdout if sys.stdout else open(os.devnull, 'w')

    # 遍历源文件夹中的所有文件并显示进度条
    for filename in tqdm(image_files, desc="Processing Images", file=tqdm_output):
        try:
            # 构建文件路径
            file_path = os.path.join(source_folder, filename)
            
            # 打开图片
            with Image.open(file_path) as img:
                # 如果是JPEG文件，转换为PNG格式
                if file_path.lower().endswith(('.jpg', '.jpeg')):
                    png_path = os.path.join(export_folder, os.path.splitext(filename)[0] + '.png')
                    # 使用quantize方法减少颜色数量
                    img = img.convert('P', palette=Image.ADAPTIVE, colors=64)
                    img.save(png_path, format='PNG', optimize=True)
                else:
                    # 如果是PNG文件，直接压缩
                    png_path = os.path.join(export_folder, filename)
                    img = img.convert('P', palette=Image.ADAPTIVE, colors=64)
                    img.save(png_path, format='PNG', optimize=True)
            
            # 使用pngquant进行二次压缩
            subprocess.run([pngquant_path, '--force', '--ext', '.png', '--quality', quality, '--speed', '1', png_path])
            
            print(f"Processed {filename} to PNG format: {png_path}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print(f"All images have been processed and saved to the '{export_folder}' folder in the same directory as the source folder.")
    messagebox.showinfo("完成", f"所有图片已处理完成！文件保存在: {export_folder}")

def select_quality():
    def on_select(quality):
        root.destroy()
        source_folder = os.path.dirname(sys.argv[0])
        process_images(source_folder, quality)

    root = tk.Tk()
    root.title("选择压缩程度")

    label = tk.Label(root, text="请选择压缩程度:")
    label.pack(pady=10)

    qualities = {
        "低": "60-80",
        "中": "40-60",
        "高": "20-40",
        "最高": "10-30"
    }

    for text, quality in qualities.items():
        button = tk.Button(root, text=text, command=lambda q=quality: on_select(q))
        button.pack(pady=5)

    root.mainloop()

def main():
    select_quality()

if __name__ == "__main__":
    main()