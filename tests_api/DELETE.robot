*** Settings ***
Library     RequestsLibrary   # Import de la bibliothèque pour les requêtes HTTP
Library     Collections       # Import de la bibliothèque pour la manipulation de collections

*** Variables ***
${Base URL}         http://localhost:5000   # Définition de l'URL de base de l'API locale

*** Test Cases ***

Test Requete DELETE Supprimer Annonce
    # Création de la liste des équipements
    @{EquipementsTest}=    Create List    Test
    
    # D'abord, créer une annonce à supprimer
    &{Annonce_A_Supprimer}=  Create Dictionary    
    ...    titre=Annonce à Supprimer
    ...    lieu=Test City
    ...    prix_par_nuit=${50}
    ...    description=Cette annonce sera supprimée
    ...    equipements=${EquipementsTest}
    
    ${ReponseCreation}=    POST    ${Base URL}/api/annonces    json=${Annonce_A_Supprimer}    expected_status=201
    ${AnnonceCreee}=    Get From Dictionary    ${ReponseCreation.json()}    annonce
    ${IdAnnonce}=    Get From Dictionary    ${AnnonceCreee}    id
    
    Log    ID de l'annonce créée pour suppression: ${IdAnnonce}
    
    # Vérifier que l'annonce existe avant suppression
    ${ReponseVerificationAvant}=    GET    ${Base URL}/api/annonces/${IdAnnonce}    expected_status=200
    Log    Annonce trouvée avant suppression
    
    # Supprimer l'annonce
    ${ReponseSuppression}=    DELETE    ${Base URL}/api/annonces/${IdAnnonce}    expected_status=200
    Log    ${ReponseSuppression.json()}
    
    # Vérifier la structure de la réponse de suppression
    Dictionary Should Contain Key    ${ReponseSuppression.json()}    message
    Dictionary Should Contain Key    ${ReponseSuppression.json()}    annonce
    
    # Vérifier le message de succès
    ${Message}=    Get From Dictionary    ${ReponseSuppression.json()}    message
    Should Contain    ${Message}    supprimée avec succès
    
    # Vérifier que l'annonce supprimée est retournée dans la réponse
    ${AnnonceSupprimee}=    Get From Dictionary    ${ReponseSuppression.json()}    annonce
    ${IdAnnonceSupprimee}=    Get From Dictionary    ${AnnonceSupprimee}    id
    Should Be Equal As Strings    ${IdAnnonce}    ${IdAnnonceSupprimee}
    
    # Vérifier que l'annonce n'existe plus
    ${ReponseVerificationApres}=    GET    ${Base URL}/api/annonces/${IdAnnonce}    expected_status=404
    Log    Annonce correctement supprimée - erreur 404 attendue
    
    # Vérifier le message d'erreur pour l'annonce inexistante
    Dictionary Should Contain Key    ${ReponseVerificationApres.json()}    erreur
    ${MessageErreur}=    Get From Dictionary    ${ReponseVerificationApres.json()}    erreur
    Should Be Equal As Strings    ${MessageErreur}    Annonce non trouvée