from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)

# Initialisation de la base de données
def init_db():
    conn = sqlite3.connect('banque.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS comptes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, solde REAL)''')
    conn.commit()
    conn.close()

init_db()

# Interface HTML simple
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Banque Web</title></head>
<body>
    <h1>Système Bancaire Simple</h1>
    <p>Utilisez les API suivantes pour interagir avec le système :</p>
    <ul>
        <li><b>POST /creer</b> : { "nom": "Jean", "solde_initial": 100 }</li>
        <li><b>DELETE /effacer/&lt;id&gt;</b></li>
        <li><b>POST /deposer/&lt;id&gt;</b> : { "montant": 50 }</li>
        <li><b>POST /retirer/&lt;id&gt;</b> : { "montant": 20 }</li>
        <li><b>GET /consulter/&lt;id&gt;</b></li>
    </ul>
    <p><i>Note : Dans un navigateur, accédez à /consulter/1 pour voir le compte 1. Utilisez Postman ou cURL pour les autres requêtes.</i></p>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

# 1. creerCompte(...)
@app.route('/creer', methods=['POST'])
def creerCompte():
    data = request.get_json()
    nom = data.get('nom')
    solde = data.get('solde_initial', 0.0)
    
    conn = sqlite3.connect('banque.db')
    c = conn.cursor()
    c.execute("INSERT INTO comptes (nom, solde) VALUES (?, ?)", (nom, solde))
    compte_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Compte créé", "id": compte_id, "nom": nom, "solde": solde}), 201

# 2. effacerCompte(...)
@app.route('/effacer/<int:compte_id>', methods=['DELETE'])
def effacerCompte(compte_id):
    conn = sqlite3.connect('banque.db')
    c = conn.cursor()
    c.execute("DELETE FROM comptes WHERE id = ?", (compte_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Compte {compte_id} effacé"}), 200

# 3. deposerArgent(...)
@app.route('/deposer/<int:compte_id>', methods=['POST'])
def deposerArgent(compte_id):
    data = request.get_json()
    montant = data.get('montant', 0.0)
    
    conn = sqlite3.connect('banque.db')
    c = conn.cursor()
    c.execute("UPDATE comptes SET solde = solde + ? WHERE id = ?", (montant, compte_id))
    conn.commit()
    conn.close()
    return jsonify({"message": f"{montant} déposé sur le compte {compte_id}"}), 200

# 4. retirerArgent(...)
@app.route('/retirer/<int:compte_id>', methods=['POST'])
def retirerArgent(compte_id):
    data = request.get_json()
    montant = data.get('montant', 0.0)
    
    conn = sqlite3.connect('banque.db')
    c = conn.cursor()
    c.execute("UPDATE comptes SET solde = solde - ? WHERE id = ?", (montant, compte_id))
    conn.commit()
    conn.close()
    return jsonify({"message": f"{montant} retiré du compte {compte_id}"}), 200

# 5. consulterCompte(...)
@app.route('/consulter/<int:compte_id>', methods=['GET'])
def consulterCompte(compte_id):
    conn = sqlite3.connect('banque.db')
    c = conn.cursor()
    c.execute("SELECT * FROM comptes WHERE id = ?", (compte_id,))
    compte = c.fetchone()
    conn.close()
    
    if compte:
        return jsonify({"id": compte[0], "nom": compte[1], "solde": compte[2]}), 200
    return jsonify({"erreur": "Compte introuvable"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)