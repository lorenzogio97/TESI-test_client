import os
import sys
import time
import httpx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import edge_http

limits = httpx.Limits(max_keepalive_connections=None, max_connections=None, keepalive_expiry=None)

# counter to keep unsuccessful requests (status different to 200)
error = 0

for i in range(20):

    s = edge_http.Client("https://compute.lorenzogiorgi.com/orchestrator/login", "lorenzo", "lorenzo", verify=True,
                         http2=True, timeout=None, limits=limits)
    print("RUN: ", i)
    for i in range(10):
        print()
        print("Request #" + str(i))
        t0 = time.time_ns()

        r = s.get("/echo/echo")
        t1 = time.time_ns()

        print("SC:", r.status_code)
        if r.status_code != 200:
            error = error + 1
            time.sleep(1)

        print("Time used (ms)", (t1 - t0) / 1000000)

    s.logout("/orchestrator/logout")
    s.close()

print("Unsuccessful requests: ", error)
