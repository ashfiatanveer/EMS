pipeline {
    agent any

    environment {
        // Set the Python version and virtual environment directory
        PYTHON_VERSION = 'python3.9'  // Adjust the Python version as needed
        VENV_DIR = '.venv'
        TEST_DIR = 'Unit Tests'  // Directory where the test files are located
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

        stage('Verify Test Files') {
            steps {
                script {
                    echo "Verifying test files in ${TEST_DIR}..."
                    sh 'ls -R ${TEST_DIR}'  // List all files in the Unit Tests directory
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run tests using pytest from the Unit Tests directory
                    sh '${VENV_DIR}/bin/pytest ${TEST_DIR}'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Add deployment steps here if needed
                    echo 'Deploying the application...'
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




