import os
import subprocess
import sys

# 定义备用虚拟环境路径
GLOBAL_ENV_PATH = r"D:\ComfyUI-aki\ComfyUI-aki-v1.4\myenv"  # 修改为你的全局虚拟环境路径

def create_venv_and_install(plugin_dir):
    """
    优先在插件目录下创建虚拟环境并安装依赖，失败时使用全局虚拟环境安装
    :param plugin_dir: 插件目录路径
    """
    # 检查插件目录是否存在
    if not os.path.exists(plugin_dir):
        print(f"插件目录不存在：{plugin_dir}")
        return

    # 定义插件目录下的虚拟环境路径
    venv_path = os.path.join(plugin_dir, "venv")
    requirements_path = os.path.join(plugin_dir, "requirements.txt")

    # 优先尝试在插件目录下创建虚拟环境
    if not os.path.exists(venv_path):
        print(f"正在为插件创建虚拟环境：{venv_path}")
        try:
            subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
        except subprocess.CalledProcessError:
            print(f"错误：无法在插件目录下创建虚拟环境！将使用全局虚拟环境。")
            install_in_global_env(requirements_path)
            return
    else:
        print(f"虚拟环境已存在：{venv_path}")

    # 获取插件目录下虚拟环境的 pip 路径
    pip_path = os.path.join(venv_path, "Scripts", "pip.exe") if os.name == "nt" else os.path.join(venv_path, "bin", "pip")

    # 确保 pip 可用
    if not os.path.exists(pip_path):
        print(f"错误：未找到 pip，无法使用插件目录下的虚拟环境！将使用全局虚拟环境。")
        install_in_global_env(requirements_path)
        return

    # 安装依赖
    if os.path.exists(requirements_path):
        print(f"正在插件目录下的虚拟环境中安装依赖：{requirements_path}")
        subprocess.run([pip_path, "install", "-r", requirements_path], check=True)
        print("依赖安装完成！")
    else:
        print(f"未找到 requirements.txt 文件，跳过依赖安装。路径：{requirements_path}")

    # 显示已安装的依赖
    print("\n插件目录虚拟环境中的已安装依赖：")
    subprocess.run([pip_path, "list"])
    print("\n插件依赖安装完成！")

def install_in_global_env(requirements_path):
    """
    安装依赖到全局虚拟环境
    :param requirements_path: requirements.txt 文件路径
    """
    # 检查全局虚拟环境是否存在
    if not os.path.exists(GLOBAL_ENV_PATH):
        print(f"全局虚拟环境不存在：{GLOBAL_ENV_PATH}，请先创建！")
        return

    # 获取全局虚拟环境的 pip 路径
    pip_path = os.path.join(GLOBAL_ENV_PATH, "Scripts", "pip.exe") if os.name == "nt" else os.path.join(GLOBAL_ENV_PATH, "bin", "pip")

    # 确保 pip 可用
    if not os.path.exists(pip_path):
        print(f"错误：未找到 pip，请检查全局虚拟环境！路径：{pip_path}")
        return

    # 安装依赖
    if os.path.exists(requirements_path):
        print(f"正在全局虚拟环境中安装依赖：{requirements_path}")
        subprocess.run([pip_path, "install", "-r", requirements_path], check=True)
        print("依赖安装完成！")
    else:
        print(f"未找到 requirements.txt 文件，跳过依赖安装。路径：{requirements_path}")

    # 显示全局虚拟环境中的已安装依赖
    print("\n全局虚拟环境中的已安装依赖：")
    subprocess.run([pip_path, "list"])
    print("\n依赖安装完成！")

# 主函数
if __name__ == "__main__":
    # 提示用户输入插件目录路径
    plugin_directory = input("请输入插件目录路径（例如 D:\\ComfyUI-aki\\ComfyUI-aki-v1.4\\custom_nodes\\YourPlugin）：\n").strip()

    # 检查路径是否为空
    if not plugin_directory:
        print("错误：您没有输入插件目录路径！")
        sys.exit(1)

    # 检查路径是否是有效的文件夹
    if not os.path.isdir(plugin_directory):
        print(f"错误：输入的路径无效或不是文件夹：{plugin_directory}")
        sys.exit(1)

    # 调用创建虚拟环境并安装依赖
    create_venv_and_install(plugin_directory)