import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def show_comparison():
    """
    简单显示原图和增强后的图片对比
    """
    # 文件路径
    original_path = "chinese_ids/front/110101194502027206_front.jpg"
    augmented_path = "augmented_id.png"
    
    # 检查文件是否存在
    if not os.path.exists(original_path):
        print(f"❌ 原图文件不存在: {original_path}")
        return
    
    if not os.path.exists(augmented_path):
        print(f"❌ 增强图片文件不存在: {augmented_path}")
        return
    
    print("🔍 正在加载图片...")
    
    # 读取图片
    original = cv2.imread(original_path)
    augmented = cv2.imread(augmented_path)
    
    # 转换颜色空间
    original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    augmented_rgb = cv2.cvtColor(augmented, cv2.COLOR_BGR2RGB)
    
    print("✅ 图片加载完成！")
    print(f"📏 原图尺寸: {original.shape[1]} x {original.shape[0]}")
    print(f"📏 增强图尺寸: {augmented.shape[1]} x {augmented.shape[0]}")
    
    # 创建对比图
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    # 显示原图
    ax1.imshow(original_rgb)
    ax1.set_title('原图 (Original)', fontsize=16, fontweight='bold', color='blue')
    ax1.axis('off')
    
    # 显示增强后的图片
    ax2.imshow(augmented_rgb)
    ax2.set_title('增强后 (Augmented)', fontsize=16, fontweight='bold', color='red')
    ax2.axis('off')
    
    # 添加说明文字
    fig.suptitle('身份证图像增强效果对比\n(左: 原图, 右: 增强后)', 
                 fontsize=18, fontweight='bold', y=0.95)
    
    plt.tight_layout()
    
    print("\n🎯 增强效果观察要点:")
    print("1. 📐 几何变化: 查看是否有轻微旋转、倾斜")
    print("2. 🎨 颜色变化: 观察亮度、对比度、色调的细微变化")
    print("3. 🌟 模糊效果: 检查是否有轻微的运动模糊或高斯模糊")
    print("4. 📱 透视变化: 观察是否模拟了不同拍摄角度")
    print("5. 💡 光照变化: 查看阴影和曝光的变化")
    
    print("\n💡 提示: 增强效果通常比较 subtle，需要仔细观察！")
    print("   如果效果不明显，可以多次运行 id_augment.py 生成不同版本")
    
    # 保存对比图
    output_path = "simple_comparison.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\n💾 对比图已保存为: {output_path}")
    
    # 显示图片
    plt.show()

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 身份证图像增强效果观察工具")
    print("=" * 60)
    
    try:
        show_comparison()
    except Exception as e:
        print(f"❌ 运行出错: {e}")
        print("请确保已安装 matplotlib 和 opencv-python")
