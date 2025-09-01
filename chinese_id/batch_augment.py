import albumentations as A
import cv2
import os
from pathlib import Path
import numpy as np

# 设置环境变量解决OpenMP问题
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# 定义一个简化的增强管道
transform = A.Compose([
    A.Affine(rotate=(-5, 5), p=0.5),
    A.GaussianBlur(blur_limit=(3, 5), p=0.3),
    A.GaussNoise(p=0.2),
    A.ColorJitter(brightness=0.2, contrast=0.2, p=0.5),
])

# 应用增强
def augment_image(image):
    augmented = transform(image=image)
    return augmented['image']

def read_image_safe(image_path):
    """
    安全地读取图片，处理编码问题
    """
    try:
        # 方法1: 使用numpy读取（在Windows中文路径下最可靠）
        try:
            image_data = np.fromfile(str(image_path), dtype=np.uint8)
            image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
            if image is not None:
                return image
        except:
            pass
        
        # 方法2: 直接使用cv2.imread
        image = cv2.imread(str(image_path))
        if image is not None:
            return image
        
        # 方法3: 使用绝对路径
        abs_path = os.path.abspath(str(image_path))
        image = cv2.imread(abs_path)
        if image is not None:
            return image
        
        return None
    except Exception as e:
        print(f"      ❌ 读取图片失败: {e}")
        return None

def save_image_safe(image, output_path):
    """安全地保存图片"""
    try:
        # 使用numpy编码保存
        encode_param = [int(cv2.IMWRITE_PNG_COMPRESSION), 9]
        result, encoded_img = cv2.imencode('.png', image, encode_param)
        
        if result:
            with open(output_path, 'wb') as f:
                f.write(encoded_img.tobytes())
            return True
        else:
            return False
    except Exception as e:
        return False

def batch_augment_images(input_dir, output_dir, num_augmentations=3, max_users=3):
    """
    批量增强图片，按姓名存储
    
    Args:
        input_dir: 输入图片目录（chinese_ids目录）
        output_dir: 输出图片目录
        num_augmentations: 每张图片生成的增强版本数量
        max_users: 最大处理用户数量（用于测试）
    """
    # 使用Path对象处理路径，避免编码问题
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # 创建输出目录
    output_path.mkdir(exist_ok=True)
    
    print(f"🔍 扫描目录: {input_path}")
    print(f"📁 输出目录: {output_path}")
    print(f"🎯 每张图片生成 {num_augmentations} 个增强版本")
    print(f"👥 最大处理用户数: {max_users}")
    
    total_generated = 0
    total_processed = 0
    user_count = 0
    
    # 遍历chinese_ids目录下的所有姓名子目录
    for person_dir in input_path.iterdir():
        if not person_dir.is_dir():
            continue
            
        # 限制处理用户数量
        if user_count >= max_users:
            print(f"\n⏹️  已达到最大用户数量限制 ({max_users})")
            break
            
        person_name = person_dir.name
        print(f"\n👤 处理用户: {person_name}")
        
        # 为每个用户创建对应的输出目录
        person_output_dir = output_path / person_name
        person_output_dir.mkdir(exist_ok=True)
        print(f"📁 创建用户目录: {person_output_dir}")
        
        # 检查是否已经有增强文件
        existing_files = [f for f in person_output_dir.iterdir() if f.is_file() and '_aug_' in f.name]
        if existing_files:
            print(f"   ⏭️  用户 {person_name} 已有增强文件 ({len(existing_files)} 个)，跳过处理")
            continue
            
        # 获取该用户目录下的所有图片文件
        image_files = [f for f in person_dir.iterdir() if f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
        
        if not image_files:
            print(f"   ⚠️  用户 {person_name} 目录下没有找到图片文件")
            continue
            
        print(f"   📸 找到 {len(image_files)} 张图片")
        
        # 处理该用户的每张图片
        for i, image_file in enumerate(image_files, 1):
            print(f"    处理第 {i}/{len(image_files)} 张: {image_file.name}")
            
            try:
                # 使用安全的图片读取方法
                image = read_image_safe(image_file)
                
                if image is None:
                    print(f"      ❌ 无法读取图片 {image_file.name}")
                    continue
                    
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                # 生成多个增强版本
                for j in range(num_augmentations):
                    try:
                        # 应用增强
                        augmented_image = augment_image(image_rgb)
                        
                        # 生成输出文件名
                        name_without_ext = image_file.stem
                        output_filename = f"{name_without_ext}_aug_{j+1:02d}.png"
                        output_file_path = person_output_dir / output_filename
                        
                        # 保存增强后的图片
                        if save_image_safe(cv2.cvtColor(augmented_image, cv2.COLOR_RGB2BGR), str(output_file_path)):
                            total_generated += 1
                            print(f"      ✅ 生成增强版本 {j+1}: {output_filename}")
                        else:
                            print(f"      ❌ 保存增强版本 {j+1} 失败: {output_file_path}")
                        
                    except Exception as e:
                        print(f"      ❌ 生成增强版本 {j+1} 失败: {e}")
                
                total_processed += 1
                
            except Exception as e:
                print(f"      ❌ 处理图片 {image_file.name} 失败: {e}")
                continue
        
        user_count += 1
    
    print(f"\n🎉 批量增强完成！")
    print(f"📊 统计信息:")
    print(f"   • 处理用户数量: {user_count}")
    print(f"   • 处理图片数量: {total_processed}")
    print(f"   • 生成增强图片数量: {total_generated}")
    print(f"   • 输出目录: {output_path}")
    print(f"\n💡 增强后的图片已按姓名分类存储，便于管理和使用")

if __name__ == "__main__":
    # 设置输入和输出目录
    input_directory = "chinese_ids"  # 身份证图片根目录
    output_directory = "e:/dataset/generated/chinese_ids_augmented"  # 增强后的图片根目录
    
    # 检查输入目录
    if not os.path.exists(input_directory):
        print(f"❌ 输入目录不存在: {input_directory}")
        print("请确保 chinese_ids 目录存在并包含身份证图片")
        exit(1)
    
    # 执行批量增强（限制处理前3个用户进行测试）
    batch_augment_images(input_directory, output_directory, num_augmentations=3, max_users=200)
    
    print(f"\n🔍 使用建议:")
    print("1. 增强后的图片按姓名分类存储，便于查找")
    print("2. 每个增强版本都有唯一的编号 (_aug_01, _aug_02, ...)")
    print("3. 可以用于训练数据增强或测试不同场景")
    print("4. 建议检查几个样本，确保增强效果符合预期")
