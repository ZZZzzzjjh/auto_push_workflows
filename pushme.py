import requests
import json
import time
import os
PUSH_KEY = os.getenv("MY_PUSH_KEY")


def load_json_and_format(filename, title_prefix):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        lines = [f"{item['rank']}. {item.get('title') or item.get('keyword') or item.get('word')}" for item in data[:5]]
        return f"【{title_prefix}】\n" + "\n".join(lines)
    except FileNotFoundError:
        return f"【{title_prefix}】数据文件未找到"
    except Exception as e:
        return f"【{title_prefix}】解析出错: {e}"


def push_to_phone():
    print("正在整理数据并推送...")
    weibo_msg = load_json_and_format('weibo.json', '微博热搜')
    bili_msg = load_json_and_format('bili.json', 'B站热搜')
    baidu_msg = load_json_and_format('baidu.json', '百度热搜')

    current_time = time.strftime("%H:%M")
    final_content = f"{weibo_msg}\n\n{bili_msg}\n\n{baidu_msg}"

    push_url = "https://push.i-i.me/"
    params = {
        "push_key": PUSH_KEY,
        "title": "今日全网热点汇总",
        "content": final_content
    }

    try:
        response = requests.get(push_url, params=params)
        if response.status_code == 200:
            print(f"推送成功！手机应已弹出通知。")
        else:
            print(f"推送失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"推送网络异常: {e}")


if __name__ == "__main__":
    push_to_phone()
