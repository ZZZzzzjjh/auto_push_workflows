import requests
import json
import pushme


# ================= 1. 微博爬取并转换 =================
def save_weibo_json():
    url = "https://weibo.com/ajax/side/hotSearch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://weibo.com/hot/search"
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        data = res.json().get('data', {}).get('realtime', [])

        # 格式化数据
        formatted_data = []
        for i, item in enumerate(data[:10], 1):
            formatted_data.append({
                "rank": i,
                "title": item.get('word'),
                "hot_score": item.get('num')
            })

        with open('weibo.json', 'w', encoding='utf-8') as f:
            json.dump(formatted_data, f, ensure_ascii=False, indent=4)
        print("weibo.json 保存成功")
    except Exception as e:
        print(f"微博保存失败: {e}")


# ================= 2. B站爬取并转换 =================
def save_bili_json():
    api_url = "https://s.search.bilibili.com/main/hotword"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com/"
    }
    try:
        response = requests.get(api_url, headers=headers)
        data = response.json().get('list', [])

        formatted_data = []
        for i, item in enumerate(data[:10], 1):
            formatted_data.append({
                "rank": i,
                "keyword": item.get('keyword'),
                "icon": item.get('icon')
            })

        with open('bili.json', 'w', encoding='utf-8') as f:
            json.dump(formatted_data, f, ensure_ascii=False, indent=4)
        print("bili.json 保存成功")
    except Exception as e:
        print(f"B站保存失败: {e}")


# ================= 3. 百度爬取并转换 =================
def save_baidu_json():
    api_url = "https://top.baidu.com/api/board?platform=pc&sa=pcindex_entry"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://top.baidu.com/board"
    }
    try:
        response = requests.get(api_url, headers=headers)
        hot_items = response.json()['data']['cards'][0]['content']

        formatted_data = []
        for i, item in enumerate(hot_items[:10], 1):
            formatted_data.append({
                "rank": i,
                "word": item.get('word'),
                "hot_score": item.get('hotScore'),
                "desc": item.get('desc')
            })

        with open('baidu.json', 'w', encoding='utf-8') as f:
            json.dump(formatted_data, f, ensure_ascii=False, indent=4)
        print("baidu.json 保存成功")
    except Exception as e:
        print(f"百度保存失败: {e}")


if __name__ == "__main__":
    save_weibo_json()
    save_bili_json()
    save_baidu_json()
    print("--- 爬取任务完成，准备推送 ---")
    pushme.push_to_phone()
