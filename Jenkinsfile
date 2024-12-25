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
                    sh 'ls Unit\\ Tests'  // Ensure the zip file exists
                    sh 'unzip -o ${TEST_ZIP} -d ${TEST_DIR}'  // Extract the test files
                }
            }
        }

        stage('Verify Test Files') {
            steps {
                script {
                    echo "Verifying test files..."
                    sh 'ls -R ${TEST_DIR}'  // List the files to verify extraction
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh '${VENV_DIR}/bin/pytest -v ${TEST_DIR}'  // Run the tests with verbose output
                }
            }
        }
    }

    post {
        always {
            sh 'rm -rf ${VENV_DIR}'  // Clean up the virtual environment
        }
        success {
            echo 'The pipeline completed successfully.'
            junit '**/test-results.xml'  // Publish test results
        }
        failure {
            echo 'The pipeline failed.'
        }
    }
}
