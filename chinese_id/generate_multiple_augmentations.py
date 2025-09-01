import albumentations as A
import cv2
import os

def generate_multiple_augmentations(input_path, output_dir, num_versions=5):
    """
    生成多个增强版本的图片，按姓名存储
    
    Args:
        input_path: 输入图片路径（从chinese_ids目录结构推断姓名）
        output_dir: 输出目录
        num_versions: 生成版本数量
    """
    # 从输入路径推断姓名
    # 假设路径格式: chinese_ids/姓名/文件名
    path_parts = input_path.split(os.sep)
    if len(path_parts) >= 3 and path_parts[0] == "chinese_ids":
        person_name = path_parts[1]
        # 为每个用户创建对应的输出目录
        person_output_dir = os.path.join(output_dir, person_name)
        os.makedirs(person_output_dir, exist_ok=True)
        print(f"👤 检测到用户: {person_name}")
        print(f"📁 输出目录: {person_output_dir}")
    else:
        # 如果不是标准路径，使用默认输出目录
        person_output_dir = output_dir
        person_name = "unknown"
        os.makedirs(person_output_dir, exist_ok=True)
        print(f"⚠️  无法识别用户姓名，使用默认输出目录: {person_output_dir}")
    
    # 读取原图
    image = cv2.imread(input_path)
    if image is None:
        print(f"❌ 无法读取图片: {input_path}")
        return
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    print(f"🔍 开始生成 {num_versions} 个增强版本...")
    
    # 定义多个不同的增强管道
    augmentation_pipelines = [
        # 管道1: 轻微几何变换
        {
            'pipeline': A.Compose([
                A.Affine(rotate=(-3, 3), translate_percent=(-0.03, 0.03), scale=(0.97, 1.03), p=0.8),
                A.GaussNoise(p=0.3),
                A.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.05, hue=0.02, p=0.6),
            ]),
            'name': "轻微变换"
        },
        
        # 管道2: 中等几何变换
        {
            'pipeline': A.Compose([
                A.Affine(rotate=(-5, 5), translate_percent=(-0.05, 0.05), scale=(0.95, 1.05), p=0.8),
                A.Perspective(scale=(0.03, 0.07), p=0.4),
                A.GaussNoise(p=0.4),
                A.ColorJitter(brightness=0.15, contrast=0.15, saturation=0.08, hue=0.03, p=0.7),
            ]),
            'name': "中等变换"
        },
        
        # 管道3: 模糊效果
        {
            'pipeline': A.Compose([
                A.OneOf([
                    A.MotionBlur(blur_limit=3, p=0.3),
                    A.GaussianBlur(blur_limit=(3, 5), p=0.3),
                ], p=0.5),
                A.GaussNoise(p=0.3),
                A.ColorJitter(brightness=0.1, contrast=0.1, p=0.5),
            ]),
            'name': "模糊效果"
        },
        
        # 管道4: 光照变化
        {
            'pipeline': A.Compose([
                A.RandomShadow(shadow_roi=(0, 0.5, 1, 1), shadow_dimension=5, p=0.4),
                A.RandomGamma(gamma_limit=(85, 115), p=0.4),
                A.ColorJitter(brightness=0.2, contrast=0.2, p=0.6),
            ]),
            'name': "光照变化"
        },
        
        # 管道5: 综合效果
        {
            'pipeline': A.Compose([
                A.Affine(rotate=(-4, 4), translate_percent=(-0.04, 0.04), scale=(0.96, 1.04), p=0.7),
                A.Perspective(scale=(0.02, 0.06), p=0.3),
                A.OneOf([
                    A.MotionBlur(blur_limit=3, p=0.2),
                    A.GaussianBlur(blur_limit=(3, 4), p=0.2),
                ], p=0.3),
                A.GaussNoise(p=0.3),
                A.ColorJitter(brightness=0.12, contrast=0.12, saturation=0.06, hue=0.02, p=0.6),
                A.RandomShadow(shadow_roi=(0, 0.5, 1, 1), shadow_dimension=3, p=0.2),
            ]),
            'name': "综合效果"
        },
    ]
    
    # 生成增强版本
    for i in range(min(num_versions, len(augmentation_pipelines))):
        try:
            # 应用增强
            pipeline_info = augmentation_pipelines[i]
            pipeline = pipeline_info['pipeline']
            name = pipeline_info['name']
            
            augmented = pipeline(image=image_rgb)
            augmented_image = augmented['image']
            
            # 生成输出文件名
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_filename = f"{base_name}_aug_{i+1:02d}_{name}.png"
            output_path = os.path.join(person_output_dir, output_filename)
            
            # 保存增强后的图片
            cv2.imwrite(output_path, cv2.cvtColor(augmented_image, cv2.COLOR_RGB2BGR))
            
            print(f"✅ 生成版本 {i+1}: {output_filename}")
            
        except Exception as e:
            print(f"❌ 生成版本 {i+1} 失败: {e}")
    
    print(f"\n🎉 增强完成！共生成 {num_versions} 个版本")
    print(f"📁 输出目录: {person_output_dir}")
    print(f"👤 用户: {person_name}")

if __name__ == "__main__":
    # 设置输入和输出
    input_image = "chinese_ids/鲁帅/610114200711228065_front.png"  # 使用实际的身份证图片路径
    output_directory = "chinese_ids_augmented"  # 增强后的图片根目录
    
    # 检查输入文件
    if not os.path.exists(input_image):
        print(f"❌ 输入图片不存在: {input_image}")
        print("请确保路径正确，格式应为: chinese_ids/姓名/文件名")
        exit(1)
    
    # 生成多个增强版本
    generate_multiple_augmentations(input_image, output_directory, num_versions=5)
    
    print("\n🔍 观察建议:")
    print("1. 对比原图和各个增强版本")
    print("2. 观察几何变换、颜色变化、模糊效果等")
    print("3. 每个版本都有不同的增强效果")
    print("4. 增强后的图片按姓名分类存储，便于管理")
    print("5. 可以运行 simple_view.py 查看对比效果")
