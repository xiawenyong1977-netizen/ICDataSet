#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
训练模式脚本
专门用于生成适合训练的微信截图，头像被弱化以减少对模型的干扰
"""

from genwechat import WeChatScreenshotGenerator
import os

def generate_training_data():
    """生成训练数据"""
    
    print("开始生成训练数据...")
    
    # 创建输出目录
    os.makedirs("output", exist_ok=True)
    
    # 训练模式配置
    training_configs = [
        {
            "name": "weak_avatar",
            "description": "弱化头像（推荐用于训练）",
            "avatar_style": "simple",
            "weaken": True,
            "level": 0.7,
            "noise": True,
            "blur": True
        },
        {
            "name": "very_weak_avatar", 
            "description": "极度弱化头像",
            "avatar_style": "simple",
            "weaken": True,
            "level": 0.9,
            "noise": True,
            "blur": True
        },
        {
            "name": "minimal_avatar",
            "description": "最小化头像",
            "avatar_style": "simple",
            "weaken": False,
            "level": 0.0,
            "noise": False,
            "blur": False
        }
    ]
    
    for config in training_configs:
        print(f"\n正在生成 {config['description']}...")
        
        # 创建生成器实例
        generator = WeChatScreenshotGenerator()
        
        # 设置头像样式
        generator.set_avatar_style(config["avatar_style"])
        
        # 设置头像弱化参数
        generator.set_avatar_weaken(
            weaken=config["weaken"],
            level=config["level"],
            noise=config["noise"],
            blur=config["blur"]
        )
        
        # 生成聊天截图
        print("正在生成聊天内容...")
        screenshot = generator.generate(num_messages=15)
        
        # 保存截图
        filename = f"training_{config['name']}.png"
        generator.save(filename)
        
        print(f"{config['description']}已保存为: {filename}")
    
    print("\n所有训练数据生成完成！")
    print("建议使用 'weak_avatar' 或 'very_weak_avatar' 进行模型训练")

def generate_comparison():
    """生成对比图，展示不同弱化程度的效果"""
    
    print("\n正在生成头像弱化效果对比图...")
    
    # 创建生成器实例
    generator = WeChatScreenshotGenerator()
    generator.set_avatar_style("geometric")
    
    # 生成不同弱化程度的头像
    weaken_levels = [0.0, 0.3, 0.6, 0.9]
    
    for level in weaken_levels:
        print(f"生成弱化程度 {level:.1f} 的头像...")
        
        # 设置弱化参数
        generator.set_avatar_weaken(
            weaken=True,
            level=level,
            noise=True,
            blur=True
        )
        
        # 生成截图
        screenshot = generator.generate(num_messages=8)
        
        # 保存
        filename = f"comparison_weaken_{level:.1f}.png"
        generator.save(filename)
    
    print("对比图生成完成！")

if __name__ == "__main__":
    try:
        generate_training_data()
        generate_comparison()
        print("\n🎯 训练模式完成！")
        print("这些图片适合用于训练模型识别微信聊天内容，而不是头像特征。")
    except Exception as e:
        print(f"生成过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
