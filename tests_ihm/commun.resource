*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}    http://livraison3.testacademy.fr
${NAVIGATEUR}    chrome
${LIEN SE CONNECTER}    xpath=//a[contains(text(),'Se connecter')]
${LIEN SE DECONNECTER}    xpath=(//a[contains(text(),'Se déconnecter')])[3]
${CHAMP NOM UTILISATEUR}    name=username
${CHAMP MOT DE PASSE}    name=password 
${UTILISATEUR VALIDE}    robot
${MOT DE PASSE VALIDE}    robot
${BOUTON SE CONNECTER}    css=.homey_login_button
${ZONE ERREUR}    css=#modal-login .error
${TITRE PAGE TABLEAU DE BORD}    Tableau de bord - Livraison 3

*** Keywords ***
Ouvrir Le Navigateur Et Accéder A L'Application
    Open Browser    ${URL}     ${NAVIGATEUR}
    Maximize Browser Window

Accéder A La Page De Connexion
    Click Element    ${LIEN SE CONNECTER} 

Saisir Le Nom D'Utilisateur
    [Arguments]    ${utilisateur valide}
    Wait Until Element Is Visible    ${CHAMP NOM UTILISATEUR}
    Click Element    ${CHAMP NOM UTILISATEUR} 
    Input Text    ${CHAMP NOM UTILISATEUR}    ${utilisateur valide}

Saisir Le Mot De Passe
    [Arguments]       ${mot de passe}
    Input Text    ${CHAMP MOT DE PASSE}     ${mot de passe}

Soumette Le Formulaire De Connexion
    Click Button    ${BOUTON SE CONNECTER}

