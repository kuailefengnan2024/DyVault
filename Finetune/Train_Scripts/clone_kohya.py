#!/usr/bin/env python3
# 第一步 此脚本用于从github克隆kohya_ss仓库
import os
import sys
import subprocess
from pathlib import Path

def main():
    # 获取Finetune根目录的路径
    root_dir = Path(__file__).parent.parent.absolute()
    
    # 检查kohya_ss目录是否已存在
    kohya_dir = root_dir / "kohya_ss"
    if kohya_dir.exists():
        print("kohya_ss目录已存在，无需克隆。")
        return 0
    
    # 如果不存在，则克隆仓库
    print("正在克隆kohya_ss仓库...")
    
    try:
        # 切换到根目录
        os.chdir(root_dir)
        
        # 使用SSH方式克隆kohya_ss
        subprocess.run(["git", "clone", "git@github.com:bmaltais/kohya_ss.git"], check=True)
        
        # 进入kohya_ss目录
        os.chdir(kohya_dir)
        
        # 初始化并更新子模块（包括sd-scripts）
        subprocess.run(["git", "submodule", "update", "--init", "--recursive"], check=True)
        
        print("kohya_ss及其子模块克隆完成！")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"克隆过程中发生错误: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 