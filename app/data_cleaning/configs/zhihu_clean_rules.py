# 知乎热榜数据清洗规则
ZHIHU_CLEAN_RULES = {
    # 字段清洗规则：键为原始字段名，值为清洗函数或处理规则
    "rank": {
        "required": True,  # 必选字段
        "type": int,       # 目标类型
        "default": 0       # 缺失时默认值
    },
    "title": {
        "required": True,
        "type": str,
        "strip": True,     # 去除首尾空白
        "max_length": 500, # 最大长度限制（对应数据库字段）
        "replace": [       # 替换特殊字符
            ("\n", ""),    # 去除换行符
            ("\t", ""),    # 去除制表符
            ("\r", "")     # 去除回车符
        ]
    },
    "hot_value": {
        "required": True,
        "type": str,
        "strip": True,
        "replace": [
            (" 万热度", "万"),  # 统一格式："100.5 万热度" → "100.5万"
            (" 万", "万"),      # 兼容其他格式："200 万" → "200万"
            ("热度", "")        # 去除冗余："300热度" → "300"
        ]
    },
    "url": {
        "required": True,
        "type": str,
        "strip": True,
        "prefix": "https://www.zhihu.com"  # 补全相对链接："/question/123" → "https://www.zhihu.com/question/123"
    }
}