node {
    def SCANNER_HOME = tool 'sonar-scanner'

    stage('Checkout Code from GitHub') {
        checkout([$class: 'GitSCM', branches: [[name: '*/main']], userRemoteConfigs: [[url: 'https://github.com/HarryRichard08/Scrappy-template.git']]])
    }

    stage('SonarQube Analysis') {
        withSonarQubeEnv('sonar-server') {
            sh """${SCANNER_HOME}/bin/sonar-scanner -Dsonar.projectName=test \
            -Dsonar.projectKey=test"""
        }
    }

    stage('Compare CSV Files') {
        def predictedFile = readFileFromGit('output/predicted.csv')
        def actualFile = readFileFromGit('output/actual.csv')

        if (predictedFile == actualFile) {
            echo 'CSV files are identical. Proceeding with file copy.'
        } else {
            error 'CSV files are different. Skipping file copy.'
        }
    }

    stage('Comparing Requirements.txt') {
        def airFlowRequirements = readFileFromGit('requirements/air_flow_requirements.txt')
        def requirements = readFileFromGit('requirements/requirements.txt')

        if (airFlowRequirements == requirements) {
            echo 'Requirements files are identical. Proceeding with the pipeline.'
        } else {
            error 'Requirements files are different. Failing the pipeline.'
        }
    }

    stage('Read VM Details') {
        def vmDetails = readJSON file: 'vm_details/vm_details.json'

        if (vmDetails.environment == 'staging') {
            vmDetails = [
                host: "209.145.55.222",
                username: "root",
                password: "oyMvIJ7Y317SWQg8",
                instance_name: "Pandora",
                instance_type: "ubuntu"
            ]
        }

        currentBuild.description = "Moving 'Scrapy-template' to ${vmDetails.host}"
        stash includes: 'Scrapy-template/**', name: 'scrapyTemplateStash'
    }

    stage('Copy File to Remote Server') {
        unstash 'scrapyTemplateStash'

        def vmDetails = readJSON file: 'vm_details/vm_details.json'
        def remoteHost = vmDetails.host
        def remoteUsername = vmDetails.username
        def remotePassword = vmDetails.password
        def sshpassPath = '/usr/bin/sshpass'

        sh "${sshpassPath} -p '${remotePassword}' scp -r -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null Scrapy-template/ ${remoteUsername}@${remoteHost}:/root/airflow/dags/"
    }
}

def readFileFromGit(filePath) {
    return sh(script: "git show origin/main:${filePath}", returnStdout: true).trim()
}
