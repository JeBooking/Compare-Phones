#!/usr/bin/env python3
"""
测试照片分析器的简单脚本
用于验证photo_analyzer.py模块是否正常工作
"""

import os
import sys
from photo_analyzer import analyze_photo

def test_analyzer():
    """测试分析器功能"""
    print("=== 照片设备识别器测试 ===\n")
    
    # 检查是否提供了测试图片路径
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        print("请提供测试图片路径:")
        print("python test_analyzer.py <图片路径>")
        print("\n示例:")
        print("python test_analyzer.py test_photo.jpg")
        return
    
    # 检查文件是否存在
    if not os.path.exists(image_path):
        print(f"错误: 文件 '{image_path}' 不存在")
        return
    
    print(f"正在分析图片: {image_path}")
    print("-" * 50)
    
    try:
        # 分析照片
        result = analyze_photo(image_path)
        
        if result['success']:
            print("✅ 分析成功!\n")
            
            # 显示设备信息
            if result['device_info']:
                print("📱 设备信息:")
                for key, value in result['device_info'].items():
                    print(f"   {key}: {value}")
                print()
            else:
                print("📱 设备信息: 未找到设备信息\n")
            
            # 显示技术信息
            if result['technical_info']:
                print("🔧 技术参数:")
                for key, value in result['technical_info'].items():
                    print(f"   {key}: {value}")
                print()
            else:
                print("🔧 技术参数: 未找到技术信息\n")
            
            # 显示警告信息（如果有）
            if result['error']:
                print("⚠️  注意:")
                print(f"   {result['error']}\n")
                
        else:
            print("❌ 分析失败:")
            print(f"   {result['error']}")
    
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {str(e)}")

def check_dependencies():
    """检查依赖是否已安装"""
    print("检查依赖库...")
    
    missing_deps = []
    
    try:
        from PIL import Image
        print("✅ Pillow (PIL) - 已安装")
    except ImportError:
        print("❌ Pillow (PIL) - 未安装")
        missing_deps.append("Pillow")
    
    try:
        import exifread
        print("✅ exifread - 已安装")
    except ImportError:
        print("❌ exifread - 未安装")
        missing_deps.append("exifread")
    
    try:
        import flask
        print("✅ Flask - 已安装")
    except ImportError:
        print("❌ Flask - 未安装")
        missing_deps.append("Flask")
    
    if missing_deps:
        print(f"\n请安装缺失的依赖:")
        print(f"pip install {' '.join(missing_deps)}")
        return False
    else:
        print("\n✅ 所有依赖都已安装!")
        return True

if __name__ == "__main__":
    print("=== 照片设备识别器 - 依赖检查 ===\n")
    
    if check_dependencies():
        print("\n" + "="*50)
        test_analyzer()
    else:
        print("\n请先安装缺失的依赖，然后重新运行测试。")
