import requests
import time
import pygame

CSFLOAT_API_KEY = "your API" #type your api

pygame.mixer.init()
alert_sound = "tradeFound.mp3"
pygame.mixer.music.load(alert_sound)

items_to_watch = [
    {"name": "Revolution Case", "min_price": 22.0},     #example item listing method
    {"name": "Blackwolf | Sabre", "min_price": 5220.0}, #example item listing method
]

def fetch_lowest_buy_now_listing(item_name):
    url = "https://csfloat.com/api/v1/listings"
    params = {
        "market_hash_name": item_name,
        "sort_by": "lowest_price",
        "limit": 50 #sometimes it can't found items even though item is avalible in csfloat if you having this problem just increase this.
    }
    headers = {"Authorization": CSFLOAT_API_KEY}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"❌ HTTP {response.status_code} - {response.text[:100]}")
        return None, None

    data = response.json()

    if isinstance(data, dict):
        listings = list(data.values())
    elif isinstance(data, list):
        listings = data
    else:
        return None, None

    buy_now_listings = []

    for l in listings:
        if isinstance(l, dict):
            if l.get("type") == "buy_now":
                buy_now_listings.append(l)
        elif isinstance(l, list): 
            for sub in l:
                if isinstance(sub, dict) and sub.get("type") == "buy_now":
                    buy_now_listings.append(sub)

    if not buy_now_listings:
        return None, None

    listing = min(
        buy_now_listings,
        key=lambda x: x.get("price", x.get("min_price", float('inf')))
    )

    price = listing.get("price", listing.get("min_price")) / 100
    listing_id = listing.get("id")

    return price, listing_id

while True:
    for item in items_to_watch:
        price, listing_id = fetch_lowest_buy_now_listing(item["name"])
        if price is None or listing_id is None:
            print(f"{item['name']} için uygun buy_now ilan bulunamadı ❌")
            continue

        if price <= item["min_price"]:
            link = f"https://csfloat.com/item/{listing_id}"
            print(f"✅ ✅ ✅ {item['name']} ----- fiyatı {price} USD! ----- LINK: {link}")

            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

    print("----- 60 saniye bekleniyor -----\n")
    time.sleep(60)
