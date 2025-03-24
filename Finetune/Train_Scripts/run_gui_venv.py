#!/usr/bin/env python3
# 第三步 此脚本用于启动kohya_ss的GUI
import os
import sys
import subprocess
import time
import webbrowser
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
    
    # 启动GUI
    print("正在启动kohya_ss GUI...")
    
    # 使用subprocess.Popen启动后台进程
    if sys.platform == "win32":
        python_cmd = str(root_dir / ".venv" / "Scripts" / "python.exe")
    else:
        python_cmd = str(root_dir / ".venv" / "bin" / "python")
    
    process = subprocess.Popen([python_cmd, "kohya_gui.py"])
    
    # 等待5秒让GUI启动
    print("等待GUI启动...")
    time.sleep(5)
    
    # 打开浏览器
    url = "http://127.0.0.1:7860"
    print(f"在浏览器中打开 {url}")
    webbrowser.open(url)
    
    # 由于我们不想脚本退出（保持服务运行），我们可以等待用户输入
    print("\n输入Ctrl+C来停止GUI服务...\n")
    try:
        process.wait()
    except KeyboardInterrupt:
        process.terminate()
        print("已停止GUI服务。")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 