# app/crawlers/configs/github_trending.py
GITHUB_TRENDING_CONFIG = {
    "items_selector": ".Box-row",  # 热榜项目行的选择器
    "repo_name_selector": ".h3.lh-condensed a",  # 项目名称+链接的选择器
    "description_selector": "p.col-9.color-fg-muted.my-1.pr-4",  # 项目描述的选择器
    "language_selector": "span[itemprop='programmingLanguage']",  # 编程语言的选择器
    "stats_selector": ".f6.color-fg-muted.mt-2",  # 星标数、Fork 数的选择器
    "today_stars_selector": ".float-sm-right"  # 今日新增星标的选择器
}