import time
import httpx
import edge_http


limits = httpx.Limits(max_keepalive_connections=None, max_connections=None, keepalive_expiry=None)
s = edge_http.Client("https://compute.lorenzogiorgi.com/orchestrator/login", "lorenzo", "lorenzo", verify=True,
                     http2=True, timeout=None, limits=limits)

for i in range(1, 10):
    print()
    print()
    print("Request #" + str(i))
    t0 = time.time_ns()
    # r = s.get("https://google.com")
    r = s.get("/echo/echo")
    print(r.http_version)

    print("SC:", r.status_code)

    t1 = time.time_ns()
    print("Time used (ms)", (t1 - t0) / 1000000)
    time.sleep(1)

#trigger migration
s.migrate_on_different_edge("https://orchestrator.lorenzogiorgi.com/migrate/lorenzo")

for i in range(1, 10):
    print()
    print()
    print("Request #" + str(i))
    t0 = time.time_ns()
    # r = s.get("https://google.com")
    r = s.get("/echo/echo")
    print(r.http_version)

    print("SC:", r.status_code)

    t1 = time.time_ns()
    print("Time used (ms)", (t1 - t0) / 1000000)
    time.sleep(1)


s.logout("/orchestrator/logout")
s.close()