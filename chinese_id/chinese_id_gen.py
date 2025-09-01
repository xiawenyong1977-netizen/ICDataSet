
from faker import Faker
from faker.providers import BaseProvider
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import textwrap
import requests
from io import BytesIO


# 加粗方法配置
BOLD_METHOD = "stroke"  # 可选值: "stroke" (描边加粗), "font" (字体加粗), "both" (两种都使用)

# 描边粗细配置（仅当BOLD_METHOD为"stroke"或"both"时生效）
STROKE_WIDTH = 0.5  # 描边宽度：0.5=细描边，1.0=中等描边，1.5=粗描边

# 描边宽度说明：
# 0.3 - 极细描边（几乎看不出加粗）
# 0.5 - 细描边（当前设置，推荐）
# 0.8 - 中等描边
# 1.0 - 标准描边（原来的效果）
# 1.5 - 粗描边
# 2.0 - 极粗描边

# 配置说明：
# 1. "stroke" - 仅使用描边加粗效果（推荐，效果最明显）
#    优点：加粗效果明显，不依赖字体
#    缺点：处理速度稍慢
#
# 2. "font" - 仅使用系统粗体字体
#    优点：处理速度快，效果自然
#    缺点：依赖系统字体，可能找不到合适的粗体字体
#
# 3. "both" - 两种方法结合使用
#    优点：加粗效果最明显
#    缺点：处理速度最慢，可能过于粗重
#
# 修改这个变量即可切换加粗方法！

# 创建一个支持中文的Faker实例
fake = Faker('zh_CN')









def generate_id_card_front_image(info, output_path, avatar_path=None):
    # 设置模板路径
    template_path = "id_card_template_front.png"
    
    # 1. 打开模板图片
    template = Image.open(template_path)
    
    # 2. 保持RGBA模式以支持透明通道
    if template.mode != 'RGBA':
        template = template.convert('RGBA')
    
    draw = ImageDraw.Draw(template)
    
    
    # 3. 定义每个字段在模板上的坐标 (x, y)
    coordinates = {
        'name': (202, 90),#134 45
        'sex': (202, 168),#36 35
        'nation': (415, 168),#38 32
        'year': (202, 240),#84 35
        'month': (350, 240),#46 32
        'day': (447, 240),#46 32
        'address': (202, 328),#420 160
        'id_number': (353, 523),#537 43
        'photo': (651, 110),#308 376
    }
    
    # 5. 绘制文本到图片上（增加字间距和加粗效果）
    def draw_text_with_spacing(draw, text, position, font, fill=(0, 0, 0), spacing=5, bold=False):
        """绘制带字间距的文本，支持加粗效果"""
        x, y = position
        for char in text:
            # 根据配置决定是否使用描边加粗
            if bold and BOLD_METHOD in ["stroke", "both"]:
                # 描边加粗效果：先绘制黑色描边，再绘制主文字
                # 描边（4个方向的偏移，使用配置的描边宽度）
                for dx, dy in [(-STROKE_WIDTH, 0), (STROKE_WIDTH, 0), (0, -STROKE_WIDTH), (0, STROKE_WIDTH)]:
                    draw.text((x + dx, y + dy), char, fill=(0, 0, 0), font=font)
                # 主文字
                draw.text((x, y), char, fill=fill, font=font)
            else:
                # 普通绘制或仅使用字体加粗
                draw.text((x, y), char, fill=fill, font=font)
            
            # 获取字符宽度并加上间距
            char_bbox = draw.textbbox((0, 0), char, font=font)
            char_width = char_bbox[2] - char_bbox[0]
            x += char_width + spacing
    
    # 绘制各个字段（带字间距和加粗）
    draw_text_with_spacing(draw, info['name'], coordinates['name'], font_front_big, spacing=8, bold=True)      # 姓名加粗
    draw_text_with_spacing(draw, info['sex'], coordinates['sex'], font_front, spacing=6, bold=False)      # 性别加粗
    draw_text_with_spacing(draw, info['nation'], coordinates['nation'], font_front, spacing=6, bold=False) # 民族加粗
    draw_text_with_spacing(draw, info['year'], coordinates['year'], font_front, spacing=3, bold=False)   # 年份不加粗
    draw_text_with_spacing(draw, info['month'], coordinates['month'], font_front, spacing=3, bold=False) # 月份不加粗
    draw_text_with_spacing(draw, info['day'], coordinates['day'], font_front, spacing=3, bold=False)    # 日期不加粗
    draw_text_with_spacing(draw, info['id_number'], coordinates['id_number'], font_front, spacing=4, bold=True) # 身份证号加粗

        # 地址可能很长，需要自动换行
    address_lines = textwrap.wrap(info['address'], width=11)
    for i, line in enumerate(address_lines):
        # 计算每行的位置：x坐标保持不变，y坐标递增
        line_position = (coordinates['address'][0], coordinates['address'][1] + i * 40)
        draw_text_with_spacing(draw, line, line_position, font_front, spacing=0, bold=False)  # 地址不加粗

    # 6. 处理头像粘贴
    if avatar_path and os.path.exists(avatar_path):
        try:
            # 打开头像图片（已经是去除背景的透明图片）
            avatar = Image.open(avatar_path)
            
            # 确保头像是RGBA模式（保持透明通道）
            if avatar.mode != 'RGBA':
                avatar = avatar.convert('RGBA')
            
            # 调整头像大小为指定尺寸 (308, 376)
            avatar_resized = avatar.resize((308, 376), Image.Resampling.LANCZOS)
            
            # 将头像粘贴到身份证图片上
            template.paste(avatar_resized, coordinates['photo'], avatar_resized)
            
            print(f"成功粘贴头像: {os.path.basename(avatar_path)}")
            
        except Exception as e:
            print(f"头像粘贴失败: {e}")
    
    # 7. 保存生成的图像和标注信息
    template.save(os.path.join(output_path, f"{info['id_number']}_front.png"))
    


def generate_id_card_back_image(info, output_path):
    # 设置模板路径
    template_path = "id_card_template_back.png"
    
    # 1. 打开模板图片
    template = Image.open(template_path)
    
    # 2. 保持RGBA模式以支持透明通道
    if template.mode != 'RGBA':
        template = template.convert('RGBA')
    
    draw = ImageDraw.Draw(template)
    

    
    # 4. 定义每个字段在模板上的坐标 (x, y)
    coordinates = {
        'authority': (248, 264),
        'valid_date': (248, 312),
    }
    
    # 5. 绘制文本到图片上（增加字间距和加粗效果）
    def draw_text_with_spacing(draw, text, position, font, fill=(0, 0, 0), spacing=5, bold=False):
        """绘制带字间距的文本，支持加粗效果"""
        x, y = position
        for char in text:
            # 根据配置决定是否使用描边加粗
            if bold and BOLD_METHOD in ["stroke", "both"]:
                # 描边加粗效果：先绘制黑色描边，再绘制主文字
                # 描边（4个方向的偏移，使用配置的描边宽度）
                for dx, dy in [(-STROKE_WIDTH, 0), (STROKE_WIDTH, 0), (0, -STROKE_WIDTH), (0, STROKE_WIDTH)]:
                    draw.text((x + dx, y + dy), char, fill=(0, 0, 0), font=font)
                # 主文字
                draw.text((x, y), char, fill=fill, font=font)
            else:
                # 普通绘制或仅使用字体加粗
                draw.text((x, y), char, fill=fill, font=font)
            
            # 获取字符宽度并加上间距
            char_bbox = draw.textbbox((0, 0), char, font=font)
            char_width = char_bbox[2] - char_bbox[0]
            x += char_width + spacing
    
    # 绘制各个字段（带字间距和加粗）
    draw_text_with_spacing(draw, info['authority'], coordinates['authority'], font, spacing=0, bold=True)      # 签发机关加粗
    draw_text_with_spacing(draw, info['valid_date'], coordinates['valid_date'], font_big, spacing=0, bold=True) # 有效期加粗
    
    # 6. （可选）生成并粘贴虚拟头像
    # ...
    
    # 7. 保存生成的图像和标注信息
    template.save(os.path.join(output_path, f"{info['id_number']}_back.png"))
    

        
# 主循环
output_base_dir = "chinese_ids"  # 基础输出目录
faces_tr_dir = "faces_tr"  # 去除背景后的头像目录
os.makedirs(output_base_dir, exist_ok=True)

# 加载中文字体！这是关键！
try:
    if BOLD_METHOD in ["font", "both"]:
        # 优先使用粗体字体
        font_paths = [
            "C:/Windows/Fonts/simsun.ttc",     # 宋体
            "C:/Windows/Fonts/msyhbd.ttc",     # 微软雅黑粗体
            "C:/Windows/Fonts/simhei.ttf",      # 黑体

            "C:/Windows/Fonts/simkai.ttf",     # 楷体
            "C:/Windows/Fonts/msyh.ttc",       # 微软雅黑
        ]
    else:
        # 使用普通字体
        font_paths = [
            "C:/Windows/Fonts/simsun.ttc",     # 宋体
            "C:/Windows/Fonts/msyh.ttc",       # 微软雅黑
            "C:/Windows/Fonts/simhei.ttf",      # 黑体
            "C:/Windows/Fonts/simkai.ttf",     # 楷体
        ]
    
    font = None
    font_big = None
    font_front = None
    font_front_big = None
    for font_path in font_paths:
        try:
            font = ImageFont.truetype(font_path, 20)
            font_big = ImageFont.truetype(font_path, 22)
            font_front = ImageFont.truetype(font_path, 35)
            font_front_big = ImageFont.truetype(font_path, 40)
            print(f"成功加载字体: {font_path}")
            break
        except IOError:
            continue
    
    if font is None:
        raise IOError("未找到可用字体")
        
except IOError:
    print("警告：未找到指定字体，使用默认字体，中文可能显示异常")
    font = ImageFont.load_default()
    font_big = ImageFont.load_default()
    font_front = ImageFont.load_default()
    font_front_big = ImageFont.load_default()

def combine_id_card_images(front_path, back_path, output_path, layout='horizontal'):
    """
    合并身份证正面和反面图片
    
    Args:
        front_path: 正面图片路径
        back_path: 反面图片路径  
        output_path: 输出路径
        layout: 排列方式，'horizontal' 为水平排列，'vertical' 为垂直排列
    """
    try:
        # 打开正面和反面图片
        front_img = Image.open(front_path)
        back_img = Image.open(back_path)
        
        # 确保两张图片大小一致（使用正面图片的尺寸作为标准）
        target_size = front_img.size
        back_img_resized = back_img.resize(target_size, Image.Resampling.LANCZOS)
        
        # 随机设置正反面之间的间距（10-50 像素）
        spacing = random.randint(10, 50)

        # 根据布局方式创建合并图片
        if layout == 'horizontal':
            # 水平排列：正面在左，反面在右
            combined_width = target_size[0] * 2 + spacing
            combined_height = target_size[1]
            combined_image = Image.new('RGBA', (combined_width, combined_height), (255, 255, 255, 0))
            
            # 粘贴图片
            combined_image.paste(front_img, (0, 0), front_img)
            combined_image.paste(back_img_resized, (target_size[0] + spacing, 0), back_img_resized)
            
        elif layout == 'vertical':
            # 垂直排列：正面在上，反面在下
            combined_width = target_size[0]
            combined_height = target_size[1] * 2 + spacing
            combined_image = Image.new('RGBA', (combined_width, combined_height), (255, 255, 255, 0))
            
            # 粘贴图片
            combined_image.paste(front_img, (0, 0), front_img)
            combined_image.paste(back_img_resized, (0, target_size[1] + spacing), back_img_resized)
        
        else:
            raise ValueError("layout 参数必须是 'horizontal' 或 'vertical'")
        
        # 保存合并图片
        combined_image.save(output_path, format='PNG')
        print(f"已生成合并图片: {os.path.basename(output_path)} ({layout} 排列, 间距 {spacing}px)")
        
    except Exception as e:
        print(f"合并图片失败: {e}")


def composite_id_card_on_background(id_card_path, output_path, background_dir="desktop_backgrounds"):
    """
    将身份证图片合成到随机选择的背景图上
    
    Args:
        id_card_path: 身份证图片路径
        output_path: 输出路径
        background_dir: 背景图片目录
    """
    try:
        # 1. 打开身份证图片
        id_card = Image.open(id_card_path)
        
        # 2. 随机选择背景图片
        background_files = []
        for root, dirs, files in os.walk(background_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    background_files.append(os.path.join(root, file))
        
        if not background_files:
            raise FileNotFoundError(f"在 {background_dir} 目录中未找到背景图片")
        
        # 随机选择一个背景文件
        selected_background = random.choice(background_files)
        background = Image.open(selected_background)
        
        # 3. 调整背景尺寸为 4000x3000
        background_resized = background.resize((4000, 3000), Image.Resampling.LANCZOS)
        
        # 4. 随机缩放身份证图片到背景图片尺寸的40%-90%
        # 随机选择缩放比例
        scale_factor = random.uniform(0.4, 0.9)
        
        # 计算身份证应该的尺寸（背景图片尺寸的随机比例）
        target_width = int(background_resized.width * scale_factor)
        target_height = int(target_width * id_card.height / id_card.width)  # 保持宽高比
        
        # 如果高度超过背景高度的随机比例，则按高度计算
        if target_height > background_resized.height * scale_factor:
            target_height = int(background_resized.height * scale_factor)
            target_width = int(target_height * id_card.width / id_card.height)  # 保持宽高比
        
        id_card_resized = id_card.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # 5. 随机选择放置位置（确保身份证完全在背景内）
        max_x = background_resized.width - id_card_resized.width
        max_y = background_resized.height - id_card_resized.height
        
        # 确保有足够的边距
        margin = 50
        max_x = max(margin, max_x - margin)
        max_y = max(margin, max_y - margin)
        
        if max_x > 0 and max_y > 0:
            x = random.randint(margin, max_x)
            y = random.randint(margin, max_y)
        else:
            # 如果背景太小，居中放置
            x = (background_resized.width - id_card_resized.width) // 2
            y = (background_resized.height - id_card_resized.height) // 2
        
        # 6. 合成图片
        # 创建背景的副本
        result = background_resized.copy()
        
        # 将身份证粘贴到背景上（使用透明通道）
        if id_card_resized.mode == 'RGBA':
            result.paste(id_card_resized, (x, y), id_card_resized)
        else:
            result.paste(id_card_resized, (x, y))
        
        # 7. 保存结果
        result.save(output_path, quality=95)
        
        print(f"已生成背景合成图片: {os.path.basename(output_path)}")
        print(f"  背景图片: {os.path.basename(selected_background)}")
        print(f"  缩放比例: {scale_factor:.2f} ({scale_factor*100:.1f}%)")
        print(f"  身份证尺寸: {target_width}x{target_height} (背景的{target_width/background_resized.width*100:.1f}%x{target_height/background_resized.height*100:.1f}%)")
        print(f"  放置位置: ({x}, {y})")
        
    except Exception as e:
        print(f"背景合成失败: {e}")


# 获取faces_tr目录下的男性和女性头像文件
male_avatar_files = []
female_avatar_files = []

male_dir = os.path.join(faces_tr_dir, "male")
female_dir = os.path.join(faces_tr_dir, "female")

# 获取男性头像
if os.path.exists(male_dir):
    for file in os.listdir(male_dir):
        if file.lower().endswith('.png'):  # 只处理PNG文件（保持透明通道）
            male_avatar_files.append(os.path.join(male_dir, file))
    print(f"找到 {len(male_avatar_files)} 个男性头像文件")
else:
    print(f"警告：{male_dir} 目录不存在")

# 获取女性头像
if os.path.exists(female_dir):
    for file in os.listdir(female_dir):
        if file.lower().endswith('.png'):  # 只处理PNG文件（保持透明通道）
            female_avatar_files.append(os.path.join(female_dir, file))
    print(f"找到 {len(female_avatar_files)} 个女性头像文件")
else:
    print(f"警告：{female_dir} 目录不存在")




# 导入真实信息生成函数
from chinese_id_gen_realistic import generate_realistic_info

# 生成男性身份证
for i, avatar_path in enumerate(male_avatar_files):
    # 生成男性身份证信息
    info = generate_realistic_info(gender='男')
    
    # 为每个姓名创建目录
    person_name = info['name']
    person_dir = os.path.join(output_base_dir, person_name)
    os.makedirs(person_dir, exist_ok=True)
    
    print(f"为男性身份证 {info['id_number']} ({person_name}) 分配头像: {os.path.basename(avatar_path)}")
    
    # 生成身份证正面和反面，保存到个人目录
    generate_id_card_back_image(info, person_dir)
    generate_id_card_front_image(info, person_dir, avatar_path)
    
    # 生成合并图片（水平排列）
    front_path = os.path.join(person_dir, f"{info['id_number']}_front.png")
    back_path = os.path.join(person_dir, f"{info['id_number']}_back.png")
    combined_horizontal_path = os.path.join(person_dir, f"{info['id_number']}_combined_horizontal.png")
    combine_id_card_images(front_path, back_path, combined_horizontal_path, 'horizontal')
    
    # 生成合并图片（垂直排列）
    combined_vertical_path = os.path.join(person_dir, f"{info['id_number']}_combined_vertical.png")
    combine_id_card_images(front_path, back_path, combined_vertical_path, 'vertical')
    
    # 生成背景合成图片（正面）
    front_bg_path = os.path.join(person_dir, f"{info['id_number']}_front_bg.jpg")
    composite_id_card_on_background(front_path, front_bg_path)
    
    # 生成背景合成图片（反面）
    back_bg_path = os.path.join(person_dir, f"{info['id_number']}_back_bg.jpg")
    composite_id_card_on_background(back_path, back_bg_path)
    
    # 生成背景合成图片（水平合并）
    combined_horizontal_bg_path = os.path.join(person_dir, f"{info['id_number']}_combined_horizontal_bg.jpg")
    composite_id_card_on_background(combined_horizontal_path, combined_horizontal_bg_path)
    
    # 生成背景合成图片（垂直合并）
    combined_vertical_bg_path = os.path.join(person_dir, f"{info['id_number']}_combined_vertical_bg.jpg")
    composite_id_card_on_background(combined_vertical_path, combined_vertical_bg_path)
    
    print(f"已生成男性 {person_name} 的身份证图片到目录: {person_dir}")

# 生成女性身份证
for i, avatar_path in enumerate(female_avatar_files):
    # 生成女性身份证信息
    info = generate_realistic_info(gender='女')
    
    # 为每个姓名创建目录
    person_name = info['name']
    person_dir = os.path.join(output_base_dir, person_name)
    os.makedirs(person_dir, exist_ok=True)
    
    print(f"为女性身份证 {info['id_number']} ({person_name}) 分配头像: {os.path.basename(avatar_path)}")
    
    # 生成身份证正面和反面，保存到个人目录
    generate_id_card_back_image(info, person_dir)
    generate_id_card_front_image(info, person_dir, avatar_path)
    
    # 生成合并图片（水平排列）
    front_path = os.path.join(person_dir, f"{info['id_number']}_front.png")
    back_path = os.path.join(person_dir, f"{info['id_number']}_back.png")
    combined_horizontal_path = os.path.join(person_dir, f"{info['id_number']}_combined_horizontal.png")
    combine_id_card_images(front_path, back_path, combined_horizontal_path, 'horizontal')
    
    # 生成合并图片（垂直排列）
    combined_vertical_path = os.path.join(person_dir, f"{info['id_number']}_combined_vertical.png")
    combine_id_card_images(front_path, back_path, combined_vertical_path, 'vertical')
    
    # 生成背景合成图片（正面）
    front_bg_path = os.path.join(person_dir, f"{info['id_number']}_front_bg.jpg")
    composite_id_card_on_background(front_path, front_bg_path)
    
    # 生成背景合成图片（反面）
    back_bg_path = os.path.join(person_dir, f"{info['id_number']}_back_bg.jpg")
    composite_id_card_on_background(back_path, back_bg_path)
    
    # 生成背景合成图片（水平合并）
    combined_horizontal_bg_path = os.path.join(person_dir, f"{info['id_number']}_combined_horizontal_bg.jpg")
    composite_id_card_on_background(combined_horizontal_path, combined_horizontal_bg_path)
    
    # 生成背景合成图片（垂直合并）
    combined_vertical_bg_path = os.path.join(person_dir, f"{info['id_number']}_combined_vertical_bg.jpg")
    composite_id_card_on_background(combined_vertical_path, combined_vertical_bg_path)
    
    print(f"已生成女性 {person_name} 的身份证图片到目录: {person_dir}")

print(f"\n总计生成身份证数量:")
print(f"男性身份证: {len(male_avatar_files)} 张")
print(f"女性身份证: {len(female_avatar_files)} 张")
print(f"总计: {len(male_avatar_files) + len(female_avatar_files)} 张")
