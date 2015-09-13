from helpers.modules.BaseModule import BaseModule

import time
import socket


class Module(BaseModule):
    internet_is_up = True

    def command_internet_statut(self, send_handler, args, kwargs, client_key):
        """Command internet statut handler"""
        send_handler('internet is %s' % 'up' if self.internet_is_up else 'down')

    def has_internet(self):
        return self.internet_is_up

    def run(self):
        while self.is_running:
            self._check_down()
            self._check_up()

    def started(self):
        self.call(
            'cli', 'register_command', 'internet', self.command_internet_statut, 'Get internet state.',
            _optional_call=True
        )

    def _check_down(self):
        while self.internet_is_up:
            if not self.is_running:
                return

            time.sleep(3)
            if not self._has_connection():
                self.internet_is_up = False

        self.notify(self._('Internet connection down.'))

    def _has_connection(self, count=0):
        host = 'google.com' if count <= 2 else 'github.com'

        try:
            socket.create_connection((host, 80), 2).close()
            return True
        except:
            return self._has_connection(count+1) if count <= 5 else False

    def _check_up(self):
        while not self.internet_is_up:
            if not self.is_running:
                return
            time.sleep(1)
            if self._has_connection():
                self.internet_is_up = True

        self.notify(self._('Internet connection up.'))
