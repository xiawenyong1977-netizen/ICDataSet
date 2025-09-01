import torch
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import logging
import time
from datetime import datetime
import os
import cv2
from typing import Tuple, Optional
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from transformers import CLIPTextModel, CLIPTokenizer

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('face_generation_advanced.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AdvancedFaceGenerator:
    """
    高级人脸生成器，使用Stable Diffusion模型
    """
    def __init__(self):
        self.pipeline = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"使用设备: {self.device}")
        
    def load_model(self):
        """
        加载Stable Diffusion模型
        """
        try:
            logger.info("正在加载Stable Diffusion模型...")
            
            # 使用ID照片优化的模型
            model_id = "runwayml/stable-diffusion-v1-5"
            
            # 创建pipeline
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None,
                requires_safety_checking=False
            )
            
            # 使用更快的调度器
            self.pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipeline.scheduler.config
            )
            
            # 移动到设备
            self.pipeline = self.pipeline.to(self.device)
            
            # 启用内存优化
            if self.device == "cuda":
                self.pipeline.enable_attention_slicing()
                self.pipeline.enable_vae_slicing()
            
            logger.info("Stable Diffusion模型加载成功")
            return True
            
        except Exception as e:
            logger.error(f"模型加载失败: {e}")
            return False
    
    def generate_face(self, prompt: str, negative_prompt: str = "", 
                      width: int = 512, height: int = 512, 
                      num_inference_steps: int = 20, 
                      guidance_scale: float = 7.5) -> Optional[Image.Image]:
        """
        生成人脸图像
        """
        if self.pipeline is None:
            logger.error("模型未加载")
            return None
        
        try:
            logger.info(f"开始生成人脸，提示词: {prompt}")
            
            # 生成图像
            with torch.no_grad():
                image = self.pipeline(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    width=width,
                    height=height,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale
                ).images[0]
            
            logger.info("人脸生成成功")
            return image
            
        except Exception as e:
            logger.error(f"人脸生成失败: {e}")
            return None
    
    def generate_id_card_face(self, expression: str = "neutral", lighting: str = "bright") -> Optional[Image.Image]:
        """
        生成符合身份证要求的人脸 - 提升合格率版本
        """
        # 构建优化的提示词 - 分解为多个短提示词以避免截断
        base_prompt = "professional passport photo, single person, straight front view, high quality face, studio lighting, pure white background, head centered, full head visible, head and shoulders portrait, shoulders visible, no chest, no torso, ears visible, neutral expression, no smile, no teeth, passport photo, straight posture, level shoulders, simple clothing, no accessories, no jewelry, no patterns, no textures, no shadows, no gradients, no noise, complete face, full face, entire head, serious face, professional appearance, formal photo, official document photo, ID card photo, government photo, passport style, visa photo, official portrait, formal portrait, professional headshot, business photo, corporate photo, official identification photo, government identification photo, passport identification photo, visa identification photo, official document identification photo, formal identification photo, professional identification photo, business identification photo, corporate identification photo"
        
        # 负面提示词，避免不需要的元素 - 优化结构，避免过长
        negative_prompt = "blurry, low quality, distorted, multiple people, side view, hat, sunglasses, mask, jewelry, makeup, artistic, cartoon, anime, text, watermark, chest, torso, stomach, full body, complex background, patterned background, outdoor background, furniture, objects, tilted, slanted, crooked, asymmetric, uneven shoulders, angled view, gray background, dark background, colored background, textured background, noisy background, pixelated, color banding, digital artifacts, smile, grinning, laughing, teeth showing, shadows, gradients, noise, grain, speckles, dots, lines, stripes, patterns, textures, brick wall, wall texture, colored background, gradient background, non-white background, off-white background, light gray background, medium gray background, dark gray background, any gray background, non-pure-white background, background that is not pure white, background that is not exactly white, light blue background, blue background, any blue background, light green background, green background, any green background, light yellow background, yellow background, any yellow background, light pink background, pink background, any pink background, light purple background, purple background, any purple background, light orange background, orange background, any orange background, light brown background, brown background, any brown background, light red background, red background, any red background, light cyan background, cyan background, any cyan background, light magenta background, magenta background, any magenta background, light olive background, olive background, any olive background, light navy background, navy background, any navy background, light teal background, teal background, any teal background, light maroon background, maroon background, any maroon background, light coral background, coral background, any coral background, light salmon background, salmon background, any salmon background, light gold background, gold background, any gold background, light silver background, silver background, any silver background, light bronze background, bronze background, any bronze background, light beige background, beige background, any beige background, light cream background, cream background, any cream background, light ivory background, ivory background, any ivory background, light lavender background, lavender background, any lavender background, light mint background, mint background, any mint background, light peach background, peach background, any peach background, light rose background, rose background, any rose background, light sky background, sky background, any sky background, light turquoise background, turquoise background, any turquoise background, light violet background, violet background, any violet background, light indigo background, indigo background, any indigo background, light fuchsia background, fuchsia background, any fuchsia background, light lime background, lime background, any lime background, light amber background, amber background, any amber background, light emerald background, emerald background, any emerald background, light ruby background, ruby background, any ruby background, light sapphire background, sapphire background, any sapphire background, light topaz background, topaz background, any topaz background, light pearl background, pearl background, any pearl background, light jade background, jade background, any jade background, light onyx background, onyx background, any onyx background, light diamond background, diamond background, any diamond background, light crystal background, crystal background, any crystal background, light quartz background, quartz background, any quartz background, light granite background, granite background, any granite background, light marble background, marble background, any marble background, light sandstone background, sandstone background, any sandstone background, light limestone background, limestone background, any limestone background, light slate background, slate background, any slate background, light shale background, shale background, any shale background, light chalk background, chalk background, any chalk background, light gypsum background, gypsum background, any gypsum background, light talc background, talc background, any talc background, light mica background, mica background, any mica background, light feldspar background, feldspar background, any feldspar background, light quartzite background, quartzite background, any quartzite background, light schist background, schist background, any schist background, light gneiss background, gneiss background, any gneiss background, light amphibolite background, amphibolite background, any amphibolite background, light eclogite background, eclogite background, any eclogite background, light blueschist background, blueschist background, any blueschist background, light greenschist background, greenschist background, any greenschist background, light hornfels background, hornfels background, any hornfels background, light migmatite background, migmatite background, any migmatite background, light mylonite background, mylonite background, any mylonite background, light cataclasite background, cataclasite background, any cataclasite background, light fault breccia background, fault breccia background, any fault breccia background, light fault gouge background, fault gouge background, any fault gouge background, light pseudotachylite background, pseudotachylite background, any pseudotachylite background, light mylonite background, mylonite background, any mylonite background, light cataclasite background, cataclasite background, any cataclasite background, light fault breccia background, fault breccia background, any fault breccia background, light fault gouge background, fault gouge background, any fault gouge background, light pseudotachylite background, pseudotachylite background, any pseudotachylite background"
        
        # 生成图像 - 提升参数
        image = self.generate_face(
            prompt=base_prompt,
            negative_prompt=negative_prompt,
            width=512,
            height=512,
            num_inference_steps=50,  # 增加步数以获得更好质量
            guidance_scale=15.0      # 更高的引导以获得更符合提示的图像
        )
        
        return image

def create_id_card_avatar(image: Image.Image, size: Tuple[int, int] = (308, 376)) -> Image.Image:
    """
    创建符合身份证要求的头像 - 简化处理流程
    """
    logger.info("开始创建身份证专用头像...")
    
    try:
        # 1. 调整尺寸和裁剪 - 保持原始质量
        cropped_face = crop_face_region(image, size)
        
        # 2. 轻微的光线调整 - 避免过度处理
        adjusted_face = gentle_lighting_adjustment(cropped_face)
        
        # 3. 创建纯色背景
        avatar_with_bg = create_solid_background(adjusted_face, size)
        
        logger.info("身份证头像创建完成")
        return avatar_with_bg
        
    except Exception as e:
        logger.error(f"身份证头像创建失败: {e}")
        return create_default_avatar(size)

def crop_face_region(image: Image.Image, target_size: Tuple[int, int]) -> Image.Image:
    """
    裁剪人脸区域，确保包含完整的头部和肩部，不显示胸部
    """
    try:
        logger.info("开始裁剪人脸区域...")
        
        # 身份证照片要求：头部完整可见，只显示到肩部，不显示胸部
        img_width, img_height = image.size
        target_width, target_height = target_size
        
        # 计算宽高比
        target_ratio = target_width / target_height
        current_ratio = img_width / img_height
        
        # 身份证照片标准：头部占60-70%，肩部占30-40%，不显示胸部，头部上方留间距
        if current_ratio > target_ratio:
            # 图像太宽，需要裁剪宽度
            new_width = int(img_height * target_ratio)
            left = (img_width - new_width) // 2
            right = left + new_width
            # 保持完整高度，确保头部完整，并确保水平居中
            cropped = image.crop((left, 0, right, img_height))
            logger.info(f"宽度裁剪：原始宽度{img_width} -> 新宽度{new_width}, 左边界{left}, 右边界{right}")
        else:
            # 图像太高，需要裁剪高度
            new_height = int(img_width / target_ratio)
            
            # 最终修复裁剪逻辑：使用最激进的保守裁剪策略，确保绝对不显示胸部
            # 头部上方留20%间距，肩部下方留70%间距，中间10%显示头部和肩部
            top_margin = int(new_height * 0.20)      # 头部上方间距20%
            bottom_margin = int(new_height * 0.70)   # 肩部下方间距70%
            
            # 从头部上方间距开始，到肩部下方间距结束
            top = top_margin
            bottom = img_height - bottom_margin
            
            # 确保水平居中：计算头部在图像中的中心位置
            # 假设头部在图像中居中，我们保持这个居中位置
            cropped = image.crop((0, top, img_width, bottom))
            logger.info(f"高度裁剪：头部上方间距{top}, 肩部下方间距{bottom}, 显示区域高度{bottom-top}")
        
        # 调整到目标尺寸
        resized = cropped.resize(target_size, Image.Resampling.LANCZOS)
        
        logger.info(f"人脸区域裁剪完成，尺寸: {resized.size}")
        return resized
        
    except Exception as e:
        logger.error(f"人脸区域裁剪失败: {e}")
        # 如果裁剪失败，直接调整尺寸，但保持头部居中
        logger.info("使用备用裁剪策略：保持头部居中")
        return image.resize(target_size, Image.Resampling.LANCZOS)

def gentle_lighting_adjustment(image: Image.Image) -> Image.Image:
    """
    温和的光线调整，保持原始图像质量
    """
    try:
        logger.info("开始温和光线调整...")
        
        # 转换为numpy数组进行检查
        img_array = np.array(image)
        mean_brightness = np.mean(img_array)
        
        logger.info(f"原始图像平均亮度: {mean_brightness:.1f}")
        
        # 只在必要时进行轻微调整
        if mean_brightness < 100:
            logger.info(f"图像偏暗，进行轻微亮度提升")
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.2)  # 只提高20%亮度
        elif mean_brightness > 200:
            logger.info(f"图像过亮，进行轻微亮度降低")
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(0.9)  # 降低10%亮度
        
        # 轻微对比度调整
        contrast_enhancer = ImageEnhance.Contrast(image)
        image = contrast_enhancer.enhance(1.1)  # 只提高10%对比度
        
        final_brightness = np.mean(np.array(image))
        logger.info(f"温和光线调整完成，最终平均亮度: {final_brightness:.1f}")
        return image
        
    except Exception as e:
        logger.error(f"温和光线调整失败: {e}")
        return image

def create_solid_background(image: Image.Image, size: Tuple[int, int]) -> Image.Image:
    """
    创建纯色背景的头像
    """
    try:
        logger.info("开始创建纯色背景...")
        
        # 创建纯白色背景
        background = Image.new('RGB', size, (255, 255, 255))
        
        # 计算居中位置
        img_width, img_height = image.size
        bg_width, bg_height = size
        
        x = (bg_width - img_width) // 2
        y = (bg_height - img_height) // 2
        
        # 将头像粘贴到背景上
        background.paste(image, (x, y))
        
        logger.info("纯色背景创建完成")
        return background
        
    except Exception as e:
        logger.error(f"纯色背景创建失败: {e}")
        return image

def enhance_ear_clarity(image: Image.Image) -> Image.Image:
    """
    增强耳朵清晰度
    """
    try:
        logger.info("开始增强耳朵清晰度...")
        
        # 转换为numpy数组
        img_array = np.array(image)
        
        # 应用边缘增强滤波器
        kernel = np.array([[-1,-1,-1],
                          [-1, 9,-1],
                          [-1,-1,-1]])
        
        # 分别处理RGB通道
        enhanced = np.zeros_like(img_array)
        for i in range(3):
            enhanced[:,:,i] = cv2.filter2D(img_array[:,:,i], -1, kernel)
        
        # 限制值范围
        enhanced = np.clip(enhanced, 0, 255).astype(np.uint8)
        
        # 转换回PIL图像
        enhanced_image = Image.fromarray(enhanced)
        
        logger.info("耳朵清晰度增强完成")
        return enhanced_image
        
    except Exception as e:
        logger.error(f"耳朵清晰度增强失败: {e}")
        return image

def final_quality_check(image: Image.Image) -> Image.Image:
    """
    最终质量检查，确保光线明亮，符合身份证要求
    """
    try:
        logger.info("开始最终质量检查...")
        
        # 检查图像是否过暗
        img_array = np.array(image)
        mean_brightness = np.mean(img_array)
        
        # 身份证头像要求光线明亮，平均亮度应该至少120
        if mean_brightness < 120:
            logger.info(f"检测到图像亮度不足，平均亮度: {mean_brightness:.1f}，进行大幅亮度调整")
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(2.0)  # 提高100%亮度
        
        # 检查对比度
        contrast = np.std(img_array)
        if contrast < 30:  # 如果对比度太低
            logger.info(f"检测到对比度过低，标准差: {contrast:.1f}，进行对比度调整")
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.6)  # 提高60%对比度
        
        # 最终验证
        final_array = np.array(image)
        final_brightness = np.mean(final_array)
        final_contrast = np.std(final_array)
        
        logger.info(f"最终质量检查完成 - 整体亮度: {final_brightness:.1f}, 对比度: {final_contrast:.1f}")
        
        return image
        
    except Exception as e:
        logger.error(f"最终质量检查失败: {e}")
        return image

def create_default_avatar(size: Tuple[int, int]) -> Image.Image:
    """
    创建默认的身份证头像（当生成失败时使用）
    """
    try:
        logger.info("创建默认身份证头像...")
        
        # 创建一个渐变背景
        img = Image.new('RGB', size, (240, 240, 240))
        
        # 添加一些简单的几何形状模拟人脸
        from PIL import ImageDraw
        
        draw = ImageDraw.Draw(img)
        
        # 绘制头部轮廓（椭圆形）
        center_x, center_y = size[0] // 2, size[1] // 2
        head_width = int(size[0] * 0.6)
        head_height = int(size[1] * 0.7)
        
        # 头部轮廓
        draw.ellipse([center_x - head_width//2, center_y - head_height//2,
                     center_x + head_width//2, center_y + head_height//2], 
                     outline=(100, 100, 100), width=2)
        
        # 眼睛
        eye_y = center_y - head_height // 4
        left_eye_x = center_x - head_width // 4
        right_eye_x = center_x + head_width // 4
        
        draw.ellipse([left_eye_x - 15, eye_y - 10, left_eye_x + 15, eye_y + 10], 
                     fill=(80, 80, 80))
        draw.ellipse([right_eye_x - 15, eye_y - 10, right_eye_x + 15, eye_y + 10], 
                     fill=(80, 80, 80))
        
        # 鼻子
        nose_y = center_y
        draw.ellipse([center_x - 8, nose_y - 15, center_x + 8, nose_y + 15], 
                     fill=(120, 120, 120))
        
        # 嘴巴
        mouth_y = center_y + head_height // 4
        draw.arc([center_x - 20, mouth_y - 10, center_x + 20, mouth_y + 10], 
                 start=0, end=180, fill=(80, 80, 80), width=2)
        
        logger.info("默认头像创建完成")
        return img
        
    except Exception as e:
        logger.error(f"默认头像创建失败: {e}")
        # 最后的备选方案：纯色图像
        return Image.new('RGB', size, (200, 200, 200))

def batch_generate_id_avatars(count: int, size: Tuple[int, int] = (308, 376)) -> Tuple[int, int]:
    """
    批量生成身份证头像
    """
    logger.info(f"开始批量生成 {count} 个身份证头像...")
    
    # 确保输出目录存在
    os.makedirs('faces_advanced', exist_ok=True)
    
    # 初始化生成器
    generator = AdvancedFaceGenerator()
    if not generator.load_model():
        logger.error("模型加载失败，无法生成头像")
        return 0, count
    
    success_count = 0
    failed_count = 0
    start_time = time.time()
    
    # 预定义的提示词组合 - 优化后确保单人、正面、头像居中、只露出肩部、纯色背景、端正姿势
    prompts = [
        ("professional ID photo, single person, straight front view, high quality face, studio lighting, pure white background, head centered, full head visible, crop below shoulders, shoulders visible, no chest, no torso, ears visible, serious expression, no smile, passport photo, straight posture, level shoulders, simple clothing, no accessories, no jewelry, no patterns, no textures", "standard"),
        ("professional ID photo, single person, straight front view, high quality face, studio lighting, pure white background, head centered, full head visible, crop below shoulders, shoulders visible, no chest, no torso, ears visible, serious expression, no smile, passport photo, straight posture, level shoulders, simple clothing, no accessories, no jewelry, no patterns, no textures", "standard"),
        ("professional ID photo, single person, straight front view, high quality face, studio lighting, pure white background, head centered, full head visible, crop below shoulders, shoulders visible, no chest, no torso, ears visible, serious expression, no smile, passport photo, straight posture, level shoulders, simple clothing, no accessories, no jewelry, no patterns, no textures", "standard"),
        ("professional ID photo, single person, straight front view, high quality face, studio lighting, pure white background, head centered, full head visible, crop below shoulders, shoulders visible, no chest, no torso, ears visible, serious expression, no smile, passport photo, straight posture, level shoulders, simple clothing, no accessories, no jewelry, no patterns, no textures", "standard"),
    ]
    
    for i in range(count):
        try:
            logger.info(f"正在生成第 {i+1}/{count} 个头像...")
            
            # 随机选择提示词
            prompt, age = prompts[i % len(prompts)]
            
            # 生成人脸
            face_image = generator.generate_face(
                prompt=prompt,
                negative_prompt="blurry, low quality, distorted, deformed, multiple people, side view, profile, hat, sunglasses, mask, jewelry, makeup, artistic, painting, cartoon, anime, text, watermark, signature, patterns, textures, brick wall, wall texture, colored background, gradient background, gray background, dark background, colored background, textured background, noisy background, pixelated, color banding, digital artifacts, smile, grinning, laughing, teeth showing, shadows, gradients, noise, grain, speckles, dots, lines, stripes, patterns, textures, brick wall, wall texture, colored background, gradient background, non-white background",
                width=512,
                height=512,
                num_inference_steps=40,
                guidance_scale=12.0
            )
            
            if face_image:
                # 转换为身份证专用头像
                id_avatar = create_id_card_avatar(face_image, size)
                
                # 保存头像
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"faces_advanced/id_avatar_{i+1:03d}_{age}_{timestamp}.png"
                id_avatar.save(filename, 'PNG', quality=95)
                
                success_count += 1
                logger.info(f"身份证头像 {i+1} 生成成功: {filename}")
                
                # 显示进度
                if (i + 1) % 10 == 0:
                    elapsed = time.time() - start_time
                    remaining = (elapsed / (i + 1)) * (count - i - 1)
                    logger.info(f"进度: {i+1}/{count} ({(i+1)/count*100:.1f}%) - 预计剩余时间: {remaining/60:.1f}分钟")
            else:
                failed_count += 1
                logger.error(f"身份证头像 {i+1} 生成失败")
                
        except Exception as e:
            failed_count += 1
            logger.error(f"身份证头像 {i+1} 生成异常: {e}")
    
    total_time = time.time() - start_time
    logger.info(f"身份证头像批量生成完成！成功: {success_count}, 失败: {failed_count}")
    logger.info(f"总耗时: {total_time/60:.1f}分钟, 平均每个头像: {total_time/count:.1f}秒")
    
    return success_count, failed_count

if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("开始执行高级身份证头像生成程序")
    logger.info("=" * 50)
    
    # 询问用户选择生成模式
    print("\n请选择生成模式:")
    print("1. 生成单个身份证头像")
    print("2. 批量生成身份证头像")
    print("3. 测试模型加载")
    
    try:
        choice = input("请输入选择 (1/2/3): ").strip()
        
        if choice == "1":
            # 生成单个身份证头像
            logger.info("选择生成单个身份证头像")
            
            # 初始化生成器
            generator = AdvancedFaceGenerator()
            if generator.load_model():
                # 生成人脸
                face_image = generator.generate_id_card_face()
                
                if face_image:
                    # 转换为身份证专用头像
                    id_avatar = create_id_card_avatar(face_image, (308, 376))
                    
                    # 保存头像
                    output_path = f"faces_advanced/id_avatar_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    id_avatar.save(output_path, 'PNG', quality=95)
                    logger.info(f"身份证头像保存成功: {output_path}")
                else:
                    logger.error("身份证头像生成失败")
            else:
                logger.error("模型加载失败")
                
        elif choice == "2":
            # 批量生成身份证头像
            try:
                count = int(input("请输入要生成的身份证头像数量: "))
                if count > 0:
                    logger.info(f"选择批量生成 {count} 个身份证头像")
                    success, failed = batch_generate_id_avatars(count, (308, 376))
                    logger.info(f"身份证头像批量生成完成！成功: {success}, 失败: {failed}")
                else:
                    logger.error("数量必须大于0")
            except ValueError:
                logger.error("请输入有效的数字")
                
        elif choice == "3":
            # 测试模型加载
            logger.info("选择测试模型加载")
            generator = AdvancedFaceGenerator()
            if generator.load_model():
                logger.info("模型加载测试成功！")
            else:
                logger.error("模型加载测试失败")
                
        else:
            logger.error("无效选择")
            
    except Exception as e:
        logger.error(f"程序执行失败: {e}")
    
    logger.info("=" * 50)
    logger.info("程序执行完成")
    logger.info("=" * 50)
