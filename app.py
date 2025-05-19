from flask import Flask, render_template, request, redirect, url_for, flash
import os
from cryptography.fernet import Fernet
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Clé de cryptage
if not os.path.exists("secret.key"):
    with open("secret.key", "wb") as key_file:
        key_file.write(Fernet.generate_key())

with open("secret.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

# Base de données des produits
PRODUCTS_FILE = "products.json"

def load_products():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "r") as f:
            return json.load(f)
    return []

def save_products(products):
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    encrypted = None
    if request.method == 'POST':
        data = request.form['data']
        encrypted = fernet.encrypt(data.encode()).decode()
    return render_template('encrypt.html', encrypted=encrypted)

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    decrypted = None
    if request.method == 'POST':
        data = request.form['data']
        try:
            decrypted = fernet.decrypt(data.encode()).decode()
        except:
            flash("Données invalides ou corrompues.", "danger")
    return render_template('decrypt.html', decrypted=decrypted)

@app.route('/shop')
def shop():
    products = load_products()
    return render_template('shop.html', products=products)

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        product = {"name": name, "price": price, "description": description}
        products = load_products()
        products.append(product)
        save_products(products)
        flash("Produit ajouté avec succès !", "success")
        return redirect(url_for('shop'))
    return render_template('add_product.html')

@app.route('/about')
def about():
    return render_template('about.html')

# ✅ Support pour Railway (ou tout autre service cloud)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
