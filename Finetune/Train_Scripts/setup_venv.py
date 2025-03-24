#!/usr/bin/env python3
# 此脚本用于创建虚拟环境并安装所有依赖

import os
import sys
import subprocess
import platform
import argparse
from pathlib import Path
import locale
import shutil

def run_command(cmd, check=True, encoding="utf-8"):
    """运行命令并打印输出"""
    print(f"执行命令: {' '.join(cmd if isinstance(cmd, list) else [cmd])}")
    result = subprocess.run(cmd, check=check, capture_output=True, text=True, encoding=encoding)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"错误: {result.stderr}")
    return result

def find_python310():
    """尝试找到Python 3.10的路径"""
    print("正在寻找系统中的Python 3.10...")
    
    try:
        if platform.system() == "Windows":
            # 常见的Python 3.10安装位置
            possible_paths = [
                r"C:\Python310\python.exe",
                r"C:\Program Files\Python310\python.exe",
                r"C:\Program Files (x86)\Python310\python.exe",
                os.path.expanduser(r"~\AppData\Local\Programs\Python\Python310\python.exe")
            ]
            
            # 尝试使用py启动器
            try:
                result = subprocess.run(["py", "-3.10", "--version"], 
                                       capture_output=True, text=True, encoding="utf-8", check=False)
                if result.returncode == 0:
                    print("找到Python 3.10 (py启动器)")
                    return "py -3.10"
            except:
                pass
                
            # 尝试在PATH中查找python3.10
            try:
                result = subprocess.run(["python3.10", "--version"], 
                                       capture_output=True, text=True, encoding="utf-8", check=False)
                if result.returncode == 0:
                    print("找到Python 3.10 (python3.10)")
                    return "python3.10"
            except:
                pass
                
            # 检查可能的安装位置
            for path in possible_paths:
                if os.path.exists(path):
                    print(f"找到Python 3.10: {path}")
                    return path
        else:
            # Linux/macOS
            try:
                result = subprocess.run(["python3.10", "--version"], 
                                       capture_output=True, text=True, encoding="utf-8", check=False)
                if result.returncode == 0:
                    print("找到Python 3.10 (python3.10)")
                    return "python3.10"
            except:
                pass
                
    except Exception as e:
        print(f"查找Python 3.10时出错: {e}")
    
    print("未找到Python 3.10，您可能需要先安装Python 3.10")
    return None

def setup_script_wrappers(venv_dir, root_dir):
    """创建脚本包装器以确保使用虚拟环境中的Python"""
    print("设置脚本运行环境...")
    
    # 创建.env文件指向虚拟环境的Python解释器
    env_file = root_dir / ".env"
    if platform.system() == "Windows":
        python_path = venv_dir / "Scripts" / "python.exe"
    else:
        python_path = venv_dir / "bin" / "python"
    
    with open(env_file, "w") as f:
        f.write(f"PYTHONPATH={root_dir}\n")
        f.write(f"PATH={os.path.dirname(python_path)}{os.pathsep}$PATH\n")
    
    print(f"已创建.env文件: {env_file}")

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="设置Python 3.10虚拟环境并安装依赖")
    parser.add_argument("--python", default=None, help="指定Python 3.10解释器路径 (默认: 自动寻找)")
    parser.add_argument("--source", default="https://pypi.tuna.tsinghua.edu.cn/simple", 
                        help="指定pip安装源 (默认: 清华大学镜像源)")
    parser.add_argument("--trusted-host", default="pypi.tuna.tsinghua.edu.cn",
                        help="指定受信任的pip源主机 (默认: pypi.tuna.tsinghua.edu.cn)")
    parser.add_argument("--force", action="store_true", help="强制重新创建虚拟环境，不询问")
    
    return parser.parse_args()

def main():
    # 设置默认编码为UTF-8
    os.environ["PYTHONIOENCODING"] = "utf-8"
    args = parse_arguments()
    
    # 获取当前工作目录（项目根目录）
    root_dir = Path.cwd().absolute()
    print(f"项目根目录: {root_dir}")
    
    print("开始设置Python 3.10虚拟环境...")
    
    # 确定Python命令
    python_cmd = args.python if args.python else find_python310()
    if not python_cmd:
        print("错误: 未找到Python 3.10。请安装Python 3.10或使用--python参数指定Python 3.10路径。")
        return 1
    
    print(f"使用Python 3.10: {python_cmd}")
    
    # 验证Python版本
    try:
        if python_cmd == "py -3.10":
            ver_result = run_command(["py", "-3.10", "-c", "import sys; print(sys.version)"], encoding="utf-8")
        else:
            ver_result = run_command([python_cmd, "-c", "import sys; print(sys.version)"], encoding="utf-8")
        
        if not "3.10" in ver_result.stdout:
            print(f"警告: 指定的Python不是3.10版本。检测到的版本: {ver_result.stdout.strip()}")
            proceed = input("是否继续? (y/n): ").strip().lower()
            if proceed != 'y':
                print("已取消安装")
                return 1
    except Exception as e:
        print(f"验证Python版本时出错: {e}")
        return 1
    
    # 创建虚拟环境目录
    venv_dir = root_dir / "venv"
    
    # 如果虚拟环境已存在，根据需要删除
    if venv_dir.exists():
        print(f"虚拟环境已存在: {venv_dir}")
        if args.force:
            proceed = 'y'
        else:
            proceed = input("是否删除并重新创建? (y/n): ").strip().lower()
        
        if proceed == 'y':
            print(f"正在删除旧的虚拟环境...")
            try:
                shutil.rmtree(venv_dir)
            except Exception as e:
                print(f"删除旧虚拟环境时出错: {e}")
                print("尝试关闭所有使用该环境的程序，然后重试")
                return 1
                
            print(f"正在创建新的虚拟环境: {venv_dir}")
            try:
                if python_cmd == "py -3.10":
                    run_command(["py", "-3.10", "-m", "venv", str(venv_dir)], encoding="utf-8")
                else:
                    run_command([python_cmd, "-m", "venv", str(venv_dir)], encoding="utf-8")
            except Exception as e:
                print(f"创建虚拟环境时出错: {e}")
                return 1
        else:
            print("保留现有虚拟环境")
    else:
        print(f"正在创建虚拟环境: {venv_dir}")
        try:
            if python_cmd == "py -3.10":
                run_command(["py", "-3.10", "-m", "venv", str(venv_dir)], encoding="utf-8")
            else:
                run_command([python_cmd, "-m", "venv", str(venv_dir)], encoding="utf-8")
        except Exception as e:
            print(f"创建虚拟环境时出错: {e}")
            return 1
    
    # 获取虚拟环境中的Python和pip路径
    if platform.system() == "Windows":
        venv_python = venv_dir / "Scripts" / "python.exe"
        venv_pip = venv_dir / "Scripts" / "pip.exe"
    else:
        venv_python = venv_dir / "bin" / "python"
        venv_pip = venv_dir / "bin" / "pip"
    
    # 检查虚拟环境中的Python版本
    try:
        result = run_command([str(venv_python), "--version"], encoding="utf-8")
        print(f"虚拟环境Python版本: {result.stdout.strip()}")
        
        # 检查是否确实是Python 3.10
        version_result = run_command([str(venv_python), "-c", "import sys; print(sys.version)"], encoding="utf-8")
        if not "3.10" in version_result.stdout:
            print(f"警告: 虚拟环境中的Python不是3.10版本。检测到的版本: {version_result.stdout.strip()}")
            proceed = input("是否继续? (y/n): ").strip().lower()
            if proceed != 'y':
                print("已取消安装")
                return 1
    except Exception as e:
        print(f"检查Python版本时出错: {e}")
        return 1
    
    # 设置脚本运行环境
    setup_script_wrappers(venv_dir, root_dir)
    
    # 设置pip源和受信任主机
    pip_source = args.source
    trusted_host = args.trusted_host
    
    # 升级pip
    print("升级pip...")
    try:
        run_command([str(venv_python), "-m", "pip", "install", "--upgrade", "pip", 
                    "-i", pip_source, "--trusted-host", trusted_host], encoding="utf-8")
    except Exception as e:
        print(f"升级pip时出错: {e}")
        print("继续安装其他依赖...")
    
    # 安装根目录的依赖
    root_requirements = root_dir / "requirements.txt"
    if root_requirements.exists():
        print(f"安装根目录依赖: {root_requirements}")
        try:
            run_command([str(venv_pip), "install", "-r", str(root_requirements), 
                        "-i", pip_source, "--trusted-host", trusted_host], encoding="utf-8", check=False)
        except Exception as e:
            print(f"安装根目录依赖时出错: {e}")
            print("继续安装其他依赖...")
    
    # 检查kohya_ss目录是否存在
    kohya_dir = root_dir / "kohya_ss"
    if kohya_dir.exists():
        print("检测到kohya_ss目录，安装kohya_ss依赖...")
        
        # 检查是否需要初始化git子模块
        sd_scripts_dir = kohya_dir / "sd-scripts"
        if not sd_scripts_dir.exists() or not any(sd_scripts_dir.iterdir()):
            print("sd-scripts子模块不存在或为空，尝试初始化子模块...")
            # 保存当前目录
            current_dir = os.getcwd()
            try:
                # 切换到kohya_ss目录
                os.chdir(kohya_dir)
                # 初始化子模块
                run_command(["git", "submodule", "init"], encoding="utf-8", check=False)
                run_command(["git", "submodule", "update"], encoding="utf-8", check=False)
            except Exception as e:
                print(f"初始化子模块时出错: {e}")
            finally:
                # 切回原来的目录
                os.chdir(current_dir)
        
        # 安装kohya_ss依赖
        kohya_requirements = kohya_dir / "requirements.txt"
        if kohya_requirements.exists():
            print(f"安装kohya_ss主要依赖: {kohya_requirements}")
            try:
                run_command([str(venv_pip), "install", "-r", str(kohya_requirements), 
                            "-i", pip_source, "--trusted-host", trusted_host], encoding="utf-8", check=False)
            except Exception as e:
                print(f"安装kohya_ss依赖时出错: {e}")
                print("继续安装其他依赖...")
        
        # 安装特定平台的依赖
        if platform.system() == "Windows":
            windows_requirements = kohya_dir / "requirements_windows.txt"
            if windows_requirements.exists():
                print(f"安装Windows特定依赖: {windows_requirements}")
                try:
                    run_command([str(venv_pip), "install", "-r", str(windows_requirements), 
                                "-i", pip_source, "--trusted-host", trusted_host], encoding="utf-8", check=False)
                except Exception as e:
                    print(f"安装Windows特定依赖时出错: {e}")
            
            pytorch_windows_requirements = kohya_dir / "requirements_pytorch_windows.txt"
            if pytorch_windows_requirements.exists():
                print(f"安装Windows PyTorch特定依赖: {pytorch_windows_requirements}")
                try:
                    run_command([str(venv_pip), "install", "-r", str(pytorch_windows_requirements), 
                                "-i", pip_source, "--trusted-host", trusted_host], encoding="utf-8", check=False)
                except Exception as e:
                    print(f"安装PyTorch依赖时出错: {e}")
        elif platform.system() == "Linux":
            linux_requirements = kohya_dir / "requirements_linux.txt"
            if linux_requirements.exists():
                print(f"安装Linux特定依赖: {linux_requirements}")
                try:
                    run_command([str(venv_pip), "install", "-r", str(linux_requirements), 
                                "-i", pip_source, "--trusted-host", trusted_host], encoding="utf-8", check=False)
                except Exception as e:
                    print(f"安装Linux特定依赖时出错: {e}")
        elif platform.system() == "Darwin":  # macOS
            if platform.machine() == "x86_64":  # Intel
                macos_requirements = kohya_dir / "requirements_macos_amd64.txt"
            else:  # ARM (Apple Silicon)
                macos_requirements = kohya_dir / "requirements_macos_arm64.txt"
            
            if macos_requirements.exists():
                print(f"安装macOS特定依赖: {macos_requirements}")
                try:
                    run_command([str(venv_pip), "install", "-r", str(macos_requirements), 
                                "-i", pip_source, "--trusted-host", trusted_host], encoding="utf-8", check=False)
                except Exception as e:
                    print(f"安装macOS特定依赖时出错: {e}")
        
        # 安装sd-scripts
        if sd_scripts_dir.exists():
            print("安装sd-scripts...")
            # 保存当前目录
            current_dir = os.getcwd()
            try:
                # 切换到kohya_ss目录
                os.chdir(kohya_dir)
                # 安装sd-scripts
                run_command([str(venv_pip), "install", "-e", "./sd-scripts", 
                            "-i", pip_source, "--trusted-host", trusted_host], encoding="utf-8", check=False)
            except Exception as e:
                print(f"安装sd-scripts时出错: {e}")
            finally:
                # 切回原来的目录
                os.chdir(current_dir)
        else:
            print("警告: sd-scripts目录不存在，可能影响部分功能。")
    
    # 检查是否有其他依赖目录需要安装
    for dir_name in ["Scripts", "Train_Scripts"]:
        script_dir = root_dir / dir_name
        if script_dir.exists():
            print(f"检查{dir_name}目录中的依赖...")
            requirements_file = script_dir / "requirements.txt"
            if requirements_file.exists():
                print(f"安装{dir_name}依赖: {requirements_file}")
                try:
                    run_command([str(venv_pip), "install", "-r", str(requirements_file), 
                                "-i", pip_source, "--trusted-host", trusted_host], encoding="utf-8", check=False)
                except Exception as e:
                    print(f"安装{dir_name}依赖时出错: {e}")
    
    # 创建.pth文件确保Python路径包含当前项目
    site_packages_dir = None
    if platform.system() == "Windows":
        site_packages_dir = venv_dir / "Lib" / "site-packages"
    else:
        lib_dir = venv_dir / "lib"
        for py_dir in lib_dir.glob("python3.*"):
            if py_dir.is_dir():
                site_packages_dir = py_dir / "site-packages"
                break
    
    if site_packages_dir and site_packages_dir.exists():
        pth_file = site_packages_dir / "project.pth"
        with open(pth_file, "w") as f:
            f.write(str(root_dir))
        print(f"已创建Python路径配置: {pth_file}")
    
    print("\n==========================")
    print("Python 3.10虚拟环境设置完成!")
    print("==========================\n")
    
    # 显示如何使用虚拟环境
    print("您的项目现在配置为使用虚拟环境中的Python 3.10")
    
    if platform.system() == "Windows":
        print(f"虚拟环境Python路径: {venv_dir}\\Scripts\\python.exe")
        print(f"要使用此环境，直接运行项目中的Python脚本即可")
    else:
        print(f"虚拟环境Python路径: {venv_dir}/bin/python")
        print(f"要使用此环境，直接运行项目中的Python脚本即可")
    
    print("\n使用的pip源: " + pip_source)
    print("如需更换源，请使用 --source 参数，例如:")
    print("python setup_venv.py --source https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 