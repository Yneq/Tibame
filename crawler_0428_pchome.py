import urllib.request as req
import bs4 as bs
import ssl
import pandas as pd
import os  # 加入 os 模組
# 忽略 SSL 憑證驗證
ssl._create_default_https_context = ssl._create_unverified_context

# 建立 pchome 資料夾（如果不存在）
if not os.path.exists("pchome"):
    os.makedirs("pchome")

url = "https://24h.pchome.com.tw/search/?q=%E5%90%B9%E9%A2%A8%E6%A9%9F"
resp = req.urlopen(url)
html = bs.BeautifulSoup(resp.read())
links = html.find_all("a", {"class":"c-prodInfoV2__link"})

# 創建一個列表來存儲所有商品資料
all_products = []

for link in links:
    link_href = "https://24h.pchome.com.tw" + link["href"]
    print("商品連結:", link_href)
    
    # 抓取商品名稱
    product_resp = req.urlopen(link_href)
    product_html = bs.BeautifulSoup(product_resp.read())
    product_name = product_html.find("h1", {"class":"o-prodMainName__grayDarkest"})

    # 產品品牌
    product_brand = product_html.find("span", {"class":"o-prodMainName__colorSecondary"})
    if product_brand:
        product_brand = product_brand.text.strip()
    else:
        product_brand = "-"

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
    
    # 評價幾分/評價幾則
    rating = product_html.find("div", {"class":"c-ratingIcon__flex"})
    product_rating_text = "-"
    product_count_text = "-"
    if rating:
        product_rating = rating.find("div", {"class":"c-ratingIcon__textNumber"})
        product_count = rating.find("a")
        if product_rating:
            product_rating_text = product_rating.text.strip()
        if product_count:
            product_count_text = product_count.text.strip().replace("則評價", "")
    
    # 介紹
    intro = product_html.find_all("li", {"class":"c-blockCombine__item--prodSlogan"})
    intro_text = []
    if intro:
        for item in intro:
            intro_text.append(item.text.strip())
        intro_text = "\n".join(intro_text)
    else:
        intro_text = "-"

    # 圖片的網址
    image_url = product_html.find("div", {"class":"c-radiusPhotoImage__img"})
    if image_url:
        image_url = image_url.find("img")["src"]
        if not "https" in image_url:
            image_url = "https:" + image_url
    else:
        image_url = "-"
    # 存圖片
    fn = link_href.split("/")[-1]
    fn = "pchome/" + fn + ".jpg"
    req.urlretrieve(image_url, fn)
    # 將商品資料加入列表
    product_data = {
        "商品名稱": product_name.text.strip() if product_name else "-",
        "品牌": product_brand,
        "原價": original_price.text.strip() if original_price else "-",
        "目前售價": current_price.text.strip() if current_price else "-",
        "滿額贈": free_gift_text,
        "評價": product_rating_text,
        "評價人數": product_count_text,
        "介紹": intro_text,
        "圖片網址": image_url
    }
    all_products.append(product_data)

    # 印出當前商品資訊
    print("商品名稱:", product_data["商品名稱"])
    print("品牌:", product_data["品牌"])
    print("原價:", product_data["原價"])
    print("目前售價:", product_data["目前售價"])
    print("滿額贈:", product_data["滿額贈"])
    print("評價:", product_data["評價"])
    print("評價人數:", product_data["評價人數"])
    print("介紹:", product_data["介紹"])
    print("圖片網址:", product_data["圖片網址"])
    print("-" * 50)

# 使用 pandas 處理資料
df = pd.DataFrame(all_products)

# 基本資料處理
print("\n基本統計資訊:")
print(df.describe())

# 計算有滿額贈的商品比例
print("\n滿額贈商品比例:")
print(df["滿額贈"].value_counts(normalize=True))

# 儲存處理後的資料
df.to_csv("pchome_products.csv", index=False, encoding="utf-8")



