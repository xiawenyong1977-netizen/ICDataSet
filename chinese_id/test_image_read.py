import cv2
import os
from pathlib import Path
import numpy as np

def test_image_read():
    """测试图片读取功能"""
    
    # 测试目录
    test_dir = "chinese_ids"
    
    if not os.path.exists(test_dir):
        print(f"❌ 目录不存在: {test_dir}")
        return
    
    # 获取第一个用户目录
    user_dirs = [d for d in os.listdir(test_dir) if os.path.isdir(os.path.join(test_dir, d))]
    
    if not user_dirs:
        print("❌ 没有找到用户目录")
        return
    
    first_user = user_dirs[0]
    print(f"👤 测试用户: {first_user}")
    
    user_path = os.path.join(test_dir, first_user)
    
    # 获取该用户的图片文件
    image_files = [f for f in os.listdir(user_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not image_files:
        print("❌ 没有找到图片文件")
        return
    
    first_image = image_files[0]
    print(f"📸 测试图片: {first_image}")
    
    # 测试不同的读取方法
    image_path = os.path.join(user_path, first_image)
    
    print(f"\n🔍 测试路径: {image_path}")
    print(f"🔍 绝对路径: {os.path.abspath(image_path)}")
    
    # 方法1: 直接cv2.imread
    print("\n📖 方法1: cv2.imread")
    try:
        image1 = cv2.imread(image_path)
        if image1 is not None:
            print(f"✅ 成功读取，尺寸: {image1.shape}")
        else:
            print("❌ 读取失败")
    except Exception as e:
        print(f"❌ 异常: {e}")
    
    # 方法2: 绝对路径
    print("\n📖 方法2: 绝对路径")
    try:
        abs_path = os.path.abspath(image_path)
        image2 = cv2.imread(abs_path)
        if image2 is not None:
            print(f"✅ 成功读取，尺寸: {image2.shape}")
        else:
            print("❌ 读取失败")
    except Exception as e:
        print(f"❌ 异常: {e}")
    
    # 方法3: numpy读取
    print("\n📖 方法3: numpy读取")
    try:
        image_data = np.fromfile(image_path, dtype=np.uint8)
        image3 = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        if image3 is not None:
            print(f"✅ 成功读取，尺寸: {image3.shape}")
        else:
            print("❌ 读取失败")
    except Exception as e:
        print(f"❌ 异常: {e}")
    
    # 方法4: 使用Path对象
    print("\n📖 方法4: Path对象")
    try:
        path_obj = Path(image_path)
        image4 = cv2.imread(str(path_obj))
        if image4 is not None:
            print(f"✅ 成功读取，尺寸: {image4.shape}")
        else:
            print("❌ 读取失败")
    except Exception as e:
        print(f"❌ 异常: {e}")
    
    # 方法5: 检查文件是否存在
    print("\n📖 方法5: 文件检查")
    try:
        if os.path.exists(image_path):
            print(f"✅ 文件存在")
            file_size = os.path.getsize(image_path)
            print(f"📏 文件大小: {file_size} 字节")
        else:
            print("❌ 文件不存在")
    except Exception as e:
        print(f"❌ 异常: {e}")

if __name__ == "__main__":
    test_image_read()
