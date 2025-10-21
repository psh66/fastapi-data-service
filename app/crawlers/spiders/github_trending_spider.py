# app/crawlers/spiders/github_trending_spider.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from app.crawlers.utils.proxy_utils import get_random_proxy
from app.crawlers.configs.github_trending import GITHUB_TRENDING_CONFIG


def crawl_github_trending(language: str = "", since: str = "daily"):
    """
    爬取 GitHub Trending 页面
    :param language: 编程语言（如 python、java，空字符串表示所有语言）
    :param since: 时间范围（daily/weekly/monthly）
    :return: 原始数据列表
    """
    # 配置浏览器和代理
    options = webdriver.ChromeOptions()
    proxy = get_random_proxy()
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
    driver = webdriver.Chrome(options=options)

    try:
        # 访问目标页面
        url = f"https://github.com/trending/{language}?since={since}"
        driver.get(url)
        # 等待页面加载完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, GITHUB_TRENDING_CONFIG["items_selector"]))
        )
        # 滚动页面加载更多内容
        for _ in range(2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        # 提取所有项目行
        items = driver.find_elements(By.CSS_SELECTOR, GITHUB_TRENDING_CONFIG["items_selector"])
        raw_data_list = []
        for item in items:
            # 解析项目名称和链接
            repo_elem = item.find_element(By.CSS_SELECTOR, GITHUB_TRENDING_CONFIG["repo_name_selector"])
            repo_name = repo_elem.text.strip().replace("\n", "").replace("  ", " ")
            repo_url = repo_elem.get_attribute("href")

            # 解析描述
            desc_elem = item.find_elements(By.CSS_SELECTOR, GITHUB_TRENDING_CONFIG["description_selector"])
            description = desc_elem[0].text.strip() if desc_elem else ""

            # 解析编程语言
            lang_elem = item.find_elements(By.CSS_SELECTOR, GITHUB_TRENDING_CONFIG["language_selector"])
            language = lang_elem[0].text.strip() if lang_elem else "Unknown"

            # 解析星标数、Fork 数
            stats_elem = item.find_elements(By.CSS_SELECTOR, GITHUB_TRENDING_CONFIG["stats_selector"])
            stats = stats_elem[0].text.strip() if stats_elem else ""
            stars = stats.split("•")[0].strip().split(" ")[0] if "•" in stats else "0"
            forks = stats.split("•")[1].strip().split(" ")[0] if len(stats.split("•")) > 1 else "0"

            # 解析今日新增星标
            today_elem = item.find_elements(By.CSS_SELECTOR, GITHUB_TRENDING_CONFIG["today_stars_selector"])
            today_stars = today_elem[0].text.strip().split(" ")[0] if today_elem else "0"

            # 组装原始数据
            raw_data_list.append({
                "repo_name": repo_name,
                "repo_url": repo_url,
                "description": description,
                "language": language,
                "stars": stars,
                "forks": forks,
                "today_stars": today_stars,
                "crawl_time": time.strftime("%Y-%m-%d %H:%M:%S")
            })
        print(f"爬取到 {len(raw_data_list)} 条原始数据")
        return raw_data_list
    finally:
        driver.quit()  # 无论成功与否，关闭浏览器