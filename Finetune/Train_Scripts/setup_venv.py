#!/usr/bin/env python3
# 第二步 此脚本用于安装kohya_ss的依赖
import os
import sys
import subprocess
from pathlib import Path

def main():
    # 检查Python版本
    python_version = sys.version_info
    if python_version.major == 3 and python_version.minor >= 11:
        print(f"提示: 检测到Python {python_version.major}.{python_version.minor}版本")
        print("某些依赖包（如wandb使用的pathtools）与Python 3.11+不兼容，将会忽略这些错误")
        print("如果您需要使用wandb功能，建议使用Python 3.10版本")
    
    # 获取Finetune根目录的路径
    root_dir = Path(__file__).parent.parent.absolute()
    os.chdir(root_dir)
    
    # 确保sd-scripts子模块已经克隆
    sd_scripts_git = root_dir / "kohya_ss" / "sd-scripts" / ".git"
    if not sd_scripts_git.exists():
        print("正在克隆sd-scripts仓库...")
        os.chdir(root_dir / "kohya_ss")
        
        # 确保子模块配置正确
        subprocess.run(["git", "config", "-f", ".gitmodules", "submodule.sd-scripts.url", "git@github.com:kohya-ss/sd-scripts.git"], check=True)
        
        # 初始化和更新子模块
        subprocess.run(["git", "submodule", "update", "--init", "--recursive"], check=True)
        
        os.chdir(root_dir)
    
    # 确保虚拟环境存在
    venv_dir = root_dir / ".venv"
    if not venv_dir.exists():
        print("创建虚拟环境...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
    
    # 确定激活脚本路径
    if sys.platform == "win32":
        activate_script = venv_dir / "Scripts" / "activate"
        python_executable = venv_dir / "Scripts" / "python.exe"
    else:
        activate_script = venv_dir / "bin" / "activate"
        python_executable = venv_dir / "bin" / "python"
    
    # 确保pip是最新版本
    print("更新pip...")
    upgrade_pip = [str(python_executable), "-m", "pip", "install", "--upgrade", "pip"]
    subprocess.run(upgrade_pip, check=True)
    
    # 安装依赖
    print("安装sd-scripts...")
    venv_pip = [str(python_executable), "-m", "pip", "install", "-e", "./kohya_ss/sd-scripts"]
    subprocess.run(venv_pip, check=True)
    
    print("安装主要依赖...")
    # 忽略安装错误，继续安装剩余依赖
    try:
        venv_pip = [str(python_executable), "-m", "pip", "install", "-r", "requirements.txt"]
        subprocess.run(venv_pip, check=False)  # 注意这里使用check=False，允许出错但继续执行
        print("依赖安装已完成！")
    except Exception as e:
        print(f"安装过程中发生异常: {e}")
    
    # 确保gradio正确安装，这对kohya_ss的GUI功能至关重要
    print("\n确保gradio正确安装...")
    try:
        venv_pip = [str(python_executable), "-m", "pip", "install", "gradio==4.43.0", "--no-deps"]
        subprocess.run(venv_pip, check=True)
        print("gradio 4.43.0 安装成功！")
    except Exception as e:
        print(f"安装gradio时发生异常: {e}")
        print("尝试安装gradio的完整依赖...")
        venv_pip = [str(python_executable), "-m", "pip", "install", "gradio==4.43.0"]
        subprocess.run(venv_pip, check=True)
    
    if python_version.major == 3 and python_version.minor >= 11:
        print("\n注意：由于使用的是Python 3.11+版本，wandb相关功能可能无法正常使用。")
        print("这是因为wandb依赖的pathtools包使用了在Python 3.11+中被移除的'imp'模块。")
        print("如果需要使用wandb功能，建议使用Python 3.10版本。")
    
    print("\n你现在可以使用共享虚拟环境来运行kohya_ss和其他脚本了。")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 