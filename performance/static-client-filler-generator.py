import os
import sys
import threading
import multiprocessing
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


def make_request(client, quantity: int, interval: float):
    # request number counter
    request_no = 0
    for _ in range(quantity):
        t_start = time.time_ns()

        #print("Request #", request_no)

        edge_id = client.get_current_edge()
        t0 = time.time_ns()
        r = client.get("/echo/echo")
        t1 = time.time_ns()

        #print(r.http_version)
        #print("SC:", r.status_code)
        #print("Time used (ms)", (t1 - t0) / 1000000)

        request_no = request_no + 1

        t_end = time.time_ns()
        time.sleep(interval - (t_end - t_start) / 1000000000)


def change_access_point():
    global first_edge, migration_number
    # migration request
    #edge_node_list = ["edge1", "edge2", "edge3"]
    #random.shuffle(edge_node_list)
    migration_number = migration_number + 1

    if migration_number % 2 != 0:
        #os.system("sudo tc filter del dev ens3 parent 1: protocol ip prio 1")
        ip = edge_ip_mapping.get(first_edge)
        os.system("sudo tc filter add dev ens3 parent 1: protocol ip prio 1 u32 match ip dst " + str(ip) + "/32 flowid 1:2")
    else:
        os.system("sudo tc filter del dev ens3 parent 1: protocol ip prio 1")



# parsing parameters
if len(sys.argv) != 2:
    print("you have to run: python3 script.py <client_number>")
    exit(1)

client_number = int(sys.argv[1])

print("Parsed arguments:")
print("Number of client: ", client_number)


#migration number (on odd number long delay)
migration_number = 0

# service time
request_time_series = []
request_edge_series = []
request_response_code_series = []
# first edge information
first_edge = "cloud"


# be sure that no artificial latency has been added
os.system("sudo tc qdisc delete dev ens3 root")
# qdisc prio creation
os.system("sudo tc qdisc add dev ens3 root handle 1: prio priomap 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2")
# class 1 represent connection to optimal edge (7ms RTT)
os.system("sudo tc qdisc add dev ens3 parent 1:1 handle 10: netem delay 7ms 1ms")
# class 2 represent connection to the previous edge (122ms RTT)
#os.system("sudo tc qdisc add dev ens3 parent 1:2 handle 20: netem delay "+str(rtt_old_node)+"ms 1ms")

# at the beginning, since it is not possible to know which edge will be selected, we apply the standard delay to all
for item in edge_ip_mapping.values():
    os.system("sudo tc filter add dev ens3 parent 1: protocol ip prio 2 u32 match ip dst " + str(
        item) + "/32 flowid 1:1")

# time start experiment
start_time = time.time_ns()

def client_requester(user:int):

    # client setup
    limits = httpx.Limits(max_keepalive_connections=None, max_connections=None, keepalive_expiry=60)
    s = edge_http.Client("https://compute.lorenzogiorgi.com/orchestrator/login", str(user), str(user), True,  verify=True,
                         http2=True, timeout=None, limits=limits)

    make_request(s, 60 * 2 *300, 0.5)
    s.logout("/orchestrator/logout")

    print(f"utente: {user} finito")



thread_list = []
for i in range(1, client_number):
    x = multiprocessing.Process(target=client_requester, args=(i,))
    thread_list.append(x)
    time.sleep(0.5*random.random())
    x.start()


for x in thread_list:
    x.join()


# collecting and saving result
#data = {
#    "request_time": request_time_series,
#    "edge": request_edge_series,
#    "response_code": request_response_code_series
#}

# load data into a DataFrame object:
#df = pd.DataFrame(data)

#df.to_csv(
    #"./result/static-no_migration-" + str(handover_time_interval) + "-" + str(rtt_old_node) + "-" + str(run_index) + ".csv")
