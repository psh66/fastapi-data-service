JD_PRODUCT_CONFIG = {
    "list_selector": ".gl-item",  # 京东商品列表选择器
    "fields": {
        "name": (".p-name em", "text"),  # 商品名称
        "price": (".p-price i", "text"),  # 价格
        "comment_count": (".p-commit a", "text")  # 评论数
    }
}