from PIL import Image
from PIL.ExifTags import TAGS
import exifread
import os
import io
from datetime import datetime
from config import Config

# ==================== 主要分析函数 ====================

def analyze_photo_from_stream(file_stream):
    """
    从文件流中分析照片的EXIF数据，提取设备信息

    Args:
        file_stream: Flask文件对象

    Returns:
        dict: 包含设备信息的字典
    """
    result = {
        'success': False,
        'device_info': {},
        'technical_info': {},
        'error': None
    }

    try:
        # 读取文件内容到内存
        file_stream.seek(0)  # 确保从文件开头读取
        file_content = file_stream.read()

        # 创建BytesIO对象用于PIL
        image_io = io.BytesIO(file_content)

        # 创建BytesIO对象用于exifread
        exifread_io = io.BytesIO(file_content)

        # 使用PIL读取EXIF数据
        pil_data = extract_exif_with_pil_stream(image_io)

        # 使用exifread读取更详细的EXIF数据
        exifread_data = extract_exif_with_exifread_stream(exifread_io)

        # 合并数据
        device_info = {}
        technical_info = {}

        # 提取设备信息
        device_fields = ['Make', 'Model', 'Software', 'LensModel', 'LensMake']
        for field in device_fields:
            value = None
            if field in pil_data:
                value = pil_data[field]
            elif f'Image {field}' in exifread_data:
                value = str(exifread_data[f'Image {field}'])
            elif f'EXIF {field}' in exifread_data:
                value = str(exifread_data[f'EXIF {field}'])

            if value:
                chinese_name = Config.EXIF_FIELD_MAPPING.get(field, field)
                device_info[chinese_name] = value

        # 提取技术信息
        technical_fields = ['DateTime', 'DateTimeOriginal', 'ExposureTime', 'FNumber',
                          'ISOSpeedRatings', 'FocalLength', 'Flash', 'WhiteBalance',
                          'ExposureMode', 'MeteringMode', 'Orientation']

        for field in technical_fields:
            value = None
            if field in pil_data:
                value = pil_data[field]
            elif f'EXIF {field}' in exifread_data:
                value = str(exifread_data[f'EXIF {field}'])
            elif f'Image {field}' in exifread_data:
                value = str(exifread_data[f'Image {field}'])

            if value:
                # 应用特殊格式化
                if field in Config.SPECIAL_FIELDS:
                    formatter = Config.SPECIAL_FIELDS[field]
                    if callable(formatter):
                        try:
                            value = formatter(value)
                        except Exception as e:
                            print(f"格式化字段 {field} 时出错: {e}")
                            value = str(value)
                    elif isinstance(formatter, dict):
                        try:
                            # 对于字典映射，尝试转换为整数作为键
                            key = int(float(str(value)))
                            value = formatter.get(key, str(value))
                        except:
                            value = formatter.get(str(value), str(value))

                chinese_name = Config.EXIF_FIELD_MAPPING.get(field, field)
                technical_info[chinese_name] = value

        # 获取图片基本信息
        try:
            image_io.seek(0)  # 重置到开头
            with Image.open(image_io) as img:
                technical_info['图片尺寸'] = f"{img.width} x {img.height}"
                technical_info['图片格式'] = img.format
                if hasattr(img, 'mode'):
                    technical_info['颜色模式'] = img.mode
        except Exception as e:
            print(f"获取图片基本信息时出错: {e}")

        result['device_info'] = device_info
        result['technical_info'] = technical_info
        result['success'] = True

        # 如果没有找到设备信息，提供提示
        if not device_info:
            result['error'] = '未能从照片中提取到设备信息，可能是因为：\n1. 照片没有EXIF数据\n2. EXIF数据已被清除\n3. 照片格式不支持EXIF'

    except Exception as e:
        result['error'] = f'分析照片时出错: {str(e)}'

    return result

def analyze_photo(image_path):
    """
    分析照片的EXIF数据，提取设备信息
    
    Args:
        image_path (str): 图片文件路径
        
    Returns:
        dict: 包含设备信息的字典
    """
    result = {
        'success': False,
        'device_info': {},
        'technical_info': {},
        'error': None
    }
    
    try:
        # 检查文件是否存在
        if not os.path.exists(image_path):
            result['error'] = '文件不存在'
            return result
        
        # 使用PIL读取EXIF数据
        pil_data = extract_exif_with_pil(image_path)
        
        # 使用exifread读取更详细的EXIF数据
        exifread_data = extract_exif_with_exifread(image_path)
        
        # 合并数据
        device_info = {}
        technical_info = {}
        
        # 提取设备信息
        device_fields = ['Make', 'Model', 'Software', 'LensModel', 'LensMake']
        for field in device_fields:
            value = None
            if field in pil_data:
                value = pil_data[field]
            elif f'Image {field}' in exifread_data:
                value = str(exifread_data[f'Image {field}'])
            elif f'EXIF {field}' in exifread_data:
                value = str(exifread_data[f'EXIF {field}'])

            if value:
                chinese_name = Config.EXIF_FIELD_MAPPING.get(field, field)
                device_info[chinese_name] = value
        
        # 提取技术信息
        technical_fields = ['DateTime', 'DateTimeOriginal', 'ExposureTime', 'FNumber',
                          'ISOSpeedRatings', 'FocalLength', 'Flash', 'WhiteBalance',
                          'ExposureMode', 'MeteringMode', 'Orientation']

        for field in technical_fields:
            value = None
            if field in pil_data:
                value = pil_data[field]
            elif f'EXIF {field}' in exifread_data:
                value = str(exifread_data[f'EXIF {field}'])
            elif f'Image {field}' in exifread_data:
                value = str(exifread_data[f'Image {field}'])

            if value:
                # 应用特殊格式化
                if field in Config.SPECIAL_FIELDS:
                    formatter = Config.SPECIAL_FIELDS[field]
                    if callable(formatter):
                        try:
                            value = formatter(value)
                        except Exception as e:
                            print(f"格式化字段 {field} 时出错: {e}")
                            value = str(value)
                    elif isinstance(formatter, dict):
                        try:
                            # 对于字典映射，尝试转换为整数作为键
                            key = int(float(str(value)))
                            value = formatter.get(key, str(value))
                        except:
                            value = formatter.get(str(value), str(value))

                chinese_name = Config.EXIF_FIELD_MAPPING.get(field, field)
                technical_info[chinese_name] = value
        
        # 获取图片基本信息
        try:
            with Image.open(image_path) as img:
                technical_info['图片尺寸'] = f"{img.width} x {img.height}"
                technical_info['图片格式'] = img.format
                if hasattr(img, 'mode'):
                    technical_info['颜色模式'] = img.mode
        except Exception as e:
            print(f"获取图片基本信息时出错: {e}")
        
        result['device_info'] = device_info
        result['technical_info'] = technical_info
        result['success'] = True
        
        # 如果没有找到设备信息，提供提示
        if not device_info:
            result['error'] = '未能从照片中提取到设备信息，可能是因为：\n1. 照片没有EXIF数据\n2. EXIF数据已被清除\n3. 照片格式不支持EXIF'
        
    except Exception as e:
        result['error'] = f'分析照片时出错: {str(e)}'
    
    return result

def extract_exif_with_pil(image_path):
    """使用PIL提取EXIF数据"""
    exif_data = {}
    try:
        with Image.open(image_path) as image:
            exifdata = image.getexif()
            if exifdata is not None:
                for tag_id in exifdata:
                    tag = TAGS.get(tag_id, tag_id)
                    data = exifdata.get(tag_id)
                    if isinstance(data, bytes):
                        try:
                            data = data.decode('utf-8')
                        except:
                            data = str(data)
                    exif_data[tag] = data
    except Exception as e:
        print(f"PIL EXIF extraction error: {e}")
    
    return exif_data

def extract_exif_with_pil_stream(image_stream):
    """使用PIL从流中提取EXIF数据"""
    exif_data = {}
    try:
        image_stream.seek(0)
        with Image.open(image_stream) as image:
            exifdata = image.getexif()
            if exifdata is not None:
                for tag_id in exifdata:
                    tag = TAGS.get(tag_id, tag_id)
                    data = exifdata.get(tag_id)
                    if isinstance(data, bytes):
                        try:
                            data = data.decode('utf-8')
                        except:
                            data = str(data)
                    exif_data[tag] = data
    except Exception as e:
        print(f"PIL EXIF extraction error: {e}")

    return exif_data

def extract_exif_with_exifread_stream(file_stream):
    """使用exifread从流中提取EXIF数据"""
    exif_data = {}
    try:
        file_stream.seek(0)
        tags = exifread.process_file(file_stream)
        for tag in tags.keys():
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                exif_data[tag] = tags[tag]
    except Exception as e:
        print(f"exifread extraction error: {e}")

    return exif_data

def extract_exif_with_exifread(image_path):
    """使用exifread提取EXIF数据"""
    exif_data = {}
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)
            for tag in tags.keys():
                if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                    exif_data[tag] = tags[tag]
    except Exception as e:
        print(f"exifread extraction error: {e}")

    return exif_data

if __name__ == "__main__":
    # 测试函数
    import sys
    if len(sys.argv) > 1:
        result = analyze_photo(sys.argv[1])
        print("设备信息:")
        for key, value in result['device_info'].items():
            print(f"  {key}: {value}")
        print("\n技术信息:")
        for key, value in result['technical_info'].items():
            print(f"  {key}: {value}")
        if result['error']:
            print(f"\n错误: {result['error']}")
    else:
        print("用法: python photo_analyzer.py <图片路径>")
