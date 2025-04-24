import json
import urllib.request as req
import bs4 as bs
import ssl
import os
# 忽略 SSL 憑證驗證
ssl._create_default_https_context = ssl._create_unverified_context


url = "https://www.ptt.cc/bbs/Beauty/M.1745412049.A.FD6.html"
r = req.Request(url)
r.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/10")
resp = req.urlopen(r)
html = bs.BeautifulSoup(resp.read())

# 開啟資料夾
dn = url.split("/")[-1]
# 如果資料夾不存在, 我們就創造起來
if not os.path.exists(dn):
    os.makedirs(dn)
# dn = os.path.join("drive/MyDrive", dn)

allow_subs = ["jpg", "jpeg", "png", "gif"]
link_list = html.find_all("a")
for link in link_list:
    link_href = link["href"]
    sub = link_href.split(".")[-1]
    if sub.lower() in allow_subs:
        img_url = link_href
        # 加上資料夾名字
        fn = img_url.split("/")[-1]
        fn = "{}/{}".format(dn, fn)

        # save img
        r = req.Request(img_url)
        r.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/10")

        img = req.urlopen(r)
        with open(fn, "wb") as f:
            f.write(img.read())

# =========================
# import os
# # 用程式開啟資料夾
# dn = "test/test2"
# fn = dn + "/a.txt"
# # 如果資料夾不存在, 我們就創造起來
# if not os.path.exists(dn):
#     os.makedirs(dn)

# with open(fn, "w", encoding="utf-8") as f:
#     f.write("adsfasdf")
# =========================