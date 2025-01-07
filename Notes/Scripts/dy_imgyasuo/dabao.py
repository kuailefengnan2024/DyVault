import PyInstaller.__main__

PyInstaller.__main__.run([
    'transfer_topng.py',  # 替换为你的脚本名
    '--onefile',
    '--windowed',
    '--add-binary', 'pngquant/pngquant.exe;pngquant',
    '--icon', 'my_icon.ico'  # 添加图标文件
])