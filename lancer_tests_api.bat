@echo off
rem Cache l'affichage des commandes dans le terminal

echo Lancement des tests d'API Robot Framework...
rem Affiche ce message avant d'exécuter les tests API

cd tests_api
robot *.robot
rem Lance tous les tests Robot Framework dans le dossier tests_api
