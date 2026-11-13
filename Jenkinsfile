pipeline {
    agent any

    environment {
        PYTHON = 'C:/Users/Анастасия/AppData/Local/Programs/Python/Python314/python.exe'
    }

    stages {
        // скачивание исходного кода той ветки, в которой лежит этот Jenkinsfile
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // установка зависимостей
        stage('Install Dependencies') {
            steps {
                bat '"%PYTHON%" -m pip install -r requirements.txt'
            }
        }

        // запуск тестов
        stage('Tests') {
            steps {
                bat '"%PYTHON%" -m pytest -v'
            }
        }

        // остановка предыдущей версии: задача планировщика Windows и процесс на порту 5000; только для main
        stage('Stop Old Version') {
            when { branch 'main' }
            steps {
                powershell '''
                    Stop-ScheduledTask -TaskName 'LibraryApp' -ErrorAction SilentlyContinue
                    Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
                    exit 0
                '''
            }
        }

        // доставка: копирование проверенной версии в C:\deploy\library; только для main
        stage('Copy Application') {
            when { branch 'main' }
            steps {
                bat '''
                    robocopy . C:\\deploy\\library /E /XD .git .pytest_cache __pycache__ /NFL /NDL /NJH /NJS /NP
                    if %ERRORLEVEL% LSS 8 exit /b 0
                    exit /b 1
                '''
                bat '"%PYTHON%" -m pip install -r C:/deploy/library/requirements.txt'
            }
        }

        // запуск приложения ОТДЕЛЬНО от Jenkins: через планировщик задач Windows.
        // Jenkins только создаёт задачу и даёт команду "запустить", после чего сборка завершается,
        // а приложение работает как самостоятельный процесс.
        stage('Start Application') {
            when { branch 'main' }
            steps {
                powershell '''
                    $Arg = '/c ""' + $env:PYTHON + '" -m flask --app app run --host 127.0.0.1 --port 5000 > C:\\deploy\\library\\app.log 2>&1"'
                    $Action = New-ScheduledTaskAction -Execute 'cmd.exe' -Argument $Arg -WorkingDirectory 'C:\\deploy\\library'
                    $Principal = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -LogonType ServiceAccount -RunLevel Highest
                    $Settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit ([TimeSpan]::Zero) -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
                    Register-ScheduledTask -TaskName 'LibraryApp' -Action $Action -Principal $Principal -Settings $Settings -Force | Out-Null
                    Start-ScheduledTask -TaskName 'LibraryApp'
                    exit 0
                '''
            }
        }

        // проверка, что приложение отвечает на этом компьютере
        stage('Health Check') {
            when { branch 'main' }
            steps {
                retry(10) {
                    sleep time: 2, unit: 'SECONDS'
                    bat 'curl.exe -fsS http://127.0.0.1:5000/health'
                }
                echo 'Application deployed and running: http://127.0.0.1:5000'
            }
        }
    }

    post {
        success {
            echo 'CI pipeline completed successfully!'
        }

        failure {
            echo 'CI pipeline failed!'
        }
    }
}

