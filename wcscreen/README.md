# 微信聊天截图生成器

一个用于生成逼真微信聊天截图的Python工具，支持多种头像样式和自定义配置。

## 功能特性

- 🎨 **多种头像样式**
  - 几何图案头像（默认）：基于名字生成独特的几何图案
  - 简单纯色头像：简洁的纯色背景
  - 彩色渐变头像：彩虹渐变效果
  - 在线头像：支持在线API生成（需要网络）

- 💬 **真实的聊天界面**
  - 状态栏和导航栏
  - 时间戳显示
  - 消息气泡
  - 头像和用户名
  - 随机消息内容

- 🎯 **高度可定制**
  - 可调整消息数量
  - 可设置头像样式
  - 可自定义颜色主题
  - 支持不同的屏幕尺寸

## 安装依赖

```bash
# 激活conda环境
conda activate wechat-classifier

# 安装依赖包
pip install Pillow requests
```

## 使用方法

### 基本使用

```python
from genwechat import WeChatScreenshotGenerator

# 创建生成器实例
generator = WeChatScreenshotGenerator()

# 设置头像样式（可选）
generator.set_avatar_style("geometric")  # 几何图案头像

# 生成聊天截图
screenshot = generator.generate(num_messages=12)

# 保存截图
generator.save("wechat_screenshot.png")
```

### 头像样式设置

```python
# 几何图案头像（默认）
generator.set_avatar_style("geometric")

# 简单纯色头像
generator.set_avatar_style("simple")

# 彩色渐变头像
generator.set_avatar_style("colorful")

# 在线头像（需要网络）
generator.set_avatar_style("online")
```

### 运行脚本

1. **生成默认截图**：
   ```bash
   python genwechat.py
   ```

2. **查看不同头像样式**：
   ```bash
   python demo_avatars.py
   ```

3. **使用批处理文件**（Windows）：
   ```bash
   run_wechat.bat
   ```

## 配置选项

### 构造函数参数

```python
generator = WeChatScreenshotGenerator(
    width=750,      # 图片宽度
    height=1334     # 图片高度
)
```

### 头像设置

```python
# 设置头像大小
generator.avatar_size = 50

# 设置头像样式
generator.set_avatar_style("geometric")

# 启用在线头像
generator.use_online_avatars = True
```

### 颜色主题

```python
generator.colors = {
    "background": "#EDEDED",      # 背景色
    "friend_bubble": "#FFFFFF",   # 朋友消息气泡
    "my_bubble": "#95EC69",       # 我的消息气泡
    "friend_text": "#000000",     # 朋友消息文字
    "my_text": "#000000",         # 我的消息文字
    "name_text": "#8B8989"        # 用户名文字
}
```

## 输出文件

生成的截图保存在 `output/` 目录中：

- `wechat_conversation.png` - 默认生成的聊天截图
- `wechat_geometric_demo.png` - 几何图案头像演示
- `wechat_simple_demo.png` - 简单纯色头像演示
- `wechat_colorful_demo.png` - 彩色渐变头像演示

## 技术特点

- **基于名字的颜色生成**：使用哈希算法确保同一名字总是生成相同颜色
- **几何图案多样性**：支持圆形、三角形、矩形、菱形等图案
- **渐变效果**：平滑的颜色过渡和阴影效果
- **字体兼容性**：自动尝试多种字体，失败时使用默认字体
- **内存优化**：高效的图像处理和内存管理

## 故障排除

### 字体加载失败

如果遇到字体加载问题，脚本会自动尝试多种字体：
1. ~~微软雅黑 (msyh.ttf)~~ - 已注释，避免权限问题
2. 黑体 (simhei.ttf) - 主要字体
3. 宋体 (simsun.ttc) - 备选字体
4. Arial (arial.ttf) - 备选字体

如果所有字体都失败，会使用系统默认字体。

### 头像样式问题

- 确保PIL/Pillow库已正确安装
- 检查Python版本兼容性
- 验证图像处理权限

## 许可证

本项目仅供学习和研究使用。

## 贡献

欢迎提交Issue和Pull Request来改进这个工具！
