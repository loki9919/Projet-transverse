*** Settings ***
Library     RequestsLibrary   # Import de la bibliothèque pour les requêtes HTTP
Library     Collections       # Import de la bibliothèque pour la manipulation de collections

*** Variables ***
${Base URL}         http://localhost:5000   # Définition de l'URL de base de l'API locale
${Titre_Attendu}    Villa Test Robot Framework
${Lieu_Attendu}     Casablanca, Maroc
${Prix_Attendu}     ${75}
${Description_Attendue}    Belle villa pour tests automatisés

*** Test Cases ***

Test Requete POST Creer Annonce
    # Création de la liste des équipements
    @{Equipements}=    Create List    WiFi    Parking    Jardin
    
    # Création du corps de la requête avec tous les champs requis
    &{Corps_Requete}=  Create Dictionary    
    ...    titre=${Titre_Attendu}        
    ...    lieu=${Lieu_Attendu}
    ...    prix_par_nuit=${Prix_Attendu}
    ...    description=${Description_Attendue}
    ...    equipements=${Equipements}
    
    # Envoi de la requête POST
    ${Reponse}=     POST    ${Base URL}/api/annonces    json=${Corps_Requete}    expected_status=201
    log      ${Reponse.json()}   # Affichage de la réponse JSON dans les logs
    
    # Vérification de la structure de la réponse
    Dictionary Should Contain Key     ${Reponse.json()}     message
    Dictionary Should Contain Key     ${Reponse.json()}     annonce
    
    # Récupération de l'annonce créée
    ${AnnonceCreee}=    Get From Dictionary    ${Reponse.json()}    annonce
    
    # Vérification de la présence de l'ID généré
    Dictionary Should Contain Key     ${AnnonceCreee}     id
    ${Id}=    Get From Dictionary    ${AnnonceCreee}    id
    Should Not Be Empty    ${Id}
    
    # Vérification des données créées
    ${titre}=    Get From Dictionary     ${AnnonceCreee}    titre
    Should Be Equal As Strings    ${Titre_Attendu}   ${titre}
    
    ${lieu}=    Get From Dictionary     ${AnnonceCreee}    lieu
    Should Be Equal As Strings    ${Lieu_Attendu}    ${lieu}
    
    ${prix}=    Get From Dictionary     ${AnnonceCreee}    prix_par_nuit
    Should Be Equal As Numbers    ${Prix_Attendu}    ${prix}
    
    ${description}=    Get From Dictionary     ${AnnonceCreee}    description
    Should Be Equal As Strings    ${Description_Attendue}    ${description}
    
    # Vérification des équipements
    Dictionary Should Contain Key     ${AnnonceCreee}     equipements
    ${equipements}=    Get From Dictionary    ${AnnonceCreee}    equipements
    Should Contain    ${equipements}    WiFi