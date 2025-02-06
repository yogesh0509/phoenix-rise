pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'phoenix-rise-app'
        DOCKER_TAG = 'latest'
    }
    
    triggers {
        cron('0 6 * * *') // Runs at 6:00 AM daily
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv  # Create a virtual environment
                    . venv/bin/activate && pip install --upgrade pip  # Activate the virtual environment and upgrade pip
                    . venv/bin/activate && pip install -r requirements.txt  # Install dependencies in the virtual environment
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
            }
        }
        
        stage('Deploy') {
            steps {
                // Stop existing container if running
                sh '''
                    docker ps -q --filter "name=phoenix-rise" | grep -q . && docker stop phoenix-rise && docker rm -f phoenix-rise || echo "No container running"
                '''
                
                // Run new container
                sh '''
                    docker run -d \
                        --name phoenix-rise \
                        -p 5000:5000 \
                        ${DOCKER_IMAGE}:${DOCKER_TAG}
                '''
            }
        }
        
        stage('Health Check') {
            steps {
                // Wait for application to start
                sh 'sleep 10'
                
                // Check if endpoint is responding
                sh 'curl -f http://localhost:5000/api/v2/monitor || exit 1'
            }
        }

        stage('Run Tests') {
            steps {
                // Run tests for both good and bad endpoints
                sh '''
                    . venv/bin/activate && pytest test_app.py
                '''
            }
        }
    }
    
    post {
        failure {
            echo 'Pipeline failed! Sending notification...'
        }
        success {
            echo 'Pipeline succeeded! Application is deployed.'
        }
        always {
            // Clean workspace
            cleanWs()
        }
    }
} 