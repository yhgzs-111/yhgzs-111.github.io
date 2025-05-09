import requests
import csv
import time
import os
from datetime import datetime
from git import Repo

# 配置
sites = {
    "维基百科": "https://zh.wikipedia.org",
    "维基文库": "https://zh.wikisource.org",
    "维基词典": "https://zh.wiktionary.org",
    "维基教科书": "https://zh.wikibooks.org",
    "维基新闻": "https://zh.wikinews.org",
    "维基物种": "https://species.wikimedia.org",
    "维基导游": "https://zh.wikivoyage.org",
    "维基学院": "https://zh.wikiversity.org",
    "维基共享资源": "https://commons.wikimedia.org",
    "维基数据": "https://www.wikidata.org",
    "MediaWiki": "https://www.mediawiki.org",
    "元维基": "https://meta.wikimedia.org"
}

CSV_FILE = "wikimedia_access_log.csv"
HTML_FILE = "wikimedia/index.html"
REPO_PATH = "."  # 当前路径是 Git 项目
COMMIT_MESSAGE = "Auto update: new stats"

# GitHub Token 配置（你可以直接写入环境变量中或配置到脚本里）
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REMOTE = "https://<TOKEN>@github.com/yhgzs-111/yhgzs-111.github.io.git"

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["时间", "项目", "URL", "状态码", "响应时间（秒）"])

def log_sites():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for name, url in sites.items():
            try:
                response = requests.get(url, timeout=10)
                status = response.status_code
                elapsed = round(response.elapsed.total_seconds(), 3)
            except Exception:
                status = "ERROR"
                elapsed = "N/A"
            writer.writerow([now, name, url, status, elapsed])
            print(f"[{now}] {name}: {status}, {elapsed}s")

def csv_to_html():
    with open(CSV_FILE, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    html = "<html><head><meta charset='utf-8'><title>维基访问统计</title>"
    html += "<style>table { border-collapse: collapse; } td, th { border: 1px solid gray; padding: 5px; }</style>"
    html += "</head><body><h1>维基访问统计</h1><table>"
    html += "<tr>" + "".join(f"<th>{col}</th>" for col in rows[0]) + "</tr>"
    for row in rows[1:]:
        html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
    html += "</table></body></html>"

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ HTML 页面已更新：{HTML_FILE}")

def push_to_github():
    repo = Repo(REPO_PATH)
    repo.git.add(A=True)
    repo.index.commit(COMMIT_MESSAGE)
    
    if GITHUB_TOKEN:
        url = GITHUB_REMOTE.replace("<TOKEN>", GITHUB_TOKEN)
        repo.remote().set_url(url)
    
    repo.remotes.origin.push()
    print("✅ 已推送到 GitHub Pages")

# 主流程
if __name__ == "__main__":
    init_csv()
    while True:
        log_sites()
        csv_to_html()
        push_to_github()
        time.sleep(60)
