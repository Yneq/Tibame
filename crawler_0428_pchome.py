import urllib.request as req
import bs4 as bs
import ssl
import pandas as pd
# 忽略 SSL 憑證驗證
ssl._create_default_https_context = ssl._create_unverified_context

url = "https://24h.pchome.com.tw/search/?q=%E5%90%B9%E9%A2%A8%E6%A9%9F"
resp = req.urlopen(url)
html = bs.BeautifulSoup(resp.read())
links = html.find_all("a", {"class":"c-prodInfoV2__link"})
for link in links:
    link_href = "https://24h.pchome.com.tw" + link["href"]
    print("商品連結:", link_href)
    
    # 抓取商品名稱
    product_resp = req.urlopen(link_href)
    product_html = bs.BeautifulSoup(product_resp.read())
    product_name = product_html.find("h1", {"class":"o-prodMainName__grayDarkest"})
    
    # 修正價格的 class 名稱
    current_price = None
    original_price = None
    price_box = product_html.find("div", {"class":"o-prodPrice"})
    if price_box:
        current_price = price_box.find("div", {"class":"o-prodPrice__price"})
        original_price = price_box.find("div", {"class":"o-prodPrice__originalPrice"})
    
    # 滿額贈是否有(Y/N)
    free_gifts = product_html.find_all("div", {"class":"c-label__rectangle"})
    free_gift_text = "N"
    for free_gift in free_gifts:
        if "滿額贈" in free_gift.text.strip():
            free_gift_text = "Y"
            break
    
    # 評價幾分
    rating = product_html.find("div", {"class":"c-ratingIcon__textNumber"})
    rating_text = "-"
    if rating:
        rating_text = rating.text.strip()
    
    # 介紹
    intro = product_html.find_all("li", {"class":"c-blockCombine__item"})
    intro_text = []
    if intro:
        for item in intro:
            intro_text.append(item.text.strip())
        intro_text = " | ".join(intro_text)
    else:
        intro_text = "-"

    # 圖片的網址
    image_url = product_html.find("div", {"class":"c-radiusPhotoImage__img"})
    if image_url:
        image_url = image_url.find("img")["src"]
    else:
        image_url = "-"

    if product_name:
        print("商品名稱:", product_name.text.strip())
    if original_price:
        print("原價:", original_price.text.strip())
    if current_price:
        print("目前售價:", current_price.text.strip())
    print("滿額贈:", free_gift_text)
    print("評價:", rating_text)
    print("介紹:", intro_text)
    print("圖片網址:", image_url)
    print("-" * 50)

    # 將資料儲存到 CSV 檔案
    data = {
        "商品名稱": [product_name.text.strip() if product_name else "-"],
        "原價": [original_price.text.strip() if original_price else "-"],
        "目前售價": [current_price.text.strip() if current_price else "-"],
        "滿額贈": [free_gift_text],
        "評價": [rating_text],
        "介紹": [intro_text],
        "圖片網址": [image_url]
    }
    df = pd.DataFrame(data)
    df.to_csv("pchome_products.csv", mode="a", header=False, index=False)



