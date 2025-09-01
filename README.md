# ICDataSet - 身份证和微信截图数据集生成工具

这是一个用于生成身份证图像和微信截图数据集的Python项目，主要用于机器学习训练和测试。

## 项目结构

```
ICDataSet/
├── chinese_id/          # 身份证图像生成模块
│   ├── chinese_ids/     # 生成的身份证图像
│   ├── faces/           # 人脸图像
│   ├── pretrained_models/ # 预训练模型
│   └── desktop_backgrounds/ # 桌面背景图像
├── wcscreen/            # 微信截图生成模块
│   ├── output/          # 生成的微信截图
│   └── training_mode.py # 训练模式脚本
├── doc/                 # 项目文档
└── downloaded_data/     # 下载的数据
```

## 功能特性

### 身份证图像生成
- 支持中文姓名生成
- 多种背景样式（桌面、咖啡厅、图书馆等）
- 图像增强和数据增强
- 批量生成功能

### 微信截图生成
- 模拟真实微信界面
- 支持多种聊天场景
- 头像和昵称生成
- 训练模式支持

## 环境要求

- Python 3.7+
- Conda环境：wechat-classifier

## 安装依赖

```bash
conda activate wechat-classifier
pip install -r requirements.txt
```

## 使用方法

### 生成身份证图像
```bash
cd chinese_id
python chinese_id_gen.py
```

### 生成微信截图
```bash
cd wcscreen
python genwechat.py
```

## 许可证

本项目仅供学习和研究使用。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。
