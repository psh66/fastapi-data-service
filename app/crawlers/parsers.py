def parse_data(soup, config):
    items = soup.select(config["list_selector"])
    result = []
    for item in items:
        data = {}
        for field, (selector, method, *default) in config["fields"].items():
            elem = item.select_one(selector)
            # 处理元素不存在的情况，使用默认值
            if not elem:
                data[field] = default[0] if default else None
                continue
            if method == "text":
                data[field] = elem.text.strip()
            elif method == "elem":
                data[field] = elem  # 存储标签元素
        # 处理URL：若url_elem为空，设为None，否则提取href
        if "url_elem" in data:
            if data["url_elem"] is not None:
                data["url"] = data["url_elem"].get("href", "")  # 提取链接
            else:
                data["url"] = None  # 空值处理
            del data["url_elem"]  # 删除临时字段
        result.append(data)
    return result