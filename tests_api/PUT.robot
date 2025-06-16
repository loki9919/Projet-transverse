*** Settings ***
Library     RequestsLibrary   # Import de la bibliothèque pour les requêtes HTTP
Library     Collections       # Import de la bibliothèque pour la manipulation de collections

*** Variables ***
${Base URL}         http://localhost:5000   # Définition de l'URL de base de l'API locale
${Nouveau_Titre}    Appartement Mis à Jour
${Nouveau_Prix}     ${120}
${Nouvelle_Description}    Description mise à jour par Robot Framework

*** Test Cases ***

Test Requete PUT Mise A Jour Annonce
    # D'abord, récupérer la liste des annonces pour obtenir un ID existant
    ${ReponseGET}=    GET    ${Base URL}/api/annonces    expected_status=200
    ${ListeAnnonces}=    Get From Dictionary    ${ReponseGET.json()}    annonces
    ${PremiereAnnonce}=    Get From List    ${ListeAnnonces}    0
    ${IdAnnonce}=    Get From Dictionary    ${PremiereAnnonce}    id
    
    Log    ID de l'annonce à modifier: ${IdAnnonce}
    
    # Création de la liste des équipements
    @{NouveauxEquipements}=    Create List    WiFi    Cuisine équipée    Balcon
    
    # Création du corps de la requête pour la mise à jour
    &{Corps_Requete}=  Create Dictionary    
    ...    titre=${Nouveau_Titre}        
    ...    prix_par_nuit=${Nouveau_Prix}
    ...    description=${Nouvelle_Description}
    ...    equipements=${NouveauxEquipements}
    
    # Envoi de la requête PUT
    ${Reponse}=     PUT    ${Base URL}/api/annonces/${IdAnnonce}    json=${Corps_Requete}    expected_status=200
    Log    ${Reponse.json()}
    
    # Vérification de la structure de la réponse
    Dictionary Should Contain Key     ${Reponse.json()}     message
    Dictionary Should Contain Key     ${Reponse.json()}     annonce
    
    # Récupération de l'annonce mise à jour
    ${AnnonceMiseAJour}=    Get From Dictionary    ${Reponse.json()}    annonce
    
    # Vérification que l'ID n'a pas changé
    ${IdRetourne}=    Get From Dictionary    ${AnnonceMiseAJour}    id
    Should Be Equal As Strings    ${IdAnnonce}    ${IdRetourne}
    
    # Vérification des données mises à jour
    ${titre}=    Get From Dictionary     ${AnnonceMiseAJour}    titre
    Should Be Equal As Strings    ${Nouveau_Titre}   ${titre}
    
    ${prix}=    Get From Dictionary     ${AnnonceMiseAJour}    prix_par_nuit
    Should Be Equal As Numbers    ${Nouveau_Prix}    ${prix}
    
    ${description}=    Get From Dictionary     ${AnnonceMiseAJour}    description
    Should Be Equal As Strings    ${Nouvelle_Description}    ${description}
    
    # Vérification des nouveaux équipements
    ${equipements}=    Get From Dictionary    ${AnnonceMiseAJour}    equipements
    Should Contain    ${equipements}    Balcon
    
    # Vérification finale : récupérer l'annonce individuellement pour confirmer la mise à jour
    ${ReponseVerification}=    GET    ${Base URL}/api/annonces/${IdAnnonce}    expected_status=200
    ${AnnonceVerifiee}=    Get From Dictionary    ${ReponseVerification.json()}    annonce
    ${TitreVerifie}=    Get From Dictionary    ${AnnonceVerifiee}    titre
    Should Be Equal As Strings    ${Nouveau_Titre}    ${TitreVerifie}