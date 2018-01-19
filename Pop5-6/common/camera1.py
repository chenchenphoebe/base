"""Camera library for scripts.
"""

from common import Common
StorePath_Media='sdcard/DCIM/Camera'

class Camera(Common):
   
    def __init__(self, device, log_name):
        Common.__init__(self, device,log_name)
        self._ssid = None
        
    def stay_in_camera(self):
        """Keep in Camera main page
        
        """
        if self.get_current_packagename() == self.get_app_package_from_file('Camera'):
            maxtime = 0
            while not ( self._device(description  = 'Shutter').exists\
                and not self._device(resourceId = 'com.android.camera2:id/action_delete').exists):
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
            self._device.delay(2)
            if self.get_current_packagename() == self.get_app_package_from_file('Camera'):  
                maxtime = 0
                while not (self._device(description  = 'Shutter').exists\
                    and not self._device(resourceId = 'com.android.camera2:id/action_delete').exists):
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
    
    def get_current_mode(self):
        """get curent mode
            @return:  ['Camera', 'Back']
                    or ['Camera', 'Front']
                    or ['Video', 'Back']
                    or ['Video', 'Front']   
                    
        """
        if self._device(resourceId='com.android.camera2:id/setting_mode').exists:
            if not self._device(text = 'Photo Settings').exists\
             and not self._device(text = 'Video Settings').exists:
                self._device(resourceId='com.android.camera2:id/setting_mode').click()
                self._device.delay(2)
            mode_current = ['', '']
            if self._device(text = 'Video Settings').exists:
                mode_current[0] = 'Video'
                if self._device(resourceId='com.android.camera2:id/layout_setting_switch').exists:
                    mode_current[1] = 'Back'
                else:
                    mode_current[1] = 'Front'
                self._logger.debug('Current mode is ' + mode_current[1] + mode_current[0])      
            elif self._device(text = 'Photo Settings').exists:
                mode_current[0] = 'Camera'
                if self._device(resourceId = 'com.android.camera2:id/mode_list_second').exists:
                    mode_current[1] = 'Back'
                else:
                    mode_current[1] = 'Front'
                self._logger.debug('Current mode is ' + mode_current[1] + mode_current[0])
                
            if self._device(text = 'OK').exists:
                self._device(text = 'OK').click()
                self._device.delay(2)        
        else:
            self._logger.debug('Isn\'t in peview mode' )
        return mode_current
    
    def Switch_mode(self,mode):
        """switch mode
            @param mode: ['Camera', 'Back']
                    or ['Camera', 'Front']
                    or ['Video', 'Back']
                    or ['Video', 'Front']
                    or '' for one item
                    if mode[0] or mode[1] is '',thati means ignorent the item
        
        """         
        self._logger.debug('switch to %s mode', mode[1]+mode[0])
        
        mode_current = self.get_current_mode() 
        if mode[0] == '':
            mode[0] = mode_current[0]
        if mode[1] == '':
            mode[1] = mode_current[1]   
        if mode == mode_current:
            return True
        elif mode[0] <> mode_current[0]:
            self._logger.debug('switch camera/video')
            if self._device(resourceId='com.android.camera2:id/video_switch_icon').exists:
                self._device(resourceId='com.android.camera2:id/video_switch_icon').click()
                self._device.delay(5)
                if mode[1] <> mode_current[1]:
                    self._logger.debug('switch front/back')
                    if self._device(resourceId='com.android.camera2:id/onscreen_camera_picker').exists:
                        self._device(resourceId='com.android.camera2:id/onscreen_camera_picker').click()
                        self._device.delay(5)   
        elif mode[1] <> mode_current[1]:
            self._logger.debug('switch front/back')
            if self._device(resourceId='com.android.camera2:id/onscreen_camera_picker').exists:
                self._device(resourceId='com.android.camera2:id/onscreen_camera_picker').click()
                self._device.delay(5)
        
        if mode == self.get_current_mode():
            self._logger.debug("Switch to %s successfully.", mode[1]+mode[0])
            return True
        else:
            self._logger.debug("Can not switch to %s", mode[1]+mode[0])
            return False        

    def enter_preview(self, preview_type):
        """enter preview mode
            @param preview_type : 'Photo' or 'Video'
            
        """   
        self._logger.debug('Enter %s preview mode.', preview_type)
        
        swipe_try_times = 0
        while True:
            if  self._device(description  = 'Shutter').exists\
                and not self._device(resourceId = 'com.android.camera2:id/action_delete').exists:
                self._device(resourceId = 'com.android.camera2:id/camera_above_filmstrip_layout').swipe.left(steps=5)
                self._device.delay(4)
            
            if self._device(resourceId = 'com.android.camera2:id/filmstrip_bottom_controls').exists\
                and self._device(resourceId = 'com.android.camera2:id/action_delete').exists:
                    break
            else:
                swipe_try_times += 1
            
            if swipe_try_times > 5:
                self._logger.debug('Swipe to preview mode failed!.')
                return  False
            
        enter_full_preview_times = 0
        while True:
            if self._device(resourceId = 'com.android.camera2:id/filmstrip_view').exists\
                and self._device(resourceId = 'com.android.camera2:id/camera_app_root').exists:
#                 self._device(resourceId = 'com.android.camera2:id/filmstrip_view').click.bottomright()
                self._device.click(230, 460)
                self._device.delay(2)
                enter_full_preview_times += 1
            else:
                break
                
            if enter_full_preview_times > 5:
                self._logger.debug('Enter full preview mode failed!.')
                return  False
    
        
        find_times = 0
        while True:
            if self._device(resourceId = 'com.android.camera2:id/filmstrip_view').exists:
#                 self._device(resourceId = 'com.android.camera2:id/filmstrip_view').click().bottomright()
                self._device.click(230, 460)
                self._device.delay(1)
                if preview_type == 'Video':
                    if self._device(resourceId = 'com.android.camera2:id/filmstrip_view').child(className  = 'android.widget.FrameLayout').exists:
                        self._logger.debug('enter video preview mode successfuly!')
                        return True
                elif preview_type == 'Photo':
                    if self._device(resourceId = 'com.android.camera2:id/filmstrip_view').child(className  = 'android.widget.ImageView').exists\
                        and not self._device(resourceId = 'com.android.camera2:id/filmstrip_view').child(className  = 'android.widget.FrameLayout').exists:
                        self._logger.debug('enter photo preview mode successfuly!')
                        return True
                else:
                    self._logger.debug('Unknown preview_type!')
                    return False

                self._device(resourceId = 'com.android.camera2:id/filmstrip_view').swipe.left(steps=5)
                self._device.delay(1)
                self._logger.debug('Swipe one time.')
                find_times += 1
                if find_times > 5:
                    break
            else:
                break
            
        self._logger.debug('Enter %s preview mode failed!.', preview_type)
        return False
    
    def take_photo(self):
        """take  a photo 
        
        """         
        self._logger.debug('take photo')
        file_number = self.get_file_num(StorePath_Media, [".jpg"])
        if self._device(description='Shutter').exists:
            self._device(description='Shutter').click()
            self._device.delay(3)
        else:
            self._logger.warning("Get take photo button failed!")
            return  False
        if self.get_file_num(StorePath_Media, [".jpg"]) == file_number + 1:
            return True
        else:
            self._logger.warning("Take picture failed!")
            return False
        
    def record_video(self,recordTime):
        """record a video
        @param (int)recordTime --time of the video

        """ 
        self._logger.debug('record video')
        file_number = self.get_file_num(StorePath_Media, ['.3gp', '.mp4'])
        if self._device(description='Shutter').exists:
            self._device(description='Shutter').click()
            self._device.delay(recordTime)
            self._device(description='Shutter').click()
            self._device.delay(2)
        else:
            self._logger.warning("Get Recording video button failed!")
            return  False
        if self.get_file_num(StorePath_Media, ['.3gp', '.mp4'])== file_number + 1:
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
        if self._device(resourceId = 'com.android.camera2:id/filmstrip_view').child(className = 'android.widget.ImageView', instance = 1).exists:
            self._device(resourceId = 'com.android.camera2:id/filmstrip_view').child(className = 'android.widget.ImageView', instance = 1).click()
            self._device.delay(3)
            # choose player if needed 
            if  self._device(text='Open with').exists and self._device(resourceId ='android:id/text1', instance = 0).exists:
                self._device(resourceId ='android:id/text1', instance = 0).click()
                self._device.delay(1)
                if self._device(text='Always').exists:
                    self._device(text='Always').click()
#                 if self._device(text='Just once').exists:
#                     self._device(text='Just once').click()
                    self._device.delay(3)
            elif self._device(text='Use a different app').exists and self._device(text='Always').exists:
                self._device(text='Always').click()
#                 self._device(text='Just once').click()
                self._device.delay(3)
        if self._device(resourceId ='com.android.gallery3d:id/surface_view').exists\
            or self._device(resourceId ='com.google.android.apps.plus:id/videoplayer').exists:
            if self._device(resourceId = 'com.android.camera2:id/filmstrip_view').wait.exists(timeout=30000):
                self._device.press.back()
                self._device.delay(2)
                self._logger.debug('Finish play video.')
                return True
            else:
                self._logger.debug('Fail to finish play video.')
                return  False
        self._logger.debug('Fail to play video.')
        return  False
        
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
            if not self._device(description='Delete').exists:
                self._device.click(200,200)
                self._device.delay(1)
            if self._device(description='Delete').exists:
                self._device(description='Delete').click()
                self._device.delay(3)
                if self._device(resourceId = 'com.android.camera2:id/camera_deletion_button').wait.exists(timeout=10000):
                    break
            else:
                try_times += 1
            if try_times > 5:
                self._logger.warning("Didn't find Delete button!")
                return False
            
        if self._device(resourceId = 'com.android.camera2:id/camera_deletion_button').wait.exists(timeout=10000):
            self._device(resourceId = 'com.android.camera2:id/camera_deletion_button').click()
            self._device.delay(3)
            if not self._device(resourceId = 'com.android.camera2:id/camera_deletion_button').exists\
            and self.get_file_num(StorePath_Media, file_type) == file_number-1:
                self._logger.warning("Delete %s successfully!", preview_type)
                return True
        self._logger.warning("Delete %s failed!", preview_type)
        return False
        
    