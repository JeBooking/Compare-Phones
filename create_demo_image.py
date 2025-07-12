#!/usr/bin/env python3
"""
创建一个带有EXIF数据的演示图片
用于测试照片设备识别器
"""

from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
import os

def create_demo_image():
    """创建一个带有模拟EXIF数据的演示图片"""
    
    # 创建一个简单的图片
    width, height = 800, 600
    image = Image.new('RGB', (width, height), color='lightblue')
    
    # 在图片上添加一些文字
    try:
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(image)
        
        # 尝试使用系统字体
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        text = "Demo Photo for Device Detection"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        draw.text((x, y), text, fill='darkblue', font=font)
        draw.text((x, y + 60), "Test Image with EXIF Data", fill='darkblue', font=font)
        
    except ImportError:
        print("PIL ImageDraw not available, creating simple image")
    
    # 创建EXIF数据字典
    exif_dict = {
        "0th": {},
        "Exif": {},
        "GPS": {},
        "1st": {},
        "thumbnail": None
    }
    
    # 添加基本的EXIF信息
    # 注意：这里使用的是EXIF标签的数字ID
    exif_dict["0th"][271] = "Apple"  # Make
    exif_dict["0th"][272] = "iPhone 13 Pro"  # Model
    exif_dict["0th"][305] = "iOS 15.0"  # Software
    exif_dict["0th"][274] = 1  # Orientation
    exif_dict["0th"][282] = (72, 1)  # XResolution
    exif_dict["0th"][283] = (72, 1)  # YResolution
    exif_dict["0th"][296] = 2  # ResolutionUnit
    
    exif_dict["Exif"][36867] = "2023:12:01 14:30:00"  # DateTimeOriginal
    exif_dict["Exif"][33434] = (1, 60)  # ExposureTime (1/60s)
    exif_dict["Exif"][33437] = (18, 10)  # FNumber (f/1.8)
    exif_dict["Exif"][34855] = 100  # ISOSpeedRatings
    exif_dict["Exif"][37386] = (26, 10)  # FocalLength (2.6mm)
    exif_dict["Exif"][37385] = 16  # Flash (no flash)
    exif_dict["Exif"][37384] = 0  # LightSource
    exif_dict["Exif"][41987] = 0  # WhiteBalance (auto)
    exif_dict["Exif"][41986] = 0  # ExposureMode (auto)
    exif_dict["Exif"][37383] = 5  # MeteringMode (pattern)
    
    # 保存图片
    output_path = "demo_photo.jpg"
    
    try:
        # 尝试使用piexif库来添加EXIF数据
        import piexif
        exif_bytes = piexif.dump(exif_dict)
        image.save(output_path, "JPEG", exif=exif_bytes, quality=95)
        print(f"✅ 成功创建带有EXIF数据的演示图片: {output_path}")
        
    except ImportError:
        # 如果没有piexif，就保存普通图片
        image.save(output_path, "JPEG", quality=95)
        print(f"⚠️  创建了演示图片但没有EXIF数据: {output_path}")
        print("   要添加EXIF数据，请安装piexif: pip install piexif")
    
    return output_path

def create_simple_demo():
    """创建一个简单的演示图片（不需要额外依赖）"""
    
    # 创建一个渐变背景的图片
    width, height = 1200, 800
    image = Image.new('RGB', (width, height))
    
    # 创建渐变效果
    for y in range(height):
        for x in range(width):
            r = int(255 * (x / width))
            g = int(255 * (y / height))
            b = int(255 * ((x + y) / (width + height)))
            image.putpixel((x, y), (r, g, b))
    
    # 保存图片
    output_path = "simple_demo.jpg"
    image.save(output_path, "JPEG", quality=90)
    print(f"✅ 创建了简单演示图片: {output_path}")
    return output_path

if __name__ == "__main__":
    print("=== 演示图片生成器 ===\n")
    
    print("1. 尝试创建带有EXIF数据的演示图片...")
    demo_path = create_demo_image()
    
    print("\n2. 创建简单演示图片...")
    simple_path = create_simple_demo()
    
    print(f"\n演示图片已创建:")
    print(f"- {demo_path}")
    print(f"- {simple_path}")
    
    print(f"\n你可以使用这些图片来测试照片设备识别器:")
    print(f"python test_analyzer.py {demo_path}")
    print(f"python test_analyzer.py {simple_path}")
    
    print(f"\n或者启动Web服务器并上传这些图片:")
    print(f"python app.py")
