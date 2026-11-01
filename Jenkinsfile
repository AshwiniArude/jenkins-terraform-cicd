// Jenkins Declarative Pipeline - Shipment Tracker
// Stages: Checkout -> Build (deps) -> Code Quality -> Unit Tests -> Docker Build -> Deploy -> Smoke Test
pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 20, unit: 'MINUTES')
    }

    // Fallback trigger: poll GitHub every ~2 minutes.
    // The GitHub webhook (configured in the job UI) triggers builds instantly on every push.
    triggers {
        pollSCM('H/2 * * * *')
    }

    environment {
        APP_NAME = 'shipment-tracker'
        APP_PORT = '5000'
        IMAGE    = "shipment-tracker:${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'echo "Commit under build:" && git log -1 --pretty=format:"%h - %s (%an)" && echo'
            }
        }

        stage('Build: Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --quiet --upgrade pip
                    pip install --quiet -r requirements.txt -r requirements-dev.txt
                    python --version
                '''
            }
        }

        stage('Code Quality (flake8)') {
            steps {
                sh '. .venv/bin/activate && flake8 app tests && echo "Lint passed"'
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    mkdir -p reports
                    pytest -v --junitxml=reports/junit.xml \
                           --cov=app --cov-report=term --cov-report=xml:reports/coverage.xml
                '''
            }
            post {
                always {
                    junit 'reports/junit.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build --build-arg BUILD_NUMBER=${BUILD_NUMBER} -t ${IMAGE} -t ${APP_NAME}:latest .
                    docker images ${APP_NAME}
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker rm -f ${APP_NAME} || true
                    docker run -d --name ${APP_NAME} --restart unless-stopped \
                        -p ${APP_PORT}:5000 -e BUILD_NUMBER=${BUILD_NUMBER} ${IMAGE}
                    docker ps --filter name=${APP_NAME}
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                    for i in $(seq 1 15); do
                        if curl -fsS http://localhost:${APP_PORT}/health; then
                            echo ""
                            curl -fsS http://localhost:${APP_PORT}/api/version
                            echo ""
                            echo "Smoke test PASSED - app is live on port ${APP_PORT}"
                            exit 0
                        fi
                        echo "Waiting for app to start... ($i)"
                        sleep 2
                    done
                    echo "Smoke test FAILED"
                    docker logs ${APP_NAME}
                    exit 1
                '''
            }
        }
    }

    post {
        success {
            echo "SUCCESS: Build #${env.BUILD_NUMBER} deployed. Open http://<EC2-PUBLIC-IP>:${env.APP_PORT}"
        }
        failure {
            echo "FAILURE: Build #${env.BUILD_NUMBER} failed - check the stage logs above."
        }
        always {
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
            sh 'docker image prune -f || true'
        }
    }
}
