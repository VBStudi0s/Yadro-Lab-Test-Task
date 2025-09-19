import requests
import pytest


def exec_command_ssh(ssh_connect, command):
    """Executes given command with established SSH connection"""

    stdin, stdout, stderr = ssh_connect.exec_command(command)
    exit_code = stdout.channel.recv_exit_status()
    output = stdout.read().decode()
    err = stderr.read().decode()

    assert exit_code == 0, f"SSH command failed: {err}"

    return output

def request_http(get_env_vars, page, timeout=10):
    """Requests given page by address specified in get_env_vars"""

    hostname = get_env_vars["hostname"]
    port = get_env_vars["http_port"]

    try:
        resp = requests.get(f"http://{hostname}:{port}/{page}", timeout=timeout)
        return resp
    except:
        return None

