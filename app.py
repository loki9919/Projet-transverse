from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# Base de données en mémoire
annonces = {}

# Fonction d'aide pour générer un nouvel ID d'annonce
def generer_id():
    return str(uuid.uuid4())

# Initialisation des données d'exemple
def init_donnees_exemple():
    exemples_annonces = [
        {
            "id": generer_id(),
            "titre": "Appartement Cosy à Paris",
            "lieu": "Paris, France",
            "prix_par_nuit": 100,
            "description": "Bel appartement près de la Tour Eiffel",
            "equipements": ["WiFi", "Cuisine", "Climatisation"]
        },
        {
            "id": generer_id(),
            "titre": "Maison de Plage à Miami",
            "lieu": "Miami, USA",
            "prix_par_nuit": 150,
            "description": "Maison de plage relaxante avec vue sur l'océan",
            "equipements": ["WiFi", "Piscine", "Accès à la plage"]
        }
    ]
    
    for annonce in exemples_annonces:
        annonces[annonce["id"]] = annonce

init_donnees_exemple()

# GET - Récupérer toutes les annonces
@app.route('/api/annonces', methods=['GET'])
def obtenir_toutes_annonces():
    return jsonify({"annonces": list(annonces.values()), "nombre": len(annonces)})

# GET - Récupérer une annonce spécifique
@app.route('/api/annonces/<id_annonce>', methods=['GET'])
def obtenir_annonce(id_annonce):
    if id_annonce in annonces:
        return jsonify({"annonce": annonces[id_annonce]})
    return jsonify({"erreur": "Annonce non trouvée"}), 404

# POST - Créer une nouvelle annonce
@app.route('/api/annonces', methods=['POST'])
def creer_annonce():
    if not request.json:
        return jsonify({"erreur": "Données de requête invalides"}), 400
    
    donnees = request.json
    champs_requis = ["titre", "lieu", "prix_par_nuit", "description"]
    
    for champ in champs_requis:
        if champ not in donnees:
            return jsonify({"erreur": f"Champ requis manquant: {champ}"}), 400
    
    id_annonce = generer_id()
    
    nouvelle_annonce = {
        "id": id_annonce,
        "titre": donnees["titre"],
        "lieu": donnees["lieu"],
        "prix_par_nuit": donnees["prix_par_nuit"],
        "description": donnees["description"],
        "equipements": donnees.get("equipements", [])
    }
    
    annonces[id_annonce] = nouvelle_annonce
    
    return jsonify({"message": "Annonce créée avec succès", "annonce": nouvelle_annonce}), 201

# PUT - Mettre à jour une annonce
@app.route('/api/annonces/<id_annonce>', methods=['PUT'])
def mettre_a_jour_annonce(id_annonce):
    if id_annonce not in annonces:
        return jsonify({"erreur": "Annonce non trouvée"}), 404
    



    if not request.json:
        return jsonify({"erreur": "Données de requête invalides"}), 400
    
    donnees = request.json
    
    # Mettre à jour les champs
    for cle in donnees:
        if cle != "id":  # Ne pas permettre de changer l'ID
            annonces[id_annonce][cle] = donnees[cle]
    
    return jsonify({"message": "Annonce mise à jour avec succès", "annonce": annonces[id_annonce]})


# DELETE - Supprimer une annonce
@app.route('/api/annonces/<id_annonce>', methods=['DELETE'])
def supprimer_annonce(id_annonce):
    if id_annonce not in annonces:
        return jsonify({"erreur": "Annonce non trouvée"}), 404
    
    annonce_supprimee = annonces.pop(id_annonce)
    
    return jsonify({"message": "Annonce supprimée avec succès", "annonce": annonce_supprimee})

# Point de terminaison de vérification de santé
@app.route('/sante', methods=['GET'])
def verification_sante():
    return jsonify({"statut": "en bonne santé", "message": "L'API Homey fonctionne"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)