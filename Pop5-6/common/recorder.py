"""Recorder library for scripts.
"""

from common import Common

RecordFilePath = '/sdcard/Recording/'

class Recorder(Common):   
     
    """Keep in Sound Recorder main page
    
    """
    def stay_in_recorder(self):
        self._logger.debug("1111")
        if self.get_current_packagename() == self.get_app_package_from_file('Sound Recorder'):
            maxtime = 0
            while not self._device(resourceId = 'com.tct.soundrecorder:id/fileListButton').exists:
                self._device.press.back()
                self._device.delay(1)
                maxtime += 1
                if maxtime > 3:
                    self._logger.debug("Can't back Sound Recorder")
                    break
            if maxtime < 4:
                return True

        self._device.press.home()
        self._logger.debug("Launch Sound Recorder.")
        if self.enter_app('Sound Recorder'):
            self._device.delay(2)
            if self.get_current_packagename() == self.get_app_package_from_file('Sound Recorder'):  
                maxtime = 0
                while not self._device(resourceId = 'com.tct.soundrecorder:id/fileListButton').exists:
                    self._device.press.back()
                    self._device.delay(1)
                    maxtime += 1
                    if maxtime > 3:
                        self._logger.debug("Can't back Sound Recorder")
                        break
                if maxtime < 4:
                    return True                 
            
            self._logger.debug('Launch Sound Recorder main page fail')
            return False
        else:
            return False 
        
    def record_audio(self, record_time = 5): 
        """record a audio.
        @param (int)record_time :recording time
        
        """
        self._logger.debug("Record audio %s seconds." % record_time)
        file_number = self.get_file_num(RecordFilePath, [".3gpp", ".m4a", ".amr"])
        if self._device(resourceId = 'com.tct.soundrecorder:id/recordButton').exists:
            self._device(resourceId='com.tct.soundrecorder:id/recordButton').click()
            self._device.delay(2)
            if self._device(resourceId = 'com.tct.soundrecorder:id/stopButton').exists:
                self._logger.debug("Recording...")
                self._device.delay(record_time)
                self._device(resourceId='com.tct.soundrecorder:id/stopButton').click()
                self._logger.debug("Stop recording audio")
                self._device.delay(3)
            if self._device(resourceId = 'com.tct.soundrecorder:id/recording_file_list_view').exists:
                self._logger.debug("Auto enter file list.")
                if self.get_file_num(RecordFilePath, [".3gpp", ".m4a", ".amr"]) == file_number+1:
                    self._logger.warning("Save audio successfully.")
                    return  True
                else:
                    self._logger.warning("Save audio failed!")
                    return False              
        else:
            self._logger.debug("Can't find the recording button.")
            return False
            
    def enter_file_list(self):
        """Enter file list.
        
        """
        self._logger.debug("Enter Audio List")
        if self._device(resourceId = 'com.tct.soundrecorder:id/fileListButton').exists:        
            self._device(resourceId = 'com.tct.soundrecorder:id/fileListButton').click()
            self._device.delay(2)
        if self._device(text = 'Recording file list'):
            self._logger.warning("Enter file list successfully")
            return True
        self._logger.warning("Cannot Enter file list")
        return False
        
    def select_audio_play(self, index, time = 0):
        """touch audio according to index.
        @param (int)index : file order in list

        """
        if self._device(resourceId = 'com.tct.soundrecorder:id/empty_view').exists:
            self._logger.debug("There is none recording file.")
            return False
        
        if self._device(resourceId = 'com.tct.soundrecorder:id/recording_file_list_view').exists:
            record_file_num = self._device(resourceId = 'com.tct.soundrecorder:id/recording_file_list_view').getChildCount()
            if record_file_num > 10 :
                record_file_num = 10
            if self._device(resourceId = 'com.tct.soundrecorder:id/record_file_item',  instance = index % record_file_num).exists:
                self._device(resourceId = 'com.tct.soundrecorder:id/record_file_item',  instance = index % record_file_num).click()
                self._device.delay(1)
                if self._device(resourceId = 'com.tct.soundrecorder:id/stateProgressBar').exists:
                    self._logger.debug("Start Playing...")
                    if time == 0:
                        self._device(resourceId = 'com.tct.soundrecorder:id/stateProgressBar').wait.gone(timeout=300000)
                    else:
                        self._device.delay(time)
                    if self._device(resourceId = 'com.tct.soundrecorder:id/stopButton').exists:
                        self._logger.debug("Stop Playing by click stop button")
                        self._device(resourceId = 'com.tct.soundrecorder:id/stopButton').click()
                        self._device.delay(2)
                    if self._device(resourceId = 'com.tct.soundrecorder:id/recordButton').exists:
                        self._logger.debug('Finish playing.')
                        return True
                    else:
                        self._logger.debug('Stop playing fail.')
                        return False     
                else:
                    self._logger.debug("Start playing fail.")
                    return False
            else:
                self._logger.debug("Can't get the recording item.")
                return False
        else:
            self._logger.debug("Recording file list isn't exist.")
            return False
            
    def delete_audio(self, index=0):
        """delete a audio
        @param (int)index :  file order in list. Default is 0.
        
        """
        self._logger.debug("Delete Audio.")
        
        if self._device(resourceId = 'com.tct.soundrecorder:id/empty_view').exists:
            self._logger.debug("There is none recording file.")
            return False
        
        if not self._device(resourceId = 'com.tct.soundrecorder:id/recording_file_list_view').exists:
            self._logger.debug("Recording file list isn't exist.")
            return False
        
        file_number = self.get_file_num(RecordFilePath, [".3gpp", ".m4a", ".amr"])
        
        # delete video from more options
        if self._device(description  = 'More options').exists:
            self._device(description  = 'More options').click()
            self._device.delay(2)
            if self._device(text = 'Delete').exists:
                self._device(text = 'Delete').click()
                self._device.delay(2)
                if self._device(resourceId  = 'com.tct.soundrecorder:id/record_file_checkbox',  instance = index).exists:
                    if not self._device(resourceId  = 'com.tct.soundrecorder:id/record_file_checkbox',  instance = index).isChecked():
                        self._device(resourceId  = 'com.tct.soundrecorder:id/record_file_checkbox',  instance = index).click()
                        self._device.delay(2)
                        if self._device(resourceId  = 'com.tct.soundrecorder:id/deleteButton').exists:
                            self._device(resourceId  = 'com.tct.soundrecorder:id/deleteButton').click()
                            self._device.delay(2)
                            if self._device(text = 'OK').exists:
                                self._device(text = 'OK').click()
                                self._device.delay(2)
#         #delete video from long click items #useless!!!
#         try_long_click_time = 0
#         while True:
#             if self._device(resourceId = 'com.tct.soundrecorder:id/record_file_item',  instance = index).exists:
#                 self._logger.debug("----------------.")
#                 self._device(resourceId = 'com.tct.soundrecorder:id/record_file_item',  instance = index).long_click()
#                 self._logger.debug("Long click firt recording one time.")
#                 self._device.delay(2)
#                 if self._device(resourceId = 'com.tct.soundrecorder:id/deleteMenu').exists:
#                     break
#                 else:
#                     try_long_click_time += 1
#             else:
#                 self._logger.debug("Can't get the recording item.")
#                 return False
#             
#             if try_long_click_time >5:
#                 self._logger.debug("Can't get the delete menu.")
#                 return False
#             
#         self._device(resourceId = 'com.tct.soundrecorder:id/deleteMenu').click()
#         self._device.delay(2)
#         if self._device(text = 'OK').exists:
#             self._device(text = 'OK').click()
#             self._device.delay(2)
        if self.get_file_num(RecordFilePath, [".3gpp", ".m4a", ".amr"]) == file_number - 1:
            self._logger.debug("Delete audio successfully.")
            return True
        else:
            self._logger.debug("Delete audio fail.")
            return False         

            
