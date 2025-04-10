# GoodNotes exercise

Repository for deploying and simulating a load test http://foo.local and http://bar.local endpoints using GitHub actions.

Layout:
  * *cluster-setup* - contains all files required to spin up a cluster with ingress and two http-echo services configured
  * *load-test* - contains a [locust](https:/locust.io) load test script and a script to publish back PR comment

Setup uses custom GitHub actions, stored in `.github/actions` directory:
    * *dns-loopback-setup* - configures `/etc/hosts` with specified DNS entries
    * *helm-install* - installs helm chart against the cluster
    * *ingress-ready* - waits until specified endpoints are available
    * *locust-test* - executes locust script and publishes results back to the PR as a comment

## Work notes
=======


Plan:
  - Use helm/kind-action to install kind. Not that we can't write our own. It depends whether this test designed to check my scripting or a practical approach.
  - Use helm action to perform helm install on required apps. I could use kubectl apply, but helm will provide a cleaner interface to configure apps in whatever way we would like. 
  - Health checks. I could depend on helm tests and add container which runs against ingress. But for this exercise I'll test end-to-end from the VM
  - DNS. I could install dnsmasq on host to setup ingress DNS, but for this exercise this is overkill. I'll just create a custom action that adds entries to /etc/hosts.
  - As I'm using helm, will helm create chart for http-echo service. Use it for both foo and bar. Maybe there is one already, but I don't need much out of it.
  - I will install 1 pod for foo and 2 for bar. For tests.
  - For perftest I will use locust, just because it's more interesting. We could plugin in test_reporter and locust-csv-to-junite-xml to make test appear nicer. If we have time.

## Output

Below is a comment that is posted on the PR:

```
Test results for http://bar.local
[2025-04-01 18:26:16,805] fv-az1675-365/INFO/locust.main: Starting Locust 2.33.2
[2025-04-01 18:26:16,805] fv-az1675-365/INFO/locust.runners: Shape test starting.
[2025-04-01 18:26:16,806] fv-az1675-365/INFO/locust.runners: Shape worker starting
[2025-04-01 18:26:16,806] fv-az1675-365/INFO/locust.runners: Shape test updating to 10 users at 10.00 spawn rate
[2025-04-01 18:26:16,806] fv-az1675-365/INFO/locust.runners: Ramping to 10 users at a rate of 10.00 per second
[2025-04-01 18:26:16,807] fv-az1675-365/INFO/locust.runners: All users spawned: {"EndpointTest": 10} (10 total users)
[2025-04-01 18:26:26,812] fv-az1675-365/INFO/locust.runners: Shape test updating to 50 users at 50.00 spawn rate
[2025-04-01 18:26:26,812] fv-az1675-365/INFO/locust.runners: Ramping to 50 users at a rate of 50.00 per second
[2025-04-01 18:26:26,815] fv-az1675-365/INFO/locust.runners: All users spawned: {"EndpointTest": 50} (50 total users)
[2025-04-01 18:26:36,817] fv-az1675-365/INFO/locust.runners: Shape test updating to 100 users at 100.00 spawn rate
[2025-04-01 18:26:36,819] fv-az1675-365/INFO/locust.runners: Ramping to 100 users at a rate of 100.00 per second
[2025-04-01 18:26:36,824] fv-az1675-365/INFO/locust.runners: All users spawned: {"EndpointTest": 100} (100 total users)
[2025-04-01 18:26:46,916] fv-az1675-365/INFO/locust.runners: Shape test updating to 200 users at 200.00 spawn rate
[2025-04-01 18:26:46,916] fv-az1675-365/WARNING/locust.runners: Your selected spawn rate is very high (>100), and this is known to sometimes cause issues. Do you really need to ramp up that fast?
[2025-04-01 18:26:46,916] fv-az1675-365/INFO/locust.runners: Ramping to 200 users at a rate of 200.00 per second
[2025-04-01 18:26:46,925] fv-az1675-365/INFO/locust.runners: All users spawned: {"EndpointTest": 200} (200 total users)
[2025-04-01 18:26:57,003] fv-az1675-365/INFO/locust.runners: Shape test stopping
[2025-04-01 18:26:57,094] fv-az1675-365/INFO/locust.main: --run-time limit reached, shutting down
[2025-04-01 18:26:57,095] fv-az1675-365/INFO/locust.main: Shutting down (exit code 0)
Type Name # reqs # fails | Avg Min Max Med | req/s failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
POST / 31293 0(0.00%) | 99 2 1152 70 | 777.04 0.00
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
Aggregated 31293 0(0.00%) | 99 2 1152 70 | 777.04 0.00

Response time percentiles (approximated)
Type Name 50% 66% 75% 80% 90% 95% 98% 99% 99.9% 99.99% 100% # reqs
--------|--------------------------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
POST / 70 92 120 160 230 320 410 490 780 1100 1200 31293
--------|--------------------------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
Aggregated 70 92 120 160 230 320 410 490 780 1100 1200 31293
```
