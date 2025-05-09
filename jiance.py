import requests
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

HTML_DIR = "wikimedia"
HTML_FILE = os.path.join(HTML_DIR, "index.html")
REPO_PATH = "."  # Git 项目根目录
COMMIT_MESSAGE = "Auto update: latest stats"

# GitHub Token (可设置为环境变量)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REMOTE = "https://<TOKEN>@github.com/yhgzs-111/yhgzs-111.github.io.git"

def fetch_stats():
    """逐站点检测，返回结果列表"""
    results = []
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for name, url in sites.items():
        try:
            resp = requests.get(url, timeout=10, proxies={})
            status = resp.status_code
            elapsed = round(resp.elapsed.total_seconds(), 3)
        except Exception:
            status = "ERROR"
            elapsed = "N/A"
        results.append({
            "name": name,
            "url": url,
            "status": status,
            "time": elapsed
        })
        print(f"[{now}] {name}: {status}, {elapsed}s")
    return now, results

def build_html(timestamp, stats):
    """生成现代化卡片式 HTML，写入文件"""
    os.makedirs(HTML_DIR, exist_ok=True)
    html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>维基访问最新状态</title>
  <link href="https://fonts.googleapis.com/css?family=Roboto:400,500&display=swap" rel="stylesheet">
  <style>
    body {{
      margin: 0; padding: 0;
      font-family: 'Roboto', sans-serif;
      background: #f0f2f5;
      color: #333;
    }}
    header {{
      background: #fff;
      padding: 16px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      text-align: center;
    }}
    header h1 {{ margin: 0; font-weight: 500; }}
    header .timestamp {{ margin-top: 4px; font-size: 0.9em; color: #666; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      padding: 16px;
    }}
    .card {{
      background: #fff;
      border-radius: 8px;
      padding: 12px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .card h2 {{ margin: 0 0 8px; font-size: 1.1em; }}
    .card a {{ color: #1a73e8; text-decoration: none; word-break: break-all; }}
    .card .status {{ font-size: 0.9em; margin-top: 8px; }}
    .status.ok {{ color: #2e7d32; }}
    .status.error {{ color: #c62828; }}
    .card .time {{ font-size: 0.9em; color: #555; margin-top: 4px; }}
  </style>
</head>
<body>
  <header>
    <h1>维基访问最新状态</h1>
    <div class="timestamp">更新时间：{timestamp}</div>
  </header>
  <div class="grid">
"""
    for item in stats:
        status_class = "ok" if str(item["status"]).isdigit() and int(item["status"]) < 400 else "error"
        html += f"""
    <div class="card">
      <h2>{item['name']}</h2>
      <a href="{item['url']}" target="_blank">{item['url']}</a>
      <div class="status {status_class}">状态：{item['status']}</div>
      <div class="time">响应：{item['time']} 秒</div>
    </div>
"""
    html += """
  </div>
</body>
</html>"""
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ 已生成 HTML：{HTML_FILE}")

def push_to_github():
    repo = Repo(REPO_PATH)
    repo.git.add(A=True)
    repo.index.commit(COMMIT_MESSAGE)
    if GITHUB_TOKEN:
        url = GITHUB_REMOTE.replace("<TOKEN>", GITHUB_TOKEN)
        repo.remote().set_url(url)
    repo.remotes.origin.push()
    print("✅ 已推送到 GitHub Pages")

if __name__ == "__main__":
    while True:
        ts, stats = fetch_stats()
        build_html(ts, stats)
        push_to_github()
        time.sleep(60)
