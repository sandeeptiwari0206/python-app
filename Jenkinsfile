pipeline {
    agent any

    environment {
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Images') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DH_USER',
                    passwordVariable: 'DH_PASS'
                )]) {
                    sh '''
                    docker build -t $DH_USER/python-backend:$IMAGE_TAG backend
                    docker build -t $DH_USER/python-frontend:$IMAGE_TAG frontend
                    '''
                }
            }
        }

        stage('Push Images') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DH_USER',
                    passwordVariable: 'DH_PASS'
                )]) {
                    sh '''
                    docker login -u $DH_USER -p $DH_PASS
                    docker push $DH_USER/python-backend:$IMAGE_TAG
                    docker push $DH_USER/python-frontend:$IMAGE_TAG
                    '''
                }
            }
        }

        stage('Deploy via Docker Compose') {
            steps {
                withCredentials([
                    string(credentialsId: 'ec2-host', variable: 'EC2_HOST'),
                    sshUserPrivateKey(
                        credentialsId: 'ec2-key',
                        keyFileVariable: 'SSH_KEY'
                    ),
                    string(credentialsId: 'mongo-uri', variable: 'MONGO_URI'),
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DH_USER',
                        passwordVariable: 'DH_PASS'
                    )
                ]) {
                    sh """
                    ssh -i $SSH_KEY ubuntu@$EC2_HOST << EOF
                    set -e

                    mkdir -p ~/app
                    cd ~/app

                    cat > docker-compose.yml << COMPOSE
                    version: "3.8"

                    services:
                      backend:
                        image: $DH_USER/python-backend:$IMAGE_TAG
                        container_name: backend
                        ports:
                          - "8000:8000"
                        environment:
                          MONGO_URI: $MONGO_URI
                          SECRET_KEY: \$(openssl rand -hex 16)
                        restart: always

                      frontend:
                        image: $DH_USER/python-frontend:$IMAGE_TAG
                        container_name: frontend
                        ports:
                          - "80:80"
                        restart: always
                    COMPOSE

                    docker login -u $DH_USER -p $DH_PASS
                    docker-compose down
                    docker-compose pull
                    docker-compose up -d
                    EOF
                    """
                }
            }
        }
    }
}
