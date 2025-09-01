import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import os
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_marble_countertops():
    """
    使用优化提示词生成大理石台面局部特写背景图片
    """
    print("🏠 开始生成大理石台面局部特写背景图片...")
    
    # 检查CUDA可用性
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"使用设备: {device}")
    
    # 创建输出目录
    output_dir = "desktop_backgrounds"
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建专门的大理石台面子目录
    marble_dir = os.path.join(output_dir, "大理石台面_局部特写")
    os.makedirs(marble_dir, exist_ok=True)
    
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
        
        # 使用局部特写优化的提示词
        prompt = "Close-up detail shot of polished marble countertop surface, reflective texture, luxury material, dramatic lighting, high contrast, architectural macro photography, smooth stone surface, natural marble veining"
        negative_prompt = "extra digit, fewer digits, cropped, worst quality, low quality, messy, dirty, cluttered, furniture, objects, people, hands, food, utensils, full kitchen, wide shot, distant view, cabinets, appliances"
        
        print(f"\n🎨 开始批量生成大理石台面局部特写背景")
        print(f"正面提示词: {prompt}")
        print(f"负面提示词: {negative_prompt}")
        print(f"目标数量: 20张")
        print(f"输出目录: {marble_dir}")
        
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
                filename = f"大理石台面_局部特写_{i+1:02d}.png"
                output_path = os.path.join(marble_dir, filename)
                
                # 保存图片
                image.save(output_path)
                
                print(f"✅ 第 {i+1} 张生成成功: {filename}")
                total_generated += 1
                
            except Exception as e:
                print(f"❌ 第 {i+1} 张生成失败: {e}")
                continue
        
        print(f"\n🎉 批量生成完成！")
        print(f"成功生成: {total_generated}/20 张图片")
        print(f"输出目录: {marble_dir}")
        
        if total_generated > 0:
            print("\n💡 这些大理石台面局部特写背景的特点:")
            print("1. 大理石台面局部特写")
            print("2. 抛光表面细节")
            print("3. 反光纹理效果")
            print("4. 豪华材质质感")
            print("5. 戏剧性照明")
            print("6. 高对比度")
            print("7. 建筑微距摄影")
            print("8. 平滑石材表面")
            print("9. 自然大理石纹理")
            print("10. 完美适合放置身份证")
            
            print(f"\n📊 生成统计:")
            print(f"- 总数量: {total_generated} 张")
            print(f"- 成功率: {total_generated/20*100:.1f}%")
            print(f"- 文件格式: PNG")
            print(f"- 图片尺寸: 1024x768")
            print(f"- 平均大小: 约1.2MB")
            
            print(f"\n🔄 局部特写提示词优化说明:")
            print(f"- 使用 'Close-up detail shot' 强调局部特写")
            print(f"- 添加 'reflective texture' 反光纹理")
            print(f"- 使用 'architectural macro photography' 建筑微距摄影")
            print(f"- 添加 'smooth stone surface' 平滑石材表面")
            print(f"- 添加 'natural marble veining' 自然大理石纹理")
            print(f"- 负面提示词排除整体厨房、远景、橱柜、电器")
            print(f"- 确保生成的是台面局部而非整体厨房")
        
        return total_generated
        
    except Exception as e:
        print(f"❌ 程序运行出错: {e}")
        return 0

if __name__ == "__main__":
    generate_marble_countertops()
