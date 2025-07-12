# 照片设备识别器

这是一个Python Web应用，可以分析上传的照片并识别拍摄设备信息。

## 功能特点

- 📱 识别照片拍摄设备的制造商和型号
- 🔧 提取技术参数（曝光时间、光圈、ISO、焦距等）
- 🌐 友好的Web界面，支持拖拽上传
- 📊 详细的EXIF数据分析
- 🎨 现代化的响应式设计

## 安装要求

### 1. 安装Python
请确保系统已安装Python 3.7或更高版本。

**Windows用户：**
- 访问 https://www.python.org/downloads/
- 下载并安装最新版本的Python
- 安装时勾选"Add Python to PATH"

**验证安装：**
```bash
python --version
# 或
python3 --version
```

### 2. 安装项目依赖

```bash
# 克隆或下载项目后，进入项目目录
cd ComparePhone

# 安装依赖
pip install -r requirements.txt
# 或
pip3 install -r requirements.txt
```

## 快速开始

### Windows用户
双击运行 `start_server.bat` 文件，脚本会自动检查依赖并启动服务器。

### 手动启动
```bash
# 启动Flask应用
python app.py
# 或
python3 app.py
```

### 测试功能
```bash
# 创建演示图片
python create_demo_image.py

# 测试分析功能
python test_analyzer.py demo_photo.jpg
```

启动后，在浏览器中访问：http://localhost:5000

## 使用方法

1. 打开Web界面
2. 点击上传区域或拖拽照片到指定区域
3. 选择要分析的照片文件
4. 等待分析完成
5. 查看设备信息和技术参数

## 支持的文件格式

- JPEG (.jpg, .jpeg)
- PNG (.png)
- TIFF (.tiff, .tif)
- BMP (.bmp)
- GIF (.gif)

## 项目结构

```
ComparePhone/
├── app.py                 # Flask主应用
├── photo_analyzer.py      # 照片分析核心模块
├── config.py             # 配置文件
├── requirements.txt      # Python依赖列表
├── start_server.bat      # Windows启动脚本
├── test_analyzer.py      # 测试脚本
├── create_demo_image.py  # 演示图片生成器
├── templates/
│   └── index.html       # Web界面模板
├── uploads/             # 临时上传文件夹（自动创建）
└── README.md            # 项目说明
```

## 技术栈

- **后端：** Flask (Python Web框架)
- **图像处理：** Pillow (PIL)
- **EXIF读取：** exifread
- **前端：** HTML5, CSS3, JavaScript
- **文件上传：** Werkzeug

## 注意事项

1. **隐私保护：** 上传的照片仅用于临时分析，分析完成后立即删除
2. **文件大小限制：** 最大支持16MB的图片文件
3. **EXIF数据：** 某些照片可能没有EXIF数据或数据已被清除
4. **网络安全：** 生产环境中请修改`app.py`中的`secret_key`

## 常见问题

### Q: 为什么有些照片无法识别设备信息？
A: 可能的原因：
- 照片没有EXIF数据
- EXIF数据已被社交媒体或图片编辑软件清除
- 照片格式不支持EXIF数据

### Q: 如何提高识别准确性？
A: 建议使用：
- 直接从相机或手机导出的原始照片
- 未经过压缩或编辑的照片
- 较新的照片格式（JPEG、TIFF等）

## 开发和扩展

如果你想扩展这个项目，可以考虑：

1. 添加更多EXIF字段的解析
2. 支持RAW格式照片
3. 添加批量处理功能
4. 集成机器学习模型进行设备识别
5. 添加照片地理位置信息提取

## 许可证

本项目仅供学习和研究使用。
