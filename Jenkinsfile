pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
        API_URL = 'http://localhost:5000'
        UI_URL = 'http://livraison3.testacademy.fr'
    }
    
    stages {
        stage('Build') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
                echo 'Build completed'
            }
        }
        
        stage('Unit Tests') {
            steps {
                bat './lancer_tests_unitaires.bat || exit /b 1'
            }
        }
        
        stage('Start API Server') {
            steps {
                script {
                    bat 'start /B python app.py'
                    // Allow time for the server to start using ping instead of timeout
                    bat 'ping -n 6 127.0.0.1 > nul'
                }
            }
        }
        
        stage('API Tests') {
            steps {
                bat './lancer_tests_api.bat || exit /b 1'
            }
        }
        
        stage('UI Tests') {
            steps {
                bat './lancer_tests_ui.bat || exit /b 1'
            }
        }
    }
    
    post {
        always {
            // Stop the API server
            bat 'taskkill /f /im python.exe /fi "WINDOWTITLE eq app.py" || exit /b 0'
        }
        success {
            echo 'All tests passed!'
        }
        failure {
            echo 'Tests failed'
        }
    }
}