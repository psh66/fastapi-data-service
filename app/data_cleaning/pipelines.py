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
    """清洗单条知乎热榜数据（核心清洗逻辑）"""
    cleaned_item = {}  # 存储清洗后的结果

    for field, rule in rules.items():  # 遍历每个字段的规则（如"rank"对应其规则）
        # 1. 获取原始值（处理缺失情况）
        raw_value = raw_item.get(field, None)  # 从原始数据中取字段值，没有则为None

        # 2. 必选字段校验（缺失时用默认值填充）
        if raw_value is None:
            if rule.get("required", False):  # 如果是必选字段（如rank、title）
                cleaned_item[field] = rule.get("default")  # 用规则中的default填充（如rank默认0）
                continue  # 跳过后续处理
            else:
                continue  # 非必选字段缺失则忽略

        # 3. 类型转换（如字符串转整数）
        target_type = rule.get("type", str)  # 默认转为字符串
        try:
            value = target_type(raw_value)  # 尝试转换类型（如"1"→int(1)）
        except (ValueError, TypeError):  # 转换失败（如"abc"转int）
            value = rule.get("default")  # 用默认值兜底（避免存储时类型错误）

        # 4. 字符串特殊处理（仅对字符串类型生效）
        if isinstance(value, str):
            if rule.get("strip", False):  # 去除首尾空白（如标题前后的空格）
                value = value.strip()

            # 替换特殊字符（如换行符、冗余文字）
            for old, new in rule.get("replace", []):
                value = value.replace(old, new)  # 如"100.5 万热度"→"100.5万"

            # 截断超长字符串（避免超过数据库字段长度限制）
            max_len = rule.get("max_length")
            if max_len and len(value) > max_len:
                value = value[:max_len]  # 超过500字符的标题截断

            # 补全链接前缀（处理相对路径）
            if rule.get("prefix") and value.startswith("/"):
                value = rule["prefix"] + value  # 如"/question/123"→"https://www.zhihu.com/question/123"

        # 5. 存入清洗后的数据
        cleaned_item[field] = value
    return cleaned_item

def clean_zhihu_hot_list(raw_list: list, rules: dict) -> list:
    """批量清洗知乎热榜列表（调用单条清洗函数处理所有数据）"""
    return [clean_zhihu_hot_item(item, rules) for item in raw_list if item]  # 过滤空数据（如None、空字典）