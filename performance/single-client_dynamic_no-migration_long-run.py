import os
import sys
import threading
import time
import random

import pandas as pd
import httpx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import edge_http

"""
Description:
Long run test for single client connected to service
4 minutes on each access point
20 migration

Total experiment duration: 80 minutes
"""

edge_ip_mapping = {
    "edge1": "172.16.4.0",
    "edge2": "172.16.4.66",
    "edge3": "172.16.3.49"
}


def make_request(quantity: int, interval: float):
    global request_no, request_time_series
    for _ in range(quantity):
        print()
        print()
        print("Request #", request_no)

        edge_id = s.get_current_edge()
        t0 = time.time_ns()
        r = s.get("/echo/echo")
        t1 = time.time_ns()

        print(r.http_version)
        print("SC:", r.status_code)

        print("Time used (ms)", (t1 - t0) / 1000000)
        request_no = request_no + 1
        request_edge_series.append(edge_id)
        request_response_code_series.append(r.status_code)
        request_time_series.append((t1 - t0) / 1000000)
        time.sleep(interval)


def change_access_point():
    global first_edge
    # migration request
    edge_node_list = ["edge1", "edge2", "edge3"]
    random.shuffle(edge_node_list)
    if edge_node_list[0] != first_edge:
        os.system("sudo tc filter del dev ens3 parent 1: protocol ip prio 1")
        ip = edge_ip_mapping.get(first_edge)
        os.system("sudo tc filter add dev ens3 parent 1: protocol ip prio 1 u32 match ip dst " + str(ip) + "/32 flowid 1:1")
    else:
        os.system("sudo tc filter del dev ens3 parent 1: protocol ip prio 1")


# request number counter
request_no = 0
# service time
request_time_series = []
request_edge_series = []
request_response_code_series = []
# first edge information
first_edge = "cloud"

# client setup
limits = httpx.Limits(max_keepalive_connections=None, max_connections=None, keepalive_expiry=60)
s = edge_http.Client("https://compute.lorenzogiorgi.com/orchestrator/login", "lorenzo", "lorenzo", True,  verify=True,
                     http2=True, timeout=None, limits=limits)

# be sure that no artificial latency has been added
os.system("sudo tc qdisc delete dev ens3 root")
# qdisc prio creation
os.system("sudo tc qdisc add dev ens3 root handle 1: prio priomap 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2")
# class 1 will be delayed
os.system("sudo tc qdisc add dev ens3 parent 1:1 handle 10: netem delay 25ms")

# time start experiment
start_time = time.time_ns()

for i in range(20):
    make_request(60 * 8, 0.5)

    if i == 0:
        first_edge = s.get_current_edge()

    x = threading.Thread(target=change_access_point)
    x.start()

# collecting and saving result
data = {
    "request_time": request_time_series,
    "edge": request_edge_series,
    "response_code": request_response_code_series
}

# load data into a DataFrame object:
df = pd.DataFrame(data)

df.to_csv("./result/dynamic-no_migration-long_run.csv")
