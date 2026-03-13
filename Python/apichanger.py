import sys
import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def main():
    print("===== 端口配置 =====")
    config = load_config()
    current_port = config["server_port"]
    print(f"当前端口: {current_port}")
    
    choice = input("是否修改端口？[y/N] (默认:N): ").strip().lower()
    if choice == "y":
        while True:
            new_port = input("请输入新的端口号（1024-65535）: ").strip()
            if new_port.isdigit() and 1024 <= int(new_port) <= 65535:
                config["server_port"] = int(new_port)
                save_config(config)
                print(f"端口已修改为: {new_port}")
                break
            else:
                print("输入无效，请输入1024-65535之间的数字")
    else:
        print("使用已有端口，跳过修改")
    
    # 按顺序运行下一个脚本
    print("\n即将进入文本内容配置...")
    os.system(f'python "{os.path.join(os.path.dirname(os.path.abspath(__file__)), "text.py")}"')
    sys.exit(0)

if __name__ == "__main__":
    main()
