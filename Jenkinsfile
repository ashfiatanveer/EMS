pipeline {
    agent any

    environment {
        PYTHON_VERSION = 'python3.9'
        VENV_DIR = '.venv'
        TEST_ZIP = 'Unit Tests/task.zip'
        TEST_DIR = 'Unit Tests/test_files'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set up Python Environment') {
            steps {
                script {
                    sh '${PYTHON_VERSION} -m venv ${VENV_DIR}'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    sh '${VENV_DIR}/bin/pip install -r requirements.txt'
                }
            }
        }

        stage('Extract Test Files') {
            steps {
                script {
                    // Ensure the zip file exists
                    sh 'ls Unit\\ Tests'
                    sh 'unzip -o ${TEST_ZIP} -d ${TEST_DIR}'
                }
            }
        }

        stage('Verify Test Files') {
            steps {
                script {
                    echo "Verifying test files..."
                    sh 'ls -R ${TEST_DIR}'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh '${VENV_DIR}/bin/pytest ${TEST_DIR}'
                }
            }
        }
    }

    post {
        always {
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
