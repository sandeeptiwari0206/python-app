pipeline {
    agent none

    environment {
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            agent { label 'windows' }
            steps {
                checkout scm
            }
        }

        stage('Build Images') {
            agent { label 'windows' }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DH_USER',
                    passwordVariable: 'DH_PASS'
                )]) {
                    bat """
                    docker build -t %DH_USER%/python-backend:%IMAGE_TAG% backend
                    docker build -t %DH_USER%/python-frontend:%IMAGE_TAG% frontend
                    """
                }
            }
        }

        stage('Push Images') {
            agent { label 'windows' }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DH_USER',
                    passwordVariable: 'DH_PASS'
                )]) {
                    bat """
                    echo %DH_PASS% | docker login -u %DH_USER% --password-stdin
                    docker push %DH_USER%/python-backend:%IMAGE_TAG%
                    docker push %DH_USER%/python-frontend:%IMAGE_TAG%
                    """
                }
            }
        }

        stage('Deploy via Docker Compose') {
            agent { label 'ec2' }

            steps {
                withCredentials([
                    string(credentialsId: 'mongo-uri', variable: 'MONGO_URI'),
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DH_USER',
                        passwordVariable: 'DH_PASS'
                    )
                ]) {
                    sh '''
                    set -e

                    mkdir -p ~/app
                    cd ~/app

                    cat > docker-compose.yml << EOF
                    version: '3.8'

                    services:
                      backend:
                        image: ${DH_USER}/python-backend:${IMAGE_TAG}
                        container_name: backend
                        ports:
                          - "8000:8000"
                        environment:
                          MONGO_URI: ${MONGO_URI}
                        restart: always

                      frontend:
                        image: ${DH_USER}/python-frontend:${IMAGE_TAG}
                        container_name: frontend
                        ports:
                          - "80:80"
                        restart: always
                    EOF

                    echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
                    docker-compose down
                    docker-compose pull
                    docker-compose up -d
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully"
        }
        failure {
            echo "❌ Pipeline failed"
        }
    }
}
