from flask import Flask, render_template, request, redirect, session
import sqlite3
from pageshtml import entete, basdepage
import random

app = Flask(__name__)
app.secret_key = "my_secret_key"

@app.route('/')
def index():
    if 'username' in session:
        return redirect('/numbers')
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Récupération du nom d'utilisateur
        username = request.form['username']

        # Vérification de l'existence de l'utilisateur dans la base de données
        conn = sqlite3.connect('static/collect.db')
        c = conn.cursor()
        c.execute("SELECT * FROM user WHERE nom=?", (username,))
        user = c.fetchone()
        conn.close()

        # Si l'utilisateur existe, on enregistre son nom dans la session et on redirige vers la page des numéros
        if user:
            session['username'] = username
            return redirect('/numbers')
        else:
            # Si l'utilisateur n'existe pas, on affiche un message d'erreur
            error = "Nom d'utilisateur invalide"
            return render_template('login/login.html', error=error)
    else:
        return render_template('login/login.html')

@app.route('/numbers')
def numbers():
    if 'username' in session:
        # Récupération des numéros de l'utilisateur
        conn = sqlite3.connect('static/collect.db')
        c = conn.cursor()
        id_usr = c.execute("SELECT id_usr FROM user WHERE nom=?", (session['username'],)).fetchone()[0]
        nums = c.execute("SELECT carte FROM assoc WHERE id_usr=?", (id_usr,)).fetchall()
        c.execute("SELECT MAX(id_carte) FROM carte")
        crt = c.fetchone()[0]
        nums = [num[0] for num in nums]
        conn.close()
        page = entete
        page += """
        <body>
            <h1>Nombres associés à votre compte</h1>
            <div class='cartes'>
        """
        new_lst = []
        if len(nums)==0:
            for j in range(crt):
                new_lst.append("0")
            for num in new_lst:
                page += f"<div class='carte'><img src='static/cartes/{num}.png' alt='Carte {num}'></div>"
            page += """
            </div>
            </body>
            """
            page += basdepage
            return page

        if nums[0] != 1:
            for j in range(1, nums[0]):
                new_lst.append("0")

        for i in range(min(crt, len(nums))):
            new_lst.append(nums[i])
            if i < len(nums)-1 and nums[i+1] - nums[i] > 1:
                for j in range(nums[i]+1, nums[i+1]):
                    new_lst.append("0")

        if crt > nums[-1]:
            for k in range(nums[-1]+1, crt+1):
                new_lst.append("0")
        for i, num in enumerate(new_lst):
            if i%5 == 0:
                page += "<div class='carte-col'>"
            page += f"<div class='carte'><img src='static/cartes/{num}.png' alt='Carte {num}'></div>"
            if (i+1)%5 == 0:
                page += "</div>"
        page += """
            </div>
        </body>
        """
        page += basdepage
        return page
    else:
        return redirect('/login')
    

@app.route('/booster')
def booster():
    page = entete
    page = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ma page web</title>
    </head>
    <body>
        <h1>Bienvenue sur ma page web !</h1>
        <img src="{{ image }}" alt="Image {{ loop.index }}">
        <button onclick="showImages()">Afficher les images</button>
        <script>
            function showImages() {
                var button = document.querySelector('button');
                button.style.display = 'none';
                {% for image in images %}
                var img = document.createElement('img');
                img.src = "{{ image }}";
                img.alt = "Image {{ loop.index }}";
                document.body.appendChild(img);
                {% endfor %}
            }
        </script>
    </body>
    </html>
    """
    images = [
        'static/cartes/1.png',
        'static/cartes/2.png',
        'static/cartes/3.png',
        'static/cartes/4.png',
        'static/cartes/5.png'
    ]
    page += basdepage
    return page


@app.route('/collection')
def collection():
    if 'username' in session:
        # Récupération des numéros de l'utilisateur
        conn = sqlite3.connect('static/collect.db')
        c = conn.cursor()
        c.execute("SELECT carte FROM assoc")
        cartes = [row[0] for row in c.fetchall()]
        conn.close()
        page = entete
        page += """
        <body>
            <h1>Collection complete du jeu</h1>
            <div class='cartes'>
        """
        
        for num in cartes:
            page += f"<div class='carte'><img src='static/cartes/{num}.png' alt='Carte {num}'></div>"
        page += """
            </div>
            </body>
            """
        page += basdepage
        return page
    else:
        return redirect('/login')


@app.route('/random_cards')
def random_cards():
    # Connexion à la base de données
    conn = sqlite3.connect('static/collect.db')
    c = conn.cursor()

    # Récupération des cartes les plus rares
    rarete_min = 1 # définir la rareté minimale souhaitée
    c.execute("SELECT nom FROM carte WHERE rarete >= ? ORDER BY rarete DESC LIMIT 3", (rarete_min,))
    result = c.fetchall()

    

     # Récupération des noms de cartes avec leur rareté
    cartes = c.execute("SELECT nom, rarete FROM carte").fetchall()
    # Fermeture de la connexion à la base de données
    c.close()
    conn.close()

    # Calcul des chances de tirage pour chaque carte en fonction de leur rareté
    chances = []
    for nom, rarete in cartes:
        if rarete == 3:
            chances.append(nom)
        elif rarete == 2:
            chances.append(nom)
            chances.append(nom)
        elif rarete == 1:
            chances.append(nom)
            chances.append(nom)
            chances.append(nom)
            chances.append(nom)
            chances.append(nom)
        elif rarete == 4:
            v= random.randint(1,4)
            if v==4:
                chances.append(nom)

    # Tirage de 5 cartes aléatoires avec les chances calculées
    resultat = random.choices(chances, k=5)

    conn.close()

    return str(resultat)

@app.route('/register')
def register1():    
#    page += """
#    <h1>Creer un compte</h1>
 #   <form method="POST" action="/register">
 #       <label for="valeur">Identifiant :</label>
#		<input type="text" id="valeur" name="valeur">
#		<button type="submit" name="action" value="update">Creer un compte</button>
#	</form>
#    """
    page ="""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Connexion</title>
        <link rel="stylesheet" href="static/register.css">
    </head>
    <div class="container">
    <form class="form-signin" method="POST" action="/register">
        <h2 class="form-signin-heading">Créer un compte</h2>
        <label for="inputUsername" class="sr-only">Nom d'utilisateur</label>
        <input type="text" id="inputUsername" name="valeur" class="form-control" placeholder="Nom d'utilisateur" required autofocus>
        <button class="btn btn-lg btn-primary btn-block" type="submit" name="action" value="update">Créer un compte</button>
    </form>
    <form class="form-signin" method="GET" action="/login">
        <button class="btn btn-lg btn-success btn-block" type="submit">Se connecter</button>
    </form>
    </div>

    """
    return page 

@app.route('/register', methods=['POST'])
def register():
    action = request.form['action']
    valeur = request.form['valeur']
    conn = sqlite3.connect('static/collect.db')
    c = conn.cursor()
    error=""
    if action == 'update':
        res = c.execute("SELECT MAX(id_usr) FROM user;")
        new_id = res.fetchone()[0] + 1
        c.execute("INSERT INTO user (id_usr, nom) VALUES (?, ?)", (new_id, valeur))
        conn.commit()
        c.close()
        error = "Enregistré avec succès"
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
