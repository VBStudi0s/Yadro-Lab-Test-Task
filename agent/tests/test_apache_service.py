import pytest
import requests
import allure

from .utils import request_http


@pytest.mark.apache
def test_web_server_running(exec_command_ssh):
    with allure.step("Checking if Apache is running"):
        output = exec_command_ssh("pgrep -xl apache2")
        assert "apache2" in output
 

@pytest.mark.apache
def test_page_on_index(get_env_vars):
    with allure.step("Requesting hosted webpage"):
        responce = request_http(get_env_vars, "index.html")

        assert responce is not None, "HTTP request failed"
        assert responce.status_code == 200

    with allure.step("Checking webpage content"):
        with open('./tests/data/index.html', 'r') as file:
            info = file.read().rstrip('\n')
            allure.attach(responce.text, name="Hosted index.html", attachment_type=allure.attachment_type.HTML)
            assert responce.text == info


@pytest.mark.apache
def test_unexisting_page(get_env_vars):
    with allure.step("Requesting unexisting webpage"):
        responce = request_http(get_env_vars, "sonic")

        assert responce is not None, "HTTP request failed"
        assert responce.status_code == 404
