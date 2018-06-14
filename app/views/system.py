# Settings
from django.conf import settings

import os
import subprocess
from typing import Tuple
from .utils import Storage
from .json_view import JsonView

# Unified responses:
responseBE = Tuple[Storage, int]

__author__ = 'anton'

"""
    system version can be found here
"""


class VersionView(JsonView):
    def get(self, request) -> responseBE:
        git_dir = os.path.dirname(settings.PROJECT_DIR)

        # try:
        #     date = subprocess.Popen(
        #         "git -C {dir} log -1 --pretty=format:\"%cd\""
        #         " --date=short".format(dir=git_dir),
        #         shell=True, stdout=subprocess.PIPE,
        #         stderr=subprocess.STDOUT).stdout.readline().strip().decode('utf-8')
        #
        #     version = subprocess.Popen(
        #         "git -C {dir} describe --tags $(git -C {dir} rev-list --tags"
        #         " --max-count=1)".format(dir=git_dir),
        #         shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)\
        #         .stdout.readline().strip().decode('utf-8')
        # except:
        #     date = 'unknown'
        #     version = 'unknown'

        try:
            with open('{}/version.txt'.format(git_dir), 'r') as my_file:
                version = my_file.read().replace('\n', '')
        except:
            version = 'unknown'

        return Storage(version=version), 200
