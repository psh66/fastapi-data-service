def clean_price(price_str):
    """清洗价格：去除¥符号，转换为浮点数"""
    if not price_str:
        return None
    return float(price_str.replace("¥", "").strip())

def clean_comment_count(count_str):
    """清洗评论数：去除“万+”，转换为整数"""
    if not count_str:
        return 0
    count_str = count_str.strip().replace("+", "")
    if "万" in count_str:
        return int(float(count_str.replace("万", "")) * 10000)
    return int(count_str)

# 清洗流水线：字段→清洗函数的映射（可根据配置动态调用）
CLEAN_PIPELINES = {
    "price": clean_price,
    "comment_count": clean_comment_count,
    "rating": lambda x: float(x) if x else None  # 评分转浮点数
}

def clean_data(raw_data, pipeline_mapping):
    """应用清洗流水线处理原始数据"""
    cleaned_data = {}
    for field, value in raw_data.items():
        if field in pipeline_mapping:
            cleaned_data[field] = pipeline_mapping[field](value)
        else:
            cleaned_data[field] = value  # 无需清洗的字段直接保留
    return cleaned_data