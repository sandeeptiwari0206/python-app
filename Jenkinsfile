pipeline {
    agent none

    environment {
        DOCKERHUB_USER = "sandeeptiwari0206"
        BACKEND_IMAGE  = "python-backend"
        FRONTEND_IMAGE = "python-frontend"
        TAG            = "11"
    }

    stages {

        stage('Checkout, Build & Push (Built-In Node)') {
            agent { label 'built-in' }

            environment {
                DOCKERHUB_TOKEN = credentials('dockerhub-pass')
            }

            steps {
                checkout scm

                sh '''
                  echo "🔹 Building Docker images"
                  docker build -t ${DOCKERHUB_USER}/${BACKEND_IMAGE}:${TAG} backend
                  docker build -t ${DOCKERHUB_USER}/${FRONTEND_IMAGE}:${TAG} frontend

                  echo "🔹 Login to Docker Hub"
                  echo "${DOCKERHUB_TOKEN}" | docker login -u ${DOCKERHUB_USER} --password-stdin

                  echo "🔹 Pushing Docker images"
                  docker push ${DOCKERHUB_USER}/${BACKEND_IMAGE}:${TAG}
                  docker push ${DOCKERHUB_USER}/${FRONTEND_IMAGE}:${TAG}

                  echo "🔹 Logout from Docker Hub"
                  docker logout
                '''
            }
        }

        stage('Deploy on EC2') {
            agent { label 'ec2' }

            steps {
                checkout scm

                sh '''
                  echo "🔹 Pulling latest images on EC2"
                  docker pull sandeeptiwari0206/python-backend:11
                  docker pull sandeeptiwari0206/python-frontend:11

                  echo "🔹 Deploying with Docker Compose"
                  docker compose down
                  docker compose up -d
                '''
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
