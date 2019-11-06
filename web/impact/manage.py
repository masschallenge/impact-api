#!/usr/bin/env python
import os
import sys
import subprocess

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'impact.settings')

    from configurations.management import execute_from_command_line

    try:
        execute_from_command_line(sys.argv)
        subprocess.call("/usr/bin/notify_slack_on_success.sh", shell=True)
    except SystemExit as exc:
        # TODO pass the error variable
        subprocess.call("/usr/bin/notify_slack_on_failure.sh", shell=True)
