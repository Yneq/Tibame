import urllib.request as req
url = "https://i.imgur.com/WdUrSRO.gif"
r = req.Request(url)
r.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/10")

img = req.urlopen(r)
# 儲存檔案
# 以前(純文字): f = open("a.txt", "w", encoding="utf-8")
# 如果不是純文字: f = open("", "wb")
with open("xx.gif", "wb") as f:
    f.write(img.read())
     