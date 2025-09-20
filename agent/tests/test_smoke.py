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

    # creating files to test
    exec_command_ssh("echo 'test info' > /tmp/test_file.txt")
    exec_command_ssh("ln -s /tmp/test_file.txt /tmp/test_ln_link")

    files = exec_command_ssh("ls /tmp")     # checks if link file was created
    assert "test_ln_link" in files

    fileinfo = exec_command_ssh("ls -l /tmp/test_ln_link")      # checks if created file is a link
    assert fileinfo[0] == 'l'
    assert "/tmp/test_file.txt" in fileinfo

    content = exec_command_ssh("cat /tmp/test_ln_link")     # checks its content
    assert 'test info' in content
