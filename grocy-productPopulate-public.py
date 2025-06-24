import requests
import json

# --- CONFIG ---
GROCY_URL = "https://paste.your-full-grocy.url/"
API_KEY = "PASTE_YOUR_KEY_HERE"
CONTINUOUS_MODE = True  # toggle False if you want to test something
LABELS_USED = ["name", 
               "description", 
               "qu_id_purchase", 
               "qu_id_stock", 
               "product_group_id", 
               "location_id", 
               "default_consume_location_id", 
               "move_on_open", 
               "min_stock_amount", 
               "default_best_before_days_after_open", 
               "default_best_before_days", 
               "default_best_before_days_after_freezing", 
               "default_best_before_days_after_thawing"
]

products_to_post = []
products_to_add = [
    ["produt name",  # use only data here
     "product description", 
     "etc. There'll be a lot of IDs. Check them first"
    ],  # MUST MATCH LABELS_USED -- adjust as needed
    ["..."],
]

def populate_products():
    for p in products_to_add:
        new_prod = {}
        i = 0
        for label in LABELS_USED:
            new_prod[label] = p[i]
            i += 1
        products_to_post.append(new_prod)
        if not CONTINUOUS_MODE:
            break

def add_product(product_data):
    headers = {
        "GROCY-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }
    url = f"{GROCY_URL}/api/objects/products"
    try:
        response = requests.post(url, headers=headers, json=product_data)
        response.raise_for_status()  # 4xx / 5xx
        print(f"'{product_data['name']}' posted successfully!")
        # print(json.dumps(response.json(), indent=2))
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error posting '{product_data['name']}': {e}")
        print(f"Server response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error posting '{product_data['name']}': {e}")

# --- EXECUTAR ADIÇÃO DE PRODUTOS ---
if __name__ == "__main__":
    print(f"Converting products…")
    populate_products()
    print(f"Posting {len(products_to_add)} product(s)…")
    for product in products_to_post:
        add_product(product)
        if not CONTINUOUS_MODE:
            break
    print("Posting ended.")
