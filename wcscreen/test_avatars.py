#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
头像效果测试脚本
专门用于测试和比较不同的头像生成效果
"""

from genwechat import WeChatScreenshotGenerator
import os
from PIL import Image, ImageDraw

def test_avatar_styles():
    """测试不同的头像样式"""
    
    # 创建输出目录
    os.makedirs("output", exist_ok=True)
    
    # 测试用的名字
    test_names = ["小明", "小红", "小张", "小李", "小王", "小赵"]
    
    # 头像样式列表
    styles = [
        ("geometric", "几何图案头像"),
        ("simple", "简单纯色头像"),
        ("colorful", "彩色渐变头像"),
        ("realistic", "逼真头像")
    ]
    
    print("开始测试头像样式...")
    
    for style, description in styles:
        print(f"\n正在测试 {description}...")
        
        # 创建生成器实例
        generator = WeChatScreenshotGenerator()
        generator.set_avatar_style(style)
        
        # 生成一个简单的测试图像，只显示头像
        test_image = Image.new("RGB", (400, 300), "#F0F0F0")
        test_draw = ImageDraw.Draw(test_image)
        
        # 绘制标题
        test_draw.text((10, 10), f"{description} 测试", fill="black", font=generator.font)
        
        # 绘制多个头像进行对比
        for i, name in enumerate(test_names):
            x = 20 + (i % 3) * 120
            y = 60 + (i // 3) * 120
            
            # 绘制头像
            generator.draw_avatar(x, y, True)
            
            # 绘制名字
            test_draw.text((x, y + generator.avatar_size + 5), name, 
                          fill="black", font=generator.name_font)
        
        # 保存测试图像
        filename = f"avatar_test_{style}.png"
        test_image.save(os.path.join("output", filename))
        print(f"{description}测试完成，保存为: {filename}")
    
    print("\n所有头像样式测试完成！")
    print("请查看 output 目录中的测试图片。")

def test_online_avatars():
    """测试在线头像功能"""
    print("\n正在测试在线头像功能...")
    
    # 创建生成器实例
    generator = WeChatScreenshotGenerator()
    generator.set_avatar_style("online")
    
    # 测试在线头像
    test_names = ["Alice", "Bob", "Charlie", "Diana"]
    
    for name in test_names:
        print(f"测试名字: {name}")
        avatar = generator.get_online_avatar(name)
        if avatar:
            print(f"  ✓ 成功获取在线头像")
        else:
            print(f"  ✗ 获取在线头像失败")
    
    print("在线头像测试完成！")

if __name__ == "__main__":
    try:
        test_avatar_styles()
        test_online_avatars()
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
