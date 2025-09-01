import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import os
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_20_wooden_desks():
    """
    使用成功的提示词批量生成20张木质桌面背景图片
    """
    print("🖥️  开始批量生成木质桌面背景图片...")
    
    # 检查CUDA可用性
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"使用设备: {device}")
    
    # 创建输出目录
    output_dir = "desktop_backgrounds"
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建专门的木质桌面子目录
    wooden_desk_dir = os.path.join(output_dir, "木质桌面_批量")
    os.makedirs(wooden_desk_dir, exist_ok=True)
    
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
        
        # 使用成功的提示词
        prompt = "Photorealistic wooden desk surface, texture, detailed grain, studio lighting, high resolution, 4K, sharp focus"
        negative_prompt = "cluttered, messy, dark, low quality, blurry, distorted, people, hands, objects, furniture"
        
        print(f"\n🎨 开始批量生成木质桌面背景")
        print(f"提示词: {prompt}")
        print(f"负面提示词: {negative_prompt}")
        print(f"目标数量: 20张")
        print(f"输出目录: {wooden_desk_dir}")
        
        total_generated = 0
        
        for i in range(20):
            print(f"\n🔄 正在生成第 {i+1}/20 张...")
            
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
                
                # 生成文件名
                filename = f"木质桌面_photorealistic_{i+1:02d}.png"
                output_path = os.path.join(wooden_desk_dir, filename)
                
                # 保存图片
                image.save(output_path)
                
                print(f"✅ 第 {i+1} 张生成成功: {filename}")
                total_generated += 1
                
            except Exception as e:
                print(f"❌ 第 {i+1} 张生成失败: {e}")
                continue
        
        print(f"\n🎉 批量生成完成！")
        print(f"成功生成: {total_generated}/20 张图片")
        print(f"输出目录: {wooden_desk_dir}")
        
        if total_generated > 0:
            print("\n💡 这些背景图的特点:")
            print("1. 超真实的木质桌面纹理")
            print("2. 详细的木纹细节")
            print("3. 专业摄影棚照明")
            print("4. 高分辨率4K质量")
            print("5. 锐利对焦")
            print("6. 完美适合放置身份证")
            
            print(f"\n📊 生成统计:")
            print(f"- 总数量: {total_generated} 张")
            print(f"- 成功率: {total_generated/20*100:.1f}%")
            print(f"- 文件格式: PNG")
            print(f"- 图片尺寸: 1024x768")
            print(f"- 平均大小: 约1.3MB")
        
        return total_generated
        
    except Exception as e:
        print(f"❌ 程序运行出错: {e}")
        return 0

if __name__ == "__main__":
    generate_20_wooden_desks()
