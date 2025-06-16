*** Settings ***
Library       RequestsLibrary   # Import de la bibliothèque pour les requêtes HTTP
Library       JSONLibrary       # Import de la bibliothèque pour la manipulation JSON
Library       Collections       # Import de la bibliothèque pour la manipulation de collections

*** Variables ***
${Base URL}   http://localhost:5000   # Définition de l'URL de base de l'API locale

*** Test Cases ***
Test 001 Requete GET Toutes Annonces
    ${Reponse}=       GET    ${Base URL}/api/annonces    expected_status=200
    ${ReponseJson}=   Set Variable     ${Reponse.json()}   # Convertir la réponse JSON en dictionnaire
    Log    ${ReponseJson}
    
    # Vérifier la structure de la réponse
    Dictionary Should Contain Key    ${ReponseJson}    annonces
    Dictionary Should Contain Key    ${ReponseJson}    nombre
    
    # Vérifier qu'il y a au moins 2 annonces d'exemple
    ${NombreAnnonces}=    Get From Dictionary    ${ReponseJson}    nombre
    Should Be True    ${NombreAnnonces} >= 2
    
    # Extraire la liste des annonces
    ${ListeAnnonces}=      Get From Dictionary     ${ReponseJson}     annonces
    ${PremiereAnnonce}=    Get From List          ${ListeAnnonces}   0
    
    # Vérifier la structure de la première annonce
    Dictionary Should Contain Key    ${PremiereAnnonce}    id
    Dictionary Should Contain Key    ${PremiereAnnonce}    titre
    Dictionary Should Contain Key    ${PremiereAnnonce}    lieu
    Dictionary Should Contain Key    ${PremiereAnnonce}    prix_par_nuit
    Dictionary Should Contain Key    ${PremiereAnnonce}    description
    Dictionary Should Contain Key    ${PremiereAnnonce}    equipements
    
    # Vérifier que le titre contient "Paris" ou "Miami" (données d'exemple)
    ${Titre}=    Get From Dictionary    ${PremiereAnnonce}    titre
    Should Match Regexp    ${Titre}    (Paris|Miami|Appartement|Maison)