pipeline {
    agent any

    environment {
        // Set the Python version and virtual environment directory
        PYTHON_VERSION = 'python3.9'
        VENV_DIR = '.venv'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the repository
                checkout scm
            }
        }

        stage('Set up Python Environment') {
            steps {
                script {
                    // Install virtual environment
                    sh '${PYTHON_VERSION} -m venv ${VENV_DIR}'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Install the dependencies from requirements.txt
                    sh '${VENV_DIR}/bin/pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run tests (assuming you are using pytest or another testing tool)
                    sh '${VENV_DIR}/bin/pytest'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Add deployment steps here (e.g., deploying to a cloud service, running a Docker container, etc.)
                    echo 'Deploying the application...'
                    // Example: docker build and push to container registry (if applicable)
                    // sh 'docker build -t my-flask-app .'
                    // sh 'docker push my-flask-app'
                }
            }
        }
    }

    post {
        always {
            // Clean up virtual environment
            sh 'rm -rf ${VENV_DIR}'
        }
        success {
            echo 'The pipeline completed successfully.'
        }
        failure {
            echo 'The pipeline failed.'
        }
    }
}
