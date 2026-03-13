import sys
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

# 配置文件路径
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
LOG_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log")

# 初始化默认配置
DEFAULT_CONFIG = {
    "html_title": "我的分享页面",
    "page_title": "欢迎来到我的页面",
    "title_font_size": 36,
    "text_font_size": 16,
    "content_blocks": [],
    "server_port": 5000
}

def load_config():
    """加载配置文件，不存在则创建默认配置"""
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=4)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_html(config):
    """运行时生成完整HTML（仅生成一次，避免刷新重复生成，满足需求二）"""
    # 生成内容块HTML
    content_html = ""
    for block in config["content_blocks"]:
        block_type = block["type"]
        block_content = block["content"]
        if block_type == "text":
            content_html += f'<div class="content-block"><p>{block_content}</p></div>\n'
        elif block_type == "image":
            content_html += f'<div class="content-block"><img src="{block_content}" alt="图片"></div>\n'
        elif block_type == "video":
            content_html += f'<div class="content-block"><video src="{block_content}" controls preload="none" muted></video></div>\n'
        elif block_type == "link":
            content_html += f'<div class="content-block">{block_content}</div>\n'

    # 完整HTML模板，内置美化CSS与动画（满足需求六）
    html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config["html_title"]}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 2rem 0;
        }}
        /* Welcome入场动画 */
        @keyframes welcome {{
            from {{
                opacity: 0;
                transform: translateY(-50px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        .welcome-title {{
            font-size: {config["title_font_size"]}pt;
            color: #1e293b;
            text-align: center;
            margin-bottom: 2rem;
            animation: welcome 1s ease-out;
            line-height: 1.2;
        }}
        .content-block {{
            width: 90%;
            max-width: 800px;
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .content-block:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        }}
        .content-block p {{
            font-size: {config["text_font_size"]}pt;
            line-height: 1.8;
            color: #334155;
            word-break: break-word;
        }}
        .content-block img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            border: 2px solid #e2e8f0;
            transition: transform 0.3s ease;
        }}
        .content-block img:hover {{
            transform: scale(1.02);
        }}
        .content-block video {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            border: 2px solid #e2e8f0;
            transition: transform 0.3s ease;
        }}
        .content-block video:hover {{
            transform: scale(1.02);
        }}
        a {{
            color: #2563eb;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s ease;
        }}
        a:hover {{
            color: #1d4ed8;
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1 class="welcome-title">{config["page_title"]}</h1>
    {content_html}
</body>
</html>
    """
    return html

def save_html_backup(html):
    """保存带时间戳的网页备份"""
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(LOG_FOLDER, f"page_backup_{timestamp}.html")
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"网页备份已保存至: {backup_path}")

# 全局预生成HTML（运行时仅生成一次）
PRE_GENERATED_HTML = ""

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 直接返回预生成的HTML，刷新不重复生成
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(PRE_GENERATED_HTML.encode("utf-8"))
    
    # 禁用终端日志刷屏
    def log_message(self, format, *args):
        return

def main():
    global PRE_GENERATED_HTML
    config = load_config()
    # 启动时仅生成一次HTML
    PRE_GENERATED_HTML = generate_html(config)
    save_html_backup(PRE_GENERATED_HTML)
    
    port = config["server_port"]
    try:
        server = HTTPServer(("0.0.0.0", port), RequestHandler)
        print(f"服务已启动！")
        print(f"本地访问地址: http://127.0.0.1:{port}")
        print(f"局域网访问地址: http://[你的IP]:{port}")
        print("按 Ctrl+C 停止服务")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")
        server.server_close()
        sys.exit(0)
    except Exception as e:
        print(f"启动服务失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
