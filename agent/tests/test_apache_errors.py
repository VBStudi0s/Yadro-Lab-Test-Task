import pytest
import datetime
import os

from .utils import exec_command_ssh


def get_last_errors(ssh_connect, minutes=5):
    """Reads Apache error.log file and parses it trying to find errors within some minutes"""

    logs = exec_command_ssh(ssh_connect, "tail -n 200 /var/log/apache2/error.log")
    cutoff = datetime.datetime.now() - datetime.timedelta(minutes=minutes)

    found_errors = []
    unparsed_lines = []

    for line in logs.splitlines():
        if "error" in line.lower():     # ignore info, warn, etc.
            try:
                parts=line.split()      # default apache format is [Tue Aug 29 21:55:52.123456 2025]
                date_format = "%b %d %H:%M:%S.%f %Y"        # Transform to "Aug 29 21:55:52.123456 2025"
                parsed_time = " ".join(parts[1:4] + [parts[4][:-1]])  # remove the ']' from year: "2025]" -> "2025"
                log_time = datetime.datetime.strptime(parsed_time, date_format)
                if log_time > cutoff:
                    found_errors.append(line)
            except:
                unparsed_lines.append(line)
    
    return found_errors, unparsed_lines


def test_apache_last_errors(ssh_connect):
    minutes = int(os.getenv("APACHE_ERROR_TIMEOUT", "5"))
    found_errors, unparsed_lines = get_last_errors(ssh_connect, minutes=minutes)

    msg = ""

    if found_errors:
        msg+=f"Found following errors in Apache logs in last {minutes} minutes: \n" + "\n".join(found_errors)
    if unparsed_lines:
        msg+=f"\nAlso could not parse following lines: \n" + "\n".join(unparsed_lines)

    assert not found_errors, msg
        


    