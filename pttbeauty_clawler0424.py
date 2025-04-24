import json
import urllib.request as req
import bs4 as bs
import ssl

# 忽略 SSL 憑證驗證
ssl._create_default_https_context = ssl._create_unverified_context


url = "https://www.ptt.cc/bbs/Beauty/M.1745412049.A.FD6.html"
r = req.Request(url)
r.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/10")
resp = req.urlopen(r)
html = bs.BeautifulSoup(resp.read())

allow_subs = ["jpg", "jpeg", "png", "gif"]
link_list = html.find_all("a")
for link in link_list:
    link_href = link["href"]
    sub = link_href.split(".")[-1]
    if sub.lower() in allow_subs:
        print(link_href)