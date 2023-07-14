import os
import sys
import time
import httpx
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import edge_http

# request number counter
request_no = 0
# data lists for performance evaluation
request_time_series = []
request_edge_series = []
request_response_code_series = []

limits = httpx.Limits(max_keepalive_connections=None, max_connections=None, keepalive_expiry=None)
s = edge_http.Client("https://compute.lorenzogiorgi.com/orchestrator/login", "lorenzo", "lorenzo", True, verify=True,
                     http2=True, timeout=None, limits=limits)

for i in range( 10):
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
    time.sleep(0.5-(t_end - t_start) / 1000000000)

# trigger migration
s.migrate_on_different_edge("https://orchestrator.lorenzogiorgi.com/migrate")

for i in range(10):
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
    time.sleep(0.5-(t_end - t_start) / 1000000000)

s.logout("/orchestrator/logout")
s.close()

# collecting and saving result
data = {
    "request_time": request_time_series,
    "edge": request_edge_series,
    "response_code": request_response_code_series
}

# load data into a DataFrame object:
df = pd.DataFrame(data)

df.to_csv(
    "./result/validation-login_request_migrate_request_logout.csv")
