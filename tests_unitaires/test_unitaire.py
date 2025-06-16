import unittest
import json
from app import app, annonces, init_donnees_exemple

class HomeyApiTestsUnitaires(unittest.TestCase):

    def setUp(self):
        # Créer un client de test
        self.app = app.test_client()
        self.app.testing = True
        
        # Réinitialiser la base de données avant chaque test
        annonces.clear()
        init_donnees_exemple()
    
    def test_obtenir_toutes_annonces(self):
        # Tester l'obtention de toutes les annonces
        response = self.app.get('/api/annonces')
        donnees = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('annonces', donnees)
        self.assertEqual(len(donnees['annonces']), 2)  # Nous avons initialisé avec 2 annonces d'exemple
    
    def test_obtenir_annonce(self):
        # Obtenir un ID d'annonce de la base de données
        id_annonce = list(annonces.keys())[0]
        
        # Tester l'obtention d'une annonce spécifique
        response = self.app.get(f'/api/annonces/{id_annonce}')
        donnees = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('annonce', donnees)
        self.assertEqual(donnees['annonce']['id'], id_annonce)
    
    def test_obtenir_annonce_inexistante(self):
        # Tester l'obtention d'une annonce qui n'existe pas
        response = self.app.get('/api/annonces/id-inexistant')
        donnees = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('erreur', donnees)
    
    def test_creer_annonce(self):
        # Créer des données de test
        nouvelle_annonce = {
            "titre": "Cabane en Montagne",
            "lieu": "Denver, USA",
            "prix_par_nuit": 120,
            "description": "Cabane confortable dans les montagnes",
            "equipements": ["Cheminée", "Sentiers de randonnée"]
        }
        
        # Tester la création d'une nouvelle annonce
        response = self.app.post('/api/annonces', 
                              data=json.dumps(nouvelle_annonce),
                              content_type='application/json')
        donnees = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('annonce', donnees)
        self.assertEqual(donnees['annonce']['titre'], nouvelle_annonce['titre'])
        
        # Vérifier que l'annonce a été ajoutée à la base de données
        self.assertEqual(len(annonces), 3)  # 2 exemples + 1 nouvelle
    
    def test_creer_annonce_champs_manquants(self):
        # Créer des données de test avec des champs requis manquants
        annonce_incomplete = {
            "titre": "Annonce Incomplète",
            "lieu": "Quelque part"
            # prix_par_nuit et description manquants
        }
        
        # Tester la création d'une annonce avec des champs manquants
        response = self.app.post('/api/annonces', 
                              data=json.dumps(annonce_incomplete),
                              content_type='application/json')
        donnees = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('erreur', donnees)
    
    def test_mettre_a_jour_annonce(self):
        # Obtenir un ID d'annonce de la base de données
        id_annonce = list(annonces.keys())[0]
        
        # Créer des données de mise à jour
        donnees_mise_a_jour = {
            "titre": "Titre Mis à Jour",
            "prix_par_nuit": 200
        }
        
        
        # Tester la mise à jour d'une annonce
        response = self.app.put(f'/api/annonces/{id_annonce}', 
                             data=json.dumps(donnees_mise_a_jour),
                             content_type='application/json')
        donnees = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('annonce', donnees)
        self.assertEqual(donnees['annonce']['titre'], donnees_mise_a_jour['titre'])
        self.assertEqual(donnees['annonce']['prix_par_nuit'], donnees_mise_a_jour['prix_par_nuit'])
    
    def test_mettre_a_jour_annonce_inexistante(self):
        # Créer des données de mise à jour
        donnees_mise_a_jour = {"titre": "Titre Mis à Jour"}
        
        # Tester la mise à jour d'une annonce qui n'existe pas
        response = self.app.put('/api/annonces/id-inexistant', 
                             data=json.dumps(donnees_mise_a_jour),
                             content_type='application/json')
        donnees = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('erreur', donnees)
    
    def test_supprimer_annonce(self):
        # Obtenir un ID d'annonce de la base de données
        id_annonce = list(annonces.keys())[0]
        
        # Tester la suppression d'une annonce
        response = self.app.delete(f'/api/annonces/{id_annonce}')
        donnees = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', donnees)
        
        # Vérifier que l'annonce a été supprimée de la base de données
        self.assertEqual(len(annonces), 1)  # Commencé avec 2, supprimé 1
    
    def test_supprimer_annonce_inexistante(self):
        # Tester la suppression d'une annonce qui n'existe pas
        response = self.app.delete('/api/annonces/id-inexistant')
        donnees = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('erreur', donnees)
    
    def test_verification_sante(self):
        # Tester le point de terminaison de vérification de santé
        response = self.app.get('/sante')
        donnees = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(donnees['statut'], 'en bonne santé')

if __name__ == '__main__':
    unittest.main()