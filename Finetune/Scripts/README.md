# 图像处理和Prompt生成脚本

这个目录包含了三个用于图像处理和prompt生成的Python脚本：

## 1. 重命名图像文件 (rename_custom_images.py)

将目录中的图像文件统一重命名为格式化的名称（例如 `image_001.jpg`, `image_002.jpg` 等）。

### 使用方法：

```bash
python rename_custom_images.py [目录路径]
```

- 如果未提供目录路径，将使用脚本中定义的默认路径。

## 2. 调整图像大小 (resize_custom_images.py)

将目录中的图像文件调整为指定大小，并保存到同一目录下的 "Modified" 文件夹中。

### 使用方法：

```bash
python resize_custom_images.py [目录路径] [--width 宽度] [--height 高度]
```

- 如果未提供目录路径，将使用脚本中定义的默认路径。
- 默认的目标尺寸为 512x512 像素。

## 3. 生成图像Prompts (generate_prompts_florence.py)

使用 Florence-2 模型为目录中的每个图像生成描述性prompt，并将结果保存到同一目录下的 "Prompts" 文件夹中。

### 安装依赖：

```bash
pip install torch transformers pillow
```

### 使用方法：

```bash
python generate_prompts_florence.py [目录路径] [--model 模型名称] [--detailed]
```

- 如果未提供目录路径，将使用脚本中定义的默认路径。
- 默认使用的模型是 "microsoft/florence-2-base"。
- 添加 `--detailed` 选项可以生成更详细的图像描述。

### 示例：

```bash
# 使用默认设置为默认目录中的图像生成prompts
python generate_prompts_florence.py

# 为指定目录中的图像生成详细的prompts
python generate_prompts_florence.py D:\我的图片集 --detailed

# 使用不同的模型
python generate_prompts_florence.py --model microsoft/florence-2-large
```

## 注意事项

1. 请先修改脚本开头的 `IMAGE_DIRECTORY` 变量为您的图片目录路径。
2. 所有脚本都会在处理过程中显示进度信息。
3. 处理大量图像可能需要较长时间，请耐心等待。
4. 使用 Florence-2 模型需要互联网连接以下载预训练模型。 