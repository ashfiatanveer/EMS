pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/YourUsername/YourRepo', 
                    credentialsId: 'github-token'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'C:\\Users\\ashfi\\AppData\\Local\\Programs\\Python\\Python313\\python.exe -m pip install --upgrade pip' // Upgrade pip
                bat 'C:\\Users\\ashfi\\AppData\\Local\\Programs\\Python\\Python313\\python.exe -m pip install -r requirements.txt' // Install dependencies
            }
        }

        stage('Run Tests') {
            steps {
                bat 'C:\\Users\\ashfi\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\pytest.exe -v tests/' // Run tests
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}

