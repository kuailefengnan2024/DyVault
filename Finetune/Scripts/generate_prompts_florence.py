import os
import argparse
import torch
from PIL import Image
from transformers import AutoProcessor, Florence2ForConditionalGeneration

# 设置默认路径
IMAGE_DIRECTORY = r"D:\BaiduSyncdisk\DyVault\Finetune\Datasets\Custom_Images_Keai"
MODEL_PATH = "microsoft/florence-2-large"
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Models")

class FlorenceModel:
    def __init__(self, model_path=MODEL_PATH, cache_dir=CACHE_DIR):
        self.processor = None
        self.model = None
        self.load_model(model_path, cache_dir)

    def load_model(self, model_path, cache_dir):
        """加载 Florence-2 模型"""
        print(f"正在加载 Florence-2-large 模型...")
        os.makedirs(cache_dir, exist_ok=True)
        
        # 使用 AutoProcessor 和 Florence2ForConditionalGeneration
        self.processor = AutoProcessor.from_pretrained(model_path, cache_dir=cache_dir, trust_remote_code=True)
        self.model = Florence2ForConditionalGeneration.from_pretrained(
            model_path,
            cache_dir=cache_dir,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            trust_remote_code=True
        )
        
        if torch.cuda.is_available():
            self.model = self.model.to("cuda")
            print("模型已加载到 GPU")
        else:
            print("GPU 不可用，使用 CPU")
        print("Florence-2-large 模型加载完成")

    def query(self, image_path, prompt):
        """使用 Florence-2 模型生成图像描述"""
        try:
            image = Image.open(image_path).convert('RGB')
            # Florence-2 需要任务前缀，这里直接将 prompt 作为输入
            inputs = self.processor(text=prompt, images=image, return_tensors="pt")
            
            if torch.cuda.is_available():
                inputs = {k: v.to("cuda") for k, v in inputs.items()}
            
            print(f"使用 Florence-2-large 模型进行推理...")
            with torch.no_grad():
                generated_ids = self.model.generate(
                    **inputs,
                    max_length=1024,
                    num_beams=5,
                    temperature=0.7,
                    top_p=0.95,
                    repetition_penalty=1.2,
                    do_sample=True
                )
            
            generated_text = self.processor.decode(generated_ids[0], skip_special_tokens=True)
            return generated_text.replace(prompt, "").strip()
        
        except Exception as e:
            error_msg = f"处理图像时出错: {str(e)}"
            print(error_msg)
            return error_msg

def process_image_with_florence(model, image_path, prompt_mode="elements"):
    """处理图像并生成描述"""
    prompt_templates = {
        "elements": "Describe this image with detailed visual elements in English. Focus on key objects, colors, composition and visual details: ",
        "style": "Analyze this image and describe its artistic style in English. Include medium, technique, artistic movement, and visual characteristics: ",
        "keywords": "List the key visual elements of this image as comma-separated keywords in English: ",
        "ai_prompt": "Generate a detailed AI image generation prompt in English based on this image. Include subject, style, colors, lighting, and composition: ",
    }
    
    prompt = prompt_templates.get(prompt_mode, "Describe this image in English: ")
    print(f"处理图像: {os.path.basename(image_path)} - 模式: {prompt_mode}")
    return model.query(image_path, prompt)

def generate_prompts(directory_path=None, prompt_mode="elements"):
    """为目录中的图片生成描述"""
    directory_path = directory_path or IMAGE_DIRECTORY
    
    if not os.path.isdir(directory_path):
        print(f"错误: 目录 '{directory_path}' 不存在")
        return
    
    output_dir = os.path.join(directory_path, "Prompts")
    os.makedirs(output_dir, exist_ok=True)
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    image_files = [f for f in os.listdir(directory_path) 
                   if os.path.splitext(f.lower())[1] in image_extensions]
    
    if not image_files:
        print(f"未找到图片文件: {directory_path}")
        return
    
    total_images = len(image_files)
    print(f"开始处理 {total_images} 张图片，模式: {prompt_mode}")
    
    model = FlorenceModel()  # 初始化模型
    
    for i, filename in enumerate(image_files, 1):
        input_path = os.path.join(directory_path, filename)
        output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".txt")
        
        try:
            print(f"\n处理进度: {i}/{total_images}")
            result = process_image_with_florence(model, input_path, prompt_mode)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"已保存结果: {output_path}")
        
        except Exception as e:
            print(f"处理 '{filename}' 失败: {e}")

def generate_combined_prompts(directory_path=None):
    """生成综合描述"""
    directory_path = directory_path or IMAGE_DIRECTORY
    
    if not os.path.isdir(directory_path):
        print(f"错误: 目录 '{directory_path}' 不存在")
        return
    
    output_dir = os.path.join(directory_path, "Prompts")
    os.makedirs(output_dir, exist_ok=True)
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    image_files = [f for f in os.listdir(directory_path) 
                   if os.path.splitext(f.lower())[1] in image_extensions]
    
    total_images = len(image_files)
    print(f"开始处理 {total_images} 张图片，生成综合描述")
    
    model = FlorenceModel()  # 初始化模型
    
    for i, filename in enumerate(image_files, 1):
        input_path = os.path.join(directory_path, filename)
        output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".txt")
        
        try:
            print(f"\n处理综合描述: {i}/{total_images}")
            results = {}
            for mode in ["elements", "style", "keywords", "ai_prompt"]:
                results[mode] = process_image_with_florence(model, input_path, mode)
            
            combined_text = "\n\n".join(f"[{k.capitalize()}]\n{v}" for k, v in results.items())
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(combined_text)
            print(f"已保存综合结果: {output_path}")
        
        except Exception as e:
            print(f"处理 '{filename}' 失败: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='使用 Florence-2 生成图像描述')
    parser.add_argument('directory', type=str, nargs='?', help='图片目录路径')
    parser.add_argument('--mode', type=str, default="elements",
                        choices=["elements", "style", "keywords", "ai_prompt", "combined"],
                        help='描述模式')
    parser.add_argument('--model_path', type=str, default=MODEL_PATH, help='模型路径或名称')
    parser.add_argument('--cache_dir', type=str, default=CACHE_DIR, help='模型缓存目录')
    
    args = parser.parse_args()
    
    # 更新全局路径
    MODEL_PATH = args.model_path
    CACHE_DIR = args.cache_dir
    
    if args.mode == "combined":
        generate_combined_prompts(args.directory)
    else:
        generate_prompts(args.directory, args.mode)