import static groovy.json.JsonOutput.*

    pipeline {

        agent any

        parameters {
            booleanParam(defaultValue: false, description: 'Deploy to E2E?', name: 'DeployPages')
        }

        stages {
            stage('Intuit PaaS Properties') {
                steps {
                    sh "ls -la"
                    script {
                        currentBuild.displayName = "CD Pipeline"
                        currentBuild.description = "CD Pipeline"

                        // trim removes leading and trailing whitespace from the string
                        intuitPaas = readYaml file: 'intuit-paas.yml'
                        intuitPaas.gitflow.to.helm["values"] = "values-dev.yaml"
                        intuitPaas.gitflow.to.helm["sets"] = "--set ${intuitPaas.gitflow.to.helm.image.key}=${intuitPaas.gitflow.to.helm.image.tag}"
                        intuitPaas.gitflow.to.helm["name"] = "paas-service-dev"
                        intuitPaas.gitflow.to.helm["values1"] = "values-qa.yaml"
                        intuitPaas.gitflow.to.helm["name1"] = "paas-service-qa"
                        intuitPaas.gitflow.to.helm["values2"] = "values-e2e.yaml"
                        intuitPaas.gitflow.to.helm["name2"] = "paas-service-e2e"
                    }

                    // Print the entire blob
                    echo prettyPrint(toJson(intuitPaas))
                    writeYaml file: 'intuit-paas-update.yml', data: intuitPaas

                    //Helm Installation
                    sh "wget https://storage.googleapis.com/kubernetes-helm/helm-v2.7.2-linux-amd64.tar.gz"
                    sh "tar -zxvf  helm-v2.7.2-linux-amd64.tar.gz"
                    sh "mv linux-amd64/helm /usr/local/bin/helm"
                    sh "helm init --upgrade"
                    sh "helm list"

                }
            }
            stage('Deployment') {
                parallel {
                    stage('Deploy to Dev') {
                        when {
                            expression {
                                fileExists('intuit-paas-update.yml')
                            }
                        }
                        steps {
                            script {
                                sh "kubectl config set-context paas-preprod.a.intuit.com"
                                intuitPaas = readYaml file: 'intuit-paas-update.yml'
                                sh "helm package ./helm-charts"
                                sh "helm install --debug --name ${intuitPaas.gitflow.to.helm.name} -f ${intuitPaas.gitflow.to.helm.values} helm-charts-1.0.0.tgz"
                                sh 'python ./tep.py'
                            }
                        }
                    }
                    stage('Deploy to QA') {
                        when {
                            expression {
                                fileExists('intuit-paas-update.yml')
                            }
                        }
                        steps {
                            script {
                                sh "kubectl config set-context paas-preprod.a.intuit.com"
                                intuitPaas = readYaml file: 'intuit-paas-update.yml'
                                sh "helm install --debug --name ${intuitPaas.gitflow.to.helm.name1} -f ${intuitPaas.gitflow.to.helm.values1} helm-charts-1.0.0.tgz"
                                sh 'python ./tep.py'
                            }
                        }
                    }
                }
            }
            stage("Deploy to E2E") {
                when {
                    expression {
                        fileExists('intuit-paas-update.yml')
                        boolean publish = false
                        if (env.DEPLOYPAGES == "true") {
                            return true
                        }
                        try {
                            timeout(time: 1, unit: 'MINUTES') {
                                input 'Promote?'
                                publish = true
                            }
                        } catch (final ignore) {
                            publish = false
                        }
                        return publish
                    }
                }
                steps {
                    script {
                        intuitPaas = readYaml file: 'intuit-paas-update.yml'
                        sh "kubectl config set-context paas.a.intuit.com"
                        sh "helm package ./helm-charts"
                        sh "helm install --debug --name ${intuitPaas.gitflow.to.helm.name2} -f ${intuitPaas.gitflow.to.helm.values2} helm-charts-1.0.0.tgz"
                        sh 'python ./tep.py'
                    }
                }
            }
        }
    }