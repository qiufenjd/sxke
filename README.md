# 声修客

> 一站式专业音频处理平台，为您提供极致的音频转换体验

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0.1-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 项目简介

**声修客** 是一个基于 Flask 的在线音频处理平台，提供简洁高效的音频格式转换和变速处理服务。用户无需下载任何软件，即可在浏览器中完成音频文件的格式转换和播放速度调整。

## 核心功能

### 格式转换
支持多种主流音频格式之间的相互转换：
- **输入格式：** MP3、WAV、OGG、FLAC、M4A、AAC
- **输出格式：** MP3、WAV、FLAC、OGG
- **音质保证：** 采用专业编解码器，确保转换后的音频质量

### 变速处理
提供精确的播放速度调整功能：
- **速度范围：** 0.5x ~ 2.0x，步进 0.1
- **音高保持：** 调整速度时不改变音高
- **应用场景：** 语言学习、视频剪辑、音乐制作等

### 便捷上传
- 支持**拖放上传**，操作直观便捷
- 支持**点击选择**，传统方式同样可用
- 文件大小限制：500MB

### 访问统计
内置访问计数器，实时显示网站访问次数

## 技术架构

### 后端技术
- **Flask 2.0.1** - 轻量级 Web 框架
- **pydub 0.25.1** - 音频处理核心库
- **FFmpeg** - 底层音频编解码引擎
- **Werkzeug 2.0.3** - 安全的文件上传处理

### 前端技术
- **原生 JavaScript (ES6+)** - 无框架依赖，轻量高效
- **CSS3** - 响应式设计，适配多种设备
- **Fetch API** - 异步文件上传
- **拖放 API** - 直观的文件交互体验

## 快速开始

### 环境要求
- Python 3.12+
- FFmpeg（系统依赖）

### 安装步骤

1. 克隆项目
```bash
git clone https://github.com/qiufenjd/sxke.git
cd sxke-two
```

2. 安装 Python 依赖
```bash
pip install -r requirements.txt
```

3. 安装 FFmpeg

**Windows:**
- 从 [FFmpeg 官网](https://ffmpeg.org/download.html) 下载
- 解压并配置环境变量

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**CentOS:**
```bash
sudo yum install epel-release
sudo yum install ffmpeg ffmpeg-devel
```

4. 启动服务
```bash
python app.py
```

5. 访问应用
打开浏览器访问：http://localhost/ip:5000/

## 项目结构

```
sxke-two/
├── app.py              # Flask 主应用
├── config.py           # 配置文件
├── requirements.txt    # Python 依赖
├── templates/
│   └── index.html      # 主页面模板
├── static/
│   ├── css/style.css   # 样式文件
│   └── js/upload.js    # 前端交互逻辑
├── temp_uploads/       # 临时上传目录（自动创建）
├── converted_files/    # 转换文件目录（自动创建）
└── visit_count.txt     # 访问计数文件
```

## 使用说明

1. 打开网站首页
2. 选择音频文件（拖放或点击选择）
3. 设置目标格式和播放速度
4. 点击"开始转换"按钮
5. 等待转换完成，下载转换后的文件

## 配置说明

编辑 `config.py` 文件可以自定义以下配置：

```python
class Config:
    SECRET_KEY = 'your-secret-key-here'      # Flask 密钥
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024    # 最大文件大小（500MB）
    UPLOAD_FOLDER = 'temp_uploads'            # 临时上传目录
    CONVERTED_FOLDER = 'converted_files'     # 转换文件目录
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac', 'm4a', 'aac'}
```

## 项目特点

- 轻量高效 - 无需安装客户端，即开即用
- 响应式设计 - 完美适配桌面和移动设备
- 实时反馈 - 转换进度、用时统计一目了然
- 安全可靠 - 文件自动清理，保护用户隐私
- 界面美观 - 现代化 UI 设计，操作流畅

## 常见问题

### Q: 转换失败怎么办？
A: 请检查文件格式是否支持，确保 FFmpeg 已正确安装。

### Q: 文件大小有限制吗？
A: 默认限制为 500MB，可在 `config.py` 中修改。

### Q: 转换后的文件会保存多久？
A: 转换后的文件会保存在服务器上，建议及时下载。原始文件会在转换后自动删除。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件至：qfjob1@163.com

---

**声修客** - 让音频处理变得简单高效
