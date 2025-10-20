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


def clean_zhihu_hot_item(raw_item: dict, rules: dict) -> dict:
    """
    清洗单条知乎热榜数据
    :param raw_item: 原始爬取数据（字典）
    :param rules: 清洗规则（来自ZHIHU_CLEAN_RULES）
    :return: 清洗后的干净数据
    """
    cleaned_item = {}

    for field, rule in rules.items():
        # 1. 获取原始值（处理缺失情况）
        raw_value = raw_item.get(field, None)

        # 2. 必选字段校验（缺失时用默认值或跳过）
        if raw_value is None:
            if rule.get("required", False):
                cleaned_item[field] = rule.get("default")
                continue
            else:
                continue  # 非必选字段缺失则忽略

        # 3. 类型转换（如字符串转整数）
        target_type = rule.get("type", str)
        try:
            value = target_type(raw_value)
        except (ValueError, TypeError):
            # 转换失败用默认值
            value = rule.get("default")

        # 4. 字符串处理（仅针对字符串类型）
        if isinstance(value, str):
            # 去除首尾空白
            if rule.get("strip", False):
                value = value.strip()

            # 替换特殊字符
            for old, new in rule.get("replace", []):
                value = value.replace(old, new)

            # 长度限制（超过则截断）
            max_len = rule.get("max_length")
            if max_len and len(value) > max_len:
                value = value[:max_len]

            # 补全链接前缀
            if rule.get("prefix") and value.startswith("/"):
                value = rule["prefix"] + value

        # 5. 存入清洗后的数据
        cleaned_item[field] = value

    return cleaned_item


def clean_zhihu_hot_list(raw_list: list, rules: dict) -> list:
    """清洗整个知乎热榜列表（批量处理）"""
    return [clean_zhihu_hot_item(item, rules) for item in raw_list if item]