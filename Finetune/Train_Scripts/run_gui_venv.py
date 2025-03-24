#!/usr/bin/env python3
# 此脚本用于使用accelerate启动kohya_ss的GUI界面
import os
import sys
import subprocess
from pathlib import Path

def main():
    # 获取Finetune根目录的路径
    root_dir = Path(__file__).parent.parent.absolute()
    kohya_dir = root_dir / "kohya_ss"
    
    # 检查kohya_ss目录是否存在
    if not kohya_dir.exists():
        print("错误：kohya_ss目录不存在，请先运行 clone_kohya.py 脚本。")
        return 1
    
    # 切换到kohya_ss目录
    os.chdir(kohya_dir)
    
    print("正在启动Kohya GUI界面，支持GPU加速训练...")
    
    # 手动指定CUDA_HOME路径 - 根据nvidia-smi显示CUDA 12.8，使用对应的路径
    # 用户可以根据自己的CUDA安装位置修改此路径
    MANUAL_CUDA_PATH = "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.8"
    
    # 设置CUDA_HOME环境变量
    if "CUDA_HOME" not in os.environ:
        # 首先尝试使用手动指定的路径
        if os.path.exists(MANUAL_CUDA_PATH):
            os.environ["CUDA_HOME"] = MANUAL_CUDA_PATH
            print(f"已使用手动设置的CUDA_HOME路径: {MANUAL_CUDA_PATH}")
        else:
            # 尝试常见的CUDA路径
            cuda_paths = [
                MANUAL_CUDA_PATH,
                "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.8",
                "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.0",
                "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.1",
                "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.2",
                "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.8",
                "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.7",
                "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.6",
            ]
            
            for path in cuda_paths:
                if os.path.exists(path):
                    os.environ["CUDA_HOME"] = path
                    print(f"已自动设置CUDA_HOME为: {path}")
                    break
            
            if "CUDA_HOME" not in os.environ:
                print("警告: 未找到CUDA安装路径，需要安装CUDA或手动设置CUDA_HOME环境变量")
                print("请尝试以下方法设置CUDA环境:")
                print("1. 检查NVIDIA CUDA是否已安装")
                print("2. 修改脚本中的MANUAL_CUDA_PATH变量指向您的CUDA安装路径")
                print("3. 或者可以手动添加环境变量: set CUDA_HOME=C:\\您的CUDA安装路径")
                print("\n如果您不需要GPU加速，将继续尝试启动...")
    
    # 设置环境变量，启用GPU加速
    os.environ["PYTHONPATH"] = str(kohya_dir)
    os.environ["ACCELERATE_MIXED_PRECISION"] = "fp16"
    
    # 确保使用kohya_gui.py作为启动脚本
    gui_script = "kohya_gui.py"
    
    if not (kohya_dir / gui_script).exists():
        print(f"错误：找不到GUI启动脚本 {gui_script}，请检查kohya_ss目录结构。")
        return 1
    
    # 设置命令行参数，强制启用GPU
    python_cmd = sys.executable
    cmd = [
        python_cmd, 
        gui_script,
        "--listen", "0.0.0.0",  # 允许远程访问
        "--inbrowser"           # 自动在浏览器中打开界面
    ]
    
    # 如果需要添加更多参数，请确保遵循正确的格式
    # 注意：--headless 参数在添加时表示无头模式，不添加则默认有GUI
    # 注意：kohya_gui.py 不支持 --gpu 参数，已移除
    
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        # 创建并保存默认的accelerate配置
        with open("default_config.yaml", "w") as f:
            f.write("""compute_environment: LOCAL_MACHINE
distributed_type: NO
mixed_precision: fp16
use_cpu: false
gpu_ids: all
debug: false
num_processes: 1
""")
        
        # 设置Accelerate环境变量
        os.environ["ACCELERATE_CONFIG_FILE"] = str(kohya_dir / "default_config.yaml")
        
        # 启动GUI
        subprocess.run(cmd, check=True)
        print("GUI界面已关闭。")
    except subprocess.CalledProcessError as e:
        print(f"启动GUI界面时出错: {e}")
        return 1
    except KeyboardInterrupt:
        print("用户中断执行。")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 