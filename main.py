import json
import os
import time
from datetime import datetime

# --- FAILLARLA ISH UCUN KOMEKCI FUNKSIYALAR ---
def load_json(filename, default_value):
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(default_value, f, indent=4)
        return default_value
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def log_event(username, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(f"history_{username}.log", "a", encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")

# --- ILKIN MELUMATLARIN YARADILMASI ---
DEFAULT_PRODUCTS = {
    "Geyimlər": [
        {"id": 1, "name": "T-Shirt", "price": 12.50},
        {"id": 2, "name": "Hoodie", "price": 45.00},
        {"id": 3, "name": "Jeans", "price": 60.00}
    ],
    "Elektronika": [
        {"id": 1, "name": "Qulaqlıq", "price": 35.00},
        {"id": 2, "name": "Powerbank", "price": 25.00},
        {"id": 3, "name": "Siçan", "price": 15.00}
    ]
}

DEFAULT_USERS = [
    {"username": "admin", "password": "123", "balance": 100.0, "failed_attempts": 0, "lock_until": None}
]

class MiniStore:
    def __init__(self):
        self.users = load_json("users.json", DEFAULT_USERS)
        self.products = load_json("products.json", DEFAULT_PRODUCTS)
        self.current_user = None

    def login(self):
        print("--- Mağaza Sisteminə Giriş ---")
        username = input("İstifadəçi adı: ")
        
        user = next((u for u in self.users if u['username'] == username), None)
        if not user:
            print("İstifadəçi tapılmadı!")
            return False

        # Cooldown yoxlanışı
        if user['lock_until'] and time.time() < user['lock_until']:
            wait_time = int(user['lock_until'] - time.time())
            print(f"Hesab bloklanıb! {wait_time} saniyə gözləyin.")
            return False

        attempts = 0
        while attempts < 3:
            password = input(f"Parol ({3 - attempts} cəhd qaldı): ")
            if user['password'] == password:
                user['failed_attempts'] = 0
                user['lock_until'] = None
                self.current_user = user
                save_json("users.json", self.users)
                log_event(username, "LOGIN_SUCCESS")
                return True
            else:
                attempts += 1
                log_event(username, "LOGIN_FAIL (wrong password)")
        
        # 3 dəfə səhv olarsa
        user['lock_until'] = time.time() + 10
        save_json("users.json", self.users)
        print("3 dəfə səhv daxil etdiniz. 10 saniyə gözləyin.")
        return False

    def show_categories(self):
        while True:
            print("\n--- Kateqoriyalar ---")
            cats = list(self.products.keys())
            for idx, cat in enumerate(cats, 1):
                print(f"{idx}. {cat}")
            print("0. Geri")
            
            secim = input("Seçim edin: ")
            if secim == "0": break
            
            try:
                cat_name = cats[int(secim)-1]
                self.show_products(cat_name)
            except:
                print("Yanlış seçim!")

    def show_products(self, cat_name):
        while True:
            print(f"\n--- {cat_name} ---")
            items = self.products[cat_name]
            for p in items:
                print(f"{p['id']}. {p['name']} - {p['price']} AZN")
            
            p_id = input("Məhsul ID seçin (və ya 'back'): ")
            if p_id == 'back': break
            
            product = next((p for p in items if str(p['id']) == p_id), None)
            if product:
                qty = int(input("Miqdar: "))
                if qty <= 0:
                    print("Miqdar müsbət olmalıdır!")
                    continue
                
                print(f"Seçim: [B] Səbət | [F] Favorit | [X] Ləğv")
                action = input("> ").upper()
                
                if action == 'B':
                    self.add_to_basket(cat_name, product, qty)
                elif action == 'F':
                    self.add_to_favorites(cat_name, product)

    def add_to_basket(self, cat, prod, qty):
        basket = load_json(f"basket_{self.current_user['username']}.json", [])
        item = {
            "category": cat,
            "product": prod['name'],
            "unit": prod['price'],
            "qty": qty,
            "line_total": prod['price'] * qty
        }
        basket.append(item)
        save_json(f"basket_{self.current_user['username']}.json", basket)
        log_event(self.current_user['username'], f"BASKET_ADD ({cat}/{prod['name']} x{qty})")
        print("Səbətə əlavə edildi.")

    def checkout(self):
        basket_file = f"basket_{self.current_user['username']}.json"
        basket = load_json(basket_file, [])
        total = sum(item['line_total'] for item in basket)
        
        if total == 0:
            print("Səbət boşdur.")
            return

        print(f"Toplam məbləğ: {total} AZN. Balans: {self.current_user['balance']} AZN")
        if self.current_user['balance'] >= total:
            self.current_user['balance'] -= total
            # Tarixçəyə və alışlara yaz
            purchases = load_json(f"purchases_{self.current_user['username']}.json", [])
            purchases.append({"ts": str(datetime.now()), "items": basket, "total": total})
            save_json(f"purchases_{self.current_user['username']}.json", purchases)
            
            # Səbəti təmizlə və balans yenilə
            save_json(basket_file, [])
            save_json("users.json", self.users)
            log_event(self.current_user['username'], f"CHECKOUT_SUCCESS total={total}")
            print("Alış uğurla tamamlandı!")
        else:
            log_event(self.current_user['username'], "CHECKOUT_FAIL (insufficient balance)")
            print("Balans kifayət deyil!")

    def main_menu(self):
        while True:
            print(f"\nXoş gəldin, {self.current_user['username']}! Balans: {self.current_user['balance']} AZN")
            print("1) Kateqoriyalar\n2) Səbətim\n3) Favoritlər\n4) Tarixçə\n5) Settings\n0) Çıxış")
            choice = input("Seçim: ")
            
            if choice == "1": self.show_categories()
            elif choice == "2": self.checkout() # Sadəlik üçün birbaşa checkout-a yönləndirir
            elif choice == "5": self.change_password()
            elif choice == "0": break

    def change_password(self):
        old_pass = input("Köhnə şifrə: ")
        if old_pass == self.current_user['password']:
            new_pass = input("Yeni şifrə (min 4 simvol): ")
            if len(new_pass) >= 4:
                self.current_user['password'] = new_pass
                save_json("users.json", self.users)
                log_event(self.current_user['username'], "PASSWORD_CHANGED")
                print("Şifrə dəyişdirildi.")
            else:
                print("Şifrə çox qısadır!")
        else:
            print("Köhnə şifrə yanlışdır!")

# Proqramı başlat
if __name__ == "__main__":
    store = MiniStore()
    if store.login():
        store.main_menu()