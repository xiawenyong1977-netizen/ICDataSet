#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
智能训练模式脚本
专门用于训练模型识别"这是微信截图"，而不是具体的聊天内容
"""

from genwechat import WeChatScreenshotGenerator
import os

def generate_smart_training_data():
    """生成智能训练数据"""
    
    print("🎯 开始生成智能训练数据...")
    print("目标：训练模型识别微信截图，而不是具体内容")
    
    # 创建输出目录
    os.makedirs("output", exist_ok=True)
    
    # 智能训练配置
    training_configs = [
        {
            "name": "wechat_style_focus",
            "description": "专注微信样式识别（推荐）",
            "avatar_weaken": True,
            "content_weaken": True,
            "avatar_level": 0.8,
            "content_level": 0.7
        },
        {
            "name": "layout_focus",
            "description": "专注布局结构识别",
            "avatar_weaken": True,
            "content_weaken": True,
            "avatar_level": 0.9,
            "content_level": 0.9
        },
        {
            "name": "balanced_training",
            "description": "平衡训练模式",
            "avatar_weaken": True,
            "content_weaken": True,
            "avatar_level": 0.6,
            "content_level": 0.5
        }
    ]
    
    for config in training_configs:
        print(f"\n正在生成 {config['description']}...")
        
        # 创建生成器实例
        generator = WeChatScreenshotGenerator()
        
        # 启用智能训练模式
        generator.set_training_mode(
            enabled=True,
            avatar_weaken=config["avatar_weaken"],
            content_weaken=config["content_weaken"],
            avatar_level=config["avatar_level"],
            content_level=config["content_level"]
        )
        
        # 生成聊天截图
        print("正在生成微信样式截图...")
        screenshot = generator.generate(num_messages=20)
        
        # 保存截图
        filename = f"smart_training_{config['name']}.png"
        generator.save(filename)
        
        print(f"{config['description']}已保存为: {filename}")
    
    print("\n✅ 所有智能训练数据生成完成！")
    print("这些图片专注于微信的视觉特征，适合训练模型识别微信截图")

def generate_style_comparison():
    """生成样式对比图，展示不同弱化策略的效果"""
    
    print("\n🔄 正在生成样式对比图...")
    
    # 对比配置
    comparison_configs = [
        {
            "name": "normal",
            "description": "正常模式（不弱化）",
            "training_mode": False
        },
        {
            "name": "avatar_only",
            "description": "仅弱化头像",
            "training_mode": True,
            "avatar_weaken": True,
            "content_weaken": False,
            "avatar_level": 0.7,
            "content_level": 0.0
        },
        {
            "name": "content_only",
            "description": "仅弱化内容",
            "training_mode": True,
            "avatar_weaken": False,
            "content_weaken": True,
            "avatar_level": 0.0,
            "content_level": 0.7
        },
        {
            "name": "both_weak",
            "description": "头像和内容都弱化",
            "training_mode": True,
            "avatar_weaken": True,
            "content_weaken": True,
            "avatar_level": 0.7,
            "content_level": 0.7
        }
    ]
    
    for config in comparison_configs:
        print(f"生成 {config['description']}...")
        
        generator = WeChatScreenshotGenerator()
        
        if config["training_mode"]:
            generator.set_training_mode(
                enabled=True,
                avatar_weaken=config["avatar_weaken"],
                content_weaken=config["content_weaken"],
                avatar_level=config["avatar_level"],
                content_level=config["content_level"]
            )
        
        # 生成截图
        screenshot = generator.generate(num_messages=12)
        
        # 保存
        filename = f"style_comparison_{config['name']}.png"
        generator.save(filename)
    
    print("样式对比图生成完成！")

def generate_wechat_style_variations():
    """生成微信样式的变体，强化微信特征"""
    
    print("\n🎨 正在生成微信样式变体...")
    
    # 微信样式变体
    style_variations = [
        {
            "name": "classic_wechat",
            "description": "经典微信样式",
            "colors": {
                "background": "#EDEDED",
                "friend_bubble": "#FFFFFF",
                "my_bubble": "#95EC69"
            }
        },
        {
            "name": "dark_theme",
            "description": "深色主题",
            "colors": {
                "background": "#1A1A1A",
                "friend_bubble": "#2D2D2D",
                "my_bubble": "#4CAF50"
            }
        },
        {
            "name": "light_theme",
            "description": "浅色主题",
            "colors": {
                "background": "#F8F8F8",
                "friend_bubble": "#FFFFFF",
                "my_bubble": "#E3F2FD"
            }
        }
    ]
    
    for style in style_variations:
        print(f"生成 {style['description']}...")
        
        generator = WeChatScreenshotGenerator()
        
        # 启用训练模式
        generator.set_training_mode(
            enabled=True,
            avatar_weaken=True,
            content_weaken=True,
            avatar_level=0.8,
            content_level=0.7
        )
        
        # 应用自定义颜色
        generator.colors.update(style["colors"])
        
        # 生成截图
        screenshot = generator.generate(num_messages=15)
        
        # 保存
        filename = f"wechat_style_{style['name']}.png"
        generator.save(filename)
    
    print("微信样式变体生成完成！")

if __name__ == "__main__":
    try:
        print("🚀 智能训练模式启动")
        print("=" * 50)
        
        # 生成智能训练数据
        generate_smart_training_data()
        
        # 生成样式对比
        generate_style_comparison()
        
        # 生成微信样式变体
        generate_wechat_style_variations()
        
        print("\n" + "=" * 50)
        print("🎯 智能训练模式完成！")
        print("\n💡 训练建议：")
        print("1. 使用 'wechat_style_focus' 作为主要训练数据")
        print("2. 通过对比图了解不同弱化策略的效果")
        print("3. 使用样式变体提高模型的泛化能力")
        print("4. 重点关注微信的整体布局和视觉特征")
        
    except Exception as e:
        print(f"生成过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
