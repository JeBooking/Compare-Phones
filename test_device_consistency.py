"""
测试设备信息一致性检查的改进
"""

from exif_integrity_checker import ExifIntegrityChecker

def test_device_consistency():
    """测试设备一致性检查"""
    
    print("=== 设备信息一致性检查测试 ===\n")
    
    # 测试用例：(制造商, 型号, 预期结果)
    test_cases = [
        # 正常匹配的情况
        ("Canon", "EOS R5", "应该匹配"),
        ("Canon", "PowerShot G7X", "应该匹配"),
        ("Nikon", "D850", "应该匹配"),
        ("Nikon", "Z7 II", "应该匹配"),
        ("Sony", "Alpha 7R IV", "应该匹配"),
        ("Sony", "RX100 VII", "应该匹配"),
        ("Apple", "iPhone 13 Pro", "应该匹配"),
        ("Samsung", "Galaxy S21", "应该匹配"),
        ("Huawei", "P40 Pro", "应该匹配"),
        ("Xiaomi", "Mi 11", "应该匹配"),
        
        # 不匹配的情况
        ("Canon", "D850", "不应该匹配 - Nikon型号"),
        ("Nikon", "EOS R5", "不应该匹配 - Canon型号"),
        ("Sony", "iPhone 13", "不应该匹配 - Apple型号"),
        ("Apple", "Galaxy S21", "不应该匹配 - Samsung型号"),
        ("Samsung", "Mi 11", "不应该匹配 - Xiaomi型号"),
        
        # 未知制造商
        ("UnknownBrand", "Model123", "未知制造商"),
        ("MyCamera", "SuperShot", "未知制造商"),
        
        # 边界情况
        ("CANON", "eos r5", "大小写不敏感"),
        ("canon", "EOS R5", "大小写不敏感"),
        ("Sony", "ALPHA 7R IV", "大小写不敏感"),
    ]
    
    checker = ExifIntegrityChecker()
    
    for i, (make, model, expected) in enumerate(test_cases, 1):
        print(f"{i:2d}. 测试: {make} - {model}")
        print(f"    预期: {expected}")
        
        # 创建模拟的EXIF数据
        pil_data = {'Make': make, 'Model': model}
        exifread_data = {}
        
        # 创建结果容器
        result = {
            'indicators': [],
            'warnings': [],
            'details': {}
        }
        
        # 调用设备一致性检查方法
        checker._check_device_consistency(pil_data, exifread_data, result)
        
        # 分析结果
        has_mismatch = any('不匹配' in indicator for indicator in result['indicators'])
        has_unknown = any('未知制造商' in warning for warning in result['warnings'])
        
        if "不应该匹配" in expected:
            status = "✅ 正确检测到不匹配" if has_mismatch else "❌ 未检测到不匹配"
        elif "未知制造商" in expected:
            status = "✅ 正确检测到未知制造商" if has_unknown else "❌ 未检测到未知制造商"
        else:  # 应该匹配
            status = "✅ 正确匹配" if not has_mismatch and not has_unknown else "❌ 误报不匹配"
        
        print(f"    结果: {status}")
        
        if result['indicators']:
            for indicator in result['indicators']:
                print(f"    指标: {indicator}")
        
        if result['warnings']:
            for warning in result['warnings']:
                print(f"    警告: {warning}")
        
        print()

def test_manufacturer_patterns():
    """测试制造商模式匹配"""
    
    print("=== 制造商模式匹配测试 ===\n")
    
    # 从代码中提取的制造商模式
    manufacturer_patterns = {
        'canon': ['canon', 'eos', 'powershot', 'rebel'],
        'nikon': ['nikon', 'd', 'coolpix', 'z'],
        'sony': ['sony', 'alpha', 'a7', 'rx', 'fx'],
        'apple': ['iphone', 'ipad'],
        'samsung': ['samsung', 'galaxy', 'sm-'],
        'huawei': ['huawei', 'mate', 'p', 'nova', 'honor'],
        'xiaomi': ['xiaomi', 'mi', 'redmi', 'poco'],
        'fujifilm': ['fujifilm', 'x-', 'gfx'],
        'olympus': ['olympus', 'om-', 'e-m', 'pen'],
        'panasonic': ['panasonic', 'lumix', 'gh', 'gx'],
        'leica': ['leica', 'q', 'm', 's'],
        'pentax': ['pentax', 'k-', 'ricoh']
    }
    
    # 测试每个制造商的模式
    for manufacturer, patterns in manufacturer_patterns.items():
        print(f"{manufacturer.upper()}:")
        print(f"  模式: {patterns}")
        
        # 测试一些真实的型号
        real_models = {
            'canon': ['EOS R5', 'EOS 5D Mark IV', 'PowerShot G7X', 'Rebel T8i'],
            'nikon': ['D850', 'D780', 'Z7 II', 'COOLPIX P1000'],
            'sony': ['Alpha 7R IV', 'A7 III', 'RX100 VII', 'FX3'],
            'apple': ['iPhone 13 Pro', 'iPad Pro'],
            'samsung': ['Galaxy S21', 'SM-G991B'],
            'huawei': ['P40 Pro', 'Mate 40', 'Nova 8'],
            'xiaomi': ['Mi 11', 'Redmi Note 10', 'POCO F3'],
        }
        
        if manufacturer in real_models:
            for model in real_models[manufacturer]:
                model_lower = model.lower()
                matches = any(pattern in model_lower for pattern in patterns)
                status = "✅" if matches else "❌"
                print(f"    {status} {model}")
        
        print()

if __name__ == "__main__":
    test_device_consistency()
    test_manufacturer_patterns()
    
    print("=== 总结 ===")
    print("改进后的设备一致性检查:")
    print("1. 支持更多制造商（12个主要品牌）")
    print("2. 每个制造商都有完整的型号模式匹配")
    print("3. 统一的检查逻辑，易于维护和扩展")
    print("4. 更准确的匹配检测，减少误报和漏报")
