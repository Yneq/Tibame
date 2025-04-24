# 融合所有
import os
import json
import urllib.request as req
import bs4 as bs
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def  get_meta(url):
    # url = "https://www.ptt.cc/bbs/Beauty/M.1745216140.A.52E.html"
    r = req.Request(url)
    r.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/10")
    resp = req.urlopen(r)
    html = bs.BeautifulSoup(resp.read())

    # meta process
    metas = html.find_all("span", {"class":"article-meta-value"})
    post_id = metas[0].text
    board_name = metas[1].text
    post_title = metas[2].text
    post_time = metas[3].text

    # push process
    push_list = []
    pushes = html.find_all("div", {"class":"push"})
    for push in pushes:
        push_meta = push.find_all("span")
        p_type = push_meta[0].text
        if "推" in p_type:
            p_type = 1
        elif "噓" in p_type:
            p_type = -1
        else:
            p_type = 0
        p_id = push_meta[1].text
        p_text = push_meta[2].text.replace(": ", "")
        p_ipanddate = push_meta[3].text.strip()
        p_dict = {
            "id":p_id,
            "type":p_type,
            "text":p_text,
            "ip/date":p_ipanddate
        }
        push_list.append(p_dict)

    row = {
        "作者":post_id,
        "標題":post_title,
        "時間":post_time,
        "看板":board_name,
        "推噓文":push_list
    }

    fn = url.split("/")[-1].replace(".html", ".json")
    with open(fn, "w", encoding="utf-8") as f:
        json.dump(row, f, ensure_ascii=False, indent=4)

def get_img(url):
    # url = "https://www.ptt.cc/bbs/Beauty/M.1745412049.A.FD6.html"
    r = req.Request(url)
    r.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/10")
    resp = req.urlopen(r)
    html = bs.BeautifulSoup(resp.read())

    # 開啟資料夾
    dn = url.split("/")[-1]
    # dn = os.path.join("drive/MyDrive", dn)
    # 如果資料夾不存在, 我們就創造起來
    if not os.path.exists(dn):
        os.makedirs(dn)

    allow_subs = ["jpg", "jpeg", "png", "gif"]
    link_list = html.find_all("a")
    for link in link_list:
        link_href = link["href"]
        sub = link_href.split(".")[-1]
        if sub.lower() in allow_subs:
            img_url = link_href
            # 加上資料夾名字
            fn = img_url.split("/")[-1]
            fn = dn + "/" + fn
            # fn = "{}/{}".format(dn, fn)

            # save img
            r = req.Request(img_url)
            r.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/10")

            img = req.urlopen(r)
            with open(fn, "wb") as f:
                f.write(img.read())



url = "https://www.ptt.cc/bbs/Beauty/index4002.html"
r = req.Request(url)
r.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/10")
resp = req.urlopen(r)
html = bs.BeautifulSoup(resp.read())
    
# 找出所有文章連結
for entry in html.find_all("div", {"class": "r-ent"}):
    link = entry.find("a")
    if link != None:
        article_url = "https://www.ptt.cc" + link["href"]
        get_img(article_url)
        get_meta(article_url)



