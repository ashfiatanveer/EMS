pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                echo 'Debugging the pipeline...'
                git branch: 'main', 
                    url: 'git@github.com:ashfiatanveer/EMS', 
                    credentialsId: 'a6d973f0-7ec8-411c-b5cd-d01c634d8e6e'
            }
        }
        stage('Install Dependencies') {
            steps {
                echo 'Debugging the pipeline...'
                bat 'C:\\Python312\\python.exe -m pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                echo 'Debugging the pipeline...'
                bat 'set PYTHONPATH=%cd%\\src && C:\\Python312\\Scripts\\pytest.exe -v Tests/'
            }
        }
    }
    post {
        always {
            echo 'Debugging the pipeline...'
            echo 'Pipeline Completed'
        }
    }
}
