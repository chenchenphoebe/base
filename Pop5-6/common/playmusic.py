"""Camera library for scripts.
"""

import re
import sys
from common import Common
PicPath = sys.path[0]+"\\ResourceFile\\PicComparison"

class Music(Common):
   
    def __init__(self, device, log_name):
        Common.__init__(self, device,log_name)
        self._ssid = None
        
    def stay_in_music(self):
        """Keep in Music main page
    
        """
        if not self.get_current_packagename() == self.get_app_package_from_file('Play Music'):
            self._logger.debug("Launch Play Music.")
            if not self.enter_app('Play Music'):
                return False
        
        while self._device(text = 'SKIP').exists:
            self._device(text = 'SKIP').click()
            self._device.delay(2)   
            self._device.delay('Skip the first page')
        maxtime = 0
        while not self._device(description  = 'Show navigation drawer').exists:
            self._device.press.back()
            self._device.delay(1)
            maxtime += 1 
            if maxtime > 3:
                self._logger.debug("Can't back Music")
                return False
            
        if self._device(resourceId = 'com.google.android.music:id/play_music_header_toolbar').child(text = 'Music library').exists:  #modified by hanbei:change widget
            self._logger.debug("Open main page successfully")
            return True
        else:
            self._device(description  = 'Show navigation drawer').click()
            self._device.delay(2)
            if self._device(className  = 'android.widget.TextView', text = 'Music library').exists:
                self._device(className  = 'android.widget.TextView', text = 'Music library').click()
                self._device.delay(2)
                if self._device(resourceId = 'com.google.android.music:id/play_music_header_toolbar').child(text = 'Music library').exists:#modified by hanbei:change widget
                    self._logger.debug("Open main page successfully")
                    return True 
                                          
        self._logger.debug('Launch Play Music main page fail')
        return False

    
    def play_mp3(self, index):
        """paly music 
        
        """
        self._logger.debug('play music')
        if not self._device(resourceId = 'com.google.android.music:id/play_header_list_tab_container').child(resourceId = 'com.google.android.music:id/title', text = 'SONGS').exists:
            self._logger.debug('There is no title songs in music.')
            return False
        
        times = 0
        while not self._device(resourceId = 'com.google.android.music:id/play_header_list_tab_container').child(resourceId = 'com.google.android.music:id/title', text = 'SONGS').isSelected():
            self._device(resourceId = 'com.google.android.music:id/play_header_list_tab_container').child(resourceId = 'com.google.android.music:id/title', text = 'SONGS').click()
            self._device.delay(2)
            times += 1
            if times > 3:
                self._logger.debug('Switch to songs fail.')
                return False
            
        if self._device(resourceId = 'android:id/list').exists:
            music_num = self._device(resourceId = 'android:id/list').getChildCount() - 1
            self._logger.debug(self._device(resourceId = 'android:id/list').getChildCount())
            if music_num < 1:
                self._logger.debug('There is no music.')
                return False
          
            if self._device(resourceId = 'com.google.android.music:id/li_title', text = 'recording2015-07-17-15-00-00').exists:
                    self._device(resourceId = 'com.google.android.music:id/list_context_menu').click()
                    self._device.delay(3)
                    if self._device(resourceId = 'android:id/text1', text = 'Delete').exists:
                        self._device(resourceId = 'android:id/text1', text = 'Delete').click()
                        self._device.delay(3)
                        if self._device(resourceId = 'android:id/button1', text = 'OK').exists:
                            self._device(resourceId = 'android:id/button1', text = 'OK').click()    
                            self._device.delay(3)
                            
            if music_num > 5:
                music_num = 5
            music_name = self._device(className='android.widget.LinearLayout').child(resourceId='com.google.android.music:id/li_title', instance = index%music_num).get_text()
            self._logger.debug("Play music " + music_name)
            self._device(className='android.widget.LinearLayout').child(resourceId='com.google.android.music:id/li_title', instance = index%music_num).click()
            self._device.delay(3)
            if self._device(resourceId='com.google.android.music:id/play_indicator').exists\
                and self._device(description ='Pause').exists\
                and self._device(resourceId='com.google.android.music:id/trackname').exists:
                music_playing = self._device(resourceId='com.google.android.music:id/trackname').get_text()
                self._logger.debug("Music " + music_name + ' is playing')
                if music_playing == music_name:
                    self._logger.debug("Play music successfully")
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
        self._logger.debug('close music')
        if self._device(description ='Pause').exists:
            self._device(description ='Pause').click()
            self._device.delay(2)
        if self._device(description ='Play').exists:
            return True
        else:
            return False

                   
    
    
    
    
    
    
    
    
    
    
    
    
    
            
            