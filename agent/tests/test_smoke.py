import pytest


def test_tar_package(exec_command_ssh):
    """Tests tar package by packing two files, unpacking them and checking its content"""

    # Creating files to test
    exec_command_ssh("mkdir /tmp/testing && cd /tmp/testing && mkdir tar && cd tar")
    exec_command_ssh("echo 'foo content' > ./foo.txt")
    exec_command_ssh("echo 'bar content' > ./bar.txt")
    exec_command_ssh("tar -cf archive.tar  foo.txt bar.txt")   # Creating archive

    archived_files = exec_command_ssh("tar -tf archive.tar")

    # check if these files are in the archive
    assert "foo.txt" in archived_files
    assert "bar.txt" in archived_files

    exec_command_ssh("rm *.txt && tar -xf archive.tar")   # delete old files and unpack the archive

    def check_file_after_unpacking(filename, expected_content):
        extracted_files = exec_command_ssh("ls")
        assert filename in extracted_files

        actual_content = exec_command_ssh(f"cat {filename}")
        assert expected_content.strip() == actual_content.strip()
    
    check_file_after_unpacking("foo.txt", "foo content")
    check_file_after_unpacking("bar.txt", "bar content")
    
def test_ln_package(exec_command_ssh):
    """Tests for ln package"""
    pass
