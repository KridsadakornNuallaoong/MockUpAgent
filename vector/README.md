# example code apply/delete qdrant on kubernetes

```bash
kubectl apply -f <file_name>.yaml
kubectl delete -f <file_name>.yaml
```

# example code to manual forwarding on kubernetes

```bash
kubectl port-forward svc/<service_name> <local_port>:<pod_port>
```

# example with specific ports

```bash
kubectl port-forward svc/<service_name> 6333:6333
```