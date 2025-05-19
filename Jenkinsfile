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
                bat 'python test_unit.py'
            }
            post {
                always {
                    junit 'unit-test-results.xml'
                }
            }
        }
        
        stage('Start API Server') {
            steps {
                script {
                    bat 'start /B python app.py'
                    // Allow time for the server to start
                    bat 'timeout /t 5'
                }
            }
        }
        
        stage('API Tests') {
            steps {
                bat 'python test_api.py'
            }
            post {
                always {
                    junit 'api-test-results.xml'
                }
            }
        }
        
        stage('UI Tests') {
            steps {
                bat 'robot --outputdir results test_ui.robot'
            }
            post {
                always {
                    robot outputPath: 'results'
                }
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