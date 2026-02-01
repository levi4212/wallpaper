import sys
import os

# 1. 基础配置
# 接收从 GitHub Actions 传进来的文件列表路径（例如 files.txt）
input_file = sys.argv[1] if len(sys.argv) > 1 else 'files.txt'
OUTPUT_FILE = 'index.html'
# 原始资源引用前缀，直接指向你的 paper 分支
REPO_BASE_URL = "https://raw.githubusercontent.com/levi4212/wallpaper/paper/"
# 你仓库中定义的分类目录
IMAGE_DIRS = ('4K16-10', '4KStandard', '4KUltraWide')

# 2. HTML 模板定义
html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wallpapers Gallery (40GB Mode)</title>
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
        .copy-btn {{ background: #238636; color: white; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 12px; margin-top: 8px; width: 100%; }}
        .copy-btn:hover {{ background: #2ea043; }}
    </style>
</head>
<body>
    <h1>🌌 我的超大容量壁纸库</h1>
    {content}
    <script>
        function copyUrl(url) {{
            navigator.clipboard.writeText(url).then(() => {{
                alert('图片链接已复制到剪贴板！');
            }}).catch(err => {{
                console.error('复制失败', err);
            }});
        }}
    </script>
</body>
</html>
"""

# 3. 核心处理逻辑
content = ""

# 读取由 Action 生成的文件列表，避免扫描物理磁盘
try:
    with open(input_file, 'r', encoding='utf-8') as f:
        all_files = f.read().splitlines()
except FileNotFoundError:
    print(f"错误: 找不到文件列表 {input_file}。请确保 Workflow 运行正确。")
    sys.exit(1)

for folder in IMAGE_DIRS:
    content += f"<h2>📂 分类: {folder}</h2><div class='grid'>"
    
    # 从虚拟列表中筛选出属于当前目录的图片，支持多级子目录
    target_files = [f for f in all_files if f.startswith(folder) and f.lower().endswith(('.jpg', '.png', '.jpeg', '.webp'))]
    
    # 按照文件名排序
    target_files.sort()

    for rel_path in target_files:
        file_name = os.path.basename(rel_path)
        raw_url = f"{REPO_BASE_URL}{rel_path}"
        
        content += f"""
        <div class="card">
            <div class="img-container">
                <img src="{raw_url}" loading="lazy" title="点击查看原图" onclick="window.open('{raw_url}')">
            </div>
            <div class="info">
                <div title="{file_name}" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{file_name}</div>
                <button class="copy-btn" onclick="copyUrl('{raw_url}')">复制链接</button>
            </div>
        </div>"""
    content += "</div>"

# 4. 生成 index.html
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(html_template.format(content=content))

print(f"✅ 导航页已成功生成到 {OUTPUT_FILE}")
