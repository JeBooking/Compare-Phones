"""
EXIF完整性检测器 - 检测EXIF信息是否被修改
"""

import re
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import exifread
import io

class ExifIntegrityChecker:
    """EXIF完整性检测器"""
    
    def __init__(self):
        # 常见的EXIF编辑软件标识
        self.editing_software_signatures = [
            'Adobe Photoshop',
            'GIMP',
            'Paint.NET',
            'Canva',
            'Snapseed',
            'VSCO',
            'Lightroom',
            'Photoshop Express',
            'PicsArt',
            'Fotor'
        ]
        
        # 可疑的软件版本模式
        self.suspicious_software_patterns = [
            r'Adobe Photoshop.*',
            r'GIMP.*',
            r'.*Editor.*',
            r'.*Photo.*Editor.*'
        ]
    
    def check_integrity(self, pil_data, exifread_data):
        """
        检查EXIF数据的完整性

        Args:
            pil_data: 已解析的PIL EXIF数据
            exifread_data: 已解析的exifread EXIF数据

        Returns:
            dict: 完整性检查结果
        """
        result = {
            'is_modified': False,
            'confidence': 0.0,  # 0-1之间，1表示100%确定被修改
            'indicators': [],   # 修改指标列表
            'warnings': [],     # 警告信息
            'details': {}       # 详细信息
        }
        
        try:
            # 验证输入数据
            if pil_data is None:
                pil_data = {}
            if exifread_data is None:
                exifread_data = {}
            
            # 执行各种检测
            self._check_software_signatures(pil_data, exifread_data, result)
            self._check_timestamp_consistency(pil_data, exifread_data, result)
            self._check_device_consistency(pil_data, exifread_data, result)
            self._check_missing_critical_fields(pil_data, exifread_data, result)
            self._check_suspicious_values(pil_data, exifread_data, result)
            
            # 计算总体置信度
            self._calculate_confidence(result)
            
        except Exception as e:
            result['warnings'].append(f'检测过程中出错: {str(e)}')
        
        return result
    

    
    def _check_software_signatures(self, pil_data, exifread_data, result):
        """检查软件签名"""
        software_fields = ['Software', 'ProcessingSoftware', 'HostComputer']
        
        for field in software_fields:
            value = None
            if field in pil_data:
                value = str(pil_data[field])
            elif f'Image {field}' in exifread_data:
                value = str(exifread_data[f'Image {field}'])
            elif f'EXIF {field}' in exifread_data:
                value = str(exifread_data[f'EXIF {field}'])
            
            if value:
                # 检查是否包含编辑软件标识
                for signature in self.editing_software_signatures:
                    if signature.lower() in value.lower():
                        result['indicators'].append(f'检测到图像编辑软件: {signature}')
                        result['details']['editing_software'] = value
                        break
                
                # 检查可疑模式
                for pattern in self.suspicious_software_patterns:
                    if re.search(pattern, value, re.IGNORECASE):
                        result['indicators'].append(f'检测到可疑软件模式: {value}')
                        break
    
    def _check_timestamp_consistency(self, pil_data, exifread_data, result):
        """检查时间戳一致性"""
        time_fields = {
            'DateTime': None,
            'DateTimeOriginal': None,
            'DateTimeDigitized': None
        }
        
        # 提取时间字段
        for field in time_fields.keys():
            if field in pil_data:
                time_fields[field] = pil_data[field]
            elif f'EXIF {field}' in exifread_data:
                time_fields[field] = str(exifread_data[f'EXIF {field}'])
            elif f'Image {field}' in exifread_data:
                time_fields[field] = str(exifread_data[f'Image {field}'])
        
        # 检查时间一致性
        valid_times = []
        for field, value in time_fields.items():
            if value:
                try:
                    # 尝试解析时间
                    parsed_time = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                    valid_times.append((field, parsed_time))
                except:
                    result['warnings'].append(f'无法解析时间字段 {field}: {value}')
        
        # 检查时间差异
        if len(valid_times) >= 2:
            for i in range(len(valid_times)):
                for j in range(i + 1, len(valid_times)):
                    field1, time1 = valid_times[i]
                    field2, time2 = valid_times[j]
                    diff = abs((time1 - time2).total_seconds())
                    
                    # 如果时间差异超过1小时，可能被修改
                    if diff > 3600:
                        result['indicators'].append(f'时间戳不一致: {field1}和{field2}相差{diff/3600:.1f}小时')
        
        result['details']['timestamps'] = time_fields
    
    def _check_device_consistency(self, pil_data, exifread_data, result):
        """检查设备信息一致性"""
        make = None
        model = None
        
        # 提取制造商和型号
        if 'Make' in pil_data:
            make = pil_data['Make']
        elif 'Image Make' in exifread_data:
            make = str(exifread_data['Image Make'])
        
        if 'Model' in pil_data:
            model = pil_data['Model']
        elif 'Image Model' in exifread_data:
            model = str(exifread_data['Image Model'])
        
        # 检查制造商和型号的一致性
        if make and model:
            make_lower = make.lower()
            model_lower = model.lower()

            # 定义制造商和其对应的型号特征
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

            # 检查是否是已知制造商
            detected_manufacturer = None
            for manufacturer, patterns in manufacturer_patterns.items():
                if manufacturer in make_lower:
                    detected_manufacturer = manufacturer
                    break

            if not detected_manufacturer:
                result['warnings'].append(f'未知制造商: {make}')
            else:
                # 检查型号是否与制造商匹配
                patterns = manufacturer_patterns[detected_manufacturer]
                model_matches = any(pattern in model_lower for pattern in patterns)

                if not model_matches:
                    result['indicators'].append(f'制造商与型号可能不匹配: {make} - {model}')
        
        result['details']['device_info'] = {'make': make, 'model': model}
    
    def _check_missing_critical_fields(self, pil_data, exifread_data, result):
        """检查关键字段缺失"""
        critical_fields = ['Make', 'Model', 'DateTime']
        missing_fields = []
        
        for field in critical_fields:
            found = False
            if field in pil_data:
                found = True
            elif f'Image {field}' in exifread_data:
                found = True
            elif f'EXIF {field}' in exifread_data:
                found = True
            
            if not found:
                missing_fields.append(field)
        
        if missing_fields:
            result['indicators'].append(f'缺失关键EXIF字段: {", ".join(missing_fields)}')
            result['details']['missing_fields'] = missing_fields
    
    def _check_suspicious_values(self, pil_data, exifread_data, result):
        """检查可疑值"""
        # 检查异常的ISO值
        iso_value = None
        if 'ISOSpeedRatings' in pil_data:
            iso_value = pil_data['ISOSpeedRatings']
        elif 'EXIF ISOSpeedRatings' in exifread_data:
            try:
                iso_value = int(str(exifread_data['EXIF ISOSpeedRatings']))
            except:
                pass
        
        if iso_value:
            if iso_value > 102400 or iso_value < 25:
                result['indicators'].append(f'异常ISO值: {iso_value}')
        
        # 检查异常的焦距
        focal_length = None
        if 'FocalLength' in pil_data:
            focal_length = pil_data['FocalLength']
        elif 'EXIF FocalLength' in exifread_data:
            try:
                focal_str = str(exifread_data['EXIF FocalLength'])
                if '/' in focal_str:
                    parts = focal_str.split('/')
                    focal_length = float(parts[0]) / float(parts[1])
                else:
                    focal_length = float(focal_str)
            except:
                pass
        
        if focal_length:
            if focal_length > 1000 or focal_length < 1:
                result['indicators'].append(f'异常焦距值: {focal_length}mm')
    
    def _calculate_confidence(self, result):
        """计算修改置信度"""
        indicator_count = len(result['indicators'])
        warning_count = len(result['warnings'])
        
        # 基础置信度计算
        confidence = 0.0
        
        # 每个指标增加置信度
        confidence += indicator_count * 0.3
        
        # 警告也会增加一些置信度
        confidence += warning_count * 0.1
        
        # 限制在0-1范围内
        confidence = min(confidence, 1.0)
        
        result['confidence'] = confidence
        result['is_modified'] = confidence > 0.3  # 30%以上置信度认为可能被修改

def check_exif_integrity(pil_data, exifread_data):
    """
    检查EXIF完整性

    Args:
        pil_data: 已解析的PIL EXIF数据
        exifread_data: 已解析的exifread EXIF数据

    Returns:
        dict: 检查结果

    Note:
        这个函数专注于完整性检查逻辑，不负责EXIF数据解析。
        EXIF数据解析应该在调用方（如photo_analyzer.py）中完成，
        然后将解析结果传递给这个函数，避免重复解析。
    """
    checker = ExifIntegrityChecker()
    return checker.check_integrity(pil_data=pil_data, exifread_data=exifread_data)

def check_exif_integrity_from_file(file_path):
    """
    从文件检查EXIF完整性（便捷函数）

    Args:
        file_path: 文件路径

    Returns:
        dict: 检查结果

    Note:
        这个函数会进行EXIF解析，如果你已经有解析好的数据，
        建议直接使用 check_exif_integrity(pil_data, exifread_data)
    """
    # 导入解析函数（避免循环导入）
    from photo_analyzer import extract_exif_with_pil, extract_exif_with_exifread

    pil_data = extract_exif_with_pil(file_path)
    exifread_data = extract_exif_with_exifread(file_path)

    return check_exif_integrity(pil_data=pil_data, exifread_data=exifread_data)

if __name__ == "__main__":
    # 测试代码
    import sys
    if len(sys.argv) > 1:
        result = check_exif_integrity_from_file(sys.argv[1])
        print("EXIF完整性检查结果:")
        print(f"是否被修改: {'是' if result['is_modified'] else '否'}")
        print(f"置信度: {result['confidence']:.2%}")

        if result['indicators']:
            print("\n修改指标:")
            for indicator in result['indicators']:
                print(f"  - {indicator}")

        if result['warnings']:
            print("\n警告:")
            for warning in result['warnings']:
                print(f"  - {warning}")
    else:
        print("用法: python exif_integrity_checker.py <图片路径>")
