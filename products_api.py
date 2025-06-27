# services/phones_api.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# ─── A realistic catalog of 100 popular phones ────
# (Here, show just first 10; you would hard-code up to id=100)
PHONES = [
    {"id": 1,  "model": "iPhone 14 Pro Max",     "brand": "Apple",     "price": 1099.00},
    {"id": 2,  "model": "iPhone 14 Pro",         "brand": "Apple",     "price": 999.00},
    {"id": 3,  "model": "iPhone 14 Plus",        "brand": "Apple",     "price": 899.00},
    {"id": 4,  "model": "iPhone 14",             "brand": "Apple",     "price": 799.00},
    {"id": 5,  "model": "iPhone 13 Pro Max",     "brand": "Apple",     "price": 1099.00},
    {"id": 6,  "model": "iPhone 13 Pro",         "brand": "Apple",     "price": 999.00},
    {"id": 7,  "model": "iPhone 13",             "brand": "Apple",     "price": 799.00},
    {"id": 8,  "model": "iPhone 12 Pro Max",     "brand": "Apple",     "price": 1099.00},
    {"id": 9,  "model": "iPhone 12 Pro",         "brand": "Apple",     "price": 999.00},
    {"id": 10, "model": "iPhone SE (2022)",      "brand": "Apple",     "price": 429.00},

    {"id": 11, "model": "Galaxy S23 Ultra",      "brand": "Samsung",   "price": 1199.99},
    {"id": 12, "model": "Galaxy S23+",           "brand": "Samsung",   "price": 999.99},
    {"id": 13, "model": "Galaxy S23",            "brand": "Samsung",   "price": 799.99},
    {"id": 14, "model": "Galaxy S22 Ultra",      "brand": "Samsung",   "price": 1199.99},
    {"id": 15, "model": "Galaxy S22+",           "brand": "Samsung",   "price": 999.99},
    {"id": 16, "model": "Galaxy S22",            "brand": "Samsung",   "price": 799.99},
    {"id": 17, "model": "Galaxy Z Fold4",        "brand": "Samsung",   "price": 1799.99},
    {"id": 18, "model": "Galaxy Z Flip4",        "brand": "Samsung",   "price": 999.99},
    {"id": 19, "model": "Galaxy A53 5G",         "brand": "Samsung",   "price": 349.99},
    {"id": 20, "model": "Galaxy A33 5G",         "brand": "Samsung",   "price": 299.99},

    {"id": 21, "model": "Pixel 7 Pro",           "brand": "Google",    "price": 899.00},
    {"id": 22, "model": "Pixel 7",               "brand": "Google",    "price": 599.00},
    {"id": 23, "model": "Pixel 6a",              "brand": "Google",    "price": 449.00},
    {"id": 24, "model": "Pixel 6 Pro",           "brand": "Google",    "price": 899.00},
    {"id": 25, "model": "Pixel 6",               "brand": "Google",    "price": 599.00},
    {"id": 26, "model": "Pixel 5",               "brand": "Google",    "price": 699.00},
    {"id": 27, "model": "Pixel 4a",              "brand": "Google",    "price": 349.00},
    {"id": 28, "model": "Pixel 4a 5G",           "brand": "Google",    "price": 499.00},
    {"id": 29, "model": "Pixel 3a",              "brand": "Google",    "price": 399.00},
    {"id": 30, "model": "Pixel 3a XL",           "brand": "Google",    "price": 479.00},

    {"id": 31, "model": "OnePlus 11",            "brand": "OnePlus",   "price": 699.00},
    {"id": 32, "model": "OnePlus 10 Pro",        "brand": "OnePlus",   "price": 799.00},
    {"id": 33, "model": "OnePlus 10T",           "brand": "OnePlus",   "price": 649.00},
    {"id": 34, "model": "OnePlus Nord 2T",       "brand": "OnePlus",   "price": 399.00},
    {"id": 35, "model": "OnePlus Nord CE 3",     "brand": "OnePlus",   "price": 299.00},
    {"id": 36, "model": "OnePlus 9 Pro",         "brand": "OnePlus",   "price": 969.00},
    {"id": 37, "model": "OnePlus 9",             "brand": "OnePlus",   "price": 729.00},
    {"id": 38, "model": "OnePlus 8T",            "brand": "OnePlus",   "price": 599.00},
    {"id": 39, "model": "OnePlus 8 Pro",         "brand": "OnePlus",   "price": 899.00},
    {"id": 40, "model": "OnePlus 8",             "brand": "OnePlus",   "price": 699.00},

    {"id": 41, "model": "Mi 13 Pro",             "brand": "Xiaomi",    "price": 899.00},
    {"id": 42, "model": "Mi 13",                 "brand": "Xiaomi",    "price": 749.00},
    {"id": 43, "model": "Mi 12 Pro",             "brand": "Xiaomi",    "price": 799.00},
    {"id": 44, "model": "Mi 12",                 "brand": "Xiaomi",    "price": 599.00},
    {"id": 45, "model": "Redmi Note 12 Pro",     "brand": "Xiaomi",    "price": 279.99},
    {"id": 46, "model": "Redmi Note 11 Pro",     "brand": "Xiaomi",    "price": 229.99},
    {"id": 47, "model": "Redmi Note 10 Pro",     "brand": "Xiaomi",    "price": 199.99},
    {"id": 48, "model": "Poco X5 Pro",           "brand": "Xiaomi",    "price": 299.99},
    {"id": 49, "model": "Poco F5",               "brand": "Xiaomi",    "price": 329.99},
    {"id": 50, "model": "Poco M5",               "brand": "Xiaomi",    "price": 179.99},

    {"id": 51, "model": "Find X5 Pro",           "brand": "Oppo",      "price": 1149.00},
    {"id": 52, "model": "Find X5",               "brand": "Oppo",      "price": 999.00},
    {"id": 53, "model": "Reno 8 Pro+",           "brand": "Oppo",      "price": 799.00},
    {"id": 54, "model": "Reno 8 Pro",            "brand": "Oppo",      "price": 699.00},
    {"id": 55, "model": "Reno 8",                "brand": "Oppo",      "price": 599.00},
    {"id": 56, "model": "A77",                   "brand": "Oppo",      "price": 299.00},
    {"id": 57, "model": "A74 5G",                "brand": "Oppo",      "price": 249.00},
    {"id": 58, "model": "A54",                   "brand": "Oppo",      "price": 229.00},
    {"id": 59, "model": "A16",                   "brand": "Oppo",      "price": 179.00},
    {"id": 60, "model": "F21 Pro",               "brand": "Oppo",      "price": 299.00},

    {"id": 61, "model": "X90 Pro",               "brand": "Vivo",      "price": 999.00},
    {"id": 62, "model": "X90",                   "brand": "Vivo",      "price": 799.00},
    {"id": 63, "model": "V27 Pro",               "brand": "Vivo",      "price": 499.00},
    {"id": 64, "model": "V27",                   "brand": "Vivo",      "price": 399.00},
    {"id": 65, "model": "Y77 5G",                "brand": "Vivo",      "price": 279.00},
    {"id": 66, "model": "Y55s",                  "brand": "Vivo",      "price": 199.00},
    {"id": 67, "model": "Y33s",                  "brand": "Vivo",      "price": 249.00},
    {"id": 68, "model": "Y21s",                  "brand": "Vivo",      "price": 159.00},
    {"id": 69, "model": "Y15s",                  "brand": "Vivo",      "price": 129.00},
    {"id": 70, "model": "Y12s",                  "brand": "Vivo",      "price": 109.00},

    {"id": 71, "model": "Moto Edge 40 Pro",      "brand": "Motorola",  "price": 699.99},
    {"id": 72, "model": "Moto G200",             "brand": "Motorola",  "price": 499.99},
    {"id": 73, "model": "Moto G62",              "brand": "Motorola",  "price": 249.99},
    {"id": 74, "model": "Moto G42",              "brand": "Motorola",  "price": 199.99},
    {"id": 75, "model": "Moto G Power (2023)",   "brand": "Motorola",  "price": 179.99},
    {"id": 76, "model": "Moto Razr 40",          "brand": "Motorola",  "price": 999.99},
    {"id": 77, "model": "Moto Razr 2022",        "brand": "Motorola",  "price": 799.99},
    {"id": 78, "model": "Moto E32",              "brand": "Motorola",  "price": 149.99},
    {"id": 79, "model": "Edge 30 Neo",           "brand": "Motorola",  "price": 299.99},
    {"id": 80, "model": "Edge 30 Fusion",        "brand": "Motorola",  "price": 399.99},

    {"id": 81, "model": "Nokia G50",             "brand": "Nokia",     "price": 249.99},
    {"id": 82, "model": "Nokia X20",             "brand": "Nokia",     "price": 399.99},
    {"id": 83, "model": "Nokia XR20",            "brand": "Nokia",     "price": 549.99},
    {"id": 84, "model": "Nokia C31",             "brand": "Nokia",     "price": 149.99},
    {"id": 85, "model": "Nokia G60",             "brand": "Nokia",     "price": 279.99},
    {"id": 86, "model": "Nokia G60 5G",          "brand": "Nokia",     "price": 299.99},
    {"id": 87, "model": "Nokia C21",             "brand": "Nokia",     "price": 119.99},
    {"id": 88, "model": "Nokia C10",             "brand": "Nokia",     "price": 109.99},
    {"id": 89, "model": "Nokia 5710 XpressAudio", "brand":"Nokia",     "price": 99.99},
    {"id": 90, "model": "Nokia 2660 Flip",       "brand":"Nokia",      "price": 89.99},

    {"id": 91, "model": "ROG Phone 6",           "brand": "Asus",      "price": 999.00},
    {"id": 92, "model": "ROG Phone 6 Pro",       "brand": "Asus",      "price": 1299.00},
    {"id": 93, "model": "Zenfone 9",             "brand": "Asus",      "price": 699.00},
    {"id": 94, "model": "Zenfone 8",             "brand": "Asus",      "price": 599.00},
    {"id": 95, "model": "Zenfone 7 Pro",         "brand": "Asus",      "price": 799.00},
    {"id": 96, "model": "Zenfone 6",             "brand": "Asus",      "price": 499.00},
    {"id": 97, "model": "ROG Phone 5",           "brand": "Asus",      "price": 799.00},
    {"id": 98, "model": "ROG Phone 3",           "brand": "Asus",      "price": 699.00},
    {"id": 99, "model": "Zenfone 5Z",            "brand": "Asus",      "price": 499.00},
    {"id": 100,"model": "ROG Phone II",          "brand": "Asus",      "price": 899.00},
]


@app.route("/phones", methods=["GET"])
def list_or_recommend():
    """
    Query params:
      - limit (int): number of items to return
      - sort (asc|desc): ascending=cheapest first, descending=most expensive first
    """
    try:
        limit = int(request.args.get("limit", 0))
    except ValueError:
        limit = 0

    sort = request.args.get("sort", "asc").lower()
    reverse = sort == "desc"

    if limit > 0:
        sorted_phones = sorted(PHONES, key=lambda p: p["price"], reverse=reverse)
        return jsonify(sorted_phones[:limit])

    # no limit → return full catalog
    return jsonify(PHONES)

@app.route("/phones/<int:pid>", methods=["GET"])
def get_phone(pid):
    p = next((p for p in PHONES if p["id"] == pid), None)
    if p:
        return jsonify(p)
    return jsonify({"error": "not found"}), 404

if __name__ == "__main__":
    app.run(port=5051, debug=True)
