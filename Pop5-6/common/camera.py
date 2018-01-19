"""Camera library for scripts.
"""

from common import Common

StorePath_Media = 'sdcard/DCIM/Camera'


class Camera(Common):
    def __init__(self, device, log_name):
        Common.__init__(self, device, log_name)
        self._ssid = None

    def stay_in_camera(self):
        """Keep in Camera main page
        
        """
        if self.get_current_packagename() == self.get_app_package_from_file('Camera'):
            maxtime = 0
            while not self._device(resourceId='com.tct.tablet.camera:id/menu_setting_button').wait.exists(timeout=2000):
                self._device.press.back()
                self._device.delay(1)
                maxtime += 1
                if maxtime > 3:
                    self._logger.debug("Can't back Camera")
                    break
            if maxtime < 4:
                return True

        self._device.press.home()
        self._logger.debug("Launch Camera.")
        if self.enter_app('Camera'):
            while self._device(resourceId='com.android.packageinstaller:id/permission_message').exists:
                self._device(text='ALLOW').click()
                self._device.delay(2)
            if self.get_current_packagename() == self.get_app_package_from_file('Camera'):
                maxtime = 0
                while not self._device(resourceId='com.tct.tablet.camera:id/menu_setting_button').exists:
                    self._device.press.back()
                    self._device.delay(1)
                    maxtime += 1
                    if maxtime > 3:
                        self._logger.debug("Can't back Camera")
                        break
                if maxtime < 4:
                    return True

            self._logger.debug('Launch Camera main page fail')
            return False
        else:
            return False

    def enter_preview(self, preview_type):
        """enter preview mode
            @param preview_type : 'Photo' or 'Video'
            
        """
        self._logger.debug('Enter %s preview mode.', preview_type)
        if self._device(resourceId='com.tct.tablet.camera:id/peek_thumb').exists:
            self._device(resourceId='com.tct.tablet.camera:id/peek_thumb').click()
            self._device.delay(4)
        self.click_allow()
        if self._device(resourceId='com.tct.tablet.gallery3d:id/imageView').exists:
            self._logger.debug('Enter %s preview mode successfully.', preview_type)
            return True
        else:
            self._logger.debug('Enter %s preview mode failed!.', preview_type)
            return False

    def take_photo(self):
        """take  a photo 
        
        """
        self._logger.debug('take photo')
        file_number = self.get_file_num(StorePath_Media, [".jpg"])
        if self._device(resourceId='com.tct.tablet.camera:id/mode_item_name', text='PHOTO').exists:
            self._device(resourceId='com.tct.tablet.camera:id/mode_item_name', text='PHOTO').click()
            if self._device(resourceId='com.tct.tablet.camera:id/shutter_button').exists:
                self._device(resourceId='com.tct.tablet.camera:id/shutter_button').click()
            self._device.delay(10)
        else:
            self._logger.warning("Get take photo button failed!")
            return False
        if self.get_file_num(StorePath_Media, [".jpg"]) == file_number + 1:
            return True
        else:
            self._logger.warning("Take picture failed!")
            return False

    def record_video(self, recordTime):
        """record a video
        @param (int)recordTime --time of the video

        """
        self._logger.debug('record video')
        file_number = self.get_file_num(StorePath_Media, ['.3gp', '.mp4'])
        if self._device(resourceId='com.tct.tablet.camera:id/mode_item_name', text='VIDEO').exists:
            self._device(resourceId='com.tct.tablet.camera:id/mode_item_name', text='VIDEO').click()
            self._device.delay(3)

            if self._device(resourceId='com.tct.tablet.camera:id/shutter_button').exists:
                self._device(resourceId='com.tct.tablet.camera:id/shutter_button').click()
                self._device.delay(recordTime)

            if self._device(resourceId='com.tct.tablet.camera:id/shutter_button').exists:
                self._device(resourceId='com.tct.tablet.camera:id/shutter_button').click()
                self._device.delay(3)

            #             if self._device(resourceId = 'com.tct.camera:id/recording_time').exists:
            #                 self._device.delay(recordTime)
            else:
                self._logger.warning("Can't get the redording time.Record video failed!")
                return False

            if not self._device(resourceId='com.tct.tablet.camera:id/mode_item_name',
                                text='VIDEO').exists:  # modified by hanbei
                self._logger.warning("Get Recording video button failed!")
                return False
            #             self._device(resourceId = 'com.tct.camera:id/camera_video_switch_icon').click()
            #             self._device.delay(2)
        else:
            self._logger.warning("Get Recording video button failed!")
            return False
        if self.get_file_num(StorePath_Media, ['.3gp', '.mp4']) == file_number + 1:
            return True
        else:
            self._logger.warning("Record video failed!")
            return False

    def play_vedio(self):
        """play a recorded video 
        
        """
        if not self.enter_preview('Video'):
            return False
        self._device.delay(2)

        self._logger.debug('play video')
        if self._device(resourceId='com.tct.camera:id/filmstrip_view').child(className='android.widget.ImageView',
                                                                             instance=1).exists:
            self._device(resourceId='com.tct.camera:id/filmstrip_view').child(className='android.widget.ImageView',
                                                                              instance=1).click()
            self._device.delay(3)
            if self.choose_first_player():
                self._device.delay(3)
        elif self._device(resourceId='com.tct.tablet.gallery3d:id/imageView').exists:
            self._device.click(540, 958)
            self._device.delay(3)

            if self.choose_first_player():
                self._device.delay(3)

        if self._device(resourceId='com.tct.tablet.gallery3d:id/surface_view').exists:
            wait_time = 0
            while True:
                if self._device(resourceId='com.tct.camera:id/filmstrip_view').exists \
                        or self._device(resourceId='com.tct.tablet.gallery3d:id/imageView').exists:
                    self._device.press.back()
                    self._device.delay(3)
                    self._logger.debug('Finish play video.')
                    return True
                else:
                    wait_time += 1
                    self._device.delay(1)
                    if wait_time > 30:
                        self._device.press.back()
                        self._logger.debug('Fail to finish play video.')
                        return False

        elif self._device(resourceId='com.google.android.apps.plus:id/videoplayer').exists \
                or self._device(resourceId='com.google.android.apps.photos:id/photo_hashtag_fragment_container').exists:
            self._device.delay(30)
            self._device.press.back()
            if self._device(resourceId='com.tct.camera:id/filmstrip_view').exists:
                self._device.press.back()
                self._device.delay(2)
                self._logger.debug('Finish play video.')
                return True
            else:
                self._device.press.back()
                self._logger.debug('Fail to finish play video.')
                return False
        self._logger.debug('Fail to play video.')
        return False

    def delete_media_file(self, preview_type, file_type):
        """delete a photo or video preview mode
        @param preview_type:  'Photo' or 'Video'
        @param file_type: ['.jpg'] for Photo or ['.mp4', '.3gp'] for Video
        
        """
        file_number = self.get_file_num(StorePath_Media, file_type)
        if file_number == 0:
            self._logger.warning("None video can be deleted.")
            return False

        if not self.enter_preview(preview_type):
            return False
        self._device.delay(4)

        try_times = 0
        while True:
            if self._device(resourceId='com.tct.tablet.gallery3d:id/imageView').exists:
                self._device(resourceId='com.tct.tablet.gallery3d:id/imageView').click.bottomright()
            else:
                self._device.click(665, 1216)
            self._device.delay(1)
            if self._device(resourceId='com.tct.tablet.gallery3d:id/photopage_delete').exists:
                self._device(resourceId='com.tct.tablet.gallery3d:id/photopage_delete').click()
                self._device.delay(2)
                if self._device(resourceId='android:id/button1', text='DELETE').exists:
                    self._device(resourceId='android:id/button1', text='DELETE').click()
                    self._device.delay(2)
                    break
                elif self._device(resourceId='android:id/button1', text='OK').exists:
                    self._device(resourceId='android:id/button1', text='OK').click()
                    self._device.delay(2)
                    break
            else:
                try_times += 1
            if try_times > 5:
                self._logger.warning("Didn't find Delete button!")
                return False

        if self.get_file_num(StorePath_Media, file_type) == file_number - 1:
            self._logger.warning("Delete %s successfully!", preview_type)
            return True
        self._logger.warning("Delete %s failed!", preview_type)
        return False
