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

def read_image_safe(image_path):
    """安全地读取图片"""
    try:
        image_data = np.fromfile(str(image_path), dtype=np.uint8)
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        return image
    except Exception as e:
        print(f"读取图片失败: {e}")
        return None

def test_single_image():
    """测试单张图片的增强功能"""
    
    # 测试图片路径
    test_image_path = "chinese_ids/任旭/420103195710125816_back.png"
    
    print(f"🔍 测试图片: {test_image_path}")
    
    # 检查文件是否存在
    if not os.path.exists(test_image_path):
        print("❌ 测试图片不存在")
        return
    
    # 读取图片
    print("📖 读取图片...")
    image = read_image_safe(test_image_path)
    
    if image is None:
        print("❌ 无法读取图片")
        return
    
    print(f"✅ 成功读取图片，尺寸: {image.shape}")
    
    # 转换颜色空间
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # 创建输出目录
    output_dir = "test_augment_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成3个增强版本
    for i in range(3):
        try:
            print(f"🎨 生成增强版本 {i+1}...")
            
            # 应用增强
            augmented = transform(image=image_rgb)
            augmented_image = augmented['image']
            
            # 转换回BGR
            augmented_bgr = cv2.cvtColor(augmented_image, cv2.COLOR_RGB2BGR)
            
            # 保存图片
            output_filename = f"test_aug_{i+1:02d}.png"
            output_path = os.path.join(output_dir, output_filename)
            
            success = cv2.imwrite(output_path, augmented_bgr)
            
            if success:
                print(f"✅ 保存成功: {output_filename}")
            else:
                print(f"❌ 保存失败: {output_filename}")
                
        except Exception as e:
            print(f"❌ 增强版本 {i+1} 失败: {e}")
    
    print(f"\n🎉 测试完成！输出目录: {output_dir}")

if __name__ == "__main__":
    test_single_image()
