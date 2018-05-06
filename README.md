# config-service-deploy

The deployment repository for the Configuration Service

# Deployment Types

* Kubernetes Objects: Low-level objects for clusters
* Kubernetes Helm: Wrapper around the Low-level objects
* Kubernetes Ksonnet: Alternative to Helm

# Kubernetes Objects

* Can be used to build Helm Deployments

## Deployment

Using kubectl, you can deploy the objects directly:

```
kubectl create -f k8s-objects/config-server.yml
```

# Kuberentes Helm

* The standard way to deploy to kubernetes

## Environments

* DEV

```
helm install --dry-run --debug . -f values/values.yaml,values/dev.yaml
```

* QAL

```
helm install --dry-run --debug . -f values/values.yaml,values/qal.yaml
```

* E2E

```
helm install --dry-run --debug . -f values/values.yaml,values/e2e.yaml
```

* PRD

```
helm install --dry-run --debug . -f values/values.yaml,values/prd.yaml
```

Docker images are defined in 2 levels: Team / Service

* Team: All users, in DevPortal, have read/write permissions.
* Service: Only CI has access to read/write to that.

# Ksonnet

* To be consired in the future
