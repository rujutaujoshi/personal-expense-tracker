
pipeline {
    agent {
    label 'built-in'
    }

    environment {
        DOCKER_IMAGE = 'rujutaujoshi/expenseflow'
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
                    python3 -m venv .venv
                    .venv/bin/python -m pip install --upgrade pip
                    .venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '.venv/bin/python -m pytest -v tests/'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} -t ${DOCKER_IMAGE}:latest .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_TOKEN'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_TOKEN" | docker login \
                          --username "$DOCKER_USER" \
                          --password-stdin

                        docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}
                        docker push ${DOCKER_IMAGE}:latest

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
    agent {
        label 'mac-minikube'
    }

    steps {
        checkout scm

        sh '''
            set -e

            export PATH="/usr/local/bin:$PATH"
            export KUBECONFIG="$HOME/.kube/config"

            echo "Checking Kubernetes context..."
            kubectl config current-context

            echo "Applying Kubernetes configurations..."
            kubectl apply -f k8s/persistent-volume-claim.yaml
            kubectl apply -f k8s/deployment.yaml
            kubectl apply -f k8s/service.yaml

            echo "Deploying image from the current Jenkins build..."
            kubectl set image deployment/expenseflow-deployment \
                expenseflow=${DOCKER_IMAGE}:${BUILD_NUMBER}

            echo "Waiting for Kubernetes rollout..."
            kubectl rollout status deployment/expenseflow-deployment --timeout=180s

            echo "Verifying Kubernetes deployment..."
            kubectl get pods -l app=expenseflow
            kubectl get service expenseflow-service
        '''
    }
}
    }
}
