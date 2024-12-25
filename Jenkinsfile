pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/ashfiatanveer/EMS', 
                    credentialsId: 'github-token'
            }
        }
        stage('Install Dependencies') {
            steps {
                bat 'C:\\Users\\ashfi\\AppData\\Local\\Programs\\Python\\Python313\\python.exe -m pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                bat 'C:\\Users\\ashfi\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\pytest.exe -v tests/'
            }
        }
    }
    post {
        always {
            echo 'Pipeline Completed'
        }
    }
}
