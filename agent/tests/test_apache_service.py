import pytest
import requests

# from conftest import exec_command_ssh

def exec_command_ssh(ssh_connect, command):
    stdin, stdout, stderr = ssh_connect.exec_command(command)
    output = stdout.read().decode()

    return output

def request_http(get_env_vars, page):
    hostname = get_env_vars["hostname"]
    port = get_env_vars["http_port"]
    return requests.get(f"http://{hostname}:{port}/{page}")


def test_web_server_running(ssh_connect):
    output=exec_command_ssh(ssh_connect, "ps aux | grep apache2")

    assert "apache2" in output
 

def test_page_on_index(get_env_vars):
    responce = request_http(get_env_vars, "index.html")

    assert responce.status_code == 200
    
    with open('./tests/data/index.html', 'r') as file:
        info = file.read().rstrip('\n')
        assert responce.text == info

def test_unexisting_page(get_env_vars):
    responce = request_http(get_env_vars, "sonic")

    assert responce.status_code == 404
