import pytest
import os
import paramiko


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "apache: marks apache server tests"
    )
    config.addinivalue_line(
        "markers", "smoke: marks additional smoke tests"
    )


@pytest.fixture(scope='session')
def get_env_vars():
    connection_vars = {
        "username": os.getenv("SSH_TARGET_USER"),
        "password": os.getenv("SSH_TARGET_PASSWORD"),
        "hostname": os.getenv("SSH_HOSTNAME", "target"),
        "ssh_port": int(os.getenv("SSH_PORT", 22)),
        "http_port": int(os.getenv("HTTP_PORT", 80))
    }

    assert connection_vars["username"] is not None
    assert connection_vars["password"] is not None

    return connection_vars

@pytest.fixture(scope='session')
def ssh_connect(request, get_env_vars):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=get_env_vars["hostname"],
        port=get_env_vars["ssh_port"],
        username=get_env_vars["username"],
        password=get_env_vars["password"]
    )

    def teardown():
        client.close()
    
    request.addfinalizer(teardown)

    return client

@pytest.fixture
def exec_command_ssh(ssh_connect):
    """Executes given command with established SSH connection"""
    def _exec(command, timeout=10):
        stdin, stdout, stderr = ssh_connect.exec_command(command, timeout=timeout)
        exit_code = stdout.channel.recv_exit_status()
        output = stdout.read().decode()
        err = stderr.read().decode()

        assert exit_code == 0, f"SSH command failed: {err}"

        return output
    return _exec