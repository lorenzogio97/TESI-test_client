import random
import time
import typing
import httpx
import socket
import json
from httpx._types import (
    AsyncByteStream,
    AuthTypes,
    CertTypes,
    CookieTypes,
    HeaderTypes,
    ProxiesTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestExtensions,
    RequestFiles,
    SyncByteStream,
    TimeoutTypes,
    URLTypes,
    VerifyTypes,
)

from httpx._client import UseClientDefault, USE_CLIENT_DEFAULT

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


class Client(httpx.Client):
    def __init__(self, auth_url: str, username: str, password: str, **kwargs):
        super().__init__(**kwargs)
        self._alt_svc_cache: typing.List[dict] = []
        self.login_data = {"username": username, "password": password}
        self.login_url = auth_url

        # make login request
        r = self.post(auth_url, json=self.login_data)
        response = json.loads(r.content.decode("utf-8"))

        domain = response["domainName"]
        self.base_url = httpx.URL("https://" + domain)

    def get(
            self,
            url: URLTypes,
            *,
            params: typing.Optional[QueryParamTypes] = None,
            headers: typing.Optional[HeaderTypes] = None,
            cookies: typing.Optional[CookieTypes] = None,
            auth: typing.Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
            follow_redirects: typing.Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
            timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
            extensions: typing.Optional[RequestExtensions] = None,
    ) -> httpx.Response:

        url, headers = self.__use_altsvc_cache(url, headers)

        response = self.request(
            "GET",
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=False,
            timeout=timeout,
            extensions=extensions,
        )

        # print("RESPONSE.URL.HOST", response.url.host)
        self.__update_alt_svc_cache(response)

        if response.status_code in [301, 302, 307, 308]:
            new_url = response.headers["Location"]
            response = super().get(
                url=new_url,
                params=params,
                headers=headers,
                cookies=cookies,
                auth=auth,
                follow_redirects=True,
                timeout=timeout,
                extensions=extensions
            )

        return response

    def post(
            self,
            url: URLTypes,
            *,
            content: typing.Optional[RequestContent] = None,
            data: typing.Optional[RequestData] = None,
            files: typing.Optional[RequestFiles] = None,
            json: typing.Optional[typing.Any] = None,
            params: typing.Optional[QueryParamTypes] = None,
            headers: typing.Optional[HeaderTypes] = None,
            cookies: typing.Optional[CookieTypes] = None,
            auth: typing.Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
            follow_redirects: typing.Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
            timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
            extensions: typing.Optional[RequestExtensions] = None,
    ) -> httpx.Response:

        url, headers = self.__use_altsvc_cache(url, headers)

        response = self.request(
            "POST",
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=False,
            timeout=timeout,
            extensions=extensions,
        )

        self.__update_alt_svc_cache(response)

        if response.status_code in [301, 302, 307, 308]:
            new_url = response.headers["Location"]
            response = self.request(
                "POST",
                new_url,
                content=content,
                data=data,
                files=files,
                json=json,
                params=params,
                headers=headers,
                cookies=cookies,
                auth=auth,
                follow_redirects=True,
                timeout=timeout,
                extensions=extensions,
            )
        return response

    def __use_altsvc_cache(self, url: httpx.URL, headers: httpx.Headers):
        # print(self._alt_svc_cache)
        url = self._merge_url(url)
        # print(url.host, url.port)

        # enabling Alt-Svc mechanism only for the domain assigned to the platform, that we can consider trusted
        if url.host == self.base_url.host and len(self._alt_svc_cache) != 0:
            # check age of cached Alt-Svc
            while len(self._alt_svc_cache) != 0 and self._alt_svc_cache[0]["timeout"] < time.time():
                self._alt_svc_cache.pop(0)
            # check if some alt-svc is still there
            if len(self._alt_svc_cache) != 0:
                # print(62, self._alt_svc_cache[0]['value'])
                alt_svc_url = url.copy_with(host=self._alt_svc_cache[0]['value'])
                # print(64, alt_svc_url.scheme, alt_svc_url.host)
                url = alt_svc_url
                if headers is None:
                    headers = httpx.Headers()
                headers["Alt-Used"] = alt_svc_url.host
        print(url.host, url.port)
        return url, headers

    def __update_alt_svc_cache(self, response: httpx.Response):
        # check if url is related to platform
        if response.url.host.endswith(self.base_url.host) or \
                response.url.host in [x['value'] for x in self._alt_svc_cache]:

            if response.status_code == 421:
                # remove the used Alt-Svc
                self._alt_svc_cache = [item for item in self._alt_svc_cache if item["value"] != response.url.host]
                return

            response_headers = {k.lower(): v for k, v in response.headers.items()}
            if "alt-svc" in response_headers:
                if response_headers["alt-svc"].strip() == "clear":
                    # delete all alt_rvc
                    self._alt_svc_cache = []
                else:
                    self.__parse_alt_svc(response_headers["alt-svc"])

    def __parse_alt_svc(self, header: str):
        alternative_list = header.split(",")
        alternative_list = [item.strip() for item in alternative_list]

        for alternative in reversed(alternative_list):
            part_list = alternative.split(";")
            part_list = [item.strip() for item in part_list]
            # protocol default to h2 (h3 not supported by HTTPX)
            if part_list[0].split("=")[0].strip() != "h2":
                break
            hostname_port = part_list[0].split("=")[1].strip().strip("\"")
            hostname: str = hostname_port.split(":")[0]
            port: int = int(hostname_port.split(":")[1])

            # envoy edge proxies run on 443, so no need to use other ports
            if hostname == "" or port != 443:
                break
            # parse max-age attribute
            max_age: int = 24 * 60 * 60
            for i in range(1, len(part_list)):
                part = part_list[i].strip()
                if len(part.split("=")) != 2:
                    # malformed, ignoring the option
                    continue
                key = part.split("=")[0].strip()
                value = part.split("=")[1].strip()
                # ignore persist option
                if key == "persist":
                    continue
                elif key == "ma":
                    max_age = int(value)
                else:
                    # malformed header, ignoring the option
                    continue
            # receiving Alt-Svc header replaces all cached alternative services for that origin (Section 3.1 RFC 7838)
            self._alt_svc_cache = []
            self._alt_svc_cache.insert(0, {"value": hostname, "timeout": time.time() + max_age})

    def authenticate(self, username, password):
        self.login_data = {"username": username, "password": password}
        self.__init__(self.login_url, username, password)

    def logout(self, logout_url: str):
        # make login request
        print("logout")
        r = self.post(logout_url, json=self.login_data)
        print(r.status_code)
        if r.status_code == 200:
            self.close()
            self.login_data = None
            self._alt_svc_cache = []
            self.login_url = None

    def migrate_on_different_edge(self, migration_url: str):
        edge_node_list = ["edge1", "edge2", "edge3"]
        if len(self._alt_svc_cache) == 0:
            print("No migration made, unknown edge")
            return

        node_to_migrate = [x for x in edge_node_list if x != self._alt_svc_cache[0]["value"].split(".")[0]]
        random.shuffle(node_to_migrate)
        migration_data = {"edgeNodeList": node_to_migrate, "username": self.login_data["username"]}
        r = self.post(migration_url, json=migration_data)

    def get_current_edge(self):
        if len(self._alt_svc_cache) == 0:
            print("No migration made, unknown edge")
            return "cloud"

        current_edge = self._alt_svc_cache[0]["value"].split(".")[0]

        return current_edge

    def get_username(self):
        return self.login_data["username"]