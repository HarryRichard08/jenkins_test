pipeline {
    agent any

    environment {
        // Initialize vmDetails as an empty environment variable.
        vmDetails = ''
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs() // This will clean the workspace before checking out the code
            }
        }

        stage('Checkout Code from GitHub') {
            steps {
                checkout([$class: 'GitSCM',
                          branches: [[name: '*/main']], // Using 'main' branch
                          userRemoteConfigs: [
                              [url: 'https://github.com/HarryRichard08/jenkins_test.git',
                               credentialsId: 'test']
                          ]
                ])
            }
        }

        stage('SonarQube Analysis') {
            environment {
                SCANNER_HOME = tool 'sonar-scanner'
            }
            steps {
                withSonarQubeEnv('sonar-server') {
                    sh "${SCANNER_HOME}/bin/sonar-scanner -Dsonar.projectName=test -Dsonar.projectKey=test"
                }
            }
        }

        stage('Compare CSV Files') {
            steps {
                script {
                    def predictedFile = readFileFromGit('output/predicted.csv')
                    def actualFile = readFileFromGit('output/actual.csv')

                    if (predictedFile == actualFile) {
                        echo 'CSV files are identical. Proceeding with file copy.'
                    } else {
                        error 'CSV files are different. Skipping file copy.'
                    }
                }
            }
        }

        stage('Comparing Requirements.txt') {
            steps {
                script {
                    def airFlowRequirements = readFileFromGit('requirements/air_flow_requirements.txt')
                    def requirements = readFileFromGit('requirements/requirements.txt')

                    if (airFlowRequirements == requirements) {
                        echo 'Requirements files are identical. Proceeding with the pipeline.'
                    } else {
                        error 'Requirements files are different. Failing the pipeline.'
                    }
                }
            }
        }

        stage('Read VM Details') {
            steps {
                script {
                    // Read the JSON file and conditionally overwrite the vmDetails
                    def localVmDetails = readJSON file: 'vm_details/vm_details.json'
                    echo "Initial VM Details: ${localVmDetails}" // Debugging line

                    if (localVmDetails.environment == 'staging') {
                        echo "Overwriting VM Details for Staging Environment" // Debugging line
                        localVmDetails = [
                            host: "209.145.55.222",
                            username: "root",
                            password: "oyMvIJ7Y317SWQg8",
                            instance_name: "Pandora",
                            instance_type: "ubuntu"
                        ]
                    }
                    echo "Final VM Details: ${localVmDetails}" // Debugging line
                    // Convert the Groovy map to a JSON string and assign it to the environment variable
                    env.vmDetails = groovy.json.JsonOutput.toJson(localVmDetails)
                    stash includes: 'Scrapy-template/**', name: 'scrapyTemplateStash'
                }
            }
        }

        stage('Copy File to Remote Server') {
            steps {
                unstash name: 'scrapyTemplateStash'
                script {
                    // Convert the JSON string back to a Groovy map
                    def details = groovy.json.JsonSlurper().parseText(env.vmDetails)
                    def remoteHost = details.host
                    def remoteUsername = details.username
                    def remotePassword = details.password
                    def sshpassPath = '/usr/bin/sshpass'

                    def newFolderName = sh(script: "cat config_file | grep 'folder_name' | cut -d'=' -f2", returnStdout: true).trim()

                    sh "${sshpassPath} -p '${remotePassword}' ssh -o StrictHostKeyChecking=no ${remoteUsername}@${remoteHost} 'mkdir -p /root/projects/${newFolderName}'"
                    sh "${sshpassPath} -p '${remotePassword}' scp -o StrictHostKeyChecking=no -r *_dag.py ${remoteUsername}@${remoteHost}:/root/airflow/dags/"
                    sh "${sshpassPath} -p '${remotePassword}' scp -o StrictHostKeyChecking=no -r Scrapy-template/ ${remoteUsername}@${remoteHost}:/root/projects/${newFolderName}/"
                }
            }
        }
    }

    post {
        always {
            script {
                try {
                    // Read the email address from the 'email.txt' file in the Git repository
                    def recipientEmail = readFileFromGit('email.txt').trim()
                    echo "Preparing to send email to: ${recipientEmail}" // For debugging

                    // Send the email
                    mail(
                        to: recipientEmail,
                        subject: "Build Notification for Branch '${env.BRANCH_NAME}'",
                        body: """Hello,

This email is to notify you that a build has been performed on the branch '${env.BRANCH_NAME}' in the ${env.JOB_NAME} job.

Build Details:
- Build Number: ${env.BUILD_NUMBER}
- Build Status: ${currentBuild.currentResult}
- Commit ID: ${env.GIT_COMMIT}

Please review the build and attached changes.

Best regards,
The Jenkins Team
"""
                    )
                    echo "Email should have been sent to: ${recipientEmail}"
                } catch (Exception e) {
                    echo "Failed to send email. Printing stack trace for debugging:"
                    e.printStackTrace()
                } finally {
                    // Clean the workspace after every build
                    cleanWs()
                }
            }
        }
    }
}

def readFileFromGit(String filePath) {
    return sh(script: "git show origin/main:${filePath}", returnStdout: true).trim()
}
