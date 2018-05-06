import static groovy.json.JsonOutput.*

pipeline {

  agent any

  stages {
        stage('Intuit PaaS Properties') {
        steps {
          sh "ls -la"

          script {
            currentBuild.displayName = "Intuit PaaS Properties"
            currentBuild.description = "Setting up PaaS Variables"

            // trim removes leading and trailing whitespace from the string
            intuitPaas = readYaml file: 'intuit-paas.yml'
            intuitPaas.gitflow.to.helm["values"] = "values.yaml"
            intuitPaas.gitflow.to.helm["dev"] = "values-${intuitPaas.gitflow.to.helm.profiles}.yaml"
			      intuitPaas.gitflow.to.helm["sets"] = "--set ${intuitPaas.gitflow.to.helm.image.key}=${intuitPaas.gitflow.to.helm.image.tag}"
            intuitPaas.gitflow.to.helm["name"] = "paas-service-qa"
			      intuitPaas.gitflow.to.helm["dev1"] = "paas-service-dev"
          }

          // Print the entire blob
          echo prettyPrint(toJson(intuitPaas))
          writeYaml file: 'intuit-paas-update.yml', data: intuitPaas
		  
        }
      }
    
	 stage ('Helm Install') {
		steps {
		  script {
	        sh "wget https://storage.googleapis.com/kubernetes-helm/helm-v2.7.2-linux-amd64.tar.gz"
          sh "tar -zxvf  helm-v2.7.2-linux-amd64.tar.gz"
			    sh "mv linux-amd64/helm /usr/local/bin/helm"
			    sh "helm init --upgrade"
        }
      }
	  } 
      stage('Deploy to Dev') {
		  when {
			expression { fileExists('intuit-paas-update.yml') }
		  }
     steps {
			script {
        sh "ls -lsa"  
			  intuitPaas = readYaml file: 'intuit-paas-update.yml'
			}
			  
      sh "helm install --debug --name ${intuitPaas.gitflow.to.helm.dev1} -f ${intuitPaas.gitflow.to.helm.dev} ${intuitPaas.gitflow.to.helm.sets} ."
	  
		 }
	 }	
 	}
}
 