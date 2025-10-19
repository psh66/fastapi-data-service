def parse_data(soup, config):
    """根据配置动态解析页面数据"""
    items = soup.select(config["list_selector"])
    result = []
    for item in items:
        data = {}
        for field, (selector, method, *default) in config["fields"].items():
            elem = item.select_one(selector)
            if not elem:
                data[field] = default[0] if default else None
                continue
            # 根据提取方法（text/attr等）处理
            if method == "text":
                data[field] = elem.text.strip()
            elif method == "attr":
                data[field] = elem.get(selector.split("@")[-1], "").strip()  # 支持提取属性（如img@src）
        result.append(data)
    return result