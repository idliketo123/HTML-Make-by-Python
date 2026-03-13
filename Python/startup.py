import os
import sys

def main():
    print("===== 页面生成服务启动器 =====")
    # 初始运行顺序：renew.py → apichanger.py → text.py → resources.py → main.py（满足需求五）
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "renew.py")
    os.system(f'python "{script_path}"')

if __name__ == "__main__":
    main()
