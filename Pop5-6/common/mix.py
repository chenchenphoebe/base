"""mix library for scripts.
"""

import re
import sys
from common import Common

PicPath = sys.path[0] + "\\PicComparison\\"


class Music(Common):
    def __init__(self, device, log_name):
        Common.__init__(self, device, log_name)
        self._ssid = None

    def stay_in_music(self):
        """Keep in Music main page
    
        """
        if self.get_current_packagename() == self.get_app_package_from_file('Music'):
            maxtime = 0
            while (not self._device(resourceId='com.alcatel.music5:id/action_bar_root').exists) \
                    or (not self._device(resourceId='com.alcatel.music5:id/toolbar').exists):
                self._device.press.back()
                self._device.delay(1)
                maxtime += 1
                if maxtime > 3:
                    self._logger.debug("Can't back Music")
                    break
            if maxtime < 4:
                return True

        self._logger.debug("Launch Music.")
        if self.enter_app('Music'):
            self.click_allow()
            self._device.delay(2)
            if self.get_current_packagename() == self.get_app_package_from_file('Music'):
                maxtime = 0
                while (not self._device(resourceId='com.alcatel.music5:id/action_bar_root').exists) \
                        or (not self._device(resourceId='com.alcatel.music5:id/toolbar').exists):
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

        self._logger.debug('Stay in music all songs page.')
        if self._device(resourceId='com.alcatel.music5:id/library_toolbar_button').wait.exists(timeout=2000):
            self._device(resourceId='com.alcatel.music5:id/library_toolbar_button').click()
            self._device.delay(2)
        if self._device(resourceId='com.alcatel.music5:id/library_tabs').child(text='SONGS').wait.exists(timeout=2000):
            self._device(resourceId='com.alcatel.music5:id/library_tabs').child(text='SONGS').click()
            self._device.delay(2)
        else:
            self._logger.debug("Tab All songs not exist.")
            return False

        if self._device(resourceId='android:id/empty').exists:
            self._logger.debug('There is no music.')
            return False

        if self._device(resourceId='com.alcatel.music5:id/all_tracks_fragment_list').wait.exists(timeout=2000):
            self._device.swipe(807, 1605, 802, 831)
            music_num = self._device(resourceId='com.alcatel.music5:id/all_tracks_fragment_list').getChildCount()
            if music_num < 1:
                self._logger.debug('There is no music.')
                return False
            else:
                self._logger.debug('There is %s music.', music_num)
            if music_num > 5:
                music_num = 5
            self._logger.debug('play music')
            if not self._device(resourceId='com.alcatel.music5:id/rl_library_track_item',
                                instance=index % music_num).child(
                resourceId='com.alcatel.music5:id/track_item_title').exists \
                    and self._device(resourceId='com.alcatel.music5:id/all_tracks_fragment_list').exists:
                if index % music_num > 3:
                    self._device(resourceId='com.alcatel.music5:id/all_tracks_fragment_list').swipe.up()
                else:
                    self._device(resourceId='com.alcatel.music5:id/all_tracks_fragment_list').swipe.down()
                self._device.delay(2)
            if not self._device(resourceId='com.alcatel.music5:id/rl_library_track_item',
                                instance=index % music_num).child(
                resourceId='com.alcatel.music5:id/track_item_title').exists:
                self._logger.debug("Can't get the music")
                return False
            music_name = self._device(resourceId='com.alcatel.music5:id/rl_library_track_item',
                                      instance=index % music_num).child(
                resourceId='com.alcatel.music5:id/track_item_title').get_text()
            self._logger.debug("Play music " + music_name)
            self._device(resourceId='com.alcatel.music5:id/rl_library_track_item',
                         instance=index % music_num).child(
                resourceId='com.alcatel.music5:id/track_item_title').click()
            self._device.delay(10)

            if self._device(resourceId='com.alcatel.music5:id/progress_bar_mini_player').exists:
                music_playing = self._device(resourceId='com.alcatel.music5:id/ll_library_track_item').child(
                    resourceId='com.alcatel.music5:id/track_item_title').get_text()
                self._logger.debug("Music " + music_name + ' is playing')
                if music_playing == music_name:
                    self._logger.debug("Play music success")
                    self.stop_play_music()
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
        self._logger.debug('To Stop play music.')
        if self._device(resourceId='com.alcatel.music5:id/add_to_queue_player_icon').exists:
            self._logger.debug('Music is playing.')
            self._device(resourceId='com.alcatel.music5:id/add_to_queue_player_icon').click()
            self._device.delay(2)
            self._logger.debug('Pause playing music.')
            return True
        else:
            self._logger.debug('Stop play music fail!')
            return False
