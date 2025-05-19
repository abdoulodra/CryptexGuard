from flask import Flask, render_template, request, redirect, url_for
import base64

app = Flask(__name__)

# Stockage temporaire des produits
products = [
    {"name": "Template CV Pro", "link": "#"},
    {"name": "Guide Sécurité PDF", "link": "#"},
    {"name": "Icônes Futuristes", "link": "#"}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crypt', methods=['GET', 'POST'])
def crypt():
    result = ""
    if request.method == 'POST':
        data = request.form.get('text')
        if data:
            result = base64.b64encode(data.encode()).decode()
    return render_template('crypt.html', result=result)

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    result = ""
    if request.method == 'POST':
        data = request.form.get('text')
        try:
            result = base64.b64decode(data.encode()).decode()
        except Exception:
            result = "Erreur de décryptage"
    return render_template('decrypt.html', result=result)

@app.route('/shop', methods=['GET', 'POST'])
def shop():
    if request.method == 'POST':
        name = request.form.get('name')
        link = request.form.get('link')
        if name and link:
            products.append({"name": name, "link": link})
    return render_template('shop.html', products=products)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)