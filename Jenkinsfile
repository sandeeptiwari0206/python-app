pipeline {
    agent any

    environment {
        DOCKERHUB_USER = "sandeeptiwari0206"
        BACKEND_IMAGE  = "python-backend"
        FRONTEND_IMAGE = "python-frontend"
        TAG            = "11"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Images') {
            environment {
                DH_PASS = credentials('dockerhub-pass')
            }
            steps {
                sh '''
                docker build -t ${DOCKERHUB_USER}/${BACKEND_IMAGE}:${TAG} backend
                docker build -t ${DOCKERHUB_USER}/${FRONTEND_IMAGE}:${TAG} frontend
                '''
            }
        }

        stage('Push Docker Images') {
            environment {
                DH_PASS = credentials('dockerhub-pass')
            }
            steps {
                sh '''
                echo "${DH_PASS}" | docker login -u ${DOCKERHUB_USER} --password-stdin
                docker push ${DOCKERHUB_USER}/${BACKEND_IMAGE}:${TAG}
                docker push ${DOCKERHUB_USER}/${FRONTEND_IMAGE}:${TAG}
                '''
            }
        }

        stage('Deploy via Docker Compose') {
            steps {
                sh '''
                cd /home/ubuntu/python-app || exit 1
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
