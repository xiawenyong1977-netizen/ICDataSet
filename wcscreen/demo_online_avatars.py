#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
在线头像演示脚本
展示使用在线API生成的头像效果
"""

from genwechat import WeChatScreenshotGenerator
import os

def demo_online_avatars():
    """演示在线头像效果"""
    
    print("开始演示在线头像功能...")
    
    # 创建生成器实例
    generator = WeChatScreenshotGenerator()
    generator.set_avatar_style("online")
    
    # 测试用的名字（使用英文名以获得更好的在线头像效果）
    test_names = [
        "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank",
        "Grace", "Henry", "Ivy", "Jack", "Kate", "Leo"
    ]
    
    print(f"将生成 {len(test_names)} 个在线头像...")
    
    # 生成聊天截图
    print("正在生成聊天内容...")
    screenshot = generator.generate(num_messages=len(test_names))
    
    # 保存截图
    print("正在保存截图...")
    generator.save("wechat_online_avatars.png")
    
    print("在线头像演示完成！")
    print("文件保存为: output/wechat_online_avatars.png")

if __name__ == "__main__":
    demo_online_avatars()
