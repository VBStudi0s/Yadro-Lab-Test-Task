import pytest

from .utils import exec_command_ssh

def test_tar_package(ssh_connect):
    """Tests tar package by packing two files, unpacking them and checking its content"""

    # Creating files to test
    exec_command_ssh(ssh_connect, "mkdir /tmp/testing && cd /tmp/testing && mkdir tar && cd tar")
    exec_command_ssh(ssh_connect, "echo 'foo content' > ./foo.txt")
    exec_command_ssh(ssh_connect, "echo 'bar content' > ./bar.txt")
    exec_command_ssh(ssh_connect, "tar -cf archive.tar  foo.txt bar.txt")   # Creating archive

    archived_files = exec_command_ssh(ssh_connect, "tar -tf archive.tar")

    # check if these files are in the archive
    assert "foo.txt" in archived_files
    assert "bar.txt" in archived_files

    exec_command_ssh(ssh_connect, "rm *.txt && tar -xf archive.tar")   # delete old files and unpack the archive

    def check_file_after_unpacking(filename, expected_content):
        extracted_files = exec_command_ssh(ssh_connect, "ls")
        assert filename in extracted_files

        actual_content = exec_command_ssh(ssh_connect, f"cat {filename}")
        assert expected_content.strip() == actual_content.strip()
    
    check_file_after_unpacking("foo.txt", "foo content")
    check_file_after_unpacking("bar.txt", "bar content")
    
def test_ln_package(ssh_connect):
    pass