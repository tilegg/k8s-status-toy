# ☸ kube-status-toy
A toy service to explore kubernetes pod status probes by manipulating liveness- and readyness-probes.

https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes


## Build :hammer:
```bash
podman build . -t kube-status-toy:v0.0.1-alpha
```

## Usage :rocket:

Start the service (locally, using podman)
```bash
# Start the service
podman run --rm -d -p 6543:6543 --name kube-status-toy kube-status-toy:v0.0.1-alpha
```

The default endpoints responds with a message and the hostname (name of the pod in k8s)
```bash
http http://127.0.0.1:6543/
# > HTTP/1.0 200 OK
# > Content-Length: 23
# > Content-Type: text/html; charset=UTF-8
# > Date: Wed, 08 Feb 2023 16:15:57 GMT
# > Server: WSGIServer/0.2 CPython/3.11.1
# >
# > Hello from 98ed9f063189
# >
```


### Check liveness probe 
The liveness-probe of the container is invoked by querying the /healthz endpoint

```bash
# Example using httpie
http http://127.0.0.1:6543/healthz

# The response will look something like this:
# > HTTP/1.0 200 OK
# > Content-Length: 16
# > Content-Type: text/html; charset=UTF-8
# > Date: Wed, 08 Feb 2023 15:59:51 GMT
# > Server: WSGIServer/0.2 CPython/3.11.1
# >
# > Service is alive
# >
```

### Change liveness probe
POST'ing true/false to the /healthz endpoint changes the liveness of the container

```bash
echo "false" | http http://127.0.0.1:6543/healthz

# > HTTP/1.0 200 OK
# > Content-Length: 21
# > Content-Type: text/html; charset=UTF-8
# > Date: Wed, 08 Feb 2023 16:09:01 GMT
# > Server: WSGIServer/0.2 CPython/3.11.1
# >
# > Liveness set to False
# >

# Check the liveness probe again
http http://127.0.0.1:6543/healthz

# The status has changed
# > HTTP/1.0 500 Internal Server Error
# > Content-Length: 15
# > Content-Type: text/html; charset=UTF-8
# > Date: Wed, 08 Feb 2023 16:10:21 GMT
# > Server: WSGIServer/0.2 CPython/3.11.1
# >
# > Service is dead
# >
```

### readyness probe
The readyness probe behaves just like the liveness-probe but uses the /healthy endpoint

```bash
http http://127.0.0.1:6543/healthy
# > HTTP/1.0 200 OK
# > Content-Length: 33
# > Content-Type: text/html; charset=UTF-8
# > Date: Wed, 08 Feb 2023 16:12:10 GMT
# > Server: WSGIServer/0.2 CPython/3.11.1
# >
# > Service is ready to serve traffic
# >


echo "false" | http http://127.0.0.1:6543/healthy
# > HTTP/1.0 200 OK
# > Content-Length: 22
# > Content-Type: text/html; charset=UTF-8
# > Date: Wed, 08 Feb 2023 16:12:18 GMT
# > Server: WSGIServer/0.2 CPython/3.11.1
# >
# > Readyness set to False
# >

http http://127.0.0.1:6543/healthy
# > HTTP/1.0 500 Internal Server Error
# > Content-Length: 37
# > Content-Type: text/html; charset=UTF-8
# > Date: Wed, 08 Feb 2023 16:12:20 GMT
# > Server: WSGIServer/0.2 CPython/3.11.1
# >
# > Service is NOT ready to serve traffic
# >


echo "true" | http http://127.0.0.1:6543/healthy
# > HTTP/1.0 200 OK
# > Content-Length: 22
# > Content-Type: text/html; charset=UTF-8
# > Date: Wed, 08 Feb 2023 16:12:27 GMT
# > Server: WSGIServer/0.2 CPython/3.11.1
# >
# > Readyness set to False
# >


http http://127.0.0.1:6543/healthy

# > HTTP/1.0 200 OK
# > Content-Length: 33
# > Content-Type: text/html; charset=UTF-8
# > Date: Wed, 08 Feb 2023 16:12:29 GMT
# > Server: WSGIServer/0.2 CPython/3.11.1
# >
# > Service is ready to serve traffic
# >
```
