import requests
import pytest


def exec_command_ssh(ssh_connect, command):
    stdin, stdout, stderr = ssh_connect.exec_command(command)
    output = stdout.read().decode()

    return output

def request_http(get_env_vars, page):
    hostname = get_env_vars["hostname"]
    port = get_env_vars["http_port"]
    return requests.get(f"http://{hostname}:{port}/{page}", timeout=10)
