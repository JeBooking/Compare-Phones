"""
EXIF数据格式化工具模块
专门负责各种EXIF字段的格式化处理
"""

def safe_float_convert(value):
    """
    安全转换为浮点数，支持分数格式
    
    Args:
        value: 要转换的值（可能是字符串分数如'1/25'）
        
    Returns:
        float: 转换后的浮点数，失败时返回原值
    """
    try:
        if isinstance(value, str) and '/' in value:
            # 处理分数格式
            parts = value.split('/')
            if len(parts) == 2:
                return float(parts[0]) / float(parts[1])
        return float(value)
    except:
        return value

def format_exposure_time(value):
    """
    格式化曝光时间显示
    
    Args:
        value: 曝光时间值（可能是分数字符串或小数）
        
    Returns:
        str: 格式化后的曝光时间字符串
    """
    try:
        # 如果已经是分数格式，直接返回
        if isinstance(value, str) and '/' in value:
            return f"{value}秒"
        
        # 转换为浮点数
        float_value = safe_float_convert(value)
        
        # 如果大于等于1秒，直接显示
        if float_value >= 1:
            if float_value == int(float_value):
                return f"{int(float_value)}秒"
            else:
                return f"{float_value}秒"
        else:
            # 转换为分数形式
            denominator = int(1 / float_value)
            return f"1/{denominator}秒"
    except:
        # 如果转换失败，返回原值
        return str(value)

def format_fnumber(value):
    """格式化光圈值"""
    try:
        return f"f/{safe_float_convert(value)}"
    except:
        return str(value)

def format_focal_length(value):
    """格式化焦距"""
    try:
        return f"{safe_float_convert(value)}mm"
    except:
        return str(value)

def format_dict_value(value, mapping):
    """使用字典映射格式化值"""
    try:
        key = int(float(str(value)))
        return mapping.get(key, str(value))
    except:
        return mapping.get(str(value), str(value))
