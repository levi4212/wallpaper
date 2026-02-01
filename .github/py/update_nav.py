import os

# 配置：针对你的仓库目录结构
IMAGE_DIRS = ['4K16-10', '4KStandard', '4KUltraWide']
OUTPUT_FILE = 'index.html'
# 这里的 URL 指向你的 paper 分支原始资源
REPO_BASE_URL = "https://raw.githubusercontent.com/levi4212/wallpaper/paper/"

html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wallpapers Gallery</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0d1117; color: #c9d1d9; padding: 20px; margin: 0; }}
        h1 {{ text-align: center; color: #58a6ff; }}
        h2 {{ border-bottom: 1px solid #30363d; padding-bottom: 10px; margin-top: 40px; color: #f0f6fc; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; padding: 20px 0; }}
        .card {{ background: #161b22; border: 1px solid #30363d; border-radius: 12px; overflow: hidden; transition: transform 0.2s; }}
        .card:hover {{ transform: translateY(-5px); border-color: #58a6ff; }}
        .img-container {{ width: 100%; height: 180px; background: #010409; display: flex; align-items: center; justify-content: center; overflow: hidden; }}
        img {{ width: 100%; height: 100%; object-fit: cover; cursor: pointer; }}
        .info {{ padding: 12px; font-size: 13px; text-align: center; }}
        .copy-btn {{ background: #238636; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer; font-size: 12px; margin-top: 8px; }}
        .copy-btn:hover {{ background: #2ea043; }}
    </style>
</head>
<body>
    <h1>🌌 我的壁纸库导航</h1>
    {content}
    <script>
        function copyUrl(url) {{
            navigator.clipboard.writeText(url).then(() => alert('原始链接已复制！'));
        }}
    </script>
</body>
</html>
"""

sections = ""
for folder in IMAGE_DIRS:
    if not os.path.exists(folder): continue
    sections += f"<h2>📂 {folder}</h2><div class='grid'>"
    
    # 递归查找图片，适应你之前的子文件夹拆分逻辑
    for root, dirs, files in os.walk(folder):
        # 按文件名排序，保证预览顺序
        for file in sorted(files):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                rel_path = os.path.join(root, file).replace("\\", "/")
                raw_url = f"{REPO_BASE_URL}{rel_path}"
                sections += f"""
                <div class="card">
                    <div class="img-container">
                        <img src="{raw_url}" loading="lazy" onclick="window.open('{raw_url}')">
                    </div>
                    <div class="info">
                        <div>{file}</div>
                        <button class="copy-btn" onclick="copyUrl('{raw_url}')">复制链接</button>
                    </div>
                </div>"""
    sections += "</div>"

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(html_template.format(content=sections))
