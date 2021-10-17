# simple_python_helm

Purpose for the code inside this repo is:

### Create Simple project in Python which creates a service that queries 2 URLs (https://httpstat.us/503 & https://httpstat.us/200)
- The service will check the external URLs
(https://httpstat.us/503 & https://httpstat.us/200 ) are up (based on http status code 200) and response time in milliseconds
### The service will run a simple http server that produces metrics and outputs a Prometheus format when hitting the service URL
#### Expected response format:
- sample_external_url_up{url="https://httpstat.us/503 "} = 0
- sample_external_url_response_ms{url="https://httpstat.us/503 "} = [value]
- sample_external_url_up{url="https://httpstat.us/200 "} = 1
- sample_external_url_response_ms{url="https://httpstat.us/200 "} = [value]

### Python app code is located in the ./python_app/ folder 
#### On every 10 seconds both url /200 and /503 are queried for the response code and the mention metrics are exposed
For metrics `sample_external_url_response_ms` two other metrics are exposed:

- `sample_external_url_response_ms_count`: Number of times this function was called.
- `sample_external_url_response_ms_sum`: Total amount of time spent in this function.
Prometheus's `rate` function allows calculation of both requests per second/milisecond, and latency over time from this data

- You can run it either locally \
`python3 ./python_app/simple_scrape.py`\
On `http://localhost:8081` you will be able to access the metrics exposed by the prometheus-client
- or create docker container and run the code inside it \
`cd python_app`\
`docker build . -t simple-python-app` \
You can run the created image and port forward some local port to the container in order to access the http server with the metrics: \
`docker run -it -p 81:8081 simple-python-app` \
On `localhost:81` you will be able to view the metrics \

#### Image was also pushed to docker hub: `dsarafski/simple-python-scrape:0.0.3`and used to deploy the app with helm inside kubernetes

### How to deploy the app inside the kubernetes cluster with helm
Helm chart was created inside `./helm-simple-python/` folder \
In order to run the app inside kubernetes use: \
- Change your context with the k8s cluster you want to deploy the app \
- Execute:
`helm install <some-name-for-the-chart> ./helm-simple-python/` \
- Since the app is using NodePor you can access it by either port-forward you local port to the pods inside the cluster: \
`kubectl port-forward <pod-name-you-can-get-it-with kubectl get pods> 8081:8081` \
On your local machine on `localhost:8081` you will be able to see the metrics
- Or you can get the IP of some k8s node and the app will be available on port `32765`\
Example: `curl <k8s-node-ip-can get it with kubectl get nodes -o wide>:32765`


