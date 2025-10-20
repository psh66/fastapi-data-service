# 知乎热榜数据清洗规则（键：字段名，值：该字段的清洗规则）
ZHIHU_CLEAN_RULES = {
    "rank": {  # 处理“排名”字段
        "required": True,  # 该字段为必选（缺失时用default填充，避免数据库报错）
        "type": int,       # 目标类型为整数（原始数据可能是字符串，如"1"→1）
        "default": 0       # 缺失或转换失败时的默认值
    },
    "title": {  # 处理“标题”字段
        "required": True,
        "type": str,       # 目标类型为字符串
        "strip": True,     # 去除首尾空白字符（如空格、换行符\n、制表符\t）
        "max_length": 500, # 最大长度500（匹配数据库模型title字段的String(500)）
        "replace": [       # 替换特殊字符（清理冗余格式）
            ("\n", ""),    # 去除换行符（原始标题可能带换行）
            ("\t", ""),    # 去除制表符
            ("\r", "")     # 去除回车符
        ]
    },
    "hot_value": {  # 处理“热度值”字段
        "required": True,
        "type": str,
        "strip": True,
        "replace": [       # 统一热度格式（避免格式混乱）
            (" 万热度", "万"),  # 如“100.5 万热度”→“100.5万”
            (" 万", "万"),      # 如“200 万”→“200万”
            ("热度", "")        # 如“300热度”→“300”
        ]
    },
    "url": {  # 处理“链接”字段
        "required": True,
        "type": str,
        "strip": True,
        "prefix": "https://www.zhihu.com"  # 补全相对链接（如HTML中提取的是"/question/123"→完整URL）
    }
}