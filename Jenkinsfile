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
                // остановить старую версию, скопировать новую и запустить приложение в фоне
                withEnv(['JENKINS_NODE_COOKIE=dontKillMe']) {
                    powershell '''
                        $ErrorActionPreference = 'Continue'
                        $Python = $env:PYTHON
                        $Target = 'C:\\deploy\\library'
                        $Port = 5000

                        # 1. stop the previous version (the process that listens on the port)
                        Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
                        Start-Sleep -Seconds 1

                        # 2. copy the tested version (robocopy codes below 8 mean success)
                        robocopy . $Target /E /XD .git .pytest_cache __pycache__ /NFL /NDL /NJH /NJS /NP | Out-Null
                        if ($LASTEXITCODE -ge 8) { throw 'robocopy failed' }

                        # 3. install dependencies in the deployed folder
                        & $Python -m pip install -r "$Target\\requirements.txt" --quiet
                        if ($LASTEXITCODE -ne 0) { throw 'pip failed' }

                        # 4. start the application in the background (it keeps running after the build)
                        $env:JENKINS_NODE_COOKIE = 'dontKillMe'
                        $ArgList = '-m','flask','--app','app','run','--host','127.0.0.1','--port',"$Port"
                        Start-Process -FilePath $Python -ArgumentList $ArgList -WorkingDirectory $Target -WindowStyle Hidden -RedirectStandardOutput "$Target\\app.log" -RedirectStandardError "$Target\\app-error.log"
                        $global:LASTEXITCODE = 0
                        exit 0
                    '''
                }
                // проверить, что приложение отвечает на этом компьютере
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
            echo 'CI pipeline completed successfully'
        }
        failure {
            echo 'CI pipeline failed'
        }
    }
}
