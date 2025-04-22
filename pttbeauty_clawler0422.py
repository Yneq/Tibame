import urllib.request as req
import bs4 as bs
import ssl
import json

# 忽略 SSL 憑證驗證
ssl._create_default_https_context = ssl._create_unverified_context

url = "https://www.ptt.cc/bbs/Beauty/M.1745240089.A.6CE.html"
r = req.Request(url)
r.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
resp = req.urlopen(r)
content = resp.read()
html = bs.BeautifulSoup(content, features="html.parser")


# 取得文章資訊
article_meta = html.find_all("span", {"class":"article-meta-value"})

# 初始化變數
author = title = time = board = ""
author = article_meta[0].text
title = article_meta[2].text
time = article_meta[3].text
board = article_meta[1].text

# 取得推文資訊
push_list = []
pushes = html.find_all("div", {"class":"push"})
for push in pushes:
    push_id = push.find("span", {"class":"push-userid"}).text
    push_type = push.find("span", {"class":"push-tag"}).text.strip()
    if "推" in push_type:
        push_type = 1
    elif "噓" in push_type:
        push_type = -1
    else:
        push_type = 0
    push_text = push.find("span", {"class":"push-content"}).text.strip()
    ipandtime = push.find("span", {"class":"push-ipdatetime"}).text.strip()
    
    push_data = {
        "id": push_id,
        "type": push_type,
        "text": push_text,
        "ip/time": ipandtime,
    }
    push_list.append(push_data)

# 建立完整的文章資料
article_data = {
    "作者": author,
    "標題": title,
    "時間": time,
    "看板": board,
    "推噓文": push_list
}


# 內文: extract() 命令消失
# 所以把main-content區塊裡面的其他的div都消失
main_content = html.find("div", {"id":"main-content"})
other_div = main_content.find_all("div")
for other in other_div:
    other.extract()
print("=========內文開始=========")
print(main_content.text.strip())
print("=========內文結束=========")

# 將資料存成 JSON 格式
with open("ptt_article.json", "w", encoding="utf-8") as f:
    json.dump(article_data, f, ensure_ascii=False, indent=4)

# 讀取並顯示 JSON 資料
with open("ptt_article.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)
    print("JSON 資料讀取成功！")
    print("\n文章資訊：")
    print(f"作者：{json_data['作者']}")
    print(f"標題：{json_data['標題']}")
    print(f"時間：{json_data['時間']}")
    print(f"看板：{json_data['看板']}")
    print(f"推文數量：{len(json_data['推噓文'])}")