#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
训练数据集生成脚本
生成不同阶段的训练图片：
- 初期训练：300张（轻度弱化）
- 中期训练：200张（中度弱化）
- 后期训练：100张（重度弱化）
- 测试阶段：50张（极度弱化）
"""

from genwechat import WeChatScreenshotGenerator
import os
import random

def generate_early_training_data(count=300):
    """生成初期训练数据 - 轻度弱化"""
    
    print(f"🎯 开始生成初期训练数据（{count}张）...")
    print("策略：轻度弱化，让模型逐步适应")
    
    # 创建输出目录
    os.makedirs("output/early_training", exist_ok=True)
    
    # 初期训练配置 - 轻度弱化
    early_configs = [
        {"avatar_level": 0.3, "content_level": 0.2},  # 很轻的弱化
        {"avatar_level": 0.4, "content_level": 0.3},  # 轻度弱化
        {"avatar_level": 0.5, "content_level": 0.4},  # 中等轻度弱化
    ]
    
    for i in range(count):
        # 随机选择配置
        config = random.choice(early_configs)
        
        # 创建生成器
        generator = WeChatScreenshotGenerator()
        
        # 启用训练模式
        generator.set_training_mode(
            enabled=True,
            avatar_weaken=True,
            content_weaken=True,
            avatar_level=config["avatar_level"],
            content_level=config["content_level"]
        )
        
        # 随机选择头像样式
        avatar_styles = ["simple", "geometric"]
        generator.set_avatar_style(random.choice(avatar_styles))
        
        # 随机消息数量
        num_messages = random.randint(8, 20)
        
        # 生成截图
        screenshot = generator.generate(num_messages=num_messages)
        
        # 保存
        filename = f"early_training_{i+1:03d}_a{config['avatar_level']:.1f}_c{config['content_level']:.1f}.png"
        generator.save(f"early_training/{filename}")
        
        if (i + 1) % 50 == 0:
            print(f"已生成 {i + 1}/{count} 张初期训练图片")
    
    print(f"✅ 初期训练数据生成完成！共 {count} 张图片")

def generate_mid_training_data(count=200):
    """生成中期训练数据 - 中度弱化"""
    
    print(f"\n🎯 开始生成中期训练数据（{count}张）...")
    print("策略：中度弱化，提高模型泛化能力")
    
    # 创建输出目录
    os.makedirs("output/mid_training", exist_ok=True)
    
    # 中期训练配置 - 中度弱化
    mid_configs = [
        {"avatar_level": 0.6, "content_level": 0.5},  # 中度弱化
        {"avatar_level": 0.7, "content_level": 0.6},  # 中重度弱化
        {"avatar_level": 0.8, "content_level": 0.7},  # 重度弱化
    ]
    
    for i in range(count):
        # 随机选择配置
        config = random.choice(mid_configs)
        
        # 创建生成器
        generator = WeChatScreenshotGenerator()
        
        # 启用训练模式
        generator.set_training_mode(
            enabled=True,
            avatar_weaken=True,
            content_weaken=True,
            avatar_level=config["avatar_level"],
            content_level=config["content_level"]
        )
        
        # 使用简单头像样式
        generator.set_avatar_style("simple")
        
        # 随机消息数量
        num_messages = random.randint(10, 25)
        
        # 生成截图
        screenshot = generator.generate(num_messages=num_messages)
        
        # 保存
        filename = f"mid_training_{i+1:03d}_a{config['avatar_level']:.1f}_c{config['content_level']:.1f}.png"
        generator.save(f"mid_training/{filename}")
        
        if (i + 1) % 50 == 0:
            print(f"已生成 {i + 1}/{count} 张中期训练图片")
    
    print(f"✅ 中期训练数据生成完成！共 {count} 张图片")

def generate_late_training_data(count=100):
    """生成后期训练数据 - 重度弱化"""
    
    print(f"\n🎯 开始生成后期训练数据（{count}张）...")
    print("策略：重度弱化，测试模型极限能力")
    
    # 创建输出目录
    os.makedirs("output/late_training", exist_ok=True)
    
    # 后期训练配置 - 重度弱化
    late_configs = [
        {"avatar_level": 0.8, "content_level": 0.8},  # 重度弱化
        {"avatar_level": 0.9, "content_level": 0.9},  # 极度弱化
        {"avatar_level": 0.95, "content_level": 0.95},  # 接近完全弱化
    ]
    
    for i in range(count):
        # 随机选择配置
        config = random.choice(late_configs)
        
        # 创建生成器
        generator = WeChatScreenshotGenerator()
        
        # 启用训练模式
        generator.set_training_mode(
            enabled=True,
            avatar_weaken=True,
            content_weaken=True,
            avatar_level=config["avatar_level"],
            content_level=config["content_level"]
        )
        
        # 使用最简单头像样式
        generator.set_avatar_style("simple")
        
        # 随机消息数量
        num_messages = random.randint(12, 30)
        
        # 生成截图
        screenshot = generator.generate(num_messages=num_messages)
        
        # 保存
        filename = f"late_training_{i+1:03d}_a{config['avatar_level']:.2f}_c{config['content_level']:.2f}.png"
        generator.save(f"late_training/{filename}")
        
        if (i + 1) % 25 == 0:
            print(f"已生成 {i + 1}/{count} 张后期训练图片")
    
    print(f"✅ 后期训练数据生成完成！共 {count} 张图片")

def generate_test_data(count=50):
    """生成测试数据 - 极度弱化"""
    
    print(f"\n🎯 开始生成测试数据（{count}张）...")
    print("策略：极度弱化，验证模型泛化能力")
    
    # 创建输出目录
    os.makedirs("output/test_data", exist_ok=True)
    
    # 测试配置 - 极度弱化
    test_configs = [
        {"avatar_level": 0.9, "content_level": 0.9},   # 极度弱化
        {"avatar_level": 0.95, "content_level": 0.95},  # 接近完全弱化
        {"avatar_level": 0.98, "content_level": 0.98},  # 几乎完全弱化
    ]
    
    for i in range(count):
        # 随机选择配置
        config = random.choice(test_configs)
        
        # 创建生成器
        generator = WeChatScreenshotGenerator()
        
        # 启用训练模式
        generator.set_training_mode(
            enabled=True,
            avatar_weaken=True,
            content_weaken=True,
            avatar_level=config["avatar_level"],
            content_level=config["content_level"]
        )
        
        # 使用最简单头像样式
        generator.set_avatar_style("simple")
        
        # 随机消息数量
        num_messages = random.randint(15, 35)
        
        # 生成截图
        screenshot = generator.generate(num_messages=num_messages)
        
        # 保存
        filename = f"test_data_{i+1:03d}_a{config['avatar_level']:.2f}_c{config['content_level']:.2f}.png"
        generator.save(f"test_data/{filename}")
        
        if (i + 1) % 10 == 0:
            print(f"已生成 {i + 1}/{count} 张测试图片")
    
    print(f"✅ 测试数据生成完成！共 {count} 张图片")

def generate_dataset_summary():
    """生成数据集总结报告"""
    
    print("\n📊 数据集生成总结")
    print("=" * 50)
    
    summary = {
        "初期训练": {"数量": 300, "弱化程度": "轻度 (0.2-0.5)", "用途": "模型适应训练"},
        "中期训练": {"数量": 200, "弱化程度": "中度 (0.5-0.8)", "用途": "提高泛化能力"},
        "后期训练": {"数量": 100, "弱化程度": "重度 (0.8-0.95)", "用途": "测试极限能力"},
        "测试数据": {"数量": 50, "弱化程度": "极度 (0.9-0.98)", "用途": "验证泛化能力"}
    }
    
    total_images = sum(item["数量"] for item in summary.values())
    
    for stage, info in summary.items():
        print(f"{stage}: {info['数量']}张 - {info['弱化程度']} - {info['用途']}")
    
    print(f"\n总计: {total_images} 张训练图片")
    print(f"输出目录: output/")
    print("\n💡 训练建议:")
    print("1. 按顺序使用：初期 → 中期 → 后期 → 测试")
    print("2. 每个阶段完成后评估模型表现")
    print("3. 根据测试结果调整训练策略")

if __name__ == "__main__":
    try:
        print("🚀 开始生成完整训练数据集")
        print("=" * 60)
        
        # 生成各阶段训练数据
        generate_early_training_data(300)    # 初期训练
        generate_mid_training_data(200)      # 中期训练
        generate_late_training_data(100)     # 后期训练
        generate_test_data(50)               # 测试数据
        
        # 生成总结报告
        generate_dataset_summary()
        
        print("\n🎉 所有训练数据生成完成！")
        print("现在你可以开始训练你的微信截图识别模型了！")
        
    except Exception as e:
        print(f"生成过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
