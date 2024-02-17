import os
import sys
import time
import httpx

# fix to make possible edge_http module import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import edge_http

n_migration = 10

limits = httpx.Limits(max_keepalive_connections=None, max_connections=None, keepalive_expiry=None)
s = edge_http.Client("https://compute.lorenzogiorgi.com/orchestrator/login", "lorenzo", "lorenzo", True, verify=True,
                     http2=True, timeout=None, limits=limits)

for j in range(n_migration):
    for i in range(10):
        t_start = time.time_ns()
        request_n = 0
        print()
        print()
        print("Request #", request_n)

        edge_id = s.get_current_edge()
        t0 = time.time_ns()
        r = s.get("/echo/echo")
        t1 = time.time_ns()

        print(r.http_version)
        print("SC:", r.status_code)
        print("Time used (ms)", (t1 - t0) / 1000000)

        request_n = request_n + 1

        t_end = time.time_ns()
        time.sleep(0.5 - (t_end - t_start) / 1000000000)

    # trigger migration
    s.migrate_on_different_edge("https://orchestrator.lorenzogiorgi.com/migrate")

s.logout("/orchestrator/logout")
s.close()
