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

def save_image_safe(image, output_path):
    """安全地保存图片"""
    try:
        # 方法1: 使用numpy编码保存
        encode_param = [int(cv2.IMWRITE_PNG_COMPRESSION), 9]
        result, encoded_img = cv2.imencode('.png', image, encode_param)
        
        if result:
            with open(output_path, 'wb') as f:
                f.write(encoded_img.tobytes())
            return True
        else:
            print("❌ 图片编码失败")
            return False
    except Exception as e:
        print(f"❌ 保存异常: {e}")
        return False

def debug_single_user():
    """调试单个用户的处理过程"""
    
    # 测试用户
    user_name = "任旭"
    input_dir = "chinese_ids"
    output_dir = "debug_augmented"
    
    print(f"🔍 调试用户: {user_name}")
    
    # 创建输出目录
    user_output_dir = os.path.join(output_dir, user_name)
    os.makedirs(user_output_dir, exist_ok=True)
    print(f"📁 创建输出目录: {user_output_dir}")
    
    # 获取用户图片
    user_input_dir = os.path.join(input_dir, user_name)
    image_files = [f for f in os.listdir(user_input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"📸 找到 {len(image_files)} 张图片")
    
    # 只处理第一张图片
    if image_files:
        first_image = image_files[0]
        image_path = os.path.join(user_input_dir, first_image)
        
        print(f"🎯 处理图片: {first_image}")
        print(f"📂 图片路径: {image_path}")
        
        # 读取图片
        image = read_image_safe(image_path)
        if image is None:
            print("❌ 无法读取图片")
            return
        
        print(f"✅ 成功读取图片，尺寸: {image.shape}")
        
        # 转换颜色空间
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # 生成一个增强版本
        try:
            print("🎨 应用增强...")
            augmented = transform(image=image_rgb)
            augmented_image = augmented['image']
            
            print(f"✅ 增强完成，尺寸: {augmented_image.shape}")
            
            # 转换回BGR
            augmented_bgr = cv2.cvtColor(augmented_image, cv2.COLOR_RGB2BGR)
            
            # 保存图片
            output_filename = f"{os.path.splitext(first_image)[0]}_aug_01.png"
            output_path = os.path.join(user_output_dir, output_filename)
            
            print(f"💾 保存路径: {output_path}")
            
            # 使用安全的保存方法
            success = save_image_safe(augmented_bgr, output_path)
            
            if success:
                print(f"✅ 保存成功: {output_filename}")
                
                # 验证文件是否真的保存了
                if os.path.exists(output_path):
                    file_size = os.path.getsize(output_path)
                    print(f"📏 文件大小: {file_size} 字节")
                else:
                    print("❌ 文件保存失败，文件不存在")
            else:
                print(f"❌ 保存失败: {output_filename}")
                
        except Exception as e:
            print(f"❌ 增强过程失败: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n🎉 调试完成！")

if __name__ == "__main__":
    debug_single_user()
