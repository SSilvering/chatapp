pipeline {
    
    agent any

    environment {
        git_commit_msg = sh(returnStdout: true, script: 'git log --format="medium" -1 ${GIT_COMMIT} | tail -1').trim()
        repository     = "chat"
        aws_registry   = "403567978083.dkr.ecr.eu-central-1.amazonaws.com"
    }

    // tools {
    //     terraform 'terraform'
    // }

    options {
        timestamps()

        timeout(unit: 'MINUTES', time: 10)

        buildDiscarder(logRotator(
            numToKeepStr: '4',
            daysToKeepStr: '7',
            artifactNumToKeepStr: '30')
        )

    }

    stages {  
        stage('Build') {  
            steps{
                echo 'Build docker image'

                sh "docker build -t chat:${BUILD_NUMBER} ."
            }
        }

        stage('Tagging') {
            when { branch 'release/*' } 
            steps {
                script {
                    sh "git fetch --tags || true"
                    cur_tag=(env.GIT_BRANCH - 'release/')
                    HIGHEST = sh(script: "git describe --tags `git rev-list --tags --max-count=1` || true", returnStdout: true).trim()

                    if (HIGHEST.isEmpty()) {                        
                        NEW_TAG=(env.GIT_BRANCH - 'release/'  + '.0')
                    } else {
                        NEW_TAG=HIGHEST.split('\\.')
                        NEW_TAG[2]=NEW_TAG[2].toInteger()+1
                        NEW_TAG=NEW_TAG.join('.')
                    }
                }
            }
        }    

        // Plugins: Docker pipeline, Amazon ECR plugin, CloudBees AWS Credentials Plugin
        stage('Push to ECR Stage') {
            when { branch 'release/*' } 
            steps {
                echo "Push to ECR"

                withDockerRegistry(credentialsId: 'ecr:eu-central-1:aws-auth', url: "https://${aws_registry}/${repository}" ) {
                    sh "docker tag chat:${BUILD_NUMBER} ${aws_registry}/${repository}:${NEW_TAG}"
                    sh "docker push ${aws_registry}/${repository}:${NEW_TAG}"
                }
                
                sh "git tag ${NEW_TAG}"
                sh "git push --tags"
            }
        }

        stage('E2E Test') {  
            steps{
                echo 'E2E Test'
            }
        }        

    }

    post { 
        always { 
            echo 'Post stage'
            deleteDir()
        }
        success {
            echo 'success'            
            // emailext (
            //     subject: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
            //     body: """<p>SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
            //         <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>""",
            //     recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            // )
        }
        failure {
            echo 'failure'
            // emailext (
            //     subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
            //     body: """<p>FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
            //         <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>""",
            //     recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            // )
        }
    }    
}