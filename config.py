"""
配置文件 - 照片设备识别器
"""

import os

class Config:
    """应用配置类"""
    
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this-in-production'
    
    # 文件上传配置
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'tiff', 'tif', 'bmp'}
    
    # 服务器配置
    HOST = '0.0.0.0'  # 允许外部访问，如果只想本地访问可改为 '127.0.0.1'
    PORT = 5000
    DEBUG = True  # 生产环境中应设为False
    
    # EXIF数据提取配置
    EXTRACT_DETAILED_EXIF = True  # 是否提取详细的EXIF数据
    INCLUDE_THUMBNAIL = False     # 是否包含缩略图信息
    
    # 支持的EXIF字段映射（中文显示名称）
    EXIF_FIELD_MAPPING = {
        # 设备信息
        'Make': '制造商',
        'Model': '型号',
        'Software': '软件版本',
        'LensModel': '镜头型号',
        'LensMake': '镜头制造商',
        
        # 拍摄参数
        'DateTime': '拍摄时间',
        'DateTimeOriginal': '原始拍摄时间',
        'ExposureTime': '曝光时间',
        'FNumber': '光圈',
        'ISOSpeedRatings': 'ISO',
        'FocalLength': '焦距',
        'Flash': '闪光灯',
        'WhiteBalance': '白平衡',
        'ExposureMode': '曝光模式',
        'MeteringMode': '测光模式',
        'SceneCaptureType': '场景模式',
        
        # 图像信息
        'ImageWidth': '图像宽度',
        'ImageLength': '图像高度',
        'Orientation': '方向',
        'XResolution': '水平分辨率',
        'YResolution': '垂直分辨率',
        'ResolutionUnit': '分辨率单位',
        'ColorSpace': '色彩空间',
        
        # GPS信息
        'GPSLatitude': 'GPS纬度',
        'GPSLongitude': 'GPS经度',
        'GPSAltitude': 'GPS海拔',
        'GPSTimeStamp': 'GPS时间',
    }
    
    # 需要特殊处理的字段
    SPECIAL_FIELDS = {
        'FNumber': lambda x: f"f/{x}",
        'FocalLength': lambda x: f"{x}mm",
        'ExposureTime': lambda x: f"{x}秒" if float(x) >= 1 else f"1/{int(1/float(x))}秒",
        'Flash': {
            0: '未闪光',
            1: '闪光',
            5: '闪光，未检测到回闪',
            7: '闪光，检测到回闪',
            9: '强制闪光',
            13: '强制闪光，未检测到回闪',
            15: '强制闪光，检测到回闪',
            16: '未闪光，强制关闭',
            24: '未闪光，自动模式',
            25: '闪光，自动模式',
            29: '闪光，自动模式，未检测到回闪',
            31: '闪光，自动模式，检测到回闪',
        },
        'WhiteBalance': {
            0: '自动',
            1: '手动',
        },
        'ExposureMode': {
            0: '自动曝光',
            1: '手动曝光',
            2: '自动包围曝光',
        },
        'MeteringMode': {
            0: '未知',
            1: '平均测光',
            2: '中央重点测光',
            3: '点测光',
            4: '多点测光',
            5: '评价测光',
            6: '局部测光',
        },
        'Orientation': {
            1: '正常',
            2: '水平翻转',
            3: '旋转180度',
            4: '垂直翻转',
            5: '水平翻转+逆时针旋转90度',
            6: '顺时针旋转90度',
            7: '水平翻转+顺时针旋转90度',
            8: '逆时针旋转90度',
        }
    }

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    HOST = '127.0.0.1'

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-must-set-a-secret-key-in-production'

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
