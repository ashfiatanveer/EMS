pipeline {
    agent any

    environment {
        PYTHON_VERSION = 'python3.9'
        VENV_DIR = '.venv'
        TEST_DIR = 'Unit Tests'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Python Version') {
            steps {
                script {
                    sh 'python3.9 --version || python --version'
                }
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

        stage('Debug Virtual Environment') {
            steps {
                script {
                    sh 'ls -R ${VENV_DIR}'
                }
            }
        }

        stage('Verify Test Files') {
            steps {
                script {
                    echo "Verifying test files in ${TEST_DIR}..."
                    sh 'ls -R "${TEST_DIR}"'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh '${VENV_DIR}/bin/pytest ${TEST_DIR} -v --capture=no'
                }
            }
        }
    }

    post {
        always {
            sh 'rm -rf ${VENV_DIR}'
        }
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}



