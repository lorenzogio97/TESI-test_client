import json
import httpx


class AlternativeServiceTransport(httpx.HTTPTransport):
    """
    A custom transport that enable support for HTTP Alt-Srv defined in RFC7838
    """

    def __init__(self):
        super().__init__(http2=True)
        self.altsrv_cache = {}

    def handle_request(self, request):
        # check if an alt-srv exists for the given origin
        alt_services = self.altsrv_cache.get(request.url.raw.raw_host, [])
        print(request.url.raw_host)
        print(request.url.raw.raw_host)
        print(request.url.host)


        if len(alt_services) != 0:
            new_url = request.url.copy_with(host="pippo.lorenzogiorgi.com")

            new_request = httpx.request(request.method, new_url, content=request.content, headers=request.headers)
            request.url.raw.raw_host = alt_services[0]
        response = super().handle_request(request)
        return response
