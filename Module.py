from core import EventManager
from core import Log
#from modules.module_parent_language.parent_class import ModuleParentLanguage

import re
import subprocess
import time

class Module:#(ModuleParentLanguage):
    def thread_check(self):
        while True:
            self.__check_down()
            self.__check_up()

    def __check_down(self):
        up = True

        while up:
            time.sleep(3)
            if not self.__has_connection():
                up = False

        Log.error('internet_down')
        EventManager.trigger('internet_down')
        #EventManager.trigger('notification', self.lang_get('internet_down'))

    def __has_connection(self, count=0):
        if count <= 2:
            host = '8.8.8.8'
        else:
            host = 'treemo.fr'

        try:
            result = subprocess.check_output(['ping','-c 1', host])
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

        Log.error('internet_up')
        EventManager.trigger('internet_up')
        #EventManager.trigger('notification', self.lang_get('internet_down'))
