import requests
import unittest
import json
import time

# URL de base de l'API - mettez à jour si votre service est déployé ailleurs
API_BASE_URL = "http://localhost:5000"

class HomeyApiTests(unittest.TestCase):
    
    def setUp(self):
        # Attendre que l'API soit disponible
        self.attendre_api()
        
        # Obtenir les annonces initiales (à utiliser dans les tests)
        response = requests.get(f"{API_BASE_URL}/api/annonces")
        self.annonces_initiales = response.json()["annonces"]
        
        # Pour les tests qui créent des annonces, nous stockerons les IDs pour nettoyer plus tard
        self.ids_annonces_creees = []
    
    def tearDown(self):
        # Nettoyer toutes les annonces créées pendant les tests
        for id_annonce in self.ids_annonces_creees:
            try:
                requests.delete(f"{API_BASE_URL}/api/annonces/{id_annonce}")
            except:
                pass
    
    def attendre_api(self, max_essais=5):
        """Attendre que l'API devienne disponible"""
        essais = 0
        while essais < max_essais:
            try:
                response = requests.get(f"{API_BASE_URL}/sante")
                if response.status_code == 200:
                    return True
                essais += 1
                time.sleep(1)
            except:
                essais += 1
                time.sleep(1)
        
        raise Exception("L'API n'est pas disponible")
    
    def test_obtenir_toutes_annonces(self):
        """Tester le point de terminaison GET /api/annonces"""
        response = requests.get(f"{API_BASE_URL}/api/annonces")
        
        self.assertEqual(response.status_code, 200)
        donnees = response.json()
        self.assertIn("annonces", donnees)
        self.assertIn("nombre", donnees)
        self.assertEqual(len(donnees["annonces"]), donnees["nombre"])
    
    def test_obtenir_annonce_specifique(self):
        """Tester le point de terminaison GET /api/annonces/{id}"""
        # Obtenir le premier ID d'annonce des annonces initiales
        if not self.annonces_initiales:
            self.skipTest("Pas d'annonces initiales disponibles pour le test")
        
        id_annonce = self.annonces_initiales[0]["id"]
        response = requests.get(f"{API_BASE_URL}/api/annonces/{id_annonce}")
        
        self.assertEqual(response.status_code, 200)
        donnees = response.json()
        self.assertIn("annonce", donnees)
        self.assertEqual(donnees["annonce"]["id"], id_annonce)
    
    def test_creer_annonce(self):
        """Tester le point de terminaison POST /api/annonces"""
        nouvelle_annonce = {
            "titre": "Annonce Test API",
            "lieu": "Lieu Test API",
            "prix_par_nuit": 99,
            "description": "Annonce test créée par test API",
            "equipements": ["Test API"]
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/annonces",
            json=nouvelle_annonce
        )
        
        self.assertEqual(response.status_code, 201)
        donnees = response.json()
        self.assertIn("annonce", donnees)
        self.assertEqual(donnees["annonce"]["titre"], nouvelle_annonce["titre"])
        
        # Stocker l'ID pour le nettoyage
        self.ids_annonces_creees.append(donnees["annonce"]["id"])
    
    def test_mettre_a_jour_annonce(self):
        """Tester le point de terminaison PUT /api/annonces/{id}"""
        # Créer une annonce à mettre à jour
        nouvelle_annonce = {
            "titre": "API Test - Mise à Jour",
            "lieu": "Lieu Test API",
            "prix_par_nuit": 99,
            "description": "Annonce test pour test de mise à jour",
            "equipements": ["Test API"]
        }
        
        create_response = requests.post(
            f"{API_BASE_URL}/api/annonces",
            json=nouvelle_annonce
        )
        
        id_annonce = create_response.json()["annonce"]["id"]
        self.ids_annonces_creees.append(id_annonce)
        
        # Mettre à jour l'annonce
        donnees_mise_a_jour = {
            "titre": "Annonce Test API Mise à Jour",
            "prix_par_nuit": 199
        }
        
        update_response = requests.put(
            f"{API_BASE_URL}/api/annonces/{id_annonce}",
            json=donnees_mise_a_jour
        )
        
        self.assertEqual(update_response.status_code, 200)
        donnees = update_response.json()
        self.assertIn("annonce", donnees)
        self.assertEqual(donnees["annonce"]["titre"], donnees_mise_a_jour["titre"])
        self.assertEqual(donnees["annonce"]["prix_par_nuit"], donnees_mise_a_jour["prix_par_nuit"])
    
    def test_supprimer_annonce(self):
        """Tester le point de terminaison DELETE /api/annonces/{id}"""
        # Créer une annonce à supprimer
        nouvelle_annonce = {
            "titre": "API Test - Suppression",
            "lieu": "Lieu Test API",
            "prix_par_nuit": 99,
            "description": "Annonce test pour test de suppression",
            "equipements": ["Test API"]
        }
        
        create_response = requests.post(
            f"{API_BASE_URL}/api/annonces",
            json=nouvelle_annonce
        )
        
        id_annonce = create_response.json()["annonce"]["id"]
        
        # Supprimer l'annonce
        delete_response = requests.delete(f"{API_BASE_URL}/api/annonces/{id_annonce}")
        
        self.assertEqual(delete_response.status_code, 200)
        donnees = delete_response.json()
        self.assertIn("message", donnees)
        self.assertIn("annonce", donnees)
        
        # Vérifier que l'annonce est supprimée
        get_response = requests.get(f"{API_BASE_URL}/api/annonces/{id_annonce}")
        self.assertEqual(get_response.status_code, 404)
    
    def test_gestion_erreurs(self):
        """Tester la gestion des erreurs de l'API"""
        # Tester ID d'annonce invalide
        response = requests.get(f"{API_BASE_URL}/api/annonces/id-inexistant")
        self.assertEqual(response.status_code, 404)
        
        # Tester données de requête invalides
        response = requests.post(
            f"{API_BASE_URL}/api/annonces",
            json={"titre": "Données Incomplètes"}  # Champs requis manquants
        )
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()