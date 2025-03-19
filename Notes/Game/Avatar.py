from PIL import Image, ImageDraw
import random

def generate_npc_avatar(size=128, seed=None):
    if seed:
        random.seed(seed)  # 可选：使用种子确保可重复生成
    
    # 创建基础图片
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))  # 透明背景
    draw = ImageDraw.Draw(img)
    
    # 皮肤颜色选项
    skin_colors = [
        (245, 215, 180),  # 浅肤色
        (210, 165, 135),  # 中肤色
        (165, 120, 90),   # 深肤色
    ]
    
    # 头发颜色选项
    hair_colors = [
        (50, 30, 20),     # 棕色
        (20, 20, 20),     # 黑色
        (200, 150, 50),   # 金色
        (150, 50, 50),    # 红色
    ]
    
    # 1. 绘制头部
    skin_color = random.choice(skin_colors)
    head_size = size * 0.7
    head_pos = (size * 0.15, size * 0.15)
    draw.ellipse([head_pos, (head_pos[0] + head_size, head_pos[1] + head_size)], 
                 fill=skin_color)
    
    # 2. 绘制头发
    hair_color = random.choice(hair_colors)
    hair_style = random.choice(['short', 'long', 'bald'])
    if hair_style == 'short':
        draw.ellipse([head_pos[0] - 5, head_pos[1] - 5, 
                     head_pos[0] + head_size + 5, head_pos[1] + head_size * 0.4],
                    fill=hair_color)
    elif hair_style == 'long':
        draw.ellipse([head_pos[0] - 10, head_pos[1] - 10, 
                     head_pos[0] + head_size + 10, head_pos[1] + head_size + 10],
                    fill=hair_color)
    
    # 3. 绘制眼睛
    eye_size = size * 0.1
    eye_y = head_pos[1] + head_size * 0.35
    draw.ellipse([head_pos[0] + head_size * 0.25, eye_y,
                 head_pos[0] + head_size * 0.35, eye_y + eye_size],
                fill=(255, 255, 255))  # 左眼
    draw.ellipse([head_pos[0] + head_size * 0.55, eye_y,
                 head_pos[0] + head_size * 0.65, eye_y + eye_size],
                fill=(255, 255, 255))  # 右眼
    # 瞳孔
    pupil_size = eye_size * 0.5
    draw.ellipse([head_pos[0] + head_size * 0.275, eye_y + eye_size * 0.25,
                 head_pos[0] + head_size * 0.325, eye_y + eye_size * 0.75],
                fill=(0, 0, 0))
    draw.ellipse([head_pos[0] + head_size * 0.575, eye_y + eye_size * 0.25,
                 head_pos[0] + head_size * 0.625, eye_y + eye_size * 0.75],
                fill=(0, 0, 0))
    
    # 4. 绘制嘴巴
    mouth_y = head_pos[1] + head_size * 0.65
    draw.arc([head_pos[0] + head_size * 0.35, mouth_y,
             head_pos[0] + head_size * 0.55, mouth_y + eye_size],
            0, 180, fill=(200, 100, 100), width=2)
    
    # 保存图片
    img.save('npc_avatar.png')
    return img

# 生成一个128x128的NPC头像
generate_npc_avatar(128)
print("NPC头像已生成并保存为 'npc_avatar.png'")