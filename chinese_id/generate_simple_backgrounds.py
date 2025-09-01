import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import os
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_desktop_backgrounds():
    """
    生成桌面背景图片，用于后续放置身份证
    """
    print("🖥️  开始生成桌面背景图片...")
    
    # 检查CUDA可用性
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"使用设备: {device}")
    
    # 创建输出目录
    output_dir = "desktop_backgrounds"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 加载模型
        print("📥 正在加载Stable Diffusion模型...")
        model_id = "runwayml/stable-diffusion-v1-5"
        
        scheduler = DPMSolverMultistepScheduler.from_pretrained(
            model_id, 
            subfolder="scheduler"
        )
        
        pipeline = StableDiffusionPipeline.from_pretrained(
            model_id,
            scheduler=scheduler,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            safety_checker=None,
            requires_safety_checker=False
        )
        
        if device == "cuda":
            pipeline = pipeline.to(device)
            pipeline.enable_attention_slicing()
            pipeline.enable_vae_slicing()
        
        print("✅ 模型加载成功！")
        
        # 定义桌面背景类型
        backgrounds = [
            {
                "name": "现代办公桌",
                "prompt": "Extreme close-up top-down view of a clean modern office desk surface, smooth lacquered finish, neutral light brown color, minimalist design, perfect for placing documents, no objects, just the flat surface, high quality, 4k",
                "negative_prompt": "cluttered, messy, dark, low quality, blurry, distorted, people, hands, furniture legs, room, rough texture, matte finish, objects, items, 3d perspective, angled view, wood grain, texture, background, environment, plants, ground, floor"
            },
            {
                "name": "温馨家庭桌",
                "prompt": "Extreme close-up top-down view of a warm dining table surface, smooth lacquered finish, warm brown color, soft natural lighting, flat surface, perfect for family documents, no objects, high quality, 4k",
                "negative_prompt": "office, corporate, cold, sterile, low quality, blurry, people, hands, furniture legs, room, rough surface, objects, items, 3d perspective, angled view, wood grain, texture, background, environment, plants, ground, floor"
            },
            {
                "name": "咖啡厅桌面",
                "prompt": "Extreme close-up top-down view of a rustic coffee shop table surface, smooth lacquered finish, warm brown color, flat table top, perfect for casual documents, no objects, high quality, 4k",
                "negative_prompt": "modern, office, cold, bright, low quality, blurry, people, hands, furniture legs, room, glossy finish, objects, items, 3d perspective, angled view, wood grain, texture, background, environment, plants, ground, floor"
            },
            {
                "name": "图书馆桌面",
                "prompt": "Extreme close-up top-down view of a classic library study table surface, smooth lacquered finish, dark brown color, scholarly atmosphere, flat surface, perfect for academic documents, no objects, high quality, 4k",
                "negative_prompt": "modern, colorful, bright, low quality, blurry, distorted, people, hands, furniture legs, room, rough texture, objects, items, 3d perspective, angled view, wood grain, texture, background, environment, plants, ground, floor"
            },
            {
                "name": "户外露台桌",
                "prompt": "Extreme close-up top-down view of an outdoor patio table surface, smooth lacquered finish, light gray color, natural daylight, flat surface, perfect for outdoor documents, no objects, high quality, 4k",
                "negative_prompt": "indoor, artificial lighting, low quality, blurry, dark, people, hands, furniture legs, room, rough stone, objects, items, 3d perspective, angled view, stone texture, texture, background, environment, plants, ground, floor, multiple tables, furniture"
            }
        ]
        
        total_generated = 0
        
        for bg in backgrounds:
            name = bg["name"]
            prompt = bg["prompt"]
            negative_prompt = bg["negative_prompt"]
            
            print(f"\n🎨 正在生成: {name} (10张)")
            
            for i in range(10):
                try:
                    # 生成图片
                    image = pipeline(
                        prompt=prompt,
                        negative_prompt=negative_prompt,
                        width=1024,
                        height=768,
                        num_inference_steps=20,
                        guidance_scale=7.5,
                        num_images_per_prompt=1
                    ).images[0]
                    
                    # 保存图片
                    filename = f"{name.replace(' ', '_')}_{i+1:02d}.png"
                    output_path = os.path.join(output_dir, filename)
                    image.save(output_path)
                    
                    print(f"✅ 生成成功: {filename}")
                    total_generated += 1
                    
                except Exception as e:
                    print(f"❌ 生成失败: {e}")
        
        print(f"\n🎉 桌面背景生成完成！")
        print(f"成功生成: {total_generated}/50 张图片")
        print(f"输出目录: {output_dir}")
        
        if total_generated > 0:
            print("\n💡 这些背景图可以用于:")
            print("1. 将身份证放置到桌面上")
            print("2. 创建更真实的身份证使用场景")
            print("3. 训练模型识别不同环境下的身份证")
            print("4. 数据增强和场景多样化")
        
        return total_generated
        
    except Exception as e:
        print(f"❌ 程序运行出错: {e}")
        return 0

if __name__ == "__main__":
    generate_desktop_backgrounds()
