import os
import argparse
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM

# 在这里设置图片目录路径 - 修复反斜杠问题
IMAGE_DIRECTORY = r"D:\BaiduSyncdisk\DyVault\Finetune\Datasets\Custom_Images_Keai"  # 请修改为您的图片目录路径

def generate_prompts(directory_path=None, model_name="microsoft/florence-2-base"):
    """
    为指定目录中的所有图片生成prompt描述，并将结果保存到同一目录下的Prompts文件夹中的txt文件
    
    Args:
        directory_path: 包含图片的目录路径
        model_name: 要使用的Florence-2模型名称
    """
    # 如果没有提供目录路径，使用默认路径
    if directory_path is None:
        directory_path = IMAGE_DIRECTORY
        
    # 确保目录存在
    if not os.path.isdir(directory_path):
        print(f"错误：目录 '{directory_path}' 不存在")
        return
    
    # 创建输出目录
    output_dir = os.path.join(directory_path, "Prompts")
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取目录中的所有文件
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    
    # 过滤出图片文件（简单检查常见图片扩展名）
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    image_files = [f for f in files if os.path.splitext(f.lower())[1] in image_extensions]
    
    if not image_files:
        print(f"在目录 '{directory_path}' 中没有找到图片文件")
        return
    
    print(f"正在加载 Florence-2 模型: {model_name}")
    try:
        # 加载模型和处理器
        processor = AutoProcessor.from_pretrained(model_name, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
        
        # 如果有CUDA可用，则使用GPU
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = model.to(device)
        
        print(f"使用设备: {device}")
    except Exception as e:
        print(f"加载模型时出错: {e}")
        return
    
    # 处理每张图片并生成prompt
    for filename in image_files:
        input_path = os.path.join(directory_path, filename)
        output_filename = os.path.splitext(filename)[0] + ".txt"
        output_path = os.path.join(output_dir, output_filename)
        
        try:
            print(f"正在处理: '{filename}'")
            # 加载图像
            image = Image.open(input_path).convert("RGB")
            
            # 准备模型输入
            inputs = processor(images=image, return_tensors="pt").to(device)
            
            # 生成描述
            with torch.no_grad():
                generated_ids = model.generate(
                    pixel_values=inputs.pixel_values,
                    max_length=50,
                    num_beams=5,
                    early_stopping=True
                )
            
            # 解码生成的ID，获取文本描述
            generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            # 将描述写入文本文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(generated_text)
            
            print(f"已生成prompt: '{filename}' -> '{output_path}'")
            print(f"Prompt: {generated_text}")
            
        except Exception as e:
            print(f"处理 '{filename}' 时出错: {e}")
    
    print(f"完成！已为 {len(image_files)} 个文件生成prompt，结果保存在 '{output_dir}'")

def generate_prompts_with_caption_task(directory_path=None, model_name="microsoft/florence-2-base"):
    """
    为指定目录中的所有图片生成详细的描述性prompt，并将结果保存到同一目录下的Prompts文件夹中的txt文件
    这个函数特别指示模型执行图像描述任务
    
    Args:
        directory_path: 包含图片的目录路径
        model_name: 要使用的Florence-2模型名称
    """
    # 如果没有提供目录路径，使用默认路径
    if directory_path is None:
        directory_path = IMAGE_DIRECTORY
        
    # 确保目录存在
    if not os.path.isdir(directory_path):
        print(f"错误：目录 '{directory_path}' 不存在")
        return
    
    # 创建输出目录
    output_dir = os.path.join(directory_path, "Prompts")
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取目录中的所有文件
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    
    # 过滤出图片文件（简单检查常见图片扩展名）
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    image_files = [f for f in files if os.path.splitext(f.lower())[1] in image_extensions]
    
    if not image_files:
        print(f"在目录 '{directory_path}' 中没有找到图片文件")
        return
    
    print(f"正在加载 Florence-2 模型: {model_name}")
    try:
        # 加载模型和处理器
        processor = AutoProcessor.from_pretrained(model_name, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
        
        # 如果有CUDA可用，则使用GPU
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = model.to(device)
        
        print(f"使用设备: {device}")
    except Exception as e:
        print(f"加载模型时出错: {e}")
        return
    
    # 处理每张图片并生成prompt
    for filename in image_files:
        input_path = os.path.join(directory_path, filename)
        output_filename = os.path.splitext(filename)[0] + ".txt"
        output_path = os.path.join(output_dir, output_filename)
        
        try:
            print(f"正在处理: '{filename}'")
            # 加载图像
            image = Image.open(input_path).convert("RGB")
            
            # 准备模型输入并指示执行图像描述任务
            inputs = processor(
                images=image, 
                text="Describe this image in detail:", 
                return_tensors="pt"
            ).to(device)
            
            # 生成描述
            with torch.no_grad():
                generated_ids = model.generate(
                    pixel_values=inputs.pixel_values,
                    input_ids=inputs.input_ids,
                    attention_mask=inputs.attention_mask,
                    max_length=100,
                    num_beams=5,
                    early_stopping=True
                )
            
            # 解码生成的ID，获取文本描述
            generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            # 清理提示词部分，只保留生成的描述
            if "Describe this image in detail:" in generated_text:
                generated_text = generated_text.replace("Describe this image in detail:", "").strip()
            
            # 将描述写入文本文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(generated_text)
            
            print(f"已生成prompt: '{filename}' -> '{output_path}'")
            print(f"Prompt: {generated_text}")
            
        except Exception as e:
            print(f"处理 '{filename}' 时出错: {e}")
    
    print(f"完成！已为 {len(image_files)} 个文件生成prompt，结果保存在 '{output_dir}'")

if __name__ == "__main__":
    # 您可以直接修改上面的 IMAGE_DIRECTORY 变量，或者使用命令行参数
    parser = argparse.ArgumentParser(description='为指定目录中的图片生成prompt')
    parser.add_argument('directory', type=str, nargs='?', help='包含图片的目录路径')
    parser.add_argument('--model', type=str, default="microsoft/florence-2-base", help='要使用的Florence-2模型名称')
    parser.add_argument('--detailed', action='store_true', help='生成更详细的描述')
    
    args = parser.parse_args()
    
    if args.detailed:
        generate_prompts_with_caption_task(args.directory, args.model)
    else:
        generate_prompts(args.directory, args.model) 