pipeline {
    agent any
    options {
        disableConcurrentBuilds()
    }
    stages {
        stage('Build') {
			      when {
                expression {
                    GIT_BRANCH = 'origin/' + sh(returnStdout: true, script: 'git rev-parse --abbrev-ref HEAD').trim()
                    return env.GIT_BRANCH == 'origin/master'
                }
            }
            steps {
                sh 'docker-compose -f docker-compose-prod.yml build'
            }
        }
        stage('Delivery') {
			      when {
                expression {
                    GIT_BRANCH = 'origin/' + sh(returnStdout: true, script: 'git rev-parse --abbrev-ref HEAD').trim()
                    return env.GIT_BRANCH == 'origin/master'
                }
            }
            steps {
                sh 'docker-compose -f docker-compose-prod.yml up -d'
            }
        }
    }
    post {
        always {
            dir("${env.WORKSPACE}cicd-jenkins@tmp") {
                deleteDir()
            }
        }
    }
}
