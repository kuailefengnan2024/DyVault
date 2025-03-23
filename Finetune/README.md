# 图像提示词生成工具

这个工具使用微软的Florence-2模型（通过Hugging Face API）或CLIP模型为图像生成英文提示词，特别适用于生成画面元素的描述。

## 安装

1. 克隆或下载此仓库
2. 安装依赖：

```bash
pip install -r requirements.txt
```

## 使用方法

### 使用脚本生成提示词

```bash
python Scripts/generate_prompts_florence.py [图片目录路径]
```

如果不提供目录路径，将使用脚本中默认的 `IMAGE_DIRECTORY`。

### 提示词生成模式

可以通过 `--mode` 参数指定不同的提示词生成模式：

- `elements`（默认）：生成详细的画面元素描述
- `style`：分析图像的艺术风格、媒介和技巧
- `keywords`：生成逗号分隔的关键词列表
- `ai_prompt`：生成适合AI图像生成的详细提示词
- `combined`：同时生成以上四种描述并合并在同一个文件中

```bash
python Scripts/generate_prompts_florence.py --mode style [图片目录路径]
python Scripts/generate_prompts_florence.py --mode keywords [图片目录路径]
python Scripts/generate_prompts_florence.py --mode ai_prompt [图片目录路径]
python Scripts/generate_prompts_florence.py --mode combined [图片目录路径]
```

### API设置

脚本已经配置了默认的Hugging Face API密钥，可以直接使用。如果您想使用自己的API密钥，可以使用`--api_key`参数：

```bash
python Scripts/generate_prompts_florence.py --api_key YOUR_API_KEY [图片目录路径]
```

如果您想禁用API调用而只使用本地CLIP模型，请使用`--no_api`参数：

```bash
python Scripts/generate_prompts_florence.py --no_api [图片目录路径]
```

## 输出示例

### Florence2 API输出（默认）
```
A young woman with long blonde hair wearing a white dress standing in a field of flowers. The background shows a blue sky with fluffy white clouds.
```

### CLIP模型输出（使用--no_api参数）
```
This image appears to be a person with elements of nature
```

## 输出

生成的提示词将保存在指定图片目录下的 `Prompts` 子文件夹中，每个图片对应一个同名的 `.txt` 文件。

## 技术说明

脚本默认使用Florence2 API生成高质量的描述，同时也提供了基于本地CLIP模型的备选方案：

1. **Florence2 API（默认）**：通过Hugging Face的API调用微软的Florence-2模型，生成高质量的图像描述
2. **CLIP模型（备选）**：当API不可用或使用`--no_api`参数时，将使用OpenAI的CLIP模型进行本地图像分类和匹配

## 故障排除

- 如果API调用失败，脚本会自动回退到使用CLIP模型
- 如果CLIP模型加载失败，请确保安装了所有依赖：`pip install -r requirements.txt`
- 如果需要更改默认API密钥，可以直接编辑脚本中的`DEFAULT_API_KEY`变量

## 图像处理工具

仓库还包含其他图像处理工具：

- `resize_custom_images.py`：调整图像大小和处理透明背景
- `rename_custom_images.py`：批量重命名图像文件

## 依赖

该工具主要依赖于：
- transformers
- torch
- PIL (Pillow)
- requests
- numpy
- ftfy (用于CLIP文本处理) 