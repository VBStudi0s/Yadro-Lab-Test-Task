import pytest
import requests

from .utils import exec_command_ssh, request_http


def test_web_server_running(ssh_connect):
    output = exec_command_ssh(ssh_connect, "pgrep -xl apache2")

    assert "apache2" in output
 

def test_page_on_index(get_env_vars):
    responce = request_http(get_env_vars, "index.html")

    assert responce is not None, "HTTP request failed"
    assert responce.status_code == 200
    
    with open('./tests/data/index.html', 'r') as file:
        info = file.read().rstrip('\n')
        assert responce.text == info


def test_unexisting_page(get_env_vars):
    responce = request_http(get_env_vars, "sonic")

    assert responce is not None, "HTTP request failed"
    assert responce.status_code == 404
