# GoodNotes exercise


## Work notes


Assumptions:
  - Exercise asks for 2 worker nodes. Does that mean 1 node dedicated for nginx-controller and 2 for workloads, or 2 for workloads? My assumption the ask is to verify how I would setup load balancing. I'll go with 3 worker setup.
  - What is randomised traffic for 2 hosts?
    * random traffic to one or the other?
    * random traffic to both hosts run sequentially/in parallel?
    * traffic to the same urls on both? Parallel, sequential?


Plan:
  - Use helm/kind-action to install kind. Not that we can't write our own. It depends whether this test designed to check my scripting or workings.
  - Use helm action to perform helm install on required apps. I could use kubectl apply, but helm will provide a cleaner interface to configure apps in whatever way we would like. 
  - Health checks. I could depend on helm tests and add container runs against ingress. But for this exercise I'll test end-to-end from the VM
  - DNS. I could install dnsmasq on host to setup ingress DNS, but for this exercise this is overkill. I'll just create a custom action that adds entries to /etc/hosts.
  - As I'm using helm, will helm create chart for http-echo service. Use it for both foo and bar. Maybe there is one already, but I don't need much out of it.
  - For perftest I will use locust, just because it's more interesting. We could plugin in test_reporter and locust-csv-to-junite-xml to make test appear nicer. If we have time.

