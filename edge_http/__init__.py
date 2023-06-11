from ._client import Client

__all__ = [
    "Client"
]

__locals = locals()
for __name in __all__:
    if not __name.startswith("__"):
        setattr(__locals[__name], "__module__", "edge_http")  # noqa
