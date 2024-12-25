pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', 
                    url: 'git@github.com:ashfiatanveer/EMS', 
                    credentialsId: 'a6d973f0-7ec8-411c-b5cd-d01c634d8e6e'
            }
        }
        stage('Install Dependencies') {
            steps {
                bat 'C:\\Python312\\python.exe -m pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                bat 'C:\\Python312\\Scripts\\pytest.exe -v tests/'
            }
        }
    }
    post {
        always {
            echo 'Pipeline Completed'
        }
    }
}


