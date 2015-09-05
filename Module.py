import socket
from helpers.modules.BaseModule import BaseModule

import os
import subprocess
import time


class Module(BaseModule):
    def run(self):
        while self.is_running:
            self._check_down()
            self._check_up()

    def _check_down(self):
        up = True

        while up:
            time.sleep(3)
            if not self._has_connection():
                up = False

        self.notify(self._('Internet connection down.'))

    def _has_connection(self, count=0):
        host = 'google.com' if count <= 2 else 'github.com'

        try:
            socket.create_connection((host, 80), 2).close()
            return True
        except:
            return self._has_connection(count+1) if count <= 5 else False

    def _check_up(self):
        down = True

        while down:
            time.sleep(1)
            if self._has_connection():
                down = False

        self.notify(self._('Internet connection up.'))
