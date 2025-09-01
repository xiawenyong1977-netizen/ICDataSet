# 中文身份证图像生成项目

这是一个用于生成逼真中文身份证图像的项目，包含多种生成方法和数据增强技术。

## 项目简介

本项目实现了中文身份证的自动化生成，包括：
- 真实身份证图像生成
- 数据增强和图像处理
- 批量处理功能
- 多种背景和材质生成

## 主要功能

### 1. 身份证生成
- `chinese_id_gen.py` - 基础身份证生成器
- `chinese_id_gen_realistic.py` - 高真实感身份证生成器
- `face_gen_advanced.py` - 高级人脸生成器

### 2. 数据增强
- `batch_augment.py` - 批量数据增强
- `generate_multiple_augmentations.py` - 多种增强方法
- `visualize_augmentation.py` - 增强效果可视化

### 3. 背景生成
- `generate_simple_backgrounds.py` - 简单背景生成
- `generate_marble_countertops.py` - 大理石台面背景
- `generate_20_bedsheets.py` - 床单背景
- `generate_20_wooden_desks.py` - 木桌背景

### 4. 图像处理
- `batch_remove_bg.py` - 批量背景移除
- `simple_view.py` - 简单图像查看器
- `view_all_augmentations.py` - 查看所有增强效果

## 环境要求

- Python 3.7+
- OpenCV
- PIL/Pillow
- NumPy
- 其他依赖见requirements.txt

## 安装和使用

1. 克隆项目
```bash
git clone [your-repo-url]
cd chinese_id
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行示例
```bash
python chinese_id_gen.py
```

## 项目结构

```
chinese_id/
├── chinese_id_gen.py              # 基础身份证生成
├── chinese_id_gen_realistic.py    # 高真实感生成
├── face_gen_advanced.py           # 高级人脸生成
├── batch_augment.py               # 批量增强
├── generate_multiple_augmentations.py  # 多种增强
├── generate_simple_backgrounds.py # 背景生成
├── batch_remove_bg.py             # 背景移除
├── simple_view.py                 # 图像查看
├── visualize_augmentation.py      # 增强可视化
├── id_card_template_front.png     # 身份证正面模板
├── id_card_template_back.png      # 身份证背面模板
├── pretrained_models/             # 预训练模型
└── README_desktop_backgrounds.md  # 背景生成说明
```

## 使用说明

### 生成身份证
```python
python chinese_id_gen.py
```

### 批量数据增强
```python
python batch_augment.py
```

### 生成背景
```python
python generate_simple_backgrounds.py
```

## 注意事项

- 本项目仅用于研究和学习目的
- 生成的图像不应用于非法用途
- 请遵守相关法律法规

## 贡献

欢迎提交Issue和Pull Request来改进项目。

## 许可证

本项目采用MIT许可证。

## 更新日志

详见项目文档和提交历史。
