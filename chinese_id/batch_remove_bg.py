#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量去除头像背景脚本
使用rembg神经网络模型去除头像背景，生成透明背景的PNG图片
"""

import os
import sys
from PIL import Image
from rembg import remove
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('background_removal.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def remove_background_from_image(input_path, output_path):
    """
    去除单张图片的背景
    
    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径
    
    Returns:
        bool: 是否成功
    """
    try:
        # 读取输入图片
        input_image = Image.open(input_path)
        logging.info(f"处理图片: {os.path.basename(input_path)}")
        
        # 使用rembg去除背景
        output_image = remove(input_image)
        
        # 保存结果
        output_image.save(output_path, 'PNG')
        logging.info(f"成功去除背景: {os.path.basename(output_path)}")
        
        return True
        
    except Exception as e:
        logging.error(f"处理图片失败 {input_path}: {e}")
        return False

def batch_remove_background(input_dir, output_dir):
    """
    批量去除背景
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 支持的图片格式
    supported_formats = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp'}
    
    # 获取所有图片文件
    image_files = []
    for file in os.listdir(input_dir):
        if any(file.lower().endswith(fmt) for fmt in supported_formats):
            image_files.append(file)
    
    if not image_files:
        logging.warning(f"在目录 {input_dir} 中没有找到支持的图片文件")
        return
    
    logging.info(f"找到 {len(image_files)} 个图片文件")
    
    # 处理每个图片
    success_count = 0
    for i, filename in enumerate(image_files, 1):
        input_path = os.path.join(input_dir, filename)
        
        # 生成输出文件名（确保是PNG格式）
        name_without_ext = os.path.splitext(filename)[0]
        output_filename = f"{name_without_ext}.png"
        output_path = os.path.join(output_dir, output_filename)
        
        # 去除背景
        if remove_background_from_image(input_path, output_path):
            success_count += 1
        
        # 显示进度
        if i % 10 == 0 or i == len(image_files):
            logging.info(f"进度: {i}/{len(image_files)} ({i/len(image_files)*100:.1f}%)")
    
    logging.info(f"批量处理完成！成功处理 {success_count}/{len(image_files)} 个文件")

def process_classified_faces():
    """
    处理faces_classified_auto目录中的头像，保持原有的性别分类结构
    """
    input_base_dir = "faces_classified_auto"
    output_base_dir = "faces_tr"
    
    if not os.path.exists(input_base_dir):
        logging.error(f"输入目录不存在: {input_base_dir}")
        return
    
    male_input_dir = os.path.join(input_base_dir, "male")
    female_input_dir = os.path.join(input_base_dir, "female")
    
    male_output_dir = os.path.join(output_base_dir, "male")
    female_output_dir = os.path.join(output_base_dir, "female")
    
    # 创建输出目录
    os.makedirs(male_output_dir, exist_ok=True)
    os.makedirs(female_output_dir, exist_ok=True)
    
    total_processed = 0
    total_success = 0
    
    # 处理男性头像
    if os.path.exists(male_input_dir):
        logging.info(f"开始处理男性头像...")
        male_files = [f for f in os.listdir(male_input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        for i, filename in enumerate(male_files, 1):
            input_path = os.path.join(male_input_dir, filename)
            name_without_ext = os.path.splitext(filename)[0]
            output_filename = f"{name_without_ext}.png"
            output_path = os.path.join(male_output_dir, output_filename)
            
            if remove_background_from_image(input_path, output_path):
                total_success += 1
            total_processed += 1
            
            if i % 10 == 0 or i == len(male_files):
                logging.info(f"男性头像进度: {i}/{len(male_files)} ({i/len(male_files)*100:.1f}%)")
        
        logging.info(f"男性头像处理完成: {len(male_files)} 个文件")
    
    # 处理女性头像
    if os.path.exists(female_input_dir):
        logging.info(f"开始处理女性头像...")
        female_files = [f for f in os.listdir(female_input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        for i, filename in enumerate(female_files, 1):
            input_path = os.path.join(female_input_dir, filename)
            name_without_ext = os.path.splitext(filename)[0]
            output_filename = f"{name_without_ext}.png"
            output_path = os.path.join(female_output_dir, output_filename)
            
            if remove_background_from_image(input_path, output_path):
                total_success += 1
            total_processed += 1
            
            if i % 10 == 0 or i == len(female_files):
                logging.info(f"女性头像进度: {i}/{len(female_files)} ({i/len(female_files)*100:.1f}%)")
        
        logging.info(f"女性头像处理完成: {len(female_files)} 个文件")
    
    logging.info(f"总计处理: {total_processed} 个文件，成功: {total_success} 个")
    logging.info(f"男性头像保存在: {male_output_dir}")
    logging.info(f"女性头像保存在: {female_output_dir}")

def process_faces_directory():
    """
    处理faces目录中的所有头像
    """
    input_dir = "faces"
    output_dir = "faces_tr"
    
    if not os.path.exists(input_dir):
        logging.error(f"输入目录不存在: {input_dir}")
        return
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取所有头像文件
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not image_files:
        logging.warning(f"在目录 {input_dir} 中没有找到头像文件")
        return
    
    logging.info(f"开始处理 {len(image_files)} 个头像文件")
    
    # 处理每个头像
    success_count = 0
    for i, filename in enumerate(image_files, 1):
        input_path = os.path.join(input_dir, filename)
        
        # 生成输出文件名
        name_without_ext = os.path.splitext(filename)[0]
        output_filename = f"{name_without_ext}.png"
        output_path = os.path.join(output_dir, output_filename)
        
        # 去除背景
        if remove_background_from_image(input_path, output_path):
            success_count += 1
        
        # 显示进度
        if i % 10 == 0 or i == len(image_files):
            logging.info(f"进度: {i}/{len(image_files)} ({i/len(image_files)*100:.1f}%)")
    
    logging.info(f"处理完成！成功处理 {success_count}/{len(image_files)} 个文件")
    logging.info(f"头像保存在: {output_dir}")

def main():
    """主函数"""
    logging.info("=" * 60)
    logging.info("开始批量去除头像背景")
    logging.info("=" * 60)
    
    # 检查rembg是否可用
    try:
        from rembg import remove
        logging.info("rembg模块加载成功")
    except ImportError:
        logging.error("rembg模块未安装，请运行: pip install rembg")
        return
    
    # 直接处理faces目录中的头像
    process_faces_directory()
    
    logging.info("=" * 60)
    logging.info("批量去除背景完成")
    logging.info("=" * 60)

if __name__ == "__main__":
    main()
