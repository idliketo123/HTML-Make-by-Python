import sys
import os
import json
import re

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def process_link_in_text(text):
    """处理文本中的链接（满足需求四）"""
    # 先处理「链接名 链接地址」格式
    text = re.sub(r'(\S+)\s+(https?://\S+)', r'<a href="\2" target="_blank">\1</a>', text)
    # 再处理纯链接（避免重复替换已在a标签中的链接）
    text = re.sub(r'(?<!href=")(https?://\S+)', r'<a href="\1" target="_blank">\1</a>', text)
    return text

def main():
    print("===== 文本内容配置 =====")
    config = load_config()
    
    while True:
        text_content = input("请输入文本内容（支持链接自动识别）: ").strip()
        if not text_content:
            print("文本内容不能为空，请重新输入")
            continue
        
        # 处理链接并保存
        processed_text = process_link_in_text(text_content)
        config["content_blocks"].append({
            "type": "text",
            "content": processed_text
        })
        save_config(config)
        print("文本内容已添加成功")
        
        # 下一步操作选择（满足需求四）
        print("\n请选择接下来操作:")
        print("1、继续添加文本")
        print("2、继续添加资源")
        print("n、不添加，直接启动服务")
        choice = input("[1/2/n] (默认:n): ").strip().lower()
        
        if choice == "1":
            print("\n--- 继续添加文本 ---")
            continue
        elif choice == "2":
            print("\n即将进入资源配置...")
            os.system(f'python "{os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources.py")}"')
            sys.exit(0)
        else:
            print("\n即将启动服务...")
            os.system(f'python "{os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")}"')
            sys.exit(0)

if __name__ == "__main__":
    main()
