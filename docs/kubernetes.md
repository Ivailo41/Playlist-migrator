# Purpose and Scope
This document presents a practical walkthrough of deploying the server application to Kubernetes.

>Kubernetes is an open-source container orchestration platform designed to automate the deployment, scaling, and management of containerized applications.

# Minikube setup
The example will be shown with the Kubernetes distro - `Minikube`

>Minikube is a local Kubernetes implementation that allows developers to run a single-node Kubernetes cluster on their local machine.

Before installing Minikube, the following components must be available on the system:

1. **Container or virtualization driver**
   - Docker
   - Alternatively: VirtualBox, Hyper-V, KVM
2. **kubectl**
   - Kubernetes command-line tool used to interact with the cluster

Then you can visit the following [link](https://minikube.sigs.k8s.io/docs/start/?arch=%2Fwindows%2Fx86-64%2Fstable%2F.exe+download) to get the Minikube installer

Validate the Minikube instalation by running the command in your terminal:
```
minikube version
```

# Configure Driver
Minikube requires a driver to run the Kubernetes node. Here it is recommended to use Docker to avoid running separate virtual machine.

Verify Docker is running:
```
docker info
```
Start Minikube with Docker:
```
minikube start --driver=docker
```
After start verify cluster setup:
```
minikube status
```
Check nodes:
```
kubectl get nodes
```
If everything is set up correctly you should see a single node in `Ready` state.

# Configuration files
>Kubernetes uses YAML configuration files to define the desired state of cluster resources in a declarative manner. These files describe what the system should look like, and Kubernetes continuously works to ensure that the actual cluster state matches this definition.

You will find the YAML files in the following directory:
```
server/
└─ k8s/
   ├─ config.yml
   ├─ deployment.yml
   └─service.yml
```

### Deployment
>A Deployment is a Kubernetes object that manages the lifecycle of application Pods. It defines the desired state of an application, including how many instances should run and how updates should be performed.
### Service
>A Service is a Kubernetes object that provides a stable network endpoint for a set of Pods. Since Pods are ephemeral and can be created or destroyed at any time, Services abstract Pod networking and ensure reliable communication.
### ConfigMap
>A ConfigMap stores non-sensitive key-value configuration data that can be injected into Pods

# Secrets setup
For running the server in Kubernetes, your API keys will be needed (See how to set them up at [README.md](/README.md)).

To avoid uploading secret keys, you should imperatively create them by using the following command:
```
kubectl create secret generic server-secret \
    --from-literal=<Key>=<Value> \
    --from-literal=<Key>=<Value>
```
Where `<key>` is the name of the secret and `value` its value. (The names of the keys can be found at [README.md](/README.md))

# Deployment setup
After successfully running minikube, the next step is to apply the configuration files by running the command:
```
kubectl apply -f server/k8s
```
In the terminal you should see something like:
```
configmap/server-config created
deployment.apps/server-deployment created
service/server-service created
```
>Keep in mind that the status can also be `configured` and `unchanged`

You can check the running pods with the command
```
kubectl get pods
```

# Test server

## Port forward
After enusring that the pods are running you can test the server. The service is of type NodePort which opens a high-numbered port on our single Node in the cluster. Because the frontend will search for localhost on port 8080 we should port-forward with the following command:
```
kubectl port-forward service/server-service 8080:8080
```
This command forwards traffic from your `host on port 8080` to the `Pods on remote port 8080`

## Test from frontend
After port-forwarding you can test the server from the frontend, two options are available:
1. Use the deployment in Github Pages available [here](https://ivailo41.github.io/Playlist-migrator/)
2. Run the frontend yourself by following the instructions from [README.md](/README.md) and set the `FRONTEND_BASE_URL` environment variable to either empty string or `http://localhost:5173/` inside the [config.yml](/server/k8s/config.yml) file

>Keep in mind that networking errors might occur by using the frontend from Github Pages because the app is still in development, for smooth experience the second option is recommended

# Clean up
After testing you would want to clean up all created resources and stop Minikube. Depending on your goals it can be done by several ways:

## Only Node stop
This option will stop the running Node and preserve the Cluster state on disk. Upon start all Services, Deployments, ConfigMaps and Secrets will be present.
```
minikube stop
```
>Prefered if you will run the server in Kubernetes again.

## Delete Specific Objects
- Delete a Deployment:
```
kubectl delete deployment server-deployment
```
- Delete a Service:
```
kubectl delete service server-service
```
- Delete a ConfigMap:
```
kubectl delete configmap server-config
```
- Delete a Secret:
```
kubectl delete secret server-secret
```

At the end run the stop command:
```
minikube stop
```

## Delete Minikube cluster completely
If you want to remove the entire Minikube cluster:
```
minikube delete
```
Deletes all nodes, Pods, Services, ConfigMaps, Secrets, everything. Essentially starts you from scratch next time you run `minikube start`

# Configuration files overview
This section will cover the configuration yaml files and what each one does

### Deployment
```
apiVersion: apps/v1           #Specifies the Kubernetes API version for this resource.
kind: Deployment              #Defines the type of resource.
metadata:                     
  name: server-deployment       #Unique name for this Deployment in the namespace.
spec:
  replicas: 2                   #Number of Pod replicas to maintain.
  selector:
    matchLabels:
      app: server               #Defines how the Deployment finds which Pods it manages.
  template:
    metadata:
      labels:
        app: server             #Labels assigned to Pods created by this Deployment.
    spec:
      containers:
        - name: server                      #Name of the container inside the Pod.
          image: ivailo41/server:develop    #The Docker image the container will run.
          imagePullPolicy: Always           #Controls when Kubernetes pulls the Docker image
          
          ports:
            - containerPort: 8080           #The port that the container listens on.

          envFrom:                          #Loads environment variables and secrets
            ...

          resources:
            limits:                         #Maximum resources the container can use.
              ...
            requests:                       #Minimum resources guaranteed to the container.
              ...

          livenessProbe:                    #Checks every few seconds if the container responds
            httpGet:
              path: /health
              port: 8080
            ...

          readinessProbe:                   #Checks every few seconds if the container is ready to take traffic
            httpGet:
              path: /ready
              port: 8080
            ...
```
### Service
```
apiVersion: v1              
kind: Service               
metadata:
  name: server-service
spec:
  type: NodePort            #Defines how the Service is exposed.
  selector:
    app: server
  ports:
    - protocol: TCP         #The network protocol used
      port: 8080            #The port on the Service
      targetPort: 8080      #The port on the Pod container to send traffic to
      nodePort: 30036       #The external port on each Node that maps to the Service port.
```
### ConfigMap
```
apiVersion: v1
kind: ConfigMap
metadata:
  name: server-config
data:                       #Contains the key-value pairs for configuration.
  FRONTEND_BASE_URL: "..."  #The environment variable name your app will see inside the Pod
```