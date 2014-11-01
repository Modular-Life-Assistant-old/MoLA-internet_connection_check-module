from core import Log

from circuits import Component, Event, handler, Timer
import subprocess
import time


class internet_up(Event):
    """Internet up event"""
    def __init__(self, timestamp): 
        super(internet_up, self).__init__(timestamp)


class internet_down(internet_up):
    """Internet down event"""


class Module(Component):
    channel = 'internet_connection'
    __is_commected = True

    def started(self, component):
        self.check_down()

    def check_down(self):
        if not self.__check_connection():
            Log.info('internet_down')
            self.fire(internet_down(time.time()))

        else:
            Timer(3, Event.create('check_down')).register(self)

    def check_up(self):
        if self.__check_connection():
            Log.info('internet_up')
            self.fire(internet_up(time.time()))

        else:
            Timer(1, Event.create('check_up')).register(self)

    def internet_down(self, timestamp):
        self.check_up()

    def internet_up(self, timestamp):
        self.check_down()

    def is_connected(self):
        return self.__is_commected

    def __check_connection(self, count=0):
        if count <= 2:
            host = '8.8.8.8'
        else:
            host = 'treemo.fr'

        try:
            result = subprocess.check_output(
                ['ping', '-c 1', host],
                timeout=4
             )
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

            self.__is_commected = True
            return True
        except:
            if count <= 5:
                return self.__check_connection(count+1)
            self.__is_commected = False
            return False

