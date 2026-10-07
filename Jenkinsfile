pipeline {
    agent any
    environment {
        PYTHON = 'C:/Users/Анастасия/AppData/Local/Programs/Python/Python314/python.exe'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install dependencies') {
            steps {
                bat '"%PYTHON%" -m pip install -r requirements.txt'
            }
        }
        stage('Run tests') {
            steps {
                bat '"%PYTHON%" -m pytest -v'
            }
        }
        stage('Deploy') {
            when { branch 'main' }
            steps {
                bat '''
                    robocopy . C:\\deploy\\library /E /XD .git .pytest_cache __pycache__ /NFL /NDL /NJH /NJS /NP
                    if %ERRORLEVEL% LSS 8 exit /b 0
                    exit /b 1
                '''
                bat '"%PYTHON%" -m pip install -r C:/deploy/library/requirements.txt'
                echo 'Application deployed to C:\\deploy\\library'
            }
        }
    }
    post {
        success {
            echo 'CI pipeline completed successfully'
        }
        failure {
            echo 'CI pipeline failed'
        }
    }
}