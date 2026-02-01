import sys

# 从命令行参数获取文件列表路径
input_file = sys.argv[1] if len(sys.argv) > 1 else 'files.txt'
OUTPUT_FILE = 'index.html'
REPO_BASE_URL = "https://raw.githubusercontent.com/levi4212/wallpaper/paper/"
IMAGE_DIRS = ('4K16-10', '4KStandard', '4KUltraWide')

# ... (保留之前的 html_template 样式) ...

content = ""
with open(input_file, 'r') as f:
    all_files = f.read().splitlines()

for folder in IMAGE_DIRS:
    content += f"<h2>📂 {folder}</h2><div class='grid'>"
    # 过滤出该文件夹下的图片
    target_files = [f for f in all_files if f.startswith(folder) and f.lower().endswith(('.jpg', '.png', '.webp'))]
    
    for rel_path in target_files:
        file_name = rel_path.split('/')[-1]
        raw_url = f"{REPO_BASE_URL}{rel_path}"
        content += f"""
        <div class="card">
            <img src="{raw_url}" loading="lazy">
            <div class="info">{file_name}</div>
        </div>"""
    content += "</div>"

# ... (写入 index.html) ...
