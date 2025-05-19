@echo off
rem Empêche d’afficher chaque commande exécutée dans le terminal

echo Lancement des tests unitaires...
rem Affiche ce message à l’écran pour indiquer ce qu’on va faire

python -m unittest discover -v unit_tests
rem Lance tous les tests dans le dossier unit_tests avec détails (-v = verbose)


