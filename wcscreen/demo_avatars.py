#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
微信头像样式演示脚本
展示不同的头像生成效果
"""

from genwechat import WeChatScreenshotGenerator
import os

def demo_avatar_styles():
    """演示不同的头像样式"""
    
    # 创建输出目录
    os.makedirs("output", exist_ok=True)
    
    # 头像样式列表
    styles = [
        ("geometric", "几何图案头像"),
        ("simple", "简单纯色头像"),
        ("colorful", "彩色渐变头像"),
        ("realistic", "逼真头像"),
        ("online", "在线头像")
    ]
    
    for style, description in styles:
        print(f"\n正在生成 {description}...")
        
        # 创建生成器实例
        generator = WeChatScreenshotGenerator()
        
        # 设置头像样式
        generator.set_avatar_style(style)
        
        # 生成聊天截图（减少消息数量以便查看头像效果）
        screenshot = generator.generate(num_messages=6)
        
        # 保存截图
        filename = f"wechat_{style}_demo.png"
        generator.save(filename)
        
        print(f"{description}已保存为: {filename}")
    
    print("\n所有头像样式演示完成！")
    print("请查看 output 目录中的图片文件。")

if __name__ == "__main__":
    demo_avatar_styles()
