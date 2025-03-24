# 载入Florence模型出问题根本原因：原始代码试图直接将模型目录添加到 sys.path 并导入 modeling_florence2，但是该文件内部使用了相对导入语法 from .configuration_florence2 import Florence2Config，
# 这在非包环境中是不允许的。

# Train_Scripts文件夹用来训练
- kohya_ss是训练脚本本体 基本不需要动 存在即可 没有就先运行脚本clone_kohya.py下载
- clone_kohya.py 是下载kohya_ss的脚本 只需要运行一次 以后不需要运行
- setup_venv.py 是安装依赖的脚本 只需要运行一次 以后不需要运行
- run_gui_venv.py 是启动kohya_ss的GUI的脚本 
  

# Datasets文件夹用来存放训练数据集
可以挑选不同风格 修改后的图片和prompt 放在一起 

# Models文件夹用来存放模型

# Scripts文件夹用来存放前置处理的脚本 包括图片的预处理 和 prompt的修改


# 在不同电脑运行 首先运行clone_kohya.py 下载kohya_ss
# 然后运行setup_venv.py 安装依赖
# 最后运行run_gui_venv.py 启动kohya_ss的GUI

# 最后下载模型 运行download_model.py 下载模型


