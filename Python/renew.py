import sys
import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
DEFAULT_CONFIG = {
    "html_title": "我的分享页面",
    "page_title": "欢迎来到我的页面",
    "title_font_size": 36,
    "text_font_size": 16,
    "content_blocks": [],
    "server_port": 5000
}

def load_config():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=4)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def main():
    print("===== 初始化与标题配置 =====")
    choice = input("是否重新初始化配置？(将清空所有内容) [y/N] (默认:N): ").strip().lower()
    config = load_config()
    
    if choice == "y":
        # 初始化清空所有内容（满足需求三）
        config = DEFAULT_CONFIG.copy()
        print("已清空所有内容，初始化完成")
        
        # 修改网页名（浏览器标签）
        html_title = input(f"请输入网页名[默认:{config['html_title']}]: ").strip()
        if html_title:
            config["html_title"] = html_title
        
        # 页面大标题
        page_title = input(f"请输入页面大标题[默认:{config['page_title']}]: ").strip()
        if page_title:
            config["page_title"] = page_title
        
        # 标题字体大小（磅）
        title_font_size = input(f"请输入标题字体大小（单位：磅）[默认:{config['title_font_size']}]: ").strip()
        if title_font_size and title_font_size.isdigit():
            config["title_font_size"] = int(title_font_size)
        
        # 文本字体大小（磅）
        text_font_size = input(f"请输入文本字体大小（单位：磅）[默认:{config['text_font_size']}]: ").strip()
        if text_font_size and text_font_size.isdigit():
            config["text_font_size"] = int(text_font_size)
        
        print("标题已设置为居中显示")
        save_config(config)
    else:
        print("使用已有配置，跳过初始化")
    
    # 按顺序运行下一个脚本
    print("\n即将进入端口配置...")
    os.system(f'python "{os.path.join(os.path.dirname(os.path.abspath(__file__)), "apichanger.py")}"')
    sys.exit(0)

if __name__ == "__main__":
    main()
