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
5 or 20 minutes on each access point
16-4 migrations

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
        t_start = time.time_ns()
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

        t_end = time.time_ns()
        time.sleep(interval - (t_end - t_start) / 1000000000)


def change_access_point():
    # remove the delay on the old edge node (not current one)
    os.system("sudo tc filter del dev ens3 parent 1: protocol ip prio 1")

    # get current edge node
    current_edge = s.get_current_edge()
    current_ip = edge_ip_mapping.get(current_edge)

    os.system("sudo tc filter add dev ens3 parent 1: protocol ip prio 1 u32 match ip dst " + str(
        current_ip) + "/32 flowid 1:2")

    # migration request
    edge_node_list = ["edge1", "edge2", "edge3"]
    node_to_migrate = [x for x in edge_node_list if x != current_edge]
    random.shuffle(node_to_migrate)

    migration_data = {"edgeNodeList": node_to_migrate, "username": s.get_username()}
    t = httpx.Client(http2=True)
    r = t.post("https://orchestrator.lorenzogiorgi.com/migrate", json=migration_data)


# parsing parameters
if len(sys.argv) != 4:
    print("you have to run: python3 script.py <handover_time_interval in min> <old_rtt_time> <run_index>")
    exit(1)


handover_time_interval = int(sys.argv[1])  # in minute
rtt_old_node = int(sys.argv[2])  # in ms
run_index = int(sys.argv[3])

optimal_rtt = 26

print("Parsed arguments:")
print("Handover time(in minute): ", handover_time_interval)
print("RTT on old node (in ms): ", rtt_old_node)
print("Run Index: ", run_index)

print("Experiment will start in 20 seconds")
time.sleep(20)

# request number counter
request_no = 0
# data lists for performance evaluation
request_time_series = []
request_edge_series = []
request_response_code_series = []

# client setup
limits = httpx.Limits(max_keepalive_connections=None, max_connections=None, keepalive_expiry=60)
s = edge_http.Client("https://compute.lorenzogiorgi.com/orchestrator/login", "lorenzo", "lorenzo", True, verify=True,
                     http2=True, timeout=None, limits=limits)

# be sure that no artificial latency has been added
os.system("sudo tc qdisc delete dev ens3 root")
# qdisc prio creation
os.system("sudo tc qdisc add dev ens3 root handle 1: prio priomap 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2")
# class 1 represent connection to optimal edge (7ms RTT)
os.system("sudo tc qdisc add dev ens3 parent 1:1 handle 10: netem delay "+str(optimal_rtt)+"ms 1ms")
# class 2 represent connection to the previous edge (122ms RTT)
os.system("sudo tc qdisc add dev ens3 parent 1:2 handle 20: netem delay "+str(rtt_old_node)+"ms 1ms")

# at the beginning, since it is not possible to know which edge will be selected, we apply the standard delay to all
for item in edge_ip_mapping.values():
    os.system("sudo tc filter add dev ens3 parent 1: protocol ip prio 2 u32 match ip dst " + str(
        item) + "/32 flowid 1:1")


# time start experiment
start_time = time.time_ns()

for i in range(int(80 / handover_time_interval)):
    make_request(60 * 2 * handover_time_interval, 0.5)
    x = threading.Thread(target=change_access_point)
    x.start()

s.logout("/orchestrator/logout")

# collecting and saving result
data = {
    "request_time": request_time_series,
    "edge": request_edge_series,
    "response_code": request_response_code_series
}

# load data into a DataFrame object:
df = pd.DataFrame(data)

df.to_csv(
    "./result/dynamic-alt_svc-" + str(handover_time_interval) + "-" + str(rtt_old_node) + "-" + str(run_index) + ".csv")
