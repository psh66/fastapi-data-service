# app/crawlers/configs/zhihu_hot.py
ZHIHU_HOT_CONFIG = {
    "list_selector": ".HotItem",  # 单个热榜条目的最外层容器
    "fields": {
        "rank": (".HotItem-rank", "text"),  # 排名（匹配<div class="HotItem-rank">）
        "title": (".HotItem-title", "text"),  # 标题（匹配<h2 class="HotItem-title">）
        "hot_value": (".HotItem-metrics", "text"),  # 热度值（匹配<div class="HotItem-metrics">）
        # 修正链接元素选择器：精准定位到标题内的<a>标签
        "url_elem": (".HotItem-content a", "elem")
    }
}