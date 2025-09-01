#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
聊天内容弱化效果演示
展示不同弱化程度下的聊天内容变化
"""

from genwechat import WeChatScreenshotGenerator
import os

def demonstrate_content_weakening():
    """演示内容弱化效果"""
    
    print("🎯 聊天内容弱化效果演示")
    print("=" * 50)
    
    # 创建输出目录
    os.makedirs("output", exist_ok=True)
    
    # 不同弱化程度的配置
    weaken_configs = [
        {
            "name": "no_weaken",
            "description": "无弱化（原始内容）",
            "content_level": 0.0
        },
        {
            "name": "light_weaken",
            "description": "轻度弱化（30%）",
            "content_level": 0.3
        },
        {
            "name": "medium_weaken",
            "description": "中度弱化（60%）",
            "content_level": 0.6
        },
        {
            "name": "heavy_weaken",
            "description": "重度弱化（90%）",
            "content_level": 0.9
        }
    ]
    
    for config in weaken_configs:
        print(f"\n正在生成 {config['description']}...")
        
        # 创建生成器实例
        generator = WeChatScreenshotGenerator()
        
        # 启用训练模式，仅弱化内容
        generator.set_training_mode(
            enabled=True,
            avatar_weaken=False,      # 不弱化头像
            content_weaken=True,      # 弱化聊天内容
            avatar_level=0.0,
            content_level=config["content_level"]
        )
        
        # 生成聊天截图
        print(f"内容弱化程度: {config['content_level']:.1f}")
        screenshot = generator.generate(num_messages=15)
        
        # 保存截图
        filename = f"content_weaken_{config['name']}.png"
        generator.save(filename)
        
        print(f"{config['description']}已保存为: {filename}")
    
    print("\n✅ 所有内容弱化演示完成！")

def show_placeholder_examples():
    """展示占位符示例"""
    
    print("\n📝 占位符内容示例")
    print("=" * 30)
    
    # 模拟内容弱化过程
    original_messages = [
        "你好呀！",
        "在干嘛呢？",
        "今天天气真不错",
        "周末有什么计划？",
        "最近看了一部好电影"
    ]
    
    placeholders = [
        "消息内容", "聊天记录", "对话内容", "文本消息",
        "用户输入", "聊天信息", "对话文本", "消息文本"
    ]
    
    print("原始消息 -> 弱化后的消息")
    print("-" * 30)
    
    import random
    
    for message in original_messages:
        # 模拟70%的弱化程度
        if random.random() < 0.7:
            weakened = random.choice(placeholders)
            print(f"'{message}' -> '{weakened}'")
        else:
            print(f"'{message}' -> '{message}' (保持原样)")
    
    print("\n💡 说明：")
    print("- 弱化程度越高，被替换为占位符的概率越大")
    print("- 占位符是通用的描述性文本，不包含具体信息")
    print("- 这样可以避免模型记忆特定的聊天内容")

def generate_comparison_grid():
    """生成对比网格，展示不同弱化程度的效果"""
    
    print("\n🔄 正在生成内容弱化对比网格...")
    
    # 创建生成器
    generator = WeChatScreenshotGenerator()
    
    # 生成不同弱化程度的截图
    weaken_levels = [0.0, 0.3, 0.6, 0.9]
    
    for level in weaken_levels:
        print(f"生成弱化程度 {level:.1f} 的截图...")
        
        # 设置弱化参数
        generator.set_training_mode(
            enabled=True,
            avatar_weaken=False,
            content_weaken=True,
            avatar_level=0.0,
            content_level=level
        )
        
        # 生成截图
        screenshot = generator.generate(num_messages=10)
        
        # 保存
        filename = f"content_comparison_{level:.1f}.png"
        generator.save(filename)
    
    print("内容弱化对比图生成完成！")

if __name__ == "__main__":
    try:
        # 演示内容弱化效果
        demonstrate_content_weakening()
        
        # 展示占位符示例
        show_placeholder_examples()
        
        # 生成对比网格
        generate_comparison_grid()
        
        print("\n" + "=" * 50)
        print("🎯 内容弱化演示完成！")
        print("\n📊 弱化效果说明：")
        print("1. 弱化程度越高，具体内容被替换的概率越大")
        print("2. 占位符保持聊天气泡的结构，但内容更通用")
        print("3. 这样训练出的模型更关注微信的界面特征")
        print("4. 而不是记忆特定的聊天内容")
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
