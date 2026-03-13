import sys
import os
import json
import base64
import re

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def image_to_base64(image_path):
    """图片转base64（满足需求一）"""
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
        base64_data = base64.b64encode(image_data).decode("utf-8")
        ext = os.path.splitext(image_path)[1].lower().replace(".", "")
        ext = "jpeg" if ext == "jpg" else ext
        return f"data:image/{ext};base64,{base64_data}"
    except Exception as e:
        print(f"图片处理失败: {e}")
        return None

def main():
    print("===== 资源配置 =====")
    config = load_config()
    
    while True:
        # 资源类型选择（满足需求一：图片、视频、链接）
        print("\n请选择要添加的资源类型:")
        print("1、图片")
        print("2、视频")
        print("3、链接")
        type_choice = input("[1/2/3]: ").strip()
        
        if type_choice == "1":
            # 图片处理（base64嵌入）
            image_path = input("请输入图片文件路径: ").strip()
            if not os.path.exists(image_path):
                print("文件不存在，请重新输入")
                continue
            base64_image = image_to_base64(image_path)
            if base64_image:
                config["content_blocks"].append({
                    "type": "image",
                    "content": base64_image
                })
                save_config(config)
                print("图片已添加成功")
        
        elif type_choice == "2":
            # 视频处理（默认不播放，满足需求一）
            video_path = input("请输入视频文件路径（建议放在当前文件夹）: ").strip()
            if not os.path.exists(video_path):
                print("文件不存在，请重新输入")
                continue
            # 转为相对路径保证HTML可访问
            relative_path = os.path.relpath(video_path, os.path.dirname(os.path.abspath(__file__)))
            config["content_blocks"].append({
                "type": "video",
                "content": relative_path
            })
            save_config(config)
            print("视频已添加成功，默认不自动播放")
        
        elif type_choice == "3":
            # 链接处理（超链接呈现，满足需求一）
            link_input = input('请输入链接（格式：链接名 链接地址）: ').strip()
            link_match = re.match(r'(\S+)\s+(https?://\S+)', link_input)
            if not link_match:
                print("格式错误，请按照「链接名 链接地址」的格式输入")
                continue
            link_name = link_match.group(1)
            link_url = link_match.group(2)
            link_html = f'<a href="{link_url}" target="_blank">{link_name}</a>'
            config["content_blocks"].append({
                "type": "link",
                "content": link_html
            })
            save_config(config)
            print("链接已添加成功")
        
        else:
            print("无效的选择，请重新输入")
            continue
        
        # 下一步操作选择（满足需求一）
        print("\n请选择接下来操作:")
        print("1、继续添加文本")
        print("2、继续添加资源")
        print("n、不添加，直接启动服务")
        choice = input("[1/2/n] (默认:n): ").strip().lower()
        
        if choice == "1":
            print("\n即将进入文本配置...")
            os.system(f'python "{os.path.join(os.path.dirname(os.path.abspath(__file__)), "text.py")}"')
            sys.exit(0)
        elif choice == "2":
            print("\n--- 继续添加资源 ---")
            continue
        else:
            print("\n即将启动服务...")
            os.system(f'python "{os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")}"')
            sys.exit(0)

if __name__ == "__main__":
    main()
