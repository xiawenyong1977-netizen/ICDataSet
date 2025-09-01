import random
import textwrap
import math
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import requests
from io import BytesIO

class WeChatScreenshotGenerator:
    def __init__(self, width=750, height=1334):
        # 微信风格颜色
        self.colors = {
            "background": "#EDEDED",
            "time_bg": "#D5D5D5",
            "friend_bubble": "#FFFFFF",
            "my_bubble": "#95EC69",
            "friend_text": "#000000",
            "my_text": "#000000",
            "name_text": "#8B8989"
        }
        
        # 创建画布
        self.width = width
        self.height = height
        self.image = Image.new("RGB", (width, height), self.colors["background"])
        self.draw = ImageDraw.Draw(self.image)
        # 尝试多个字体路径
        font_paths = [
            # r"C:\Windows\Fonts\msyh.ttf",  # 微软雅黑 - 注释掉，避免权限问题
            r"C:\Windows\Fonts\simhei.ttf",  # 黑体
            r"C:\Windows\Fonts\simsun.ttc",  # 宋体
            r"C:\Windows\Fonts\arial.ttf"   # Arial
        ]
        
        font_loaded = False
        for font_path in font_paths:
            try:
                self.font = ImageFont.truetype(font_path, 18)
                self.name_font = ImageFont.truetype(font_path, 16)
                self.time_font = ImageFont.truetype(font_path, 14)
                print(f"成功加载字体: {font_path}")
                font_loaded = True
                break
            except Exception as e:
                print(f"尝试加载字体 {font_path} 失败: {e}")
                continue
        
        if not font_loaded:
            print("所有字体加载失败，使用默认字体")
            self.font = ImageFont.load_default()
            self.name_font = ImageFont.load_default()
            self.time_font = ImageFont.load_default()
        
        # 聊天内容库
        self.messages = [
            "你好呀！",
            "在干嘛呢？",
            "吃饭了吗？",
            "今天天气真不错",
            "周末有什么计划？",
            "最近看了一部好电影",
            "推荐一家好吃的餐厅",
            "记得明天开会",
            "代码写完了吗？",
            "什么时候有空聚聚？",
            "这个项目进度如何？",
            "帮我看看这个怎么样",
            "收到，谢谢！",
            "OK，没问题",
            "好的，明白了",
            "哈哈，太好笑了",
            "真的吗？太惊讶了",
            "恭喜恭喜！",
            "生日快乐！",
            "新年快乐！"
        ]
        
        # 用户名
        self.friend_names = ["小明", "小红", "小张", "小李", "小王", "小赵"]
        self.my_name = "我"
        
        # 头像设置
        self.use_online_avatars = False  # 是否使用在线头像
        self.avatar_cache = {}  # 头像缓存
        self.avatar_style = "geometric"  # 头像样式: geometric, simple, colorful, realistic
        
        # 头像弱化设置（用于训练）
        self.avatar_weaken = False  # 是否弱化头像
        self.avatar_weaken_level = 0.5  # 弱化程度 (0.0-1.0)
        self.avatar_noise = False  # 是否添加噪声
        self.avatar_blur = False  # 是否模糊化
        
        # 训练模式设置
        self.training_mode = False  # 是否启用训练模式
        self.content_weaken = False  # 是否弱化聊天内容
        self.content_weaken_level = 0.5  # 内容弱化程度
        
        # 位置参数
        self.margin = 20
        self.avatar_size = 40
        self.bubble_padding = 12
        self.current_y = 80  # 从顶部开始的位置
    
    def generate_avatar_color(self, name):
        """根据名字生成稳定的颜色"""
        # 使用名字的哈希值生成颜色，确保同一名字总是相同颜色
        hash_value = hash(name) % 0xFFFFFF
        r = (hash_value >> 16) & 0xFF
        g = (hash_value >> 8) & 0xFF
        b = hash_value & 0xFF
        
        # 确保颜色不会太暗
        if r + g + b < 200:
            r = min(255, r + 100)
            g = min(255, g + 100)
            b = min(255, b + 100)
        
        return (r, g, b)
    
    def draw_geometric_avatar(self, avatar_draw, name, size):
        """绘制几何图案头像"""
        # 根据名字选择不同的几何图案
        pattern_type = hash(name) % 4
        
        if pattern_type == 0:
            # 圆形图案
            center = size // 2
            radius = size // 3
            avatar_draw.ellipse(
                (center - radius, center - radius, center + radius, center + radius),
                fill="white"
            )
        elif pattern_type == 1:
            # 三角形图案
            points = [
                (size // 2, size // 4),
                (size // 4, 3 * size // 4),
                (3 * size // 4, 3 * size // 4)
            ]
            avatar_draw.polygon(points, fill="white")
        elif pattern_type == 2:
            # 矩形图案
            margin = size // 4
            avatar_draw.rectangle(
                (margin, margin, size - margin, size - margin),
                fill="white"
            )
        else:
            # 菱形图案
            center = size // 2
            points = [
                (center, size // 4),
                (size // 4, center),
                (center, 3 * size // 4),
                (3 * size // 4, center)
            ]
            avatar_draw.polygon(points, fill=255)
    
    def draw_realistic_avatar(self, avatar_draw, name, size):
        """绘制更逼真的头像"""
        # 根据名字生成更复杂的图案
        seed = hash(name)
        random.seed(seed)
        
        # 生成多层图案
        layers = seed % 3 + 2  # 2-4层
        
        for layer in range(layers):
            # 每层使用不同的颜色和透明度
            layer_color = (
                (seed >> (layer * 8)) % 200 + 55,
                (seed >> (layer * 8 + 4)) % 200 + 55,
                (seed >> (layer * 8 + 8)) % 200 + 55
            )
            
            # 随机选择图案类型
            pattern = (seed >> (layer * 4)) % 6
            
            if pattern == 0:
                # 同心圆
                radius = size // (3 + layer * 2)
                center = size // 2
                avatar_draw.ellipse(
                    (center - radius, center - radius, center + radius, center + radius),
                    fill=layer_color
                )
            elif pattern == 1:
                # 随机多边形
                points = []
                num_points = 3 + (seed % 4)
                for i in range(num_points):
                    angle = (i * 360 / num_points + seed) % 360
                    radius = size // (4 + layer)
                    x = size // 2 + int(radius * math.cos(math.radians(angle)))
                    y = size // 2 + int(radius * math.sin(math.radians(angle)))
                    points.append((x, y))
                avatar_draw.polygon(points, fill=layer_color)
            elif pattern == 2:
                # 随机线条
                for _ in range(3):
                    x1 = (seed % size)
                    y1 = (seed >> 8) % size
                    x2 = (seed >> 16) % size
                    y2 = (seed >> 24) % size
                    avatar_draw.line([(x1, y1), (x2, y2)], fill=layer_color, width=2)
            elif pattern == 3:
                # 随机矩形
                margin = size // (6 + layer)
                avatar_draw.rectangle(
                    (margin, margin, size - margin, size - margin),
                    fill=layer_color
                )
            elif pattern == 4:
                # 随机椭圆
                center_x = size // 2 + (seed % (size // 4)) - size // 8
                center_y = size // 2 + ((seed >> 8) % (size // 4)) - size // 8
                radius_x = size // (6 + layer)
                radius_y = size // (8 + layer)
                avatar_draw.ellipse(
                    (center_x - radius_x, center_y - radius_y, center_x + radius_x, center_y + radius_y),
                    fill=layer_color
                )
            else:
                # 随机点
                for _ in range(5):
                    x = (seed % size)
                    y = ((seed >> 8) % size)
                    avatar_draw.ellipse((x-2, y-2, x+2, y+2), fill=layer_color)
                    seed = seed >> 16
        
        random.seed()  # 重置随机种子
    
    def set_avatar_weaken(self, weaken=True, level=0.5, noise=False, blur=False):
        """设置头像弱化参数（用于训练时减少头像对模型的干扰）
        
        Args:
            weaken (bool): 是否启用头像弱化
            level (float): 弱化程度 (0.0-1.0)，0.0为不弱化，1.0为完全弱化
            noise (bool): 是否添加随机噪声
            blur (bool): 是否模糊化头像
        """
        self.avatar_weaken = weaken
        self.avatar_weaken_level = max(0.0, min(1.0, level))
        self.avatar_noise = noise
        self.avatar_blur = blur
    
    def weaken_avatar(self, avatar):
        """弱化头像效果"""
        if not self.avatar_weaken:
            return avatar
        
        # 创建头像副本
        weakened_avatar = avatar.copy()
        
        # 降低对比度和亮度
        if self.avatar_weaken_level > 0:
            # 转换为numpy数组进行处理
            import numpy as np
            img_array = np.array(weakened_avatar)
            
            # 降低对比度
            contrast_factor = 1.0 - self.avatar_weaken_level * 0.8
            img_array = (img_array - 128) * contrast_factor + 128
            
            # 降低亮度
            brightness_factor = 1.0 - self.avatar_weaken_level * 0.6
            img_array = img_array * brightness_factor
            
            # 确保值在有效范围内
            img_array = np.clip(img_array, 0, 255).astype(np.uint8)
            
            # 转换回PIL图像
            weakened_avatar = Image.fromarray(img_array)
        
        # 添加噪声
        if self.avatar_noise:
            import numpy as np
            img_array = np.array(weakened_avatar)
            noise = np.random.normal(0, 25 * self.avatar_weaken_level, img_array.shape)
            img_array = img_array + noise
            img_array = np.clip(img_array, 0, 255).astype(np.uint8)
            weakened_avatar = Image.fromarray(img_array)
        
        # 模糊化
        if self.avatar_blur:
            blur_radius = int(3 * self.avatar_weaken_level)
            if blur_radius > 0:
                weakened_avatar = weakened_avatar.filter(ImageFilter.GaussianBlur(blur_radius))
        
        return weakened_avatar
    
    def set_training_mode(self, enabled=True, avatar_weaken=True, content_weaken=True, 
                         avatar_level=0.7, content_level=0.6):
        """设置训练模式（专门用于训练模型识别微信截图）
        
        Args:
            enabled (bool): 是否启用训练模式
            avatar_weaken (bool): 是否弱化头像
            content_weaken (bool): 是否弱化聊天内容
            avatar_level (float): 头像弱化程度 (0.0-1.0)
            content_level (float): 内容弱化程度 (0.0-1.0)
        """
        self.training_mode = enabled
        
        if enabled:
            # 自动设置头像弱化
            if avatar_weaken:
                self.set_avatar_weaken(
                    weaken=True,
                    level=avatar_level,
                    noise=True,
                    blur=True
                )
            
            # 设置内容弱化
            self.content_weaken = content_weaken
            self.content_weaken_level = max(0.0, min(1.0, content_level))
            
            # 自动使用最简单的头像样式
            self.set_avatar_style("simple")
            
            print(f"训练模式已启用 - 头像弱化: {avatar_level:.1f}, 内容弱化: {content_level:.1f}")
    
    def weaken_content(self, text):
        """弱化聊天内容（用于训练时减少对具体内容的依赖）"""
        if not self.content_weaken or not self.training_mode:
            return text
        
        # 根据弱化程度决定是否替换内容
        if random.random() < self.content_weaken_level:
            # 使用占位符替换具体内容
            placeholders = [
                "消息内容", "聊天记录", "对话内容", "文本消息",
                "用户输入", "聊天信息", "对话文本", "消息文本"
            ]
            return random.choice(placeholders)
        
        return text
    
    def get_online_avatar(self, name):
        """尝试从在线API获取头像"""
        if not self.use_online_avatars:
            return None
            
        # 检查缓存
        if name in self.avatar_cache:
            return self.avatar_cache[name]
        
        try:
            # 使用多个头像生成API
            apis = [
                # DiceBear - 卡通风格头像
                f"https://api.dicebear.com/7.x/avataaars/png?seed={name}&size={self.avatar_size}&backgroundColor=b6e3f4,c0aede,d1d4f9,ffd5dc,ffdfbf",
                # DiceBear - 像素风格头像
                f"https://api.dicebear.com/7.x/pixel-art/png?seed={name}&size={self.avatar_size}&backgroundColor=b6e3f4,c0aede,d1d4f9,ffd5dc,ffdfbf",
                # DiceBear - 机器人风格头像
                f"https://api.dicebear.com/7.x/bottts/png?seed={name}&size={self.avatar_size}&backgroundColor=b6e3f4,c0aede,d1d4f9,ffd5dc,ffdfbf",
                # DiceBear - 人类风格头像
                f"https://api.dicebear.com/7.x/human/png?seed={name}&size={self.avatar_size}&backgroundColor=b6e3f4,c0aede,d1d4f9,ffd5dc,ffdfbf"
            ]
            
            for api_url in apis:
                try:
                    response = requests.get(api_url, timeout=10)
                    if response.status_code == 200:
                        # 将PNG数据转换为PIL图像
                        img_data = BytesIO(response.content)
                        avatar_img = Image.open(img_data)
                        
                        # 调整大小
                        avatar_img = avatar_img.resize((self.avatar_size, self.avatar_size), Image.Resampling.LANCZOS)
                        
                        # 缓存图像对象
                        self.avatar_cache[name] = avatar_img
                        return avatar_img
                except Exception as e:
                    print(f"API {api_url} 失败: {e}")
                    continue
                    
        except Exception as e:
            print(f"获取在线头像失败: {e}")
        
        return None
    
    def set_avatar_style(self, style="geometric"):
        """设置头像样式
        
        Args:
            style (str): 头像样式
                - "geometric": 几何图案头像（默认）
                - "simple": 简单纯色头像
                - "colorful": 彩色渐变头像
                - "online": 在线头像（需要网络）
        """
        self.avatar_style = style
        if style == "online":
            self.use_online_avatars = True
        else:
            self.use_online_avatars = False
    
    def draw_avatar(self, x, y, is_friend=True):
        """绘制圆形头像"""
        # 获取名字
        name = random.choice(self.friend_names) if is_friend else self.my_name
        
        # 尝试获取在线头像
        online_avatar = self.get_online_avatar(name)
        
        # 如果成功获取在线头像，直接使用
        if online_avatar and isinstance(online_avatar, Image.Image):
            # 应用弱化效果
            online_avatar = self.weaken_avatar(online_avatar)
            
            # 创建圆形掩模
            mask = Image.new("L", (self.avatar_size, self.avatar_size), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0, self.avatar_size, self.avatar_size), fill=255)
            
            # 应用圆形掩模
            online_avatar.putalpha(mask)
            
            # 将头像粘贴到主图像上
            self.image.paste(online_avatar, (x, y), online_avatar)
            return name
        
        # 生成基于名字的颜色
        base_color = self.generate_avatar_color(name)
        
        # 根据样式绘制头像
        if self.avatar_style == "simple":
            # 简单纯色头像
            avatar = Image.new("RGB", (self.avatar_size, self.avatar_size), base_color)
            avatar_draw = ImageDraw.Draw(avatar)
        elif self.avatar_style == "colorful":
            # 彩色渐变头像
            avatar = Image.new("RGB", (self.avatar_size, self.avatar_size), base_color)
            avatar_draw = ImageDraw.Draw(avatar)
            
            # 添加彩虹渐变效果
            for i in range(self.avatar_size):
                hue = (i / self.avatar_size) * 360
                # 简单的颜色变化
                r = int(255 * (1 + math.sin(hue * 0.0174533)) / 2)
                g = int(255 * (1 + math.sin((hue + 120) * 0.0174533)) / 2)
                b = int(255 * (1 + math.sin((hue + 240) * 0.0174533)) / 2)
                avatar_draw.line([(0, i), (self.avatar_size, i)], fill=(r, g, b))
        elif self.avatar_style == "realistic":
            # 逼真头像样式
            avatar = Image.new("RGB", (self.avatar_size, self.avatar_size), base_color)
            avatar_draw = ImageDraw.Draw(avatar)
            
            # 添加渐变背景
            for i in range(self.avatar_size):
                alpha = int(255 * (1 - i / self.avatar_size))
                color = tuple(max(0, min(255, c + alpha // 15)) for c in base_color)
                avatar_draw.line([(0, i), (self.avatar_size, i)], fill=color)
            
            # 绘制逼真图案
            self.draw_realistic_avatar(avatar_draw, name, self.avatar_size)
        else:
            # 几何图案头像（默认）
            avatar = Image.new("RGB", (self.avatar_size, self.avatar_size), base_color)
            avatar_draw = ImageDraw.Draw(avatar)
            
            # 添加渐变效果
            for i in range(self.avatar_size):
                alpha = int(255 * (1 - i / self.avatar_size))
                color = tuple(max(0, min(255, c + alpha // 10)) for c in base_color)
                avatar_draw.line([(0, i), (self.avatar_size, i)], fill=color)
            
            # 绘制几何图案
            self.draw_geometric_avatar(avatar_draw, name, self.avatar_size)
        
        # 在头像上写一个字
        text = name[0]  # 取第一个字
        bbox = avatar_draw.textbbox((0, 0), text, font=self.font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 添加文字阴影效果
        shadow_offset = 1
        avatar_draw.text(
            ((self.avatar_size - text_width) // 2 + shadow_offset, 
             (self.avatar_size - text_height) // 2 + shadow_offset),
            text, fill=(50, 50, 50), font=self.font
        )
        
        # 绘制主文字
        avatar_draw.text(
            ((self.avatar_size - text_width) // 2, 
             (self.avatar_size - text_height) // 2),
            text, fill="white", font=self.font
        )
        
        # 创建圆形掩模
        mask = Image.new("L", (self.avatar_size, self.avatar_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, self.avatar_size, self.avatar_size), fill=255)
        
        # 应用圆形掩模
        avatar.putalpha(mask)
        
        # 应用弱化效果
        avatar = self.weaken_avatar(avatar)
        
        # 将头像粘贴到主图像上
        self.image.paste(avatar, (x, y), avatar)
        
        return name
    
    def draw_time(self):
        """绘制时间戳"""
        # 生成随机时间（最近24小时内）
        time_offset = random.randint(0, 86400)
        time = datetime.now() - timedelta(seconds=time_offset)
        time_str = time.strftime("%H:%M")
        
        # 绘制时间背景
        time_bg_width = 60
        time_bg_height = 25
        time_bg_x = (self.width - time_bg_width) // 2
        time_bg_y = self.current_y
        
        self.draw.rounded_rectangle(
            (time_bg_x, time_bg_y, time_bg_x + time_bg_width, time_bg_y + time_bg_height),
            radius=10, fill=self.colors["time_bg"]
        )
        
        # 绘制时间文本
        bbox = self.draw.textbbox((0, 0), time_str, font=self.time_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        self.draw.text(
            (time_bg_x + (time_bg_width - text_width) // 2, 
             time_bg_y + (time_bg_height - text_height) // 2),
            time_str, fill="black", font=self.time_font
        )
        
        self.current_y += time_bg_height + 15
    
    def draw_message_bubble(self, message, is_friend=True):
        """绘制消息气泡"""
        # 应用内容弱化（训练模式）
        processed_message = self.weaken_content(message)
        
        # 设置气泡参数
        bubble_color = self.colors["friend_bubble"] if is_friend else self.colors["my_bubble"]
        text_color = self.colors["friend_text"] if is_friend else self.colors["my_text"]
        
        # 计算文本尺寸并换行
        max_width = self.width * 0.6
        wrapped_text = textwrap.fill(processed_message, width=20)
        lines = wrapped_text.split('\n')
        
        # 计算气泡尺寸
        line_height = 20
        bubble_width = min(max(self.draw.textbbox((0, 0), line, font=self.font)[2] for line in lines) + 
                          self.bubble_padding * 2, max_width)
        bubble_height = len(lines) * line_height + self.bubble_padding * 2
        
        # 确定气泡位置
        if is_friend:
            avatar_x = self.margin
            bubble_x = avatar_x + self.avatar_size + 10
        else:
            avatar_x = self.width - self.margin - self.avatar_size
            bubble_x = avatar_x - 10 - bubble_width
        
        avatar_y = self.current_y
        bubble_y = self.current_y
        
        # 绘制头像和名称
        name = self.draw_avatar(avatar_x, avatar_y, is_friend)
        
        if is_friend:
            # 绘制朋友名称
            self.draw.text(
                (bubble_x, bubble_y - 20), name, 
                fill=self.colors["name_text"], font=self.name_font
            )
        
        # 绘制气泡
        self.draw.rounded_rectangle(
            (bubble_x, bubble_y, bubble_x + bubble_width, bubble_y + bubble_height),
            radius=10, fill=bubble_color
        )
        
        # 绘制文本
        for i, line in enumerate(lines):
            self.draw.text(
                (bubble_x + self.bubble_padding, bubble_y + self.bubble_padding + i * line_height),
                line, fill=text_color, font=self.font
            )
        
        # 更新当前位置
        self.current_y += max(bubble_height, self.avatar_size) + 20
    
    def draw_status_bar(self):
        """绘制手机状态栏"""
        # 绘制背景
        self.draw.rectangle((0, 0, self.width, 40), fill="#000000")
        
        # 绘制时间（假设当前时间）
        current_time = datetime.now().strftime("%H:%M")
        bbox = self.draw.textbbox((0, 0), current_time, font=self.time_font)
        text_width = bbox[2] - bbox[0]
        self.draw.text(
            ((self.width - text_width) // 2, 10), 
            current_time, fill="white", font=self.time_font
        )
        
        # 绘制电池图标等（简化处理）
        self.draw.rectangle((self.width - 30, 15, self.width - 15, 25), outline="white")
        self.draw.rectangle((self.width - 28, 17, self.width - 22, 23), fill="white")
    
    def draw_navigation_bar(self):
        """绘制底部导航栏"""
        # 绘制背景
        self.draw.rectangle((0, self.height - 50, self.width, self.height), fill="#F7F7F7")
        
        # 绘制分割线
        self.draw.line((0, self.height - 50, self.width, self.height - 50), fill="#DDDDDD")
        
        # 绘制导航项（简化处理）
        nav_items = ["微信", "通讯录", "发现", "我"]
        item_width = self.width // len(nav_items)
        
        for i, item in enumerate(nav_items):
            x = i * item_width + item_width // 2
            self.draw.text(
                (x - 10, self.height - 35), item, 
                fill="#000000" if i == 0 else "#888888", font=self.name_font
            )
    
    def generate(self, num_messages=10):
        """生成聊天截图"""
        # 绘制状态栏和导航栏
        self.draw_status_bar()
        self.draw_navigation_bar()
        
        # 绘制初始时间
        self.draw_time()
        
        # 生成多条消息
        for _ in range(num_messages):
            # 随机决定是朋友发送还是自己发送
            is_friend = random.choice([True, False])
            
            # 随机选择消息内容
            message = random.choice(self.messages)
            
            # 绘制消息气泡
            self.draw_message_bubble(message, is_friend)
            
            # 随机决定是否添加时间戳
            if random.random() < 0.2:  # 20%的概率添加时间戳
                self.draw_time()
        
        return self.image
    
    def save(self, filename="wechat_screenshot.png"):
        """保存生成的图片"""
        # 创建输出目录（如果不存在）
        os.makedirs("output", exist_ok=True)
        
        # 保存图片
        path = os.path.join("output", filename)
        self.image.save(path)
        print(f"截图已保存至: {path}")
        
        return path

# 使用示例
if __name__ == "__main__":
    print("开始生成微信聊天截图...")
    
    # 创建生成器实例
    generator = WeChatScreenshotGenerator()
    
    # 设置头像样式（可选）
    # 可选值: "geometric"（几何图案，默认）, "simple"（简单纯色）, "colorful"（彩色渐变）, "online"（在线头像）
    avatar_style = "geometric"  # 可以修改这里来改变头像样式
    generator.set_avatar_style(avatar_style)
    print(f"使用头像样式: {avatar_style}")
    
    # 生成聊天截图（可以指定消息数量）
    print("正在生成聊天内容...")
    screenshot = generator.generate(num_messages=12)
    
    # 保存截图
    print("正在保存截图...")
    generator.save("wechat_conversation.png")
    
    print("微信聊天截图生成完成！")
    
    # 如果需要显示图片（可选）
    # screenshot.show()