pipeline {
    agent none

    environment {
        DOCKERHUB_USER = "sandeeptiwari0206"
        BACKEND_IMAGE  = "python-backend"
        FRONTEND_IMAGE = "python-frontend"
        TAG            = "11"
    }

    stages {

        stage('Checkout') {
            agent { label 'Jenkins' }   // Windows master
            steps {
                checkout scm
            }
        }

        stage('Build Docker Images') {
            agent { label 'Jenkins' }   // Windows master
            environment {
                DH_PASS = credentials('dockerhub-pass')
            }
            steps {
                bat """
                docker build -t %DOCKERHUB_USER%/%BACKEND_IMAGE%:%TAG% backend
                docker build -t %DOCKERHUB_USER%/%FRONTEND_IMAGE%:%TAG% frontend
                """
            }
        }

        stage('Push Docker Images') {
            agent { label 'Jenkins' }   // Windows master
            environment {
                DH_PASS = credentials('dockerhub-pass')
            }
            steps {
                bat """
                echo %DH_PASS% | docker login -u %DOCKERHUB_USER% --password-stdin
                docker push %DOCKERHUB_USER%/%BACKEND_IMAGE%:%TAG%
                docker push %DOCKERHUB_USER%/%FRONTEND_IMAGE%:%TAG%
                """
            }
        }

        stage('Deploy via Docker Compose') {
            agent { label 'ec2' }   // Ubuntu EC2
            options {
                skipDefaultCheckout(true)
            }
            steps {
                sh '''
                docker login -u sandeeptiwari0206 -p $(aws ecr get-login-password 2>/dev/null || true)

                docker pull sandeeptiwari0206/python-backend:11
                docker pull sandeeptiwari0206/python-frontend:11

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
