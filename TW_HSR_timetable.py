import requests
import json
import pandas as pd
url = "https://www.thsrc.com.tw/TimeTable/Search"

payload_s = """SearchType: S
Lang: TW
StartStation: TaiPei
EndStation: ZuoYing
OutWardSearchDate: 2025/04/28
OutWardSearchTime: 15:30
ReturnSearchDate: 2025/04/28
ReturnSearchTime: 15:30
DiscountType: """
payload = {}
for spl in payload_s.split("\n"):
    k, v = spl.split(": ")
    k, v = k.strip(), v.strip()
    payload[k] = v

resp = requests.post(url, payload)
resp_json = json.loads(resp.text)
data = resp_json["data"]["DepartureTable"]["TrainItem"]

df = pd.json_normalize(data)
print(df)

df.to_csv("TW_HSR_timetable.csv", index=False, encoding="utf-8")