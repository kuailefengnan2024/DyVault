import os
import sys
import torch
from PIL import Image
from transformers import AutoProcessor

# 将模型目录添加到 sys.path，以便导入 modeling_florence2.py
MODEL_PATH = r"D:\BaiduSyncdisk\DyVault\Finetune\Models\florence-2-large"
sys.path.append(MODEL_PATH)

# 手动导入 modeling_florence2
try:
    from modeling_florence2 import Florence2ForConditionalGeneration
except ImportError as e:
    print(f"无法导入 modeling_florence2: {e}")
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
            self.processor = AutoProcessor.from_pretrained(
                self.model_path,
                local_files_only=True,
                trust_remote_code=True
            )
            # 加载模型，使用本地 modeling_florence2 中的 Florence2ForConditionalGeneration
            self.model = Florence2ForConditionalGeneration.from_pretrained(
                self.model_path,
                torch_dtype=self.torch_dtype,
                trust_remote_code=True,
                local_files_only=True
            ).to(self.device)
            print("Florence-2 模型加载成功")
        except Exception as e:
            print(f"加载 Florence-2 模型失败: {str(e)}")
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
            return error_msg

# 测试代码
if __name__ == "__main__":
    model = FlorenceModel()
    image_path = r"D:\BaiduSyncdisk\DyVault\Finetune\Datasets\Custom_Images_Keai\test.jpg"
    description = model.generate_description(image_path)
    print(f"生成的描述: {description}")