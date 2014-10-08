from core import Log
from core.decorator import threaded

from circuits import Component, Event, task, Worker
import subprocess
import time


class internet_up(Event):
    """Internet up event"""


class internet_down(Event):
    """Internet down event"""


class Module(Component):
    @threaded
    def started(self, component):
        while True:
            self.__check_down()
            self.__check_up()

    def __check_down(self):
        up = True

        while up:
            time.sleep(3)
            if not self.__has_connection():
                up = False

        Log.info('internet_down')
        self.fire(internet_down())

    def __has_connection(self, count=0):
        if count <= 2:
            host = '8.8.8.8'
        else:
            host = 'treemo.fr'

        try:
            result = subprocess.check_output(['ping', '-c 1', host])
#            time = re.search('time=(.*) ms', result)
#
#            if time and count <= 2:
#                time = float(time.group(1))
#
#                if self.__average_time:
#                    if time >= 3 * self.__average_time:
#                        Log.error('internet_lag')
#                        EventManager.trigger('notification', self.lang_get('internet_lag'))
#                    self.__average_time = (time + self.__average_time) / 2
#                else:
#                    self.__average_time = time

            return True
        except:
            if count <= 5:
                return self.__has_connection(count+1)
            return False

    def __check_up(self):
        down = True

        while down:
            time.sleep(1)
            if self.__has_connection():
                down = False

        Log.info('internet_up')
        self.fire(internet_up())
