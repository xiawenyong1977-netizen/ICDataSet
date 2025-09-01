import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def view_all_augmentations():
    """
    显示原图和所有增强版本的对比
    """
    # 文件路径
    original_path = "chinese_ids/front/110101194502027206_front.jpg"
    augmented_dir = "augmented_versions_english"  # 使用英文版本目录
    
    # 检查文件是否存在
    if not os.path.exists(original_path):
        print(f"❌ 原图文件不存在: {original_path}")
        return
    
    if not os.path.exists(augmented_dir):
        print(f"❌ 增强图片目录不存在: {augmented_dir}")
        return
    
    # 读取原图
    original = cv2.imread(original_path)
    original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    
    # 获取所有增强版本
    augmented_files = [f for f in os.listdir(augmented_dir) if f.endswith('.png')]
    augmented_files.sort()  # 按文件名排序
    
    if not augmented_files:
        print(f"❌ 增强图片目录为空: {augmented_dir}")
        return
    
    print(f"🔍 找到 {len(augmented_files)} 个增强版本")
    
    # 创建网格布局
    num_cols = 3
    num_rows = (len(augmented_files) + 1 + num_cols - 1) // num_cols  # +1 for original
    
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(20, 6 * num_rows))
    if num_rows == 1:
        axes = axes.reshape(1, -1)
    
    # 显示原图
    row = 0
    col = 0
    axes[row, col].imshow(original_rgb)
    axes[row, col].set_title('原图 (Original)', fontsize=14, fontweight='bold', color='blue')
    axes[row, col].axis('off')
    
    # 显示所有增强版本
    for i, filename in enumerate(augmented_files):
        row = (i + 1) // num_cols
        col = (i + 1) % num_cols
        
        # 读取增强图片
        aug_path = os.path.join(augmented_dir, filename)
        augmented = cv2.imread(aug_path)
        augmented_rgb = cv2.cvtColor(augmented, cv2.COLOR_BGR2RGB)
        
        # 显示图片
        axes[row, col].imshow(augmented_rgb)
        
        # 提取增强类型名称
        name_parts = filename.replace('.png', '').split('_')
        if len(name_parts) >= 4:
            aug_type = name_parts[-1]  # 最后一个部分应该是增强类型
        else:
            aug_type = f"版本{i+1}"
        
        axes[row, col].set_title(f'增强版本 {i+1}\n({aug_type})', fontsize=12, fontweight='bold', color='red')
        axes[row, col].axis('off')
    
    # 隐藏多余的子图
    for i in range(len(augmented_files) + 1, num_rows * num_cols):
        row = i // num_cols
        col = i % num_cols
        axes[row, col].axis('off')
    
    # 调整布局
    plt.tight_layout()
    
    # 添加总标题
    fig.suptitle('身份证图像增强效果完整对比\n(原图 + 5个增强版本)', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    # 保存图片
    output_path = "all_augmentations_comparison.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"💾 完整对比图已保存为: {output_path}")
    
    # 显示图片
    plt.show()
    
    # 打印观察指南
    print("\n" + "="*80)
    print("🔍 增强效果观察指南")
    print("="*80)
    print("1. 📐 轻微变换版本 (light_transform):")
    print("   - 观察是否有轻微的旋转、缩放")
    print("   - 颜色是否有细微变化")
    
    print("\n2. 📐 中等变换版本 (medium_transform):")
    print("   - 观察透视变换效果（模拟不同拍摄角度）")
    print("   - 几何变换是否更明显")
    
    print("\n3. 🌟 模糊效果版本 (blur_effect):")
    print("   - 观察是否有运动模糊或高斯模糊")
    print("   - 图片清晰度的变化")
    
    print("\n4. 💡 光照变化版本 (lighting_change):")
    print("   - 观察阴影效果")
    print("   - 亮度和对比度的变化")
    
    print("\n5. 🎯 综合效果版本 (comprehensive):")
    print("   - 综合了多种增强效果")
    print("   - 观察整体效果的变化")
    
    print("\n💡 提示:")
    print("- 增强效果通常比较 subtle，需要仔细观察")
    print("- 重点关注头像区域和文字区域的变化")
    print("- 这些变化模拟了真实拍摄环境中的各种情况")

if __name__ == "__main__":
    print("=" * 80)
    print("🔍 身份证图像增强效果完整观察工具")
    print("=" * 80)
    
    try:
        view_all_augmentations()
    except Exception as e:
        print(f"❌ 运行出错: {e}")
        import traceback
        traceback.print_exc()
