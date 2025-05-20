*** Settings ***
Library    SeleniumLibrary
Resource    commun.resource
Suite Teardown     Close All Browsers

*** Test Cases ***
Le Tableau De Bord Doit Etre Visible Apres Une Connexion Réussie
    [Setup]    Effectuer Une Connexion Réussie
    Vérifier Que Le Tableau De Bord Est Visible
    [Teardown]    Effectuer Une Déconnexion Réussie


Le Lien De Deconnexion Devrait Etre Visible Après Une Déconnexion Réussie
    [Setup]    Effectuer Une Connexion Réussie
    Vérifier Que Le Tableau De Bord Est Visible
    Effectuer Une Déconnexion Réussie
    Vérifier Que Le Lien De Connexion Est Visible
    

*** Keywords ***
Effectuer Une Connexion Réussie
    Ouvrir Le Navigateur Et Accéder A L'Application
    Accéder A La Page De Connexion
    Saisir Le Nom D'Utilisateur    ${UTILISATEUR VALIDE} 
    Saisir Le Mot De Passe    ${MOT DE PASSE VALIDE} 
    Soumette Le Formulaire De Connexion

Vérifier Que Le Tableau De Bord Est Visible
    Wait Until Element Is Visible    ${LIEN SE DECONNECTER}
    Title Should Be    ${TITRE PAGE TABLEAU DE BORD} 

Effectuer Une Déconnexion Réussie
    Click Element    ${LIEN SE DECONNECTER} 
    Wait Until Element Is Not Visible    ${LIEN SE DECONNECTER} 
    
Vérifier Que Le Lien De Connexion Est Visible
    Wait Until Element Is Visible    ${LIEN SE CONNECTER} 

    
    
    
    