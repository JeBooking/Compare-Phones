"""
EXIF完整性检测演示脚本
"""

def demo_integrity_results():
    """演示不同的完整性检测结果"""
    
    print("=" * 60)
    print("EXIF完整性检测功能演示")
    print("=" * 60)
    
    # 模拟不同类型的检测结果
    demo_cases = [
        {
            'title': '📱 原始手机照片（未修改）',
            'result': {
                'is_modified': False,
                'confidence': 0.05,
                'indicators': [],
                'warnings': ['未找到GPS信息'],
                'details': {
                    'device_info': {'make': 'Apple', 'model': 'iPhone 13 Pro'},
                    'timestamps': {
                        'DateTime': '2024:01:15 14:30:25',
                        'DateTimeOriginal': '2024:01:15 14:30:25',
                        'DateTimeDigitized': '2024:01:15 14:30:25'
                    }
                }
            }
        },
        {
            'title': '📷 数码相机照片（轻微异常）',
            'result': {
                'is_modified': False,
                'confidence': 0.35,
                'indicators': ['时间戳不一致: DateTime和DateTimeOriginal相差1.5小时'],
                'warnings': ['异常焦距值: 1200mm'],
                'details': {
                    'device_info': {'make': 'Canon', 'model': 'EOS R5'},
                    'timestamps': {
                        'DateTime': '2024:01:15 16:00:25',
                        'DateTimeOriginal': '2024:01:15 14:30:25',
                        'DateTimeDigitized': '2024:01:15 14:30:25'
                    }
                }
            }
        },
        {
            'title': '🖼️ 经过编辑的照片（高度可疑）',
            'result': {
                'is_modified': True,
                'confidence': 0.85,
                'indicators': [
                    '检测到图像编辑软件: Adobe Photoshop CC 2023',
                    '缺失关键EXIF字段: DateTimeOriginal, Make',
                    '异常ISO值: 409600',
                    '制造商与型号可能不匹配'
                ],
                'warnings': ['无法解析时间字段 DateTime: Invalid format'],
                'details': {
                    'device_info': {'make': None, 'model': 'Unknown Camera'},
                    'editing_software': 'Adobe Photoshop CC 2023 (Windows)',
                    'timestamps': {
                        'DateTime': '2024:01:15 20:45:12',
                        'DateTimeOriginal': None,
                        'DateTimeDigitized': None
                    }
                }
            }
        }
    ]
    
    for i, case in enumerate(demo_cases, 1):
        print(f"\n{i}. {case['title']}")
        print("-" * 50)
        
        result = case['result']
        
        # 显示基本结果
        status = "⚠️ 可能被修改" if result['is_modified'] else "✅ 完整"
        confidence_percent = result['confidence'] * 100
        
        print(f"状态: {status}")
        print(f"修改置信度: {confidence_percent:.1f}%")
        
        # 显示置信度条
        bar_length = 30
        filled_length = int(bar_length * result['confidence'])
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        if confidence_percent < 30:
            color_desc = "（低风险 - 绿色）"
        elif confidence_percent < 70:
            color_desc = "（中等风险 - 黄色）"
        else:
            color_desc = "（高风险 - 红色）"
        
        print(f"置信度条: [{bar}] {color_desc}")
        
        # 显示检测指标
        if result['indicators']:
            print("\n🔍 检测到的异常指标:")
            for indicator in result['indicators']:
                print(f"   • {indicator}")
        
        # 显示警告
        if result['warnings']:
            print("\n⚠️ 警告信息:")
            for warning in result['warnings']:
                print(f"   • {warning}")
        
        # 显示设备信息
        if 'device_info' in result['details']:
            device = result['details']['device_info']
            print(f"\n📱 设备信息:")
            print(f"   制造商: {device.get('make', '未知')}")
            print(f"   型号: {device.get('model', '未知')}")
        
        # 显示时间戳信息
        if 'timestamps' in result['details']:
            timestamps = result['details']['timestamps']
            print(f"\n🕐 时间戳信息:")
            for field, value in timestamps.items():
                print(f"   {field}: {value or '缺失'}")
        
        # 显示编辑软件信息
        if 'editing_software' in result['details']:
            print(f"\n🛠️ 检测到编辑软件: {result['details']['editing_software']}")

def explain_detection_methods():
    """解释检测方法"""
    
    print("\n" + "=" * 60)
    print("EXIF完整性检测方法说明")
    print("=" * 60)
    
    methods = [
        {
            'name': '1. 软件签名检测',
            'description': '检查EXIF中的Software字段，识别图像编辑软件标识',
            'examples': ['Adobe Photoshop', 'GIMP', 'Lightroom', 'Snapseed']
        },
        {
            'name': '2. 时间戳一致性检查',
            'description': '比较DateTime、DateTimeOriginal等时间字段的一致性',
            'examples': ['时间差异超过1小时', '时间格式异常', '关键时间字段缺失']
        },
        {
            'name': '3. 设备信息验证',
            'description': '检查制造商和型号的匹配性，验证设备信息逻辑',
            'examples': ['Canon相机但型号不匹配', '未知制造商', '设备信息不完整']
        },
        {
            'name': '4. 参数异常检测',
            'description': '检测异常的拍摄参数值',
            'examples': ['ISO值过高(>102400)', '焦距异常(<1mm或>1000mm)', '光圈值异常']
        },
        {
            'name': '5. 关键字段完整性',
            'description': '检查重要EXIF字段是否缺失',
            'examples': ['缺少拍摄时间', '缺少设备信息', '缺少拍摄参数']
        }
    ]
    
    for method in methods:
        print(f"\n{method['name']}")
        print(f"   原理: {method['description']}")
        print("   示例:")
        for example in method['examples']:
            print(f"     • {example}")

def usage_examples():
    """使用示例"""
    
    print("\n" + "=" * 60)
    print("使用方法示例")
    print("=" * 60)
    
    print("\n1. 通过Web界面使用:")
    print("   • 运行: python app.py")
    print("   • 打开浏览器访问: http://localhost:5000")
    print("   • 上传照片查看完整性检查结果")
    
    print("\n2. 命令行使用:")
    print("   • 检测单个文件: python exif_integrity_checker.py photo.jpg")
    print("   • 运行测试: python test_integrity_checker.py")
    
    print("\n3. 编程接口:")
    print("""
   from exif_integrity_checker import check_exif_integrity
   
   # 检测文件
   result = check_exif_integrity(file_path="photo.jpg")
   print(f"是否被修改: {result['is_modified']}")
   print(f"置信度: {result['confidence']:.2%}")
   
   # 检测文件流
   with open("photo.jpg", "rb") as f:
       result = check_exif_integrity(file_stream=f)
   """)

if __name__ == "__main__":
    demo_integrity_results()
    explain_detection_methods()
    usage_examples()
    
    print("\n" + "=" * 60)
    print("注意事项:")
    print("• 检测结果仅供参考，不能作为法律证据")
    print("• 某些正常照片可能被误判，高级编辑技术可能绕过检测")
    print("• 建议结合多种方法进行综合判断")
    print("=" * 60)
