pipeline {
    agent none

    environment {
        DOCKERHUB_USER = "sandeeptiwari0206"
        BACKEND_IMAGE  = "python-backend"
        FRONTEND_IMAGE = "python-frontend"
        TAG            = "${BUILD_NUMBER}"
        PLATFORM       = "linux/amd64"
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
                  set -e

                  echo "🔹 Building Docker images with tag: ${TAG}"

                  docker build --platform=${PLATFORM} \
                    -t ${DOCKERHUB_USER}/${BACKEND_IMAGE}:${TAG} backend

                  docker build --platform=${PLATFORM} \
                    -t ${DOCKERHUB_USER}/${FRONTEND_IMAGE}:${TAG} frontend

                  echo "🔹 Login to Docker Hub"
                  echo "${DOCKERHUB_TOKEN}" | docker login -u ${DOCKERHUB_USER} --password-stdin

                  echo "🔹 Pushing Docker images"
                  docker push ${DOCKERHUB_USER}/${BACKEND_IMAGE}:${TAG}
                  docker push ${DOCKERHUB_USER}/${FRONTEND_IMAGE}:${TAG}

                  docker logout
                '''
            }
        }

        stage('Deploy on EC2') {
            agent { label 'ec2' }

            steps {
                checkout scm

                sh '''
                  set -e

                  echo "🔹 Deploying images with tag: ${TAG}"

                  docker pull ${DOCKERHUB_USER}/${BACKEND_IMAGE}:${TAG}
                  docker pull ${DOCKERHUB_USER}/${FRONTEND_IMAGE}:${TAG}

                  export IMAGE_TAG=${TAG}

                  docker compose down
                  docker compose up -d
                '''
            }
        }

        stage('Cleanup old Docker images on EC2') {
            agent { label 'ec2' }

            steps {
                sh '''
                  echo "🧹 Cleaning unused Docker images on EC2"
                  docker image prune -af
                  docker system df
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully with tag ${TAG}"
        }
        failure {
            echo "❌ Pipeline failed"
        }
    }
}
