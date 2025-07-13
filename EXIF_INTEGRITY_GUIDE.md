# EXIF完整性检测功能说明

## 功能概述

EXIF完整性检测功能可以帮助识别照片的EXIF信息是否被修改过。该功能通过分析EXIF数据中的各种指标来判断照片是否经过编辑软件处理。

## 检测原理

### 1. 软件签名检测
- 检查EXIF中的Software、ProcessingSoftware等字段
- 识别常见的图像编辑软件标识（如Adobe Photoshop、GIMP等）
- 检测可疑的软件版本模式

### 2. 时间戳一致性检查
- 比较DateTime、DateTimeOriginal、DateTimeDigitized等时间字段
- 检测时间戳之间的异常差异（超过1小时）
- 验证时间格式的有效性

### 3. 设备信息一致性
- 检查制造商（Make）和型号（Model）的匹配性
- 验证是否为已知的相机/手机制造商
- 检测制造商与型号的逻辑一致性

### 4. 关键字段完整性
- 检查关键EXIF字段是否缺失
- 验证必要的拍摄参数是否存在

### 5. 异常值检测
- 检测异常的ISO值（过高或过低）
- 检测异常的焦距值
- 识别不合理的拍摄参数

## 检测结果说明

### 置信度等级
- **0-30%**: 绿色 - EXIF数据完整，未发现修改痕迹
- **30-70%**: 黄色 - EXIF数据存在异常，可能被修改
- **70-100%**: 红色 - EXIF数据很可能被修改

### 结果字段
- `is_modified`: 布尔值，是否被修改
- `confidence`: 浮点数（0-1），修改的置信度
- `indicators`: 列表，检测到的修改指标
- `warnings`: 列表，警告信息
- `details`: 字典，详细的检测信息

## 使用方法

### 1. 通过Web界面
1. 启动服务器：`python app.py`
2. 打开浏览器访问 `http://localhost:5000`
3. 上传照片，查看完整性检查结果

### 2. 命令行使用
```bash
# 检测单个文件
python exif_integrity_checker.py photo.jpg

# 运行测试
python test_integrity_checker.py

# 测试指定文件
python test_integrity_checker.py photo.jpg
```

### 3. 编程接口
```python
from exif_integrity_checker import check_exif_integrity

# 检测文件
result = check_exif_integrity(file_path="photo.jpg")

# 检测文件流
with open("photo.jpg", "rb") as f:
    result = check_exif_integrity(file_stream=f)

print(f"是否被修改: {result['is_modified']}")
print(f"置信度: {result['confidence']:.2%}")
```

## 检测指标说明

### 常见修改指标
1. **检测到图像编辑软件**: 在Software字段中发现编辑软件标识
2. **时间戳不一致**: 不同时间字段之间存在异常差异
3. **制造商与型号不匹配**: 设备信息逻辑不一致
4. **缺失关键EXIF字段**: 重要的拍摄信息丢失
5. **异常参数值**: ISO、焦距等参数超出正常范围

### 常见警告信息
1. **未知制造商**: 无法识别的相机制造商
2. **无法解析时间字段**: 时间格式异常
3. **未找到GPS信息**: 缺少位置信息（正常现象）

## 注意事项

### 检测限制
1. **不是100%准确**: 检测结果仅供参考，不能作为法律证据
2. **误报可能**: 某些正常照片可能被误判为修改过
3. **漏报可能**: 高级的编辑技术可能绕过检测

### 影响因素
1. **相机设置**: 某些相机设置可能导致异常的EXIF数据
2. **传输过程**: 文件传输或转换可能影响EXIF信息
3. **软件版本**: 不同版本的编辑软件留下的痕迹不同

### 最佳实践
1. **结合多种方法**: 不要仅依赖EXIF检测，结合其他技术手段
2. **了解设备特性**: 熟悉不同相机/手机的EXIF特征
3. **保持更新**: 定期更新检测规则和软件签名库

## 技术实现

### 核心类
- `ExifIntegrityChecker`: 主要的检测类
- 包含多个检测方法，每个方法负责特定的检测任务

### 依赖库
- `PIL (Pillow)`: 图像处理和EXIF读取
- `exifread`: 详细的EXIF数据提取
- `datetime`: 时间处理
- `re`: 正则表达式匹配

### 扩展性
- 可以轻松添加新的检测规则
- 支持自定义软件签名库
- 可以调整置信度计算算法

## 更新日志

### v1.0.0
- 基础的EXIF完整性检测功能
- 支持软件签名、时间戳、设备信息检测
- Web界面集成
- 命令行工具支持
