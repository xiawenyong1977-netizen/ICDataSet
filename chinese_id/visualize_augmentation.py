import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

def visualize_augmentation_effects():
    """
    可视化图像增强效果，对比原图和增强后的图片
    """
    
    # 检查文件是否存在
    original_path = "chinese_ids/front/110101194502027206_front.jpg"
    augmented_path = "augmented_id.png"
    
    if not os.path.exists(original_path):
        print(f"错误：原图文件不存在: {original_path}")
        return
    
    if not os.path.exists(augmented_path):
        print(f"错误：增强图片文件不存在: {augmented_path}")
        return
    
    # 读取图片
    original = cv2.imread(original_path)
    augmented = cv2.imread(augmented_path)
    
    # 转换颜色空间用于显示
    original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    augmented_rgb = cv2.cvtColor(augmented, cv2.COLOR_BGR2RGB)
    
    # 创建对比图
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('身份证图像增强效果对比', fontsize=16, fontweight='bold')
    
    # 1. 原图
    axes[0, 0].imshow(original_rgb)
    axes[0, 0].set_title('原图 (Original)', fontsize=14, fontweight='bold')
    axes[0, 0].axis('off')
    
    # 2. 增强后的图片
    axes[0, 1].imshow(augmented_rgb)
    axes[0, 1].set_title('增强后 (Augmented)', fontsize=14, fontweight='bold')
    axes[0, 1].axis('off')
    
    # 3. 差异图（突出显示变化）
    diff = cv2.absdiff(original, augmented)
    diff_rgb = cv2.cvtColor(diff, cv2.COLOR_BGR2RGB)
    axes[0, 2].imshow(diff_rgb)
    axes[0, 2].set_title('差异图 (Difference)', fontsize=14, fontweight='bold')
    axes[0, 2].axis('off')
    
    # 4. 局部放大对比 - 头像区域
    # 身份证头像位置大约在 (651, 110) 附近，尺寸 308x376
    h, w = original.shape[:2]
    
    # 头像区域坐标（根据身份证模板调整）
    face_x, face_y = 651, 110
    face_w, face_h = 308, 376
    
    # 确保坐标在图片范围内
    face_x = max(0, min(face_x, w - face_w))
    face_y = max(0, min(face_y, h - face_h))
    
    # 提取头像区域
    face_original = original_rgb[face_y:face_y+face_h, face_x:face_x+face_w]
    face_augmented = augmented_rgb[face_y:face_y+face_h, face_x:face_x+face_w]
    
    axes[1, 0].imshow(face_original)
    axes[1, 0].set_title('原图头像区域', fontsize=12)
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(face_augmented)
    axes[1, 1].set_title('增强后头像区域', fontsize=12)
    axes[1, 1].axis('off')
    
    # 5. 文字区域对比
    # 姓名区域大约在 (202, 90) 附近
    text_x, text_y = 202, 90
    text_w, text_h = 200, 50
    
    text_x = max(0, min(text_x, w - text_w))
    text_y = max(0, min(text_y, h - text_h))
    
    text_original = original_rgb[text_y:text_y+text_h, text_x:text_x+text_w]
    text_augmented = augmented_rgb[text_y:text_y+text_h, text_x:text_x+text_w]
    
    axes[1, 2].imshow(text_original)
    axes[1, 2].set_title('原图文字区域', fontsize=12)
    axes[1, 2].axis('off')
    
    # 调整布局
    plt.tight_layout()
    
    # 保存对比图
    output_path = "augmentation_comparison.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"对比图已保存为: {output_path}")
    
    # 显示图片
    plt.show()
    
    # 打印增强效果说明
    print("\n" + "="*60)
    print("🔍 图像增强效果说明")
    print("="*60)
    print("1. 📐 几何变换:")
    print("   - 轻微旋转: ±5度")
    print("   - 轻微缩放: 95%-105%")
    print("   - 轻微剪切: ±2度")
    print("   - 透视变换: 模拟拍摄角度")
    
    print("\n2. 🎨 像素变换:")
    print("   - 运动模糊: 模拟手抖")
    print("   - 高斯模糊: 模拟焦距问题")
    print("   - 高斯噪声: 模拟传感器噪声")
    print("   - 颜色抖动: 亮度、对比度、饱和度、色调变化")
    
    print("\n3. 🌟 环境因素:")
    print("   - 随机阴影: 模拟光照变化")
    print("   - 随机伽马: 模拟曝光变化")
    print("   - ISO噪声: 模拟高ISO拍摄")
    
    print("\n4. 📏 尺寸调整:")
    print("   - 填充和裁剪: 保持最终尺寸一致")
    
    print("\n💡 这些增强效果模拟了真实拍摄环境中的各种情况，")
    print("   使训练数据更加多样化和真实化！")

def create_simple_comparison():
    """
    创建简单的并排对比图
    """
    # 检查文件是否存在
    original_path = "chinese_ids/front/110101194502027206_front.jpg"
    augmented_path = "augmented_id.png"
    
    if not os.path.exists(original_path) or not os.path.exists(augmented_path):
        print("错误：需要原图和增强图片文件")
        return
    
    # 读取图片
    original = cv2.imread(original_path)
    augmented = cv2.imread(augmented_path)
    
    # 转换颜色空间
    original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    augmented_rgb = cv2.cvtColor(augmented, cv2.COLOR_BGR2RGB)
    
    # 创建并排对比图
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    ax1.imshow(original_rgb)
    ax1.set_title('原图 (Original)', fontsize=16, fontweight='bold')
    ax1.axis('off')
    
    ax2.imshow(augmented_rgb)
    ax2.set_title('增强后 (Augmented)', fontsize=16, fontweight='bold')
    ax2.axis('off')
    
    plt.tight_layout()
    
    # 保存简单对比图
    output_path = "simple_comparison.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"简单对比图已保存为: {output_path}")
    
    plt.show()

if __name__ == "__main__":
    print("🔍 开始可视化图像增强效果...")
    
    try:
        # 尝试创建详细对比图
        visualize_augmentation_effects()
    except Exception as e:
        print(f"详细对比图创建失败: {e}")
        print("尝试创建简单对比图...")
        try:
            create_simple_comparison()
        except Exception as e2:
            print(f"简单对比图也创建失败: {e2}")
            print("请检查matplotlib是否正确安装")
