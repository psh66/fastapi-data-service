DOUBAN_MOVIE_CONFIG = {
    "list_selector": ".grid_view li.item",  # 列表容器选择器
    "fields": {  # 字段名: 选择器+提取规则
        "title": (".title", "text"),
        "intro": (".quote span", "text", "暂无简介"),  # 第三个参数：默认值
        "rating": (".rating_num", "text")
    }
}