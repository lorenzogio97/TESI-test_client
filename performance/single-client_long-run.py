import os
import sys
import time
import pandas as pd
import httpx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import edge_http

"""
Description:
Long run test for single client connected to service
Migration every 10 minutes
0-8 min standard latency
8-9:30 increased latency
9:30-10 terrible latency

Total experiment duration: 90 minutes
"""


def make_request(quantity: int, interval: float):
    global request_no, request_time_series
    for _ in range(quantity):
        print()
        print()
        print("Request #", request_no)

        t0 = time.time_ns()
        r = s.get("/echo/echo")
        t1 = time.time_ns()

        print(r.http_version)

        print("SC:", r.status_code)

        print("Time used (ms)", (t1 - t0) / 1000000)
        print(r.elapsed.total_seconds())
        request_no = request_no + 1
        request_time_series.append((t1 - t0) / 1000000)
        time.sleep(interval)


# request number counter
request_no = 0
# service time
request_time_series = []

# client setup
limits = httpx.Limits(max_keepalive_connections=None, max_connections=None, keepalive_expiry=None)
s = edge_http.Client("https://compute.lorenzogiorgi.com/orchestrator/login", "lorenzo", "lorenzo", verify=True,
                     http2=True, timeout=None, limits=limits)

# be sure that no artificial latency has been added
os.system("sudo tc qdisc delete dev ens3 root")

# time start experiment
start_time = time.time_ns()

for i in range(9):
    make_request(60 * 1, 1)
    os.system("sudo tc qdisc add dev ens3 root netem delay 20ms")
    make_request(90, 1)
    os.system("sudo tc qdisc change dev ens3 root netem delay 50ms")
    make_request(30, 1)
    os.system("sudo tc qdisc delete dev ens3 root")

    # trigger migration
    s.migrate_on_different_edge("https://orchestrator.lorenzogiorgi.com/migrate/")

# collecting and saving result
series = pd.Series(request_time_series)
series.to_csv("single_client-long_run.csv")
