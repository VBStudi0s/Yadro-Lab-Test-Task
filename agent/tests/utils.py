import requests
import pytest


def request_http(get_env_vars, page, timeout=10):
    """Requests given page by address specified in get_env_vars"""

    hostname = get_env_vars["hostname"]
    port = get_env_vars["http_port"]

    try:
        resp = requests.get(f"http://{hostname}:{port}/{page}", timeout=timeout)
        return resp
    except:
        return None

