"""Recorder library for scripts.
"""

from common import Common

RecordFilePath = '/sdcard/Recording/'

class Recorder(Common):   
     
    """Keep in Sound Recorder main page
    
    """
    def stay_in_recorder(self):
        if self.get_current_packagename() == self.get_app_package_from_file('Sound Recorder'):
            maxtime = 0
            while not self._device(resourceId = 'com.android.soundrecorder:id/uvMeter').exists:
                if self._device(resourceId = 'com.android.soundrecorder:id/discardButton').exists:
                    self._device(resourceId = 'com.android.soundrecorder:id/discardButton').click()
                    self._device.delay(2)
                elif self._device(resourceId = 'com.android.soundrecorder:id/stopButton').exists:
                    self._device(resourceId = 'com.android.soundrecorder:id/stopButton').click()
                    self._device.delay(2)
                elif self._device(resourceId = 'com.android.soundrecorder:id/fileListButton').exists:
                    self._device(resourceId = 'com.android.soundrecorder:id/fileListButton').click()
                    self._device.delay(2)
                else:
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
                while not self._device(resourceId = 'com.android.soundrecorder:id/uvMeter').exists:
                    if self._device(resourceId = 'com.android.soundrecorder:id/discardButton').exists:
                        self._device(resourceId = 'com.android.soundrecorder:id/discardButton').click()
                        self._device.delay(2)
                    elif self._device(resourceId = 'com.android.soundrecorder:id/stopButton').exists:
                        self._device(resourceId = 'com.android.soundrecorder:id/stopButton').click()
                        self._device.delay(2)
                    elif self._device(resourceId = 'com.android.soundrecorder:id/fileListButton').exists:
                        self._device(resourceId = 'com.android.soundrecorder:id/fileListButton').click()
                        self._device.delay(2)
                    else:
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
        if self._device(resourceId = 'com.android.soundrecorder:id/recordButton').exists:
            self._device(resourceId='com.android.soundrecorder:id/recordButton').click()
            self._device.delay(2)
            if self._device(resourceId = 'com.android.soundrecorder:id/pauseRecordingButton').exists\
                and self._device(resourceId = 'com.android.soundrecorder:id/stopButton').exists:
                self._logger.debug("Recording...")
                self._device.delay(record_time)
                self._device(resourceId = 'com.android.soundrecorder:id/stopButton').click()
                self._logger.debug("Stop recording audio")
                self._device.delay(3)
            if self._device(resourceId = 'com.android.soundrecorder:id/acceptButton', text = 'Save').exists:
                self._device(resourceId = 'com.android.soundrecorder:id/acceptButton', text = 'Save').click()
                self._device.delay(2)
            if self._device(resourceId = 'com.android.soundrecorder:id/fileListButton').exists:
                self._logger.debug("Auto enter file list.")
                if self.get_file_num(RecordFilePath, [".3gpp", ".m4a", ".amr"]) == file_number+1:
                    self._logger.warning("Save audio successfully.")
                    return  True
            self._logger.warning("Save audio failed!")
            return False              
        else:
            self._logger.debug("Can't find the recording button.")
            return False
            
    def enter_file_list(self):
        """Enter file list.
        
        """
        self._logger.debug("Enter Audio List")
        if self._device(resourceId = 'com.android.soundrecorder:id/fileListButton').exists:
            self._device(resourceId = 'com.android.soundrecorder:id/fileListButton').click()
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
        if not self._device(resourceId = 'com.android.soundrecorder:id/record_file_name').exists \
            or self._device(resourceId = 'com.android.soundrecorder:id/empty_view').exists:
            self._logger.debug("There is none recording file.")
            return False
        if not self._device(resourceId = 'com.android.soundrecorder:id/recording_file_list_view').exists:
            self._logger.debug("Can't get the file list.")
            return False
        record_file_num = self._device(resourceId = 'com.android.soundrecorder:id/recording_file_list_view').getChildCount()
        if record_file_num > 10 :
            record_file_num = 10
        if self._device(resourceId = 'com.android.soundrecorder:id/record_file_name',  instance = index % record_file_num).exists:
            self._device(resourceId = 'com.android.soundrecorder:id/record_file_name',  instance = index % record_file_num).click()
            self._device.delay(2)
#             self._device.screenshot(sys.path[0]+"\\PicComparison\\recorder.png")
#             self._device.dump(sys.path[0]+"\\PicComparison\\recorder.uix")
            if self._device(resourceId = 'com.android.soundrecorder:id/stateProgressBar').exists:
                self._logger.debug("Start Playing...")
                if time == 0:
                    self._device(resourceId = 'com.android.soundrecorder:id/stateProgressBar').wait.gone(timeout=300000)
                else:
                    self._device.delay(time)
                if self._device(resourceId = 'com.android.soundrecorder:id/stateProgressBar').exists:
                    self._logger.debug("Stop Playing by press stop icon")
                    self._device(resourceId = 'com.android.soundrecorder:id/stopButton').click()
                    self._device.delay(2)
                if not self._device(resourceId = 'com.android.soundrecorder:id/stateProgressBar').exists:
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

            
    def delete_audio(self, index=0):
        """delete a audio
        @param (int)index :  file order in list. Default is 0.
        
        """
        self._logger.debug("Delete Audio.")


        if not self._device(resourceId = 'com.android.soundrecorder:id/record_file_name').exists \
            or self._device(resourceId = 'com.android.soundrecorder:id/empty_view').exists:
            self._logger.debug("There is none recording file.")
            return False
        
        file_number = self.get_file_num(RecordFilePath, [".3gpp", ".m4a", ".amr"])

        self._device(resourceId  = 'com.android.soundrecorder:id/record_file_name',  instance = 0).long_click()
        self._device.delay(2)
        if self._device(resourceId = 'com.android.soundrecorder:id/deleteButton').exists:
            self._device(resourceId = 'com.android.soundrecorder:id/deleteButton').click()
            self._device.delay(2)
            if self._device(text = 'OK').exists:
                self._device(text = 'OK').click()
                self._device.delay(2)
        if self.get_file_num(RecordFilePath, [".3gpp", ".m4a", ".amr"]) == file_number - 1:
            self._logger.debug("Delete audio successfully.")
            return True
        else:
            self._logger.debug("Delete audio fail.")
            return False         

            
