from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'real_world_secret_food_key'

food_menu = {
    "Starters": {
        "Veg Crispy": 160,
        "Paneer Chilli": 180,
        "Chicken Lollipop (4 Pcs)": 190,
        "Chicken Tikka": 220
    },
    "Main Course": {
        "Paneer Butter Masala": 190,
        "Veg Maratha": 180,
        "Dal Makhani": 150,
        "Chicken Handi": 260,
        "Butter Chicken": 250,
        "Tandoori Roti": 20,
        "Butter Naan": 45
    },
    "Today Special": {
        "Paneer Pasanda": 210,
        "Chicken Rara": 270,
        "Matka Paneer Biryani": 220,
        "Mutton Rogan Josh": 320
    },
    "Combo Offers": {
        "Mini Veg Combo": 149,
        "Executive Veg Thali": 199,
        "Chicken Semi-Thali": 219,
        "Single Biryani Combo": 199,
        "Burger Buddy Combo": 149,
        "Chinese Combo": 169
    }
}

print("🔮 🍽️ ━━━━━━━ ROHINI'S SECRET SPICE LAB ━━━━━━━ 🍽️ 🔮")
print("             Where Flavor Meets Your Soul             ")
for category, items in food_menu.items():
    print(f"\n🔹 {category} 🔹")
    for dish, price in items.items():
        print(f"   - {dish}: ₹{price}")

@app.route('/')
def index():
    if 'cart' not in session:
        session['cart'] = {}
    return render_template('menu.html', menu=food_menu, cart=session['cart'])


@app.route('/add_to_cart/<string:item_name>', methods=['POST'])
def add_to_cart(item_name):
    cart = session.get('cart', {})

    all_dishes = {}
    for cat, items in food_menu.items():
        all_dishes.update(items)
    if item_name in all_dishes:
        cart[item_name] = cart.get(item_name, 0) + 1
        session['cart'] = cart
        
    return redirect(url_for('index'))

@app.route('/checkout')
def checkout():
    cart = session.get('cart', {})
    order_items = []
    subtotal = 0.0
    all_dishes = {}
    for cat, items in food_menu.items():
        all_dishes.update(items)
    for dish_name, quantity in cart.items():
        if dish_name in all_dishes:
            price = all_dishes[dish_name]
            total_item_price = price * quantity
            subtotal += total_item_price
            order_items.append({
                "name": dish_name,
                "quantity": quantity,
                "price_per_unit": price,
                "total_price": round(total_item_price, 2)
            })

    tax = round(subtotal * 0.08, 2)       # ८% फूड टॅक्स
    final_total = round(subtotal + tax, 2)

    return render_template('checkout.html', items=order_items, subtotal=round(subtotal, 2), tax=tax, total=final_total)

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
