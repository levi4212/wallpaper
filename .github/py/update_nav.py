import sys
import os

# 配置信息
input_file = sys.argv[1] if len(sys.argv) > 1 else 'files.txt'
OUTPUT_FILE = 'index.html'
REPO_BASE_URL = "https://raw.githubusercontent.com/levi4212/wallpaper/paper/"
IMAGE_DIRS = ('4K16-10', '4KStandard', '4KUltraWide')

# AdSense 配置
ADS_JS = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9823824864995295"
PUBLISHER_ID = "ca-pub-9823824864995295"

# 使用普通字符串拼接，避免 f-string 误解析 CSS 的花括号
html_head = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wallpapers Gallery (40GB Mode)</title>
    <script async src="{ADS_JS}" crossorigin="anonymous"></script>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0d1117; color: #c9d1d9; padding: 20px; margin: 0; }}
        h1 {{ text-align: center; color: #58a6ff; margin-bottom: 30px; }}
        h2 {{ border-bottom: 1px solid #30363d; padding-bottom: 10px; margin-top: 40px; color: #f0f6fc; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; padding: 20px 0; }}
        .card {{ background: #161b22; border: 1px solid #30363d; border-radius: 12px; overflow: hidden; transition: transform 0.2s; }}
        .card:hover {{ transform: translateY(-5px); border-color: #58a6ff; }}
        .img-container {{ width: 100%; height: 180px; background: #010409; display: flex; align-items: center; justify-content: center; overflow: hidden; }}
        img {{ width: 100%; height: 100%; object-fit: cover; cursor: pointer; }}
        .info {{ padding: 12px; font-size: 13px; text-align: center; border-top: 1px solid #30363d; }}
        .btn-group {{ display: flex; gap: 8px; margin-top: 8px; }}
        .btn {{ flex: 1; color: white; border: none; padding: 8px; border-radius: 6px; cursor: pointer; font-size: 12px; text-decoration: none; text-align: center; display: inline-block; }}
        .copy-btn {{ background: #238636; }}
        .copy-btn:hover {{ background: #2ea043; }}
        .dl-btn {{ background: #2188ff; }}
        .dl-btn:hover {{ background: #0969da; }}
        .ads-container {{ text-align: center; margin: 20px 0; min-height: 90px; }}
    </style>
</head>
<body>
    <h1>🌌 我的壁纸库导航 (含下载与广告)</h1>
    <div class="ads-container">
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="{PUBLISHER_ID}"
             data-ad-slot="auto"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
        <script> (adsbygoogle = window.adsbygoogle || []).push({{}}); </script>
    </div>
"""

html_foot = """
    <script>
        function copyUrl(url) {
            navigator.clipboard.writeText(url).then(() => alert('图片链接已复制！'));
        }
    </script>
</body>
</html>
"""

# 处理内容
content = ""
try:
    with open(input_file, 'r', encoding='utf-8') as f:
        all_files = f.read().splitlines()
except FileNotFoundError:
    print(f"Error: {input_file} not found.")
    sys.exit(1)

for folder in IMAGE_DIRS:
    content += f"<h2>📂 分类: {folder}</h2><div class='grid'>"
    # 筛选对应目录下的图片并排序
    target_files = sorted([f for f in all_files if f.startswith(folder) and f.lower().endswith(('.jpg', '.png', '.jpeg', '.webp'))])
    
    for rel_path in target_files:
        file_name = os.path.basename(rel_path)
        raw_url = f"{REPO_BASE_URL}{rel_path}"
        content += f"""
        <div class="card">
            <div class="img-container">
                <img src="{raw_url}" loading="lazy" onclick="window.open('{raw_url}')">
            </div>
            <div class="info">
                <div title="{file_name}" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{file_name}</div>
                <div class="btn-group">
                    <button class="btn copy-btn" onclick="copyUrl('{raw_url}')">复制链接</button>
                    <a href="{raw_url}" download="{file_name}" target="_blank" class="btn dl-btn">下载图片</a>
                </div>
            </div>
        </div>"""
    content += "</div>"

# 写入文件
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(html_head + content + html_foot)

print("✅ index.html 已成功生成，包含下载按钮和 AdSense 代码。")
