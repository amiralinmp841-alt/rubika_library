import requests

# API public روبیکا (safe برای تست)
url = "https://messengerapi.ir/api/v3/getUserInfo"

# فقط یک یوزرنیم تستی، مهم نیست
data = {
    "username": "rubika"
}

try:
    r = requests.post(url, json=data, timeout=8)
    print("Status code:", r.status_code)
    print("Response:", r.text)
except Exception as e:
    print("Error:", e)
`
