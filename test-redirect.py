import time
import socket
import edge_http

"""
workaround to get resolved IP by DNS : https://stackoverflow.com/questions/44374215/how-do-i-specify-url-resolution-in-pythons-requests-library-in-a-similar-fashio
"""
prv_getaddrinfo = socket.getaddrinfo


def new_getaddrinfo(*args):
    # Uncomment to see what calls to `getaddrinfo` look like.
    # print(args)
    addr = prv_getaddrinfo(*args)
    print(addr)
    return addr


socket.getaddrinfo = new_getaddrinfo

s = edge_http.Client("https://compute.lorenzogiorgi.com/orchestrator/login", "lorenzo", "lorenzo", verify=True,
                     http2=True, timeout=None)

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
