pipeline {
    agent any

    environment {
        // Set the Python version and virtual environment directory
        PYTHON_VERSION = 'python3.9'
        VENV_DIR = '.venv'
        TEST_ZIP = 'Unit Tests/task.zip'  // Path to the zip file in your repository
        TEST_DIR = 'Unit Tests/test_files'  // Directory to extract the test files
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

        stage('Extract Test Files') {
            steps {
                script {
                    // Unzip the test files into a specific directory
                    sh 'unzip -o ${TEST_ZIP} -d ${TEST_DIR}'  // Extract test files from zip
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run tests using pytest from the test directory
                    sh '${VENV_DIR}/bin/pytest ${TEST_DIR}'
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

