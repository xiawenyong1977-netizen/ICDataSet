import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import os
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_marble_countertop():
    """
    使用指定提示词生成大理石台面背景图片
    """
    print("🖥️  开始生成大理石台面背景图片...")
    
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
        
        # 使用指定的提示词
        prompt = "Soft linen bedsheet, neatly made, subtle folds, natural window light, shallow depth of field, professional product photography"
        negative_prompt = "extra digit, fewer digits, cropped, worst quality, low quality"
        
        print(f"\n🎨 正在生成: 大理石台面")
        print(f"正面提示词: {prompt}")
        print(f"负面提示词: {negative_prompt}")
        
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
            filename = "大理石台面_linen_bedsheet.png"
            output_path = os.path.join(output_dir, filename)
            image.save(output_path)
            
            print(f"✅ 生成成功: {filename}")
            print(f"📁 保存路径: {output_path}")
            
        except Exception as e:
            print(f"❌ 生成失败: {e}")
            return False
        
        print(f"\n🎉 大理石台面背景生成完成！")
        print(f"输出目录: {output_dir}")
        
        print("\n💡 这个背景图的特点:")
        print("1. 柔软的亚麻床单纹理")
        print("2. 整齐的折叠效果")
        print("3. 自然窗户光线")
        print("4. 浅景深效果")
        print("5. 专业产品摄影风格")
        print("6. 完美适合放置身份证")
        
        return True
        
    except Exception as e:
        print(f"❌ 程序运行出错: {e}")
        return False

if __name__ == "__main__":
    generate_marble_countertop()
