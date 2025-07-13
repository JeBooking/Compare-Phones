"""
测试EXIF完整性检测器
"""

import os
import sys
from exif_integrity_checker import check_exif_integrity
from photo_analyzer import analyze_photo

def test_integrity_checker():
    """测试完整性检测器"""
    print("=== EXIF完整性检测器测试 ===\n")
    
    # 测试文件路径
    test_files = []
    
    # 查找测试图片
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff', '.tif')):
                test_files.append(os.path.join(root, file))
    
    if not test_files:
        print("未找到测试图片文件")
        print("请在当前目录放置一些图片文件进行测试")
        return
    
    # 测试每个文件
    for i, file_path in enumerate(test_files[:5]):  # 只测试前5个文件
        print(f"\n--- 测试文件 {i+1}: {file_path} ---")
        
        try:
            # 使用完整性检测器
            result = check_exif_integrity(file_path=file_path)
            
            print(f"是否被修改: {'是' if result['is_modified'] else '否'}")
            print(f"置信度: {result['confidence']:.2%}")
            
            if result['indicators']:
                print("修改指标:")
                for indicator in result['indicators']:
                    print(f"  • {indicator}")
            
            if result['warnings']:
                print("警告:")
                for warning in result['warnings']:
                    print(f"  • {warning}")
            
            # 显示一些详细信息
            if 'timestamps' in result['details']:
                timestamps = result['details']['timestamps']
                print("时间戳信息:")
                for field, value in timestamps.items():
                    if value:
                        print(f"  {field}: {value}")
            
            if 'device_info' in result['details']:
                device_info = result['details']['device_info']
                print("设备信息:")
                for field, value in device_info.items():
                    if value:
                        print(f"  {field}: {value}")
            
            if 'editing_software' in result['details']:
                print(f"检测到编辑软件: {result['details']['editing_software']}")
                
        except Exception as e:
            print(f"测试失败: {e}")

def test_with_analyzer():
    """测试与分析器的集成"""
    print("\n\n=== 与照片分析器集成测试 ===\n")
    
    # 查找测试图片
    test_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff', '.tif')):
                test_files.append(os.path.join(root, file))
    
    if not test_files:
        print("未找到测试图片文件")
        return
    
    # 测试第一个文件
    file_path = test_files[0]
    print(f"测试文件: {file_path}")
    
    try:
        result = analyze_photo(file_path)
        
        print(f"分析成功: {result['success']}")
        
        if result['success']:
            print("\n设备信息:")
            for key, value in result['device_info'].items():
                print(f"  {key}: {value}")
            
            print("\n完整性检查:")
            integrity = result['integrity_check']
            print(f"  是否被修改: {'是' if integrity['is_modified'] else '否'}")
            print(f"  置信度: {integrity['confidence']:.2%}")
            
            if integrity['indicators']:
                print("  修改指标:")
                for indicator in integrity['indicators']:
                    print(f"    • {indicator}")
        
        if result['error']:
            print(f"错误: {result['error']}")
            
    except Exception as e:
        print(f"集成测试失败: {e}")

def create_demo_results():
    """创建演示结果"""
    print("\n\n=== 演示不同检测结果 ===\n")
    
    # 模拟不同的检测结果
    demo_results = [
        {
            'name': '原始照片（未修改）',
            'is_modified': False,
            'confidence': 0.1,
            'indicators': [],
            'warnings': ['未找到GPS信息']
        },
        {
            'name': '轻微异常照片',
            'is_modified': False,
            'confidence': 0.4,
            'indicators': ['时间戳不一致: DateTime和DateTimeOriginal相差2.5小时'],
            'warnings': ['未知制造商: Unknown']
        },
        {
            'name': '可能被编辑的照片',
            'is_modified': True,
            'confidence': 0.8,
            'indicators': [
                '检测到图像编辑软件: Adobe Photoshop',
                '缺失关键EXIF字段: DateTimeOriginal',
                '异常ISO值: 204800'
            ],
            'warnings': []
        }
    ]
    
    for demo in demo_results:
        print(f"--- {demo['name']} ---")
        print(f"是否被修改: {'是' if demo['is_modified'] else '否'}")
        print(f"置信度: {demo['confidence']:.2%}")
        
        if demo['indicators']:
            print("修改指标:")
            for indicator in demo['indicators']:
                print(f"  • {indicator}")
        
        if demo['warnings']:
            print("警告:")
            for warning in demo['warnings']:
                print(f"  • {warning}")
        
        print()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 测试指定文件
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            print(f"测试文件: {file_path}")
            result = check_exif_integrity(file_path=file_path)
            
            print(f"是否被修改: {'是' if result['is_modified'] else '否'}")
            print(f"置信度: {result['confidence']:.2%}")
            
            if result['indicators']:
                print("修改指标:")
                for indicator in result['indicators']:
                    print(f"  • {indicator}")
            
            if result['warnings']:
                print("警告:")
                for warning in result['warnings']:
                    print(f"  • {warning}")
        else:
            print(f"文件不存在: {file_path}")
    else:
        # 运行所有测试
        test_integrity_checker()
        test_with_analyzer()
        create_demo_results()
