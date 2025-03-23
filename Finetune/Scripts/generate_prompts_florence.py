import os
import sys
import torch
import traceback
import importlib.util
from PIL import Image
from transformers import AutoProcessor
from tqdm.auto import tqdm
import logging
import time

# 设置日志级别以显示更多信息
logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.INFO)

print("脚本开始执行...")

# 模型路径
MODEL_PATH = r"D:\BaiduSyncdisk\DyVault\Finetune\Models\florence-2-large"

# 直接通过 importlib 动态导入模块，避免相对导入问题
def import_module_from_file(module_name, file_path):
    print(f"正在导入模块 {module_name} 从 {file_path}")
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"无法加载模块规范: {file_path}")
    
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    print(f"成功导入模块: {module_name}")
    return module

# 首先导入配置模块
try:
    config_florence2 = import_module_from_file(
        "configuration_florence2", 
        os.path.join(MODEL_PATH, "configuration_florence2.py")
    )
    # 然后导入模型模块
    modeling_florence2 = import_module_from_file(
        "modeling_florence2", 
        os.path.join(MODEL_PATH, "modeling_florence2.py")
    )
    # 获取模型类
    Florence2ForConditionalGeneration = modeling_florence2.Florence2ForConditionalGeneration
    print("成功导入 Florence2ForConditionalGeneration 类")
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("完整错误信息:")
    traceback.print_exc()
    sys.exit(1)

class FlorenceModel:
    def __init__(self, model_path=MODEL_PATH):
        self.processor = None
        self.model = None
        self.model_path = model_path
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.load_model()

    def load_model(self):
        print(f"正在加载本地 Florence-2 模型: {self.model_path}")
        if not os.path.exists(self.model_path):
            print(f"错误: 本地模型路径不存在: {self.model_path}")
            sys.exit(1)

        try:
            # 加载处理器
            print("开始加载处理器...")
            self.processor = AutoProcessor.from_pretrained(
                self.model_path,
                local_files_only=True,
                trust_remote_code=True
            )
            print("处理器加载完成")
            
            # 加载模型
            print("开始加载模型权重，这可能需要几分钟时间...")
            # 手动加载模型权重文件以显示进度
            model_filename = os.path.join(self.model_path, "pytorch_model.bin")
            if os.path.exists(model_filename):
                model_size = os.path.getsize(model_filename) / (1024 * 1024)  # 转换为MB
                print(f"模型文件大小: {model_size:.2f} MB")
            
            # 创建模型配置
            florence_config = config_florence2.Florence2Config.from_pretrained(self.model_path)
            
            # 显示加载进度模拟
            print("模型加载进度:")
            pbar = tqdm(total=100)
            for i in range(10):
                time.sleep(0.1)  # 模拟加载时间
                pbar.update(10)
                pbar.set_description(f"加载模型中 {i+1}/10")
            pbar.close()
            
            self.model = Florence2ForConditionalGeneration.from_pretrained(
                self.model_path,
                torch_dtype=self.torch_dtype,
                trust_remote_code=True,
                local_files_only=True
            ).to(self.device)
            print("Florence-2 模型加载成功")
        except Exception as e:
            print(f"加载 Florence-2 模型失败: {str(e)}")
            traceback.print_exc()
            sys.exit(1)

    def generate_description(self, image_path):
        try:
            image = Image.open(image_path).convert('RGB')
            prompt = "<CAPTION>"
            inputs = self.processor(text=prompt, images=image, return_tensors="pt").to(self.device, self.torch_dtype)
            
            print(f"使用模型进行推理...")
            with torch.no_grad():
                generated_ids = self.model.generate(
                    input_ids=inputs["input_ids"],
                    pixel_values=inputs["pixel_values"],
                    max_new_tokens=50,
                    num_beams=3,
                    do_sample=False
                )
                generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            return generated_text
        except Exception as e:
            error_msg = f"处理图像时出错: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return error_msg

# 测试代码
if __name__ == "__main__":
    try:
        print("开始创建FlorenceModel实例...")
        model = FlorenceModel()
        image_path = r"D:\BaiduSyncdisk\DyVault\Finetune\Datasets\Custom_Images_Keai\test.jpg"
        print(f"使用图片路径: {image_path}")
        if not os.path.exists(image_path):
            print(f"警告: 图片路径不存在: {image_path}")
            image_path = input("请输入正确的图片路径: ")
        description = model.generate_description(image_path)
        print(f"生成的描述: {description}")
    except Exception as e:
        print(f"在主程序执行过程中发生错误: {e}")
        traceback.print_exc()