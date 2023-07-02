import os
import sys
import time
import httpx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import edge_http



limits = httpx.Limits(max_keepalive_connections=None, max_connections=None, keepalive_expiry=None)
s = edge_http.Client("https://compute.lorenzogiorgi.com/orchestrator/login", "lorenzo", "lorenzo", True, verify=True,
                     http2=True, timeout=None, limits=limits)

for i in range(1, 10):
    print()
    print()
    print("Request #" + str(i))
    t0 = time.time_ns()

    r = s.get("/echo/echo")
    print(r.http_version)

    print("SC:", r.status_code)

    t1 = time.time_ns()
    print("Time used (ms)", (t1 - t0) / 1000000)
    time.sleep(1)


s.logout("/orchestrator/logout")
s.close()
