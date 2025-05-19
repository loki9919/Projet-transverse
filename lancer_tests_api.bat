@echo off
rem Cache l'affichage des commandes dans le terminal

echo Lancement des tests d’API (unittest)...
rem Affiche ce message avant d'exécuter les tests API

python -m unittest discover -v api_tests
rem Lance tous les tests dans le dossier api_tests avec détails

pause
rem Garde la fenêtre ouverte pour voir les résultats