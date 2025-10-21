# app/data_cleaning/configs/github_clean_rules.py
GITHUB_CLEAN_RULES = {
    "stars": {
        "required": True,
        "type": str,
        "replace": [("k", "000"), ("m", "000000"), (",", "")],  # 处理 "10.5k" → "10500"
        "cast": "int"  # 转换为整数
    },
    "forks": {
        "required": True,
        "type": str,
        "replace": [("k", "000"), ("m", "000000"), (",", "")],
        "cast": "int"
    },
    "today_stars": {
        "required": True,
        "type": str,
        "replace": [(",", "")],
        "cast": "int"
    },
    "description": {
        "required": False,
        "type": str,
        "strip": True,
        "replace": [("\n", " "), ("  ", " ")]  # 清洗换行和多余空格
    }
}