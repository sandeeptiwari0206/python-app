pipeline {
    agent none

    environment {
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            agent any
            steps {
                checkout scm
            }
        }

        stage('Build Images') {
            agent any
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DH_USER',
                    passwordVariable: 'DH_PASS'
                )]) {
                    sh """
                    docker build -t ${DH_USER}/python-backend:${IMAGE_TAG} backend
                    docker build -t ${DH_USER}/python-frontend:${IMAGE_TAG} frontend
                    """
                }
            }
        }

        stage('Push Images') {
            agent any
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DH_USER',
                    passwordVariable: 'DH_PASS'
                )]) {
                    sh """
                    docker login -u ${DH_USER} -p ${DH_PASS}
                    docker push ${DH_USER}/python-backend:${IMAGE_TAG}
                    docker push ${DH_USER}/python-frontend:${IMAGE_TAG}
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
                    sh """
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

                    docker login -u ${DH_USER} -p ${DH_PASS}
                    docker-compose down
                    docker-compose pull
                    docker-compose up -d
                    """
                }
            }
        }
    }
}
