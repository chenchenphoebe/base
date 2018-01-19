"""music library for scripts.
"""

import re
import sys
from common import Common
PicPath = sys.path[0]+"\\PicComparison\\"

class Music(Common):
   
    def __init__(self, device, log_name):
        Common.__init__(self, device,log_name)
        self._ssid = None
        
    def stay_in_music(self):
        """Keep in Music main page
    
        """
        if self.get_current_packagename() == self.get_app_package_from_file('Music'):
            maxtime = 0
            while not self._device(resourceId = 'com.tct.music:id/title_name', text = 'Music').exists:
                self._device.press.back()
                self._device.delay(1)
                maxtime += 1
                if maxtime > 3:
                    self._logger.debug("Can't back Music")
                    break
            if maxtime < 4:
                return True

        self._device.press.home()
        self._logger.debug("Launch Music.")
        if self.enter_app('Music'):
            self._device.delay(2)
            if self.get_current_packagename() == self.get_app_package_from_file('Music'):  
                maxtime = 0
                while not self._device(resourceId = 'com.tct.music:id/title_name', text = 'Music').exists:
                    self._device.press.back()
                    self._device.delay(1)
                    maxtime += 1
                    if maxtime > 3:
                        self._logger.debug("Can't back Music")
                        break
                if maxtime < 4:
                    return True                 
            
            self._logger.debug('Launch Music main page fail')
            return False
        else:
            return False 
    
    def play_mp3(self, index):
        """paly music 
        
        """
        self._logger.debug('play music')
        self._device.delay(1)
        if self._device(text='All').exists:
            self._device(text='All').click()
            self._device.delay(2)
        if self._device(resourceId = 'android:id/list').exists:
            music_num = self._device(resourceId = 'android:id/list').getChildCount()
            if music_num < 1:
                self._logger.debug('There is no music.')
                return False
            if music_num > 5:
                music_num = 5
            music_name = self._device(className='android.widget.ListView').child(resourceId='com.tct.music:id/line1', instance = index%music_num).get_text()
            self._logger.debug("Play music " + music_name)
            self._device(className='android.widget.ListView').child(resourceId='com.tct.music:id/line1', instance = index%music_num).click()
            self._device.delay(3)
            if self._device(resourceId='com.tct.music:id/mb_progress_bar').exists:
                music_playing = self._device(resourceId='com.tct.music:id/title').get_text()
                self._logger.debug("Music " + music_name + ' is playing')
                if music_playing == music_name:
                    self._logger.debug("Play music success")
                    return True
                else:
                    self._logger.debug('play the other music!')
                    return False
            else:
                self._logger.debug('play music fail')
                return False
            
        else:
            self._logger.debug('There is no music.')
            return False    
            
    def stop_play_music(self):
        """stop playing music 
        
        """
        self._logger.debug('Stop play music.')
        self._device.delay(1)
        if self._device(text='All').exists:
            self._device(text='All').click()
            self._device.delay(2)
        if self._device.find(PicPath+'music_play.png'):
            self._logger.debug('Music is playing.')
            if self._device(resourceId='com.tct.music:id/play_icon').exists:
    #             self._device.screenshot(sys.path[0]+"\\PicComparison\\music.png")
    #             self._device.dump(sys.path[0]+"\\PicComparison\\music.uix")
                self._device(resourceId='com.tct.music:id/play_icon').click()
                self._device.delay(2)
                self._logger.debug('Pause playing music.')
        if self._device.find(PicPath+'music_pause.png'):
            self._logger.debug('Music is pause.')
            return True
        else:
            self._logger.debug('Stop play music fail!')
            return False
            