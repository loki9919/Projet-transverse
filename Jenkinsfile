pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
        API_URL        = 'http://localhost:5000'
        UI_URL         = 'http://livraison3.testacademy.fr'
    }
    
    stages {
        stage('Construction') { // Étape 1 : installer les dépendances
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
                echo 'Construction terminée'
            }
        }
        
        stage('Tests unitaires') { // Étape 2 : exécuter les tests unitaires
            steps {
                bat './lancer_tests_unitaires.bat'
            }
        }
        
        stage('Démarrage du serveur API') { // Étape 3 : lancer l’API en arrière‑plan
            steps {
                script {
                    bat 'start /B python app.py'
                    // Attendre le démarrage du serveur via ping au lieu de timeout
                    bat 'ping -n 6 127.0.0.1 > nul'
                }
            }
        }
        
        stage('Tests de l’API') { // Étape 4 : exécuter les tests d’API
            steps {
                bat './lancer_tests_api.bat'
            }
        }
        
        stage('Tests de l’interface utilisateur') { // Étape 5 : exécuter les tests UI
            steps {
                bat './lancer_tests_ui.bat'
            }
        }
    }
    
    post {
        always {
            // Arrêter le serveur API
            bat 'taskkill /f /im python.exe /fi "WINDOWTITLE eq app.py" || exit /b 0'
        }
        success {
            echo 'Tous les tests ont réussi !'
        }
        failure {
            echo 'Échec des tests'
        }
    }
}

