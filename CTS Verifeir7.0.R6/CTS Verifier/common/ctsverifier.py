# -*- coding: UTF-8 -*-
from __builtin__ import True
from pickle import TRUE
import re
from sqlite3.test.userfunctions import func_returntext
import string
import sys

from cv2 import FAST_FEATURE_DETECTOR_TYPE_5_8

from common import Common
from _ast import If
from xml.dom import WRONG_DOCUMENT_ERR


#from __main__ import name 
# from __main__ import name
class Ctsverifier(Common):
    def __init__(self, device, log_name):
        Common.__init__(self, device,log_name)
    def scroll_find_file(self,name):
        scroll_time = 0
        while True:
            if self._device(resourceId = 'android:id/text1',text = name).exists:
                return True
            else:
                self._device(resourceId= 'android:id/list').scroll.vert.forward(steps=100)
                self._logger.debug("Scroll one time.")
                scroll_time += 1
            if scroll_time > 20:
                self._logger.debug("Don't get the option") 
                return False 
    """
            将公共条件写入 common——func        
    """
    def common_fuc(self,name):
           
        if self.enter_app('CTS Verifier'):
            self._device.delay(1) 
        if self._device(resourceId = 'android:id/text1',text = name).exists:
            self._device(resourceId = 'android:id/text1',text = name).click()
            self._device.delay(1)
        elif self.scroll_find_file(name):
            self._logger.debug('Scroll the page to %s',name)
            self._device(resourceId = 'android:id/text1',text = name).click()
        if self._device(resourceId = 'android:id/button1',text = 'OK').exists:
            self._device(resourceId = 'android:id/button1',text = 'OK').click()
            self._device.delay(2)
            return True
    def Initial(self):
        while self._device(resourceId='com.android.packageinstaller:id/permission_message').wait.exists(timeout=2000):
            self._device(resourceId='com.android.packageinstaller:id/permission_allow_button').click()
            self._device.delay(2)
        self._logger.debug('ALLOW click finished')
        return True
    
    def Always_Wake(self):  #待修改
        
        """
        Enter Settings and set a screen lock
        """
        self._device.press.home() 
        if self.enter_app('Settings'):
            if self._device(resourceId = 'android:id/title',text='Security').exists:
                self._device(resourceId = 'android:id/title',text='Security').click()
                self._device.delay(2)
                self._logger.debug("enter Security setting")
            else:
                self._device(scrollable=True).scroll.vert.forward(steps=10)
                self._logger.debug("enter Security setting")
                self._device(resourceId = 'android:id/title',text='Security').click()
                self._device.delay(2)
        if self._device(resourceId = 'android:id/title',text='Screen lock').exists:
            self._device(resourceId = 'android:id/title',text='Screen lock').click()
            self._device.delay(2)
            if self._device(resourceId = 'android:id/title',text = 'None').exists:
                self._device(resourceId = 'android:id/title',text = 'None').click()
                self._device.delay(2)
                self._logger.debug("scrren lock is none")
#                 if self._device(resourceId = 'android:id/title',text = 'Require PIN to start device').exists:
#                     self._device(resourceId = 'android:id/title',text = 'Require PIN to start device').click()
#                     self._device.delay(2)
                if self._device(resourceId = 'android:id/button1',text = 'OK').exists:
                    self._device(resourceId = 'android:id/button1',text = 'OK').click()
                    self._device.delay(2)
                else:
                    self._device.press.home()    
                
    def Audio_Frequency_Line_Test(self,name):
        self.common_fuc(name)
        if self._device(className = 'android.widget.Button',resourceId = 'com.android.cts.verifier:id/audio_general_headset_yes',text = 'YES').exists:
            self._device(className = 'android.widget.Button',resourceId = 'com.android.cts.verifier:id/audio_general_headset_yes',text = 'YES').click()
            self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/audio_frequency_line_plug_ready_btn',text = 'LOOPBACK PLUG READY').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/audio_frequency_line_plug_ready_btn',text = 'LOOPBACK PLUG READY').click()
            self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/audio_frequency_line_test_btn',text = 'TEST').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/audio_frequency_line_test_btn',text = 'TEST').click()
            self._device.delay(5) 
#             self._device(scrollable=True).scroll.toEnd()
            self._device(scrollable=True).fling.toEnd()  
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
            self._device.delay(3)
            self._logger.debug('Audio Frequency Line Test successfully')
            return True
        else:
            self._logger.debug('Audio Frequency Line Test fail')
            return False
        
    def Audio_Input_Devices_Notifications_Test(self,name):
        self.common_fuc(name)
        if self._device(className = 'android.widget.Button',resourceId = 'com.android.cts.verifier:id/audio_general_headset_yes',text = 'YES').exists:
            self._device(className = 'android.widget.Button',resourceId = 'com.android.cts.verifier:id/audio_general_headset_yes',text = 'YES').click()
            self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/audio_dev_notification_connect_clearmsgs_btn',text = 'CLEAR MESSAGES').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/audio_dev_notification_connect_clearmsgs_btn',text = 'CLEAR MESSAGES').click()
            self._device.delay(2)
#             if self._device(resourceId = 'com.android.cts.verifier:id/audio_frequency_line_test_btn',text = 'TEST').isEnabled:
#                 self._device(resourceId = 'com.android.cts.verifier:id/audio_frequency_line_test_btn',text = 'TEST').click()
#                 self._device.delay(5) 
#         #             self._device(scrollable=True).scroll.toEnd()
#                 self._device(scrollable=True).fling.toEnd()  
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
            self._device.delay(3)
            self._logger.debug('Audio Input Devices Notifications Test pass')
            return True
        else:
            self._logger.debug('Audio Input Devices Notifications Test fail')
            return False

    def Audio_Input_Routing_Notifications_Test(self,name):
        self.common_fuc(name)
        if self._device(className = 'android.widget.Button',resourceId = 'com.android.cts.verifier:id/audio_general_headset_yes',text = 'YES').exists:
            self._device(className = 'android.widget.Button',resourceId = 'com.android.cts.verifier:id/audio_general_headset_yes',text = 'YES').click()
            self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/audio_routingnotification_recordBtn',text = 'RECORD').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/audio_routingnotification_recordBtn',text = 'RECORD').click()
            self._device.delay(4)
            if self._device(resourceId = 'com.android.cts.verifier:id/audio_routingnotification_recordStopBtn',text = 'STOP').isEnabled:
                self._device(resourceId = 'com.android.cts.verifier:id/audio_routingnotification_recordStopBtn',text = 'STOP').click()
                self._device.delay(5) 
    #               self._device(scrollable=True).scroll.toEnd()
    #               self._device(scrollable=True).fling.toEnd()  
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
            self._device.delay(3)
            self._logger.debug('Audio Input Routing Notifications Test pass')
            return True
        else:
            self._logger.debug('Audio Input Routing Notifications Test fail')
            return False
    
    def Audio_Output_Devices_Notifications_Test(self,name):
        self.common_fuc(name)
        if self._device(className = 'android.widget.Button',resourceId = 'com.android.cts.verifier:id/audio_general_headset_yes',text = 'YES').exists:
            self._device(className = 'android.widget.Button',resourceId = 'com.android.cts.verifier:id/audio_general_headset_yes',text = 'YES').click()
            self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/audio_dev_notification_connect_clearmsgs_btn',text = 'CLEAR MESSAGES').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/audio_dev_notification_connect_clearmsgs_btn',text = 'CLEAR MESSAGES').click()
            self._device.delay(2)
    #             if self._device(resourceId = 'com.android.cts.verifier:id/audio_frequency_line_test_btn',text = 'TEST').isEnabled:
    #                 self._device(resourceId = 'com.android.cts.verifier:id/audio_frequency_line_test_btn',text = 'TEST').click()
    #                 self._device.delay(5) 
    #         #             self._device(scrollable=True).scroll.toEnd()
    #                 self._device(scrollable=True).fling.toEnd()  
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
            self._device.delay(3)
            self._logger.debug('Audio Input Devices Notifications Test pass')
            return True
        else:
            self._logger.debug('Audio Input Devices Notifications Test fail')
            return False
     
    def Audio_Output_Routing_Notifications_Test(self,name):
        self.common_fuc(name)
        if self._device(className = 'android.widget.Button',resourceId = 'com.android.cts.verifier:id/audio_general_headset_yes',text = 'YES').exists:
            self._device(className = 'android.widget.Button',resourceId = 'com.android.cts.verifier:id/audio_general_headset_yes',text = 'YES').click()
            self._device.delay(2)
            self._logger.debug('go to play')
        if self._device(resourceId = 'com.android.cts.verifier:id/audio_routingnotification_playBtn',text = 'PLAY').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/audio_routingnotification_playBtn',text = 'PLAY').click()
            self._device.delay(2)
            if self._device(resourceId = 'com.android.cts.verifier:id/audio_routingnotification_playStopBtn',text = 'STOP').isEnabled:
                self._device(resourceId = 'com.android.cts.verifier:id/audio_routingnotification_playStopBtn',text = 'STOP').click()
                self._device.delay(2) 
    #               self._device(scrollable=True).scroll.toEnd()
    #               self._device(scrollable=True).fling.toEnd()  
        if self._device(resourceId='com.android.cts.verifier:id/pass_button').isEnabled:
            self._device(resourceId='com.android.cts.verifier:id/pass_button').click()
            self._device.delay(3)
            self._logger.debug('Audio Input Routing Notifications Test pass')
            return True
        else:
            self._logger.debug('Audio Input Routing Notifications Test fail')
            return False
     
    def Hifi_Ultrasound_Speaker_Test(self,name):
        self.common_fuc(name)
        if self._device(className = 'android.widget.Button',resourceId = 'com.android.cts.verifier:id/player_button',text = 'PLAY').exists:
            self._device(className = 'android.widget.Button',resourceId = 'com.android.cts.verifier:id/player_button',text = 'PLAY').click()
            self._device.delay(5)
            self._device.click(360,676)
#         if self._device(resourceId = 'com.android.cts.verifier:id/audio_routingnotification_playBtn',text = 'PLAY').isEnabled:
#             self._device(resourceId = 'com.android.cts.verifier:id/audio_routingnotification_playBtn',text = 'PLAY').click()
#             self._device.delay(4)
#             if self._device(resourceId = 'com.android.cts.verifier:id/audio_routingnotification_recordStopBtn',text = 'STOP').isEnabled:
#                 self._device(resourceId = 'com.android.cts.verifier:id/audio_routingnotification_recordStopBtn',text = 'STOP').click()
#                 self._device.delay(5) 
    #               self._device(scrollable=True).scroll.toEnd()
    #               self._device(scrollable=True).fling.toEnd()  
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
            self._device.delay(3)
            self._logger.debug('Audio Input Routing Notifications Test pass')
            return True
        else:
            self._logger.debug('Audio Input Routing Notifications Test fail')
            return False   
               
    def Car_Dock_Test(self,name):
        self.common_fuc(name)
        self.Always_Wake()
        if self._device(resourceId = 'com.android.cts.verifier:id/car_mode',text = 'ENABLE CAR MODE').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/car_mode',text = 'ENABLE CAR MODE').click()
            self._device.delay(2)
            while self._device(textContains = 'Complete action using').exists:
                self._device(text = 'CTS Verifier').click()
                self._device(text = 'ALWAYS').click()
                self._device.delay(2)
        if self._device(text = 'Press the Home button').exists:
            self._device.press.home()
            self._device.delay(2)
            self._logger.debug('Car_Dock_Test Successfully')
            return True
        else:
            self._logger.debug('Car_Dock_Test Fail')
            return False
        
    def Camera_FOV_Calibration(self,name):
        self.common_fuc(name)
        self._device.delay(2)
        click_time = 0
#         if self._device(resourceId = 'android:id/text1',text = 'Camera FOV Calibration').exists:
#             self._logger.debug('Camera FOV Calibration test successfully7') 
#             self._device(resourceId = 'android:id/text1',text = 'Camera FOV Calibration').click()
#             self._logger.debug('enter Camera') 
#             self._device.delay(2)
        while self._device(resourceId = 'com.android.cts.verifier:id/camera_fov_tap_to_take_photo' ,text='Tap to calibrate').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/camera_fov_tap_to_take_photo' ,text='Tap to calibrate').click()
            self._device.delay(2)
            self._device(resourceId = 'com.android.cts.verifier:id/camera_fov_fov_done',text = 'Done').click()
            self._device.delay(2)
            click_time += 1
            self._logger.debug('click time is %s',click_time)
        self._logger.debug('Camera FOV Calibration test successfully') 
        return True 
#         self._logger.debug('Camera FOV Calibration test successfully') 
#         return False  

    def Camera_Flashlight(self,name):
        self.common_fuc(name)
        self._logger.debug('what is WRONG')
        self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/flash_instruction_button',text = 'START').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/flash_instruction_button',text = 'START').click()
            self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/flash_on_button').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/flash_on_button').click()
            self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/flash_instruction_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/flash_instruction_button',text = 'NEXT').click()
            self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/flash_off_button').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/flash_off_button').click()
            self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/flash_instruction_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/flash_instruction_button',text = 'NEXT').click()
            self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/flash_on_button').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/flash_on_button').click()
            self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/flash_instruction_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/flash_instruction_button',text = 'NEXT').click()
            self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/flash_off_button').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/flash_off_button').click()
            self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/flash_instruction_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/flash_instruction_button',text = 'NEXT').click()
            self._device.delay(2)
#         if self._device(resourceId = 'com.android.cts.verifier:id/flash_instruction_button',text = 'DONE').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/flash_instruction_button',text = 'DONE').click()
#             self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
            self._device.delay(3)
            self._logger.debug('Camera Flashlight Test pass')
            return True
        else:
            self._logger.debug('Camera Flashlight Test fail')
            return False   
        
    def Camera_Formats(self, name):
        self.common_fuc(name)
        Camera_name={0:'Camera 0', 1:'Camera 1'}
        
        Camera0={0:'176 x 144',1:'320 x 240',2:'352 x 288',3:'480 x 320',4:'480 x 368',5:'640 x 480',6:'720 x 480',7:'720 x 720',8:'800 x 480',9:'800 x 600',10:'864 x 480',11:'960 x 540',12:'1280 x 720'}
        Camera1 = {0:'176 x 144',1:'320 x 240',2:'352 x 288',3:'480 x 320',4:'480 x 368',5:'640 x 480',6:'720 x 480',7:'720 x 720',8:'800 x 480',9:'800 x 600',10:'864 x 480',11:'960 x 540',12:'1280 x 720'}
        Camera={0:Camera0,1:Camera1}
        switch_times=0
            
        for i in xrange(2):
            if self._device(resourceId = 'com.android.cts.verifier:id/cameras_selection').wait.exists(timeout=5000):
                self._device(resourceId = 'com.android.cts.verifier:id/cameras_selection').click()
                self._device.delay(2)
                self._logger.debug('Select camera to %s',Camera_name[i])
                self._device(className='android.widget.ListView').child(text=Camera_name[i]).click()
                #？？？？？？？？？android.widget.ListView
                for j in xrange(len(Camera[i])):
                    switch_times+=1
                    if self._device(resourceId='com.android.cts.verifier:id/cameras_selection').child(text=Camera_name[i]).wait.exists(timeout=5000):
                        self._logger.debug('Select Resolution')
                        if self._device(resourceId = 'com.android.cts.verifier:id/resolution_selection').wait.exists(timeout=5000):
                            self._device(resourceId = 'com.android.cts.verifier:id/resolution_selection').click()
                            if self._device(text=Camera[i][j]).wait.exists(timeout=5000):
                                self._logger.debug('Select Resolution to %s',Camera[i][j])
                                self._device(text=Camera[i][j]).click()
                                self._device.delay(2) 
                                if self._device(resourceId = 'com.android.cts.verifier:id/format_selection').child(text='NV21').wait.exists(timeout=5000):
                                    self._logger.debug('Switch format to YV12')
                                    self._device(resourceId = 'com.android.cts.verifier:id/format_selection').click()
                                    self._device.delay(2)
                                    if self._device(text='YV12').wait.exists(timeout=5000):
                                        self._device(text='YV12').click()
                                        self._device.delay(2)
                                elif self._device(resourceId = 'com.android.cts.verifier:id/format_selection').child(text='YV12').wait.exists(timeout=5000):
                                    self._logger.debug('Switch format to NV21')
                                    self._device(resourceId = 'com.android.cts.verifier:id/format_selection').click()
                                    self._device.delay(2)
                                    if self._device(text='NV21').wait.exists(timeout=5000):
                                        self._device(text='NV21').click()
                                        self._device.delay(2)
                                else:
                                    self._logger.debug('Can not find the format')
                                    return False
                            else:
                                self._logger.debug('Can not find the %s',Camera[i][j])
                                return False
                        else:
                            self._logger.debug('Can not find the selection')
                            return False
        if switch_times == len(Camera[0])+len(Camera[1]):
            self._logger.debug('switch camera format sucesse')
            if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled():
                self._logger.debug('Camera Foramt test Pass')
                self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                self._device.delay(2)
                return True
            elif self._device(resourceId = 'com.android.cts.verifier:id/fail_button').isEnabled():
                self._logger.debug('Camera Foramt test fail')
                self._device(resourceId = 'com.android.cts.verifier:id/fail_button').click()
                self._device.delay(2)
                return False
    
    def Camera_ITS_Test(self,name):
        self.common_fuc(name)
        self._logger.debug('Camera ITS Test')
#         if self.enter_app('CTS Verifier'):
#             self._device.delay(2)
        if self._device(resourceId = 'android:id/text1',text = 'Camera ITS Test').exists:
            self._device(resourceId = 'android:id/text1',text = 'Camera ITS Test').click()
            self._device.delay(2) 
            self._logger.debug('Camera ITS Test Successfully')
            return True
        else:
            self._logger.debug('Camera ITS Test Successfully')
            return False
        
            
    def Camera_Intents(self,name):
        self.common_fuc(name)
        self._logger.debug('Enter the Camera Intents')
        """
        begin to test taking photo
        """
        if self._device(resourceId = 'com.android.cts.verifier:id/start_test_button',text = 'START TEST').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/start_test_button',text = 'START TEST').click()
            self._device.delay(2)
            self._logger.debug('Enter the Camera Intents11111111111')
            self._device.press.home()
            self.enter_app('Camera')
            self.Initial()
            if self._device(resourceId = 'com.tct.tablet.camera:id/mode_item_name',text ='PHOTO').exists:
                self._device(resourceId = 'com.tct.tablet.camera:id/mode_item_name',text ='PHOTO').click() 
                self._device.delay(2)
                if self._device(resourceId = 'com.tct.tablet.camera:id/shutter_button').exists:
                    self._device(resourceId = 'com.tct.tablet.camera:id/shutter_button').click()
                    self._device.delay(5)  
                self._device.press.home()
                self.enter_app('CTS Verifier')
                self._logger.debug('Enter Cts Verifier again successfully')

            if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                self._device.delay(2)
                self._logger.debug('taking photo successfully')
                
            else:
                self._logger.debug('Camera_Intents test fail')
                return False
            """
            begin to test taking video
            """
        if self._device(resourceId = 'com.android.cts.verifier:id/start_test_button',text = 'START TEST').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/start_test_button',text = 'START TEST').click()
            self._device.delay(2)
            self._device.press.home()
            self.enter_app('Camera')
            if self._device(resourceId = 'com.tct.tablet.camera:id/mode_item_name',text ='VIDEO').exists:
                self._device(resourceId = 'com.tct.tablet.camera:id/mode_item_name',text ='VIDEO').click()
                self._device.delay(3)  
                if self._device(resourceId = 'com.tct.tablet.camera:id/shutter_button').exists:
                    self._device(resourceId = 'com.tct.tablet.camera:id/shutter_button').click() 
                    self._device.delay(10)
                    if self._device(resourceId = 'com.tct.tablet.camera:id/shutter_button').exists:
                        self._device(resourceId = 'com.tct.tablet.camera:id/shutter_button').click()
                        self._device.delay(2)
                self._device.press.home()
                self.enter_app('CTS Verifier')
                self._logger.debug('Enter Cts Verifier again successfully')
            if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                self._device.delay(2)
                self._logger.debug('taking video successfully')
            else:
                self._logger.debug('taking video fail')
                
            """
            begin to test Capture photo 
            """
        if self._device(resourceId = 'com.android.cts.verifier:id/start_test_button',text = 'START TEST').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/start_test_button',text = 'START TEST').click()
            self._device.delay(2)
            if self._device(resourceId = 'com.tct.tablet.camera:id/shutter_button').exists:
                self._device(resourceId = 'com.tct.tablet.camera:id/shutter_button').click()
                self._logger.debug('click the shutter button')
                self._device.delay(5)
                if self._device(resourceId = 'com.tct.tablet.camera:id/button_done').exists:
                    self._device(resourceId = 'com.tct.tablet.camera:id/button_done').click()
                    self._device.delay(2)
                    if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                        self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                        self._device.delay(2)
                    else:
                        self._logger.debug('taking photo fail')
        self._logger.debug('capture photo  successfully') 
        """
        begin to test Capture video
        
        """         
        if self._device(resourceId = 'com.android.cts.verifier:id/start_test_button',text = 'START TEST').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/start_test_button',text = 'START TEST').click()
            self._device.delay(2)
            if self._device(resourceId = 'com.tct.tablet.camera:id/shutter_button').exists:
                self._device(resourceId = 'com.tct.tablet.camera:id/shutter_button').click()
                self._device.delay(10)
                if self._device(resourceId = 'com.tct.tablet.camera:id/shutter_button').exists:
                    self._device(resourceId = 'com.tct.tablet.camera:id/shutter_button').click()
                    self._device.delay(2)
                    if self._device(resourceId = 'com.tct.tablet.camera:id/button_done').exists:
                        self._device(resourceId = 'com.tct.tablet.camera:id/button_done').click()
                        self._device.delay(2)
                        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                                self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                                self._device.delay(2)
                        else:
                            self._logger.debug('taking photo fail')
        self._logger.debug('capture Video successfully')                   
        return True                
#                     if self._device(resourceId = 'com.tct.tablet.camera:id/button_done').exists:
#                         self._device(resourceId = 'com.tct.tablet.camera:id/button_done').click()
#                         self._device.delay(2)
#                 if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
#                     self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
#                     self._device.delay(2)
#         self._logger.debug('capture photo and video successfully')
#   return True
    def Camera_Orientation(self,name):
        self.common_fuc(name)
        orientation_time = 0
        while self._device(resourceId = 'com.android.cts.verifier:id/take_picture_button',text = 'TAKE PHOTO').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/take_picture_button',text = 'TAKE PHOTO').click()
            self._device.delay(2)
            if self._device(resourceId = 'com.android.cts.verifier:id/format_view').exists:
                self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                orientation_time += 1
                self._logger.debug('Orientation take photo %d times',orientation_time)

            else:
                self._logger.debug('Camera Orientation Test fail')
                return False 
        self._logger.debug('Camera Orientation Test Scuccessfully')
        return True 
    def Camera_Video(self,name):
        self.common_fuc(name)
        Camera_name={0:'Camera 0',1:'Camera 1'}
        
        Camera0 = {0:'LOW',1:'HIGH',2:'QCIF',3:'QVGA',4:'CIF',5:'480P',6:'720P'}
        Camera1 = {0:'LOW',1:'HIGH',2:'QCIF',3:'QVGA',4:'CIF',5:'480P',6:'720P'}
        Camera={0:Camera0,1:Camera1}
        switch_times=0
        
        if self._device(resourceId = 'android:id/text1',text = 'Camera Formats').exists:
            self._device(resourceId = 'android:id/text1',text = 'Camera Formats').click()
            self._device.delay(2)
        if self._device(text='OK').exists:
            self._device(text='OK').click()
            self._device.delay(2)
            
        for i in xrange(2):
           
            if self._device(resourceId = 'com.android.cts.verifier:id/cameras_selection').wait.exists(timeout=5000):
                self._device(resourceId = 'com.android.cts.verifier:id/cameras_selection').click()
                self._device.delay(2)
                self._logger.debug('Select camera to %s',Camera_name[i])
                self._device(className='android.widget.ListView').child(text=Camera_name[i]).click()
                for j in xrange(len(Camera[i])):
                    switch_times+=1
                    if self._device(resourceId='com.android.cts.verifier:id/cameras_selection').child(text=Camera_name[i]).wait.exists(timeout=5000):
#                         self._logger.debug('Select Resolution')
                        if self._device(resourceId = 'com.android.cts.verifier:id/resolution_selection').wait.exists(timeout=5000):
                            self._device(resourceId = 'com.android.cts.verifier:id/resolution_selection').click()
                            if self._device(text=Camera[i][j]).wait.exists(timeout=5000):
                                self._logger.debug('Select Resolution to %s',Camera[i][j])
                                self._device(text=Camera[i][j]).click()
                                self._device.delay(2) 
                                if self._device(resourceId='com.android.cts.verifier:id/record_button',text='TEST').isEnabled:
                                    self._device(resourceId='com.android.cts.verifier:id/record_button',text='TEST').click()
                                    self._device.delay(2)
                                    if self._device(resourceId='com.android.cts.verifier:id/status_label',text='Playing back').wait.exists(timeout=5000):
#                                         self._logger.debug('Playing back with %s',Camera[i][j])
                                        if self._device(resourceId='com.android.cts.verifier:id/status_label',text='Ready').wait.exists(timeout=5000):
                                            self._logger.debug('%s %s test is completed',Camera_name[i],Camera[i][j])
                            else:
                                self._logger.debug('Can not find the %s',Camera[i][j])
                                return False
                        else:
                            self._logger.debug('Can not find the selection')
                            return False
        if switch_times == len(Camera[0])+len(Camera[1]):
            self._logger.debug('switch camera format sucesse')
            if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled():
                self._logger.debug('Camera Foramt test Pass')
                self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                self._device.delay(2)
                return True
            elif self._device(resourceId = 'com.android.cts.verifier:id/fail_button').isEnabled():
                self._logger.debug('Camera Foramt test fail')
                self._device(resourceId = 'com.android.cts.verifier:id/fail_button').click()
                self._device.delay(2)
                return False
    def Alarms_And_Timers_Tests(self,name):
        self.common_fuc(name)
        self._logger.debug('Enter Alarms and Timers Tests')
        """
        Test Show Alarms Test
        """ 
        if self._device(resourceId = 'android:id/text1',text = 'Show Alarms Test').exists:
            self._device(resourceId = 'android:id/text1',text = 'Show Alarms Test').click()
            self._device.delay(2)
            if self._device(className = 'android.widget.Button',text = 'SHOW ALARMS').exists:
                self._device(className = 'android.widget.Button',text = 'SHOW ALARMS').click()
                self._device.delay(2)  
#                 if self._device(resourceId = 'com.android.deskclock:id/fab',text = 'Add alarm').exists:
#                     self._logger.debug('22222222222222')
                self._device.press.back()
                if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                    self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                    self._device.delay(2)
                    self._logger.debug('Test Show Alarms Test Successfully')
        else:
            self._logger.debug('Test Show Alarms Test fail')
            return False
        """
        Test Set Alarm Test
        """
        if self._device(resourceId = 'android:id/text1',text = 'Set Alarm Test').exists:
            self._device(resourceId = 'android:id/text1',text = 'Set Alarm Test').click()
            self._device.delay(2)
            if self._device(className = 'android.widget.Button',text = 'SET ALARM').exists:
                self._device(className = 'android.widget.Button',text = 'SET ALARM').click()
                self._device.delay(2) 
#                 if self._device(resourceId = 'android:id/radial_picker').exists:
                self._device.press.back()
                self._device.press.back()
                if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                    self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                    self._device.delay(2)
                    self._logger.debug('Test Set Alarms Test Successfully')
        else:
            self._logger.debug('Test Set Alarms Test Fail')
            return False
        """
        Test Start Alarm Test
        """
        if self._device(resourceId = 'android:id/text1',text = 'Start Alarm Test').exists:
            self._device(resourceId = 'android:id/text1',text = 'Start Alarm Test').click()
            self._device.delay(2)
            if self._device(className = 'android.widget.Button',text = 'SET ALARM').exists:
                self._device(className = 'android.widget.Button',text = 'SET ALARM').click()
                self._logger.debug('Wait for 2 minutes')
                self._device.delay(130)
                if self._device(className = 'android.widget.Button',text = 'VERIFY').exists:
                    self._device(className = 'android.widget.Button',text = 'VERIFY').click()
                    self._device.delay(2)
                if self._device(resourceId = 'com.android.deskclock:id/label',text ='Start Alarm Test').exists:
                    self._device.swipe(394,6,394,1089)
                    self._device.delay(2)
                    if self._device(resourceId = 'android:id/action0',text ='DISMISS').exists:
                        self._device(resourceId = 'android:id/action0',text ='DISMISS').click()
                        self._device.swipe(394,1089,394,6)
                        self._device.press.back()
                        self._device.delay(2)
                        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                            self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                            self._device.delay(2)
                            self._logger.debug('Test Set Alarms Test Successfully')
        else:
            self._logger.debug('Test Set Alarms Test Fail')
            return False
        """
        Test Full Alarm Test
        """
        if self._device(resourceId = 'android:id/text1',text = 'Full Alarm Test').exists:
                self._device(resourceId = 'android:id/text1',text = 'Full Alarm Test').click()
                self._device.delay(2)
                if self._device(className = 'android.widget.Button',text = 'CREATE ALARM').exists:
                    self._device(className = 'android.widget.Button',text = 'CREATE ALARM').click()
                    self._logger.debug('clear alarm')
                    self._device.delay(2)
                    if self._device(resourceId = 'com.android.deskclock:id/edit_label',text ='Create Alarm Test').exists:
                        self._device.press.back()
                        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                            self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                            self._device.delay(2)
                            self._logger.debug('Test Full Alarm Test Successfully')
        else:
            self._logger.debug('Test Full Alarm Test Fail')
            return False
        """
        Test Set Timer Test
        """
        if self._device(resourceId = 'android:id/text1',text = 'Set Timer Test').exists:
            self._device(resourceId = 'android:id/text1',text = 'Set Timer Test').click()
            self._device.delay(2)
            if self._device(className = 'android.widget.Button',text = 'SET TIMER').exists:
                self._device(className = 'android.widget.Button',text = 'SET TIMER').click()
                self._logger.debug('Set timer')
                self._device.delay(2)
                if self._device(resourceId = 'com.android.deskclock:id/timer_time_text').exists:
                    self._device.press.back()
                    if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                        self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                        self._device.delay(2)
                        self._logger.debug('Test Set Timer Test Successfully')
        else:
            self._logger.debug('Test Set Timer Test Fail')
            return False
        """
        Test Start Timer Test
        """
        if self._device(resourceId = 'android:id/text1',text = 'Start Timer Test').exists:
            self._device(resourceId = 'android:id/text1',text = 'Start Timer Test').click()
            self._device.delay(2)
            if self._device(className = 'android.widget.Button',text = 'START TIMER').exists:
                self._device(className = 'android.widget.Button',text = 'START TIMER').click()
                self._logger.debug('Start timer and wait 30 seconds')
                self._device.delay(30)
                self._device.swipe(394,6,394,1089)
                if self._device(resourceId = 'android:id/action0',text ='STOP').exists:
                    self._device(resourceId = 'android:id/action0',text ='STOP').click()
                    self._device.delay(2)
                    self._device.swipe(394,1089,394,6)
                    self._device.delay(2)
                    if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                        self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                        self._device.delay(2)
                        self._logger.debug('Test Start Timer Test Successfully')
        else:
            self._logger.debug('Test Start Timer Test Fail')
            return False
        """
        Test Start Timer With UI Test
        """
        self._logger.debug('Begin to  Start Timer With UI Test')
        if self._device(resourceId = 'android:id/text1',text = 'Start Timer With UI Test').exists:
            self._device(resourceId = 'android:id/text1',text = 'Start Timer With UI Test').click()
            self._device.delay(2)
            if self._device(className = 'android.widget.Button',text = 'START TIMER').exists:
                self._device(className = 'android.widget.Button',text = 'START TIMER').click()
                self._logger.debug('Start timer With UI Test and wait 30 seconds')
                self._device.delay(30) 
                self._device.press.back()
                self._device.swipe(394,6,394,1089)
                if self._device(resourceId = 'android:id/action0',text ='STOP').exists:
                    self._device(resourceId = 'android:id/action0',text ='STOP').click()
                    self._device.delay(2)
                    self._device.swipe(394,1089,394,6)
                    self._device.delay(2)
                    if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                        self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                        self._device.delay(2)
                        self._logger.debug('Test Start Timer With UI Test Successfully')
                        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                            self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                            self._device.delay(2)     
                            self._logger.debug('Alarms And Timers Tests successfully')
                            return True
        else:
            self._logger.debug('Alarms And Timers Tests Fail')
            return False          
    def Screen_Lock_Test(self,name):
        if self.enter_app('Settings'):
            if self._device(resourceId = 'android:id/title',text='Security').exists:
                self._device(resourceId = 'android:id/title',text='Security').click()
                self._device.delay(2)
                self._logger.debug("enter Security setting")
            else:
                self._device(scrollable=True).scroll.vert.forward(steps=10)
                self._logger.debug("enter Security setting")
                self._device(resourceId = 'android:id/title',text='Security').click()
                self._device.delay(2)
        if self._device(resourceId = 'android:id/title',text='Screen lock').exists:
            self._device(resourceId = 'android:id/title',text='Screen lock').click()
            self._device.delay(2)
            if self._device(resourceId = 'android:id/title',text = 'Swipe').exists:
                self._device(resourceId = 'android:id/title',text = 'Swipe').click()
                self._device.delay(2)
                self._device.press.home()
        self.common_fuc(name)
        self._logger.debug('Enter Screen Lock Test') 
        if self._device(resourceId = 'com.android.cts.verifier:id/da_force_lock_button',text = 'FORCE LOCK').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/da_force_lock_button',text = 'FORCE LOCK').click()
            self._device.delay(5)
            while self._device(resourceId = 'com.android.settings:id/action_button',text = 'Activate').exists:
                self._device(resourceId = 'com.android.settings:id/action_button',text = 'Activate').click()
                self._device.delay(5)
            self._device.screen.on()
            self._device.swipe(394,1089,394,6)
            self._device.press.home()
            self.enter_app('CTS Verifier') 
            if self._device(text = 'It appears the screen was locked successfully!').wait.exists(timeout = 5000):
                self._device(text = 'OK').click()
                self._device.delay(5)
            if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                self._device.delay(2)
                self._logger.debug('Screen Lock Test Successfully') 
                return True  
            else:
                self._logger.debug('Screen Lock Test Fail') 
                return False           
                      

            
    def Keyguard_Disabled_Features_Test(self,name):
        self.common_fuc(name)
        self._logger.debug('Enter Keyguard Disabled Features Test')
        if self._device(resourceId = 'android:id/text1',text = 'Disable trust agents').exists:
            self._device(resourceId = 'android:id/text1',text = 'Disable trust agents').click()
            self._device.delay(2)
            if self._device(resourceId = 'android:id/button1',text = 'PASS').exists:
                self._device(resourceId = 'android:id/button1',text = 'PASS').click()
                self._device.delay(2) 
        if self._device(resourceId = 'android:id/text1',text = 'Disable camera').exists:
            self._device(resourceId = 'android:id/text1',text = 'Disable camera').click()
            self._device.delay(2)
            if self._device(resourceId = 'android:id/button1',text = 'PASS').exists:
                self._device(resourceId = 'android:id/button1',text = 'PASS').click()
                self._device.delay(2)  
        if self._device(resourceId = 'android:id/text1',text = 'Disable notifications').exists:
            self._device(resourceId = 'android:id/text1',text = 'Disable notifications').click()
            self._device.delay(2)
            if self._device(resourceId = 'android:id/button1',text = 'PASS').exists:
                self._device(resourceId = 'android:id/button1',text = 'PASS').click()
                self._device.delay(2) 
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
            self._device.delay(2)
            self._logger.debug('Keyguard Disabled Features Test Successfully') 
            return True
        else:
            self._logger.debug('Keyguard Disabled Features Test Fail') 
            return False

    def Redacted_Notifications_Keyguard_Disabled_Features_Test(self,name):
        self.common_fuc(name)   
        self._logger.debug('Enter Redacted Notifications Keyguard Disabled Features Test')
        if self._device(resourceId = 'android:id/text1',text = 'Disable unredacted notifications').exists:
            self._device(resourceId = 'android:id/text1',text = 'Disable unredacted notifications').click()
            self._device.delay(2)
            if self._device(resourceId = 'android:id/button1',text = 'PASS').exists:
                self._device(resourceId = 'android:id/button1',text = 'PASS').click()
                self._device.delay(2)
            if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                self._device.delay(2)
                self._logger.debug('Redacted Notifications Keyguard Disabled Features Test Successfully') 
                return True
        else:
            self._logger.debug('Redacted Notifications Keyguard Disabled Features Test Fail') 
            return False   
        
    def Hardware_Software_Feature_Summary(self,name): 
        self.common_fuc(name)
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                self._device.delay(2)
                self._logger.debug('Hardware/Software Feature Summary Test Successfully')
                return True
        else:
            self._logger.debug('Hardware/Software Feature Summary Test Fail')
            return False
        """
        Connectivity_Constraints need to close wifi ana Cellular data
        """
    def Connectivity_Constraints(self,name):
        self.common_fuc(name) 
        if self._device(resourceId = 'com.android.cts.verifier:id/js_connectivity_start_test_button',text = 'START TEST').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/js_connectivity_start_test_button',text = 'START TEST').click()
            self._device.delay(15)
            if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                self._device.delay(2)
                self._logger.debug('Connectivity Constraints Test Successfully')
                return True
        else:
            self._logger.debug('Connectivity Constraints Test Fail')
            return False
    def Battery_Saving_Mode_Test(self,name):
        self.common_fuc(name)
        if self._device(className = 'android.widget.RelativeLayout',index = '1').child(resourceId = 'com.android.cts.verifier:id/launch_settings',text = 'LAUNCH SETTINGS').isEnabled:
            self._device(className = 'android.widget.RelativeLayout',index = '1').child(resourceId = 'com.android.cts.verifier:id/launch_settings',text = 'LAUNCH SETTINGS').click()
            self._device.delay(2)
            self._logger.debug('Launch setting successfully')
            """
            change Mode modem to Battery saving
            """
            while self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'OFF').exists:
                self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'OFF').click()
                self._device.delay(2)
            if self._device(resourceId = 'android:id/title',text = 'Mode').exists:
                self._device(resourceId = 'android:id/title',text = 'Mode').click()
                self._device.delay(2)
                if self._device(resourceId = 'android:id/title',text = 'Battery saving').exists:
                    self._device(resourceId = 'android:id/title',text = 'Battery saving').click()
                    self._device.delay(2)
                    self._logger.debug("enter the battery saving mode")
                    
                    self._device.press.back()
                    self._device.press.back()
                    if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                        self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                        self._device.delay(2)
                        self._logger.debug('Battery Saving Mode Test Successfully')
                        return True
            else:
                self._logger.debug('Battery Saving Mode Test Fail')
                return False
                 
    def Device_Only_Mode_Test(self,name): 
        self.common_fuc(name)
        if self._device(className = 'android.widget.RelativeLayout',index = '2').child(resourceId = 'com.android.cts.verifier:id/launch_settings',text = 'LAUNCH SETTINGS').isEnabled:
            self._device(className = 'android.widget.RelativeLayout',index = '2').child(resourceId = 'com.android.cts.verifier:id/launch_settings',text = 'LAUNCH SETTINGS').click()
            self._device.delay(2)
            self._logger.debug('Launch setting successfully')
            """
            change Mode modem to Device Only
            """
            if self._device(resourceId = 'android:id/title',text = 'Mode').exists:
                self._device(resourceId = 'android:id/title',text = 'Mode').click()
                self._device.delay(2)
                if self._device(resourceId = 'android:id/title',text = 'Device only').exists:
                    self._device(resourceId = 'android:id/title',text = 'Device only').click()
                    self._device.delay(2)
                    self._logger.debug("enter the Device only mode")
                    self._device.press.back()
                    self._device.press.back()
                    if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                        self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                        self._device.delay(2)
                        self._logger.debug('Device Only Mode Test Successfully') 
                        return True
        else:
            self._logger.debug('Device Only Mode Test Fail') 
            return False
    def High_Accuracy_Mode_Test(self,name):
        self.common_fuc(name)
        if self._device(className = 'android.widget.RelativeLayout',index = '2').child(resourceId = 'com.android.cts.verifier:id/launch_settings',text = 'LAUNCH SETTINGS').isEnabled:
            self._device(className = 'android.widget.RelativeLayout',index = '2').child(resourceId = 'com.android.cts.verifier:id/launch_settings',text = 'LAUNCH SETTINGS').click()
            self._device.delay(2)
            self._logger.debug('Launch setting successfully')
            """
            change Mode modem to High Accuracy Mode Test
            """
            if self._device(resourceId = 'android:id/title',text = 'Mode').exists:
                self._device(resourceId = 'android:id/title',text = 'Mode').click()
                self._device.delay(2)
                if self._device(resourceId = 'android:id/title',text = 'High accuracy').exists:
                    self._device(resourceId = 'android:id/title',text = 'High accuracy').click()
                    self._device.delay(2)
                    self._logger.debug("enter the High Accuracy Mode")
                    self._device.press.back()
                    self._device.press.back()
                    if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                        self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                        self._device.delay(2)
                        self._logger.debug('High Accuracy Mode Test Successfully') 
                        return True
        else:
            self._logger.debug('High Accuracy Mode Test Fail')
            return False
    def Location_Mode_Off_Test(self,name):
        self.common_fuc(name)
        if self._device(resourceId = 'com.android.cts.verifier:id/launch_settings',text = 'LAUNCH SETTINGS').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/launch_settings',text = 'LAUNCH SETTINGS').click()
            self._device.delay(2)
            self._logger.debug('Launch setting successfully')
            """
            Turn off the location access
            """
            if self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'ON').exists:
                self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'ON').click()
                self._device.delay(2)
                self._device.press.back()
            if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                self._device.delay(2)
                self._logger.debug('Location Mode Off Test Successfully')
                return True
        else:
            self._logger.debug('Location Mode Off Test Fail')
    def BYOD_Provisioning_tests(self,name):
        self.common_fuc(name)
        """
        Enter Custom provisioning color test
        """
        if self._device(resourceId = 'android:id/text1',text = 'Custom provisioning color').exists:
            self._device(resourceId = 'android:id/text1',text = 'Custom provisioning color').click()
            self._device.delay(2)
            if self._device(className = 'android.widget.Button',text = 'GO').exists:
                self._device(className = 'android.widget.Button',text = 'GO').click()
                self._device.delay(2)
            if self._device(resourceId = 'com.android.managedprovisioning:id/suw_navbar_next',text = 'NEXT').exists:
                self._device(resourceId = 'com.android.managedprovisioning:id/suw_navbar_next',text = 'NEXT').click()
                self._device.delay(2)
            if self._device(resourceId = 'com.android.managedprovisioning:id/positive_button',text = 'OK').exists:
                self._device(resourceId = 'com.android.managedprovisioning:id/positive_button',text = 'OK').click()
                self._device.delay(10)
            if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                self._device.delay(5)
                self._logger.debug('Custom provisioning color Test Successfully')
        else:
            self._logger.debug('Custom provisioning color Test Fail')
            return False
        
            """
             Enter Custom provisioning image
            """
        if self._device(resourceId = 'android:id/text1',text = 'Custom provisioning image').exists:
            self._device(resourceId = 'android:id/text1',text = 'Custom provisioning image').click()
            self._device.delay(2)
            if self._device(className = 'android.widget.Button',text = 'GO').exists:
                self._device(className = 'android.widget.Button',text = 'GO').click()
                self._device.delay(2)
            if self._device(className = 'android.widget.Button',text = 'DELETE').exists:
                self._device(className = 'android.widget.Button',text = 'DELETE').click()
                self._device.delay(2)
            if self._device(resourceId = 'com.android.managedprovisioning:id/suw_navbar_next',text = 'NEXT').exists:
                self._device(resourceId = 'com.android.managedprovisioning:id/suw_navbar_next',text = 'NEXT').click()
                self._device.delay(2)
            if self._device(resourceId = 'com.android.managedprovisioning:id/positive_button',text = 'OK').exists:
                self._device(resourceId = 'com.android.managedprovisioning:id/positive_button',text = 'OK').click()
                self._device.delay(10)
            if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                self._device.delay(2)
                self._logger.debug('Custom provisioning image Test Successfully')
        else:
            self._logger.debug('Custom provisioning image Test Fail')
            return False       
        self._logger.debug('Test two cases completely')
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                self._device.delay(2)
                self._logger.debug('Custom provisioning image Test Successfully')
                self._logger.debug('BYOD Provisioning tests successfully')
                return True
        else:
            self._logger.debug('BYOD Provisioning tests successfully')
            return False     
    def Device_Owner_Provisioning(self,name):
        self.common_fuc(name)
        """
        Enter the Device owner nagative test
        """
        if self._device(resourceId = 'android:id/text1',text = 'Device owner negative test').exists:
            self._device(resourceId = 'android:id/text1',text = 'Device owner negative test').click()
            self._device.delay(2)
            if self._device(className = 'android.widget.Button',text = 'START PROVISIONING').exists:
                self._device(className = 'android.widget.Button',text = 'START PROVISIONING').click()
                self._device.delay(2)
            if self._device(resourceId = 'android:id/button1',text = 'OK').exists:
                self._device(resourceId = 'android:id/button1',text = 'OK').click()
                self._device.delay(2) 
            if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                self._device.delay(5)    
            if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                self._device.delay(2)
            self._logger.debug('Device owner negative test successfully')
            return True
        else:
            self._logger.debug('Device owner negative test fail')
            return False 
    def CA_Cert_Notification_Test(self,name):    
        self.common_fuc(name) 
        """
        index = 0
        """    
        if self._device(className = 'android.widget.RelativeLayout',index = 0).child(resourceId = 'com.android.cts.verifier:id/ca_notify_do_something',text = 'DO IT').exists:
            self._device(className = 'android.widget.RelativeLayout',index = 0).child(resourceId = 'com.android.cts.verifier:id/ca_notify_do_something',text = 'DO IT').click()
            self._device.delay(2) 
        if self._device(resourceId = 'android:id/title',text = 'VFD 1300').exists:
            self._device(resourceId = 'android:id/title',text = 'VFD 1300').click()
            self._device.delay(2) 
        self._device.press.back()
        """
        index = 1
        """
        if self._device(className = 'android.widget.RelativeLayout',index = 1).child(resourceId = 'com.android.cts.verifier:id/ca_notify_do_something',text = 'DO IT').exists:
            self._device(className = 'android.widget.RelativeLayout',index = 1).child(resourceId = 'com.android.cts.verifier:id/ca_notify_do_something',text = 'DO IT').click()
            self._device.delay(2) 
        if self._device(resourceId = 'android:id/title',text = 'SYSTEM').exists:
            self._device(resourceId = 'android:id/title',text = 'SYSTEM').click()
            self._device.delay(2) 
        self._device.press.back()
        """
        index = 2
        """
        if self._device(className = 'android.widget.RelativeLayout',index = 2).child(resourceId = 'com.android.cts.verifier:id/ca_notify_do_something',text = 'DO IT').exists:
            self._device(className = 'android.widget.RelativeLayout',index = 2).child(resourceId = 'com.android.cts.verifier:id/ca_notify_do_something',text = 'DO IT').click()
            self._device.delay(2) 
        if self._device(resourceId = 'android:id/title',text = 'None').exists:
            self._device(resourceId = 'android:id/title',text = 'None').click()
            self._device.delay(2) 
        """
        index = 3
        """      
        if self._device(className = 'android.widget.RelativeLayout',index = 3).child(resourceId = 'com.android.cts.verifier:id/ca_notify_do_something',text = 'DONE').exists:
            self._device(className = 'android.widget.RelativeLayout',index = 3).child(resourceId = 'com.android.cts.verifier:id/ca_notify_do_something',text = 'DONE').click()
            self._device.delay(2) 

        """
        index = 4
        """     
        if self._device(className = 'android.widget.RelativeLayout',index = 4).child(resourceId = 'com.android.cts.verifier:id/ca_notify_do_something',text = 'DONE').exists:
            self._device(className = 'android.widget.RelativeLayout',index = 4).child(resourceId = 'com.android.cts.verifier:id/ca_notify_do_something',text = 'DONE').click()
            self._device.delay(2) 
            
        """
        End the CA Cert Notification Test
        """
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
            self._device.delay(2)
            self._logger.debug('CA Cert Notification Test successfully') 
            return True
        else:
            self._logger.debug('CA Cert Notification Test Fail') 
            return False
               
    
    
    def CA_Cert_Notification_on_Boot_test(self,name):
        self.common_fuc(name)
        if self._device(resourceId = 'com.android.cts.verifier:id/check_creds',text = 'CHECK CREDENTIALS').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/check_creds',text = 'CHECK CREDENTIALS').click()
            self._device.delay(2)
            if self._device(resourceId = 'android:id/title',text = 'SYSTEM').exists:
                self._device(resourceId = 'android:id/title',text = 'SYSTEM').click()
                self._device.delay(2)
                self._device.press.back()
        if self._device(resourceId = 'com.android.cts.verifier:id/install',text = 'INSTALL CREDENTIAL').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/install',text = 'INSTALL CREDENTIAL').click()
            self._device.delay(2)
            if self._device(className = 'android.widget.TextView',text = '9008X').exists:
                self._device.delay(2)        
                self._device.press.back()
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
            self._device.delay(2)
            self._logger.debug('CA Cert Notification on Boot Test successfully') 
            return True
        else:
            self._logger.debug('CA Cert Notification on Boot Test fail') 
            return False
                    
    def Condition_Provider_test(self,name):
        self.common_fuc(name)
        if self._device(className = 'android.widget.RelativeLayout',index = '0').child(resourceId = 'com.android.cts.verifier:id/nls_action_button',text = 'LAUNCH SETTINGS').isEnabled:
            self._device(className = 'android.widget.RelativeLayout',index = '0').child(resourceId = 'com.android.cts.verifier:id/nls_action_button',text = 'LAUNCH SETTINGS').click()
            self._device.delay(2)
            self._logger.debug('Enable Cts Verifier')
            
            if self._device(resourceId = 'android:id/switch_widget',text = 'OFF').exists:
                self._device(resourceId = 'android:id/switch_widget',text = 'OFF').click()
                self._device.delay(2)
                if self._device(resourceId = 'android:id/button1',text = 'ALLOW').exists:
                    self._device(resourceId = 'android:id/button1',text = 'ALLOW').click()
                    self._device.delay(2) 
                    self._device.press.back()
                    self._device.delay(50)
        if self._device(className = 'android.widget.RelativeLayout',index = '8').child(resourceId = 'com.android.cts.verifier:id/nls_action_button',text = 'LAUNCH SETTINGS').isEnabled:
            self._device(className = 'android.widget.RelativeLayout',index = '8').child(resourceId = 'com.android.cts.verifier:id/nls_action_button',text = 'LAUNCH SETTINGS').click()
            self._device.delay(2)
            self._logger.debug('Disable Cts Verifier')
            
            if self._device(resourceId = 'android:id/switch_widget',text = 'ON').exists:
                self._device(resourceId = 'android:id/switch_widget',text = 'ON').click()
                self._device.delay(2)
                if self._device(resourceId = 'android:id/button1',text = 'OK').exists:
                    self._device(resourceId = 'android:id/button1',text = 'OK').click()
                    self._device.delay(2) 
                    self._device.press.back()
                    self._device.delay(6)
        
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
            self._device.delay(2)
            self._logger.debug('Condition Provider test successfully') 
            return True  
        else:
            self._logger.debug('Condition Provider test Fail')  
            return False                
                    
    def Notification_Listener_Test(self,name):
        self.common_fuc(name)
        if self._device(className = 'android.widget.RelativeLayout',index = '0').child(resourceId = 'com.android.cts.verifier:id/nls_action_button',text = 'LAUNCH SETTINGS').isEnabled:
            self._device(className = 'android.widget.RelativeLayout',index = '0').child(resourceId = 'com.android.cts.verifier:id/nls_action_button',text = 'LAUNCH SETTINGS').click()
            self._device.delay(2)
            self._logger.debug('Enable Notification Listener for Cts Verifier')
            
            if self._device(resourceId = 'android:id/switch_widget',text = 'OFF').exists:
                self._device(resourceId = 'android:id/switch_widget',text = 'OFF').click()
                self._device.delay(2)
                if self._device(resourceId = 'android:id/button1',text = 'ALLOW').exists:
                    self._device(resourceId = 'android:id/button1',text = 'ALLOW').click()
                    self._device.delay(2) 
                    self._device.press.back()
                    self._device.delay(40)
#                     self._device(scrollable=True).scroll.toEnd()
                    self._device(scrollable=True).scroll.toEnd()
        if self._device(className = 'android.widget.RelativeLayout',index = '6').child(resourceId = 'com.android.cts.verifier:id/nls_action_button',text = 'LAUNCH SETTINGS').isEnabled:
            self._device(className = 'android.widget.RelativeLayout',index = '6').child(resourceId = 'com.android.cts.verifier:id/nls_action_button',text = 'LAUNCH SETTINGS').click()
            self._device.delay(2)
            self._logger.debug('Disable Notification Listener for Cts Verifier')
            
            if self._device(resourceId = 'android:id/switch_widget',text = 'ON').exists:
                self._device(resourceId = 'android:id/switch_widget',text = 'ON').click()
                self._device.delay(2)
                if self._device(resourceId = 'android:id/button1',text = 'TURN OFF').exists:
                    self._device(resourceId = 'android:id/button1',text = 'TURN OFF').click()
                    self._device.delay(2) 
                    self._device.press.back()
                    self._device.delay(10)
        
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
            self._device.delay(2)
            self._logger.debug('Notification_Listener_Test successfully')  
            return True
        else:
            self._logger.debug('Notification_Listener_Test test Fail')        
            return False        
                    
    def Projection_Cube_Test(self,name):
        self.common_fuc(name)
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
            self._device.delay(5)
            self._logger.debug('Projection Cube Test test successfully')
            return True
        else:
            self._logger.debug('Projection Cube Test test fail')
    def Projection_Multitouch_Test(self,name):
        self.common_fuc(name)
        self._device.click(430,650)
        self._device.click(349,291)
        self._device.click(458,504)
        self._device.swipe(435,1015,435,294)
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
            self._device.delay(5)
            self._logger.debug('Projection Multitouch Test test successfully')
            return True
        else:
            self._logger.debug('Projection Multitouch Test test Fail')  
            return False                
    def Projection_Offscreen_Activity(self,name):
        self.common_fuc(name)
        self._device.screen.off()
        self._device.delay(10)
        self._device.screen.on()
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
            self._device.delay(5)
            self._logger.debug('Projection Offscreen Activity Test successfully') 
            return True
        else:
            self._logger.debug('Projection Offscreen Activity Test Fail') 
            return False              
    def Projection_Scrolling_List_Test(self,name):
        self.common_fuc(name)
        self._device(resourceId = 'com.android.cts.verifier:id/texture_view').scroll.vert.forward(steps=100) 
        self._device.delay(2)
        self._device(resourceId = 'com.android.cts.verifier:id/texture_view').scroll.vert.backward(steps=100)
        self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
            self._device.delay(5)
            self._logger.debug('Projection Scrolling List Test successfully') 
            return True
        else:
            self._logger.debug('Projection Scrolling List Test Fail')
            return False
    def Projection_Widget_Test(self,name):
        self.common_fuc(name)
        if self._device(resourceId = 'com.android.cts.verifier:id/up_button',text = 'UP').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/up_button',text = 'UP').click()
            self._device.delay(2)
            click_down = 0
            while click_down < 3:
                if self._device(resourceId = 'com.android.cts.verifier:id/down_button',text = 'DOWN').exists:
                    self._device(resourceId = 'com.android.cts.verifier:id/down_button',text = 'DOWN').click()
                    self._device.delay(2)
                    click_down += 1
                    
            if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                self._device.delay(5)
                self._logger.debug('Projection Widget Test successfully')
                return True
        else:
            self._logger.debug('Projection Widget Test fail')     
            return False
        
    def KeyChain_Storage_Test(self,name):
        self.common_fuc(name)
        if self._device(resourceId = 'com.android.cts.verifier:id/action_next',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/action_next',text = 'NEXT').click()
            self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/action_next',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/action_next',text = 'NEXT').click()
            self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/action_skip',text = 'SKIP').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/action_skip',text = 'SKIP').click()
            self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/action_next',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/action_next',text = 'NEXT').click()
            self._device.delay(2) 
        if self._device(resourceId = 'android:id/button2',text = 'CANCEL').exists:
            self._device(resourceId = 'android:id/button2',text = 'CANCEL').click()
            self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/action_next',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/action_next',text = 'NEXT').click()
            self._device.delay(2)              
        if self._device(resourceId = 'com.android.cts.verifier:id/action_skip',text = 'SKIP').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/action_skip',text = 'SKIP').click()
            self._device.delay(2)        
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
            self._device.delay(5)
            self._logger.debug('KeyChain Storage Test successfully') 
            return True
        else:
            self._logger.debug('KeyChain Storage Test Fail')
            return False 
                   
        
    def Keyguard_Password_Verification(self,name):
        self.common_fuc(name)
        """
        set password
        """
        if self._device(resourceId = 'com.android.cts.verifier:id/lock_set_btn',text = 'SET PASSWORD').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/lock_set_btn',text = 'SET PASSWORD').click()
            self._device.delay(2)
            if self._device(resourceId = 'android:id/title',text = 'PIN').exists:
                self._device(resourceId = 'android:id/title',text = 'PIN').click()
                self._device.delay(2)
                if self._device(resourceId = 'android:id/title',text = 'Require PIN to start device').exists:
                    self._device(resourceId = 'android:id/title',text = 'Require PIN to start device').click()
                    self._device.delay(2)
                    if self._device(resourceId = 'android:id/button1',text = 'OK').exists:
                        self._device(resourceId = 'android:id/button1',text = 'OK').click()
                        self._device.delay(2)
                    """
                    input the password
                    """
                    if self._device(resourceId = 'com.android.settings:id/password_entry').exists:
                        self._device(resourceId = 'com.android.settings:id/password_entry').set_text(1234)
                        self._device.delay(2)
                    if self._device(resourceId = 'com.android.settings:id/next_button',text = 'CONTINUE').isEnabled:
                        self._device(resourceId = 'com.android.settings:id/next_button',text = 'CONTINUE').click()
                        self._device.delay(5) 
                        self._logger.debug('Set the password successfully')
                    """
                    confirm the password
                    """                  
                    if self._device(resourceId = 'com.android.settings:id/password_entry').exists:
                        self._device(resourceId = 'com.android.settings:id/password_entry').set_text(1234)
                        self._device.delay(2)
                    if self._device(resourceId = 'com.android.settings:id/next_button',text = 'OK').isEnabled:
                        self._device(resourceId = 'com.android.settings:id/next_button',text = 'OK').click()
                        self._device.delay(2)
                    if self._device(text = "Don't show notifications at all").exists:
                        self._device(text = "Don't show notifications at all").click()
                        self._device(resourceId = 'com.android.settings:id/next_button',text = 'DONE').click()
                        self._device.delay(2) 
                        self._logger.debug('Confirm the password successfully')
        """
        Change password
        """
        if self._device(resourceId = 'com.android.cts.verifier:id/lock_change_btn',text = 'CHANGE PASSWORD').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/lock_change_btn',text = 'CHANGE PASSWORD').click()
            self._device.delay(2) 
            if self._device(resourceId = 'com.android.settings:id/password_entry').exists:
                self._device(resourceId = 'com.android.settings:id/password_entry').set_text(1234)
                self._device.delay(2)
                self._device.press.enter()
                self._device.delay(2)
                if self._device(resourceId = 'android:id/title',text = 'None').exists:
                    self._device(resourceId = 'android:id/title',text = 'None').click()
                    self._device.delay(2)
                    if self._device(resourceId = 'android:id/button1',text = 'YES, REMOVE').exists:
                        self._device(resourceId = 'android:id/button1',text = 'YES, REMOVE').click()
                        self._device.delay(5)
                    if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                        self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                        self._device.delay(5)
                        self._logger.debug('Keyguard Password Verification successfully')
                        return True
        else:
            self._logger.debug('Keyguard Password Verification Fail') 
            return False  
                      
    def Lock_Bound_Keys_Test(self,name):
        """
        Enter Settings and set a screen lock
        """
        self._device.press.home()
        if self.enter_app('Settings'):
            if self._device(resourceId = 'android:id/title',text='Security').exists:
                self._device(resourceId = 'android:id/title',text='Security').click()
                self._device.delay(2)
                self._logger.debug("enter Security setting")
            else:
                self._device(scrollable=True).scroll.vert.forward(steps=10)
                self._logger.debug("enter Security setting")
                self._device(resourceId = 'android:id/title',text='Security').click()
                self._device.delay(2)
        if self._device(resourceId = 'android:id/title',text='Screen lock').exists:
            self._device(resourceId = 'android:id/title',text='Screen lock').click()
            self._device.delay(2)
            if self._device(resourceId = 'android:id/title',text = 'PIN').exists:
                self._device(resourceId = 'android:id/title',text = 'PIN').click()
                self._device.delay(2)
                if self._device(resourceId = 'android:id/title',text = 'Require PIN to start device').exists:
                    self._device(resourceId = 'android:id/title',text = 'Require PIN to start device').click()
                    self._device.delay(2)
                    if self._device(resourceId = 'android:id/button1',text = 'OK').exists:
                        self._device(resourceId = 'android:id/button1',text = 'OK').click()
                        self._device.delay(2)
                    """
                    input the password
                    """
                    if self._device(resourceId = 'com.android.settings:id/password_entry').exists:
                        self._device(resourceId = 'com.android.settings:id/password_entry').set_text(1234)
                        self._device.delay(2)
                    if self._device(resourceId = 'com.android.settings:id/next_button',text = 'CONTINUE').isEnabled:
                        self._device(resourceId = 'com.android.settings:id/next_button',text = 'CONTINUE').click()
                        self._device.delay(5) 
                    """
                    confirm the password
                    """                  
                    if self._device(resourceId = 'com.android.settings:id/password_entry').exists:
                        self._device(resourceId = 'com.android.settings:id/password_entry').set_text(1234)
                        self._device.delay(2)
                    if self._device(resourceId = 'com.android.settings:id/next_button',text = 'OK').isEnabled:
                        self._device(resourceId = 'com.android.settings:id/next_button',text = 'OK').click()
                        self._device.delay(2) 
                    if self._device(resourceId = 'com.android.settings:id/next_button',text = 'DONE').exists:
                        self._device(resourceId = 'com.android.settings:id/next_button',text = 'DONE').click()
                        self._device.delay(2)
                        
        self.common_fuc(name)
        if self._device(resourceId = 'com.android.cts.verifier:id/sec_start_test_button',text = 'START TEST').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/sec_start_test_button',text = 'START TEST').click()
            self._device.delay(8)
            if self._device(resourceId = 'com.android.settings:id/password_entry').exists:
                self._device(resourceId = 'com.android.settings:id/password_entry').set_text(1234)
                self._device.delay(2)
                self._device.press.enter()
                self._device.delay(2)
                if self._device(resourceId = 'com.android.cts.verifier:id/pass_button').isEnabled:
                    self._device(resourceId = 'com.android.cts.verifier:id/pass_button').click()
                    self._device.delay(5)
                    self._logger.debug('Lock Bound Keys Test successfully')
                    return True
        else:
            self._logger.debug('Lock Bound Keys Test Fail')
            return False
    
    def CTS_Sensor_Batching_Tests(self,name):
        self.common_fuc(name)
        """
        set flight mode as true 
        """ 
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(2) 
            if self._device(resourceId = 'android:id/switch_widget',text = 'OFF').exists:
                self._device(resourceId = 'android:id/switch_widget',text = 'OFF').click()
                self._device.delay(2) 
                self._logger.debug('set flight mode as on')
                self._device.press.back()
        """
        set Adaptive Brightness as false
        """            
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(2)
#             self._logger.debug('111111111111111')
            if self._device(className = 'android.widget.LinearLayout',index = 2).child(resourceId = 'android:id/switch_widget',text = 'ON').exists:
                self._device(className = 'android.widget.LinearLayout',index = 2).child(resourceId = 'android:id/switch_widget',text = 'ON').click() 
                self._device.delay(2)
#                 self._logger.debug('222222222222')
                self._logger.debug('set Adaptive Brightness as off')
                self._device.press.back()
                self._device.delay(2)
                if self._device(resourceId = 'com.android.settings:id/action_button',text = 'Activate').exists:
                    self._device(resourceId = 'com.android.settings:id/action_button',text = 'Activate').click()
                    self._device.delay(2)
                    self._logger.debug('Activate the Cts verifier')
        """
        set Auto-rotate screen  as false
        """            
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(2)
            self._device(scrollable=True).scroll.toEnd()
#             self._logger.debug('111111111111111')
#             self._device(resourceId = 'android:id/title',text='Auto-rotate screen').click()
            if self._device(className = 'android.widget.LinearLayout',index = 0).child(resourceId = 'android:id/switch_widget',text = 'ON').exists:
                self._device(className = 'android.widget.LinearLayout',index = 0).child(resourceId = 'android:id/switch_widget',text = 'ON').click() 
                self._device.delay(2)
#                 self._logger.debug('222222222222')
                self._logger.debug('set Auto-rotate screen  as false')
                self._device.press.back()
                self._device.delay(2)
                if self._device(resourceId = 'com.android.settings:id/action_button',text = 'Activate').exists:
                    self._device(resourceId = 'com.android.settings:id/action_button',text = 'Activate').click()
                    self._device.delay(2)
                    self._logger.debug('Activate the Cts verifier')          
#         """
#         set Stay awake  as on
#         """            
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2)
# #             self._device(scrollable=True).scroll.toEnd()
# #             self._logger.debug('111111111111111')
# #             self._device(resourceId = 'android:id/title',text='Auto-rotate screen').click()
#             if self._device(className = 'android.widget.LinearLayout',index = 2).child(resourceId = 'android:id/switch_widget',text = 'ON').exists:
#                 self._device(className = 'android.widget.LinearLayout',index = 2).child(resourceId = 'android:id/switch_widget',text = 'ON').click() 
#                 self._device.delay(2)
# #                 self._logger.debug('222222222222')
#                 self._logger.debug('set Stay awake  as on')
#                 self._device.press.back()
#                 self._device.delay(2)
#                 if self._device(resourceId = 'com.android.settings:id/action_button',text = 'Activate').exists:
#                     self._device(resourceId = 'com.android.settings:id/action_button',text = 'Activate').click()
#                     self._device.delay(2)
#                     self._logger.debug('Activate the Cts verifier')   
        """
        set location as off
        """
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(2)
            self._logger.debug('11111111111111111111111')
            if self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'ON').exists:
                self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'ON').click()
                self._device.delay(2)
                self._logger.debug('set location as Off')
                self._device.press.back()
                self._device.delay(2) 
        """
        click two NEXT
        """
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(2)
            self._logger.debug('22222222222222222222') 
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._logger.debug('to sleep')
            self._device.delay(200)
            self._logger.debug('wake up') 
#             if self._device(resourceId = 'com.android.settings:id/action_button',text = 'Activate').exists:
#                 self._device(resourceId = 'com.android.settings:id/action_button',text = 'Activate').click()
#                 self._device.delay(2)
#                 self._logger.debug('Activate the Cts verifier') 
#                 self._device.press.back()
#                 self._device.delay(2) 
#                 if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#                     self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#                     self._device.delay(10) 
#         """        
#         set location as off
#         """
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2)
#             while self._device(resourceId = 'android:id/switch_widget',text = 'ON').exists: 
#                 self._device(resourceId = 'android:id/switch_widget',text = 'ON').click()
#                 self._device.delay(2)
#                 self._logger.debug('Activate the Cts verifier')
#         self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#         self._device.delay(3)
#         self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#         self._device.delay(60)
#         """
#         set flight mode as true
#         """             
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2) 
#             if self._device(resourceId = 'android:id/switch_widget',text = 'ON').exists:
#                 self._device(resourceId = 'android:id/switch_widget',text = 'ON').click()
#                 self._device.delay(2) 
#                 self._logger.debug('set flight mode as Off')
#                 self._device.press.back() 
#         """
#         set Adaptive Brightness as false
#         """            
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2)
#             if self._device(className = 'android.widget.LinearLayout',index = 13).child(resourceId = 'android:id/switch_widget',text = 'OFF').exists:
#                 self._device(className = 'android.widget.LinearLayout',index = 13).child(resourceId = 'android:id/switch_widget',text = 'OFF').click() 
#                 self._device.delay(2)
#                 self._logger.debug('set Adaptive Brightness as on')
#                 self._device.press.back()
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(2)
            self._device.press.back()
            self._logger.debug('33333333333333333')
            if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
                self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
                self._device.delay(2)
                self._device.press.back()
                if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
                    self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
                    self._device.delay(2)
                    self._device.press.back()
                    if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
                        self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
                        self._device.delay(2)
                        self._device.press.back()
        """
        Test Complete
        """
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button',text = 'PASS').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button',text = 'PASS').click()
            self._device.delay(5)
            self._logger.debug('CTS Sensor Batching Tests successfully')
            return True
        else:
            self._logger.debug('CTS Sensor Batching Tests Fail')
            return False
                   
    def CTS_Sensor_Integration_Tests(self,name):
        self.common_fuc(name)
#         """
#         set flight mode as true 
#         """ 
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2) 
#             if self._device(resourceId = 'android:id/switch_widget',text = 'OFF').exists:
#                 self._device(resourceId = 'android:id/switch_widget',text = 'OFF').click()
#                 self._device.delay(2) 
#                 self._logger.debug('set flight mode as on')
#                 self._device.press.back()
#         """
#         set Adaptive Brightness as false
#         """            
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2)
#             if self._device(className = 'android.widget.LinearLayout',index = 13).child(resourceId = 'android:id/switch_widget',text = 'ON').exists:
#                 self._device(className = 'android.widget.LinearLayout',index = 13).child(resourceId = 'android:id/switch_widget',text = 'ON').click() 
#                 self._device.delay(2)
#                 self._logger.debug('set Adaptive Brightness as off')
#                 self._device.press.back()
#                 self._device.delay(2)
#         """
#         set location as off
#         """
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2)
#             if self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'ON').exists:
#                 self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'ON').click()
#                 self._device.delay(2)
#                 self._logger.debug('set location as off')
#                 self._device.press.back()
#                 self._device.delay(5)
#         
#         self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#         self._device.delay(3)
#         self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#         self._device.delay(60)
#         
#         """
#         set flight mode as true
#         """             
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2) 
#             if self._device(resourceId = 'android:id/switch_widget',text = 'ON').exists:
#                 self._device(resourceId = 'android:id/switch_widget',text = 'ON').click()
#                 self._device.delay(2) 
#                 self._logger.debug('set flight mode as Off')
#                 self._device.press.back() 
#         """
#         set Adaptive Brightness as false
#         """            
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2)
#             if self._device(className = 'android.widget.LinearLayout',index = 13).child(resourceId = 'android:id/switch_widget',text = 'OFF').exists:
#                 self._device(className = 'android.widget.LinearLayout',index = 13).child(resourceId = 'android:id/switch_widget',text = 'OFF').click() 
#                 self._device.delay(2)
#                 self._logger.debug('set Adaptive Brightness as on')
#                 self._device.press.back()
#         """
#         set location as on
#         """
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2)
#             if self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'OFF').exists:
#                 self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'OFF').click()
#                 self._device.delay(2)
#                 self._logger.debug('set Adaptive Brightness as on')
#                 self._device.press.back()
#                 self._device.delay(5)
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(300) 
        """
        Test Complete
        """
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button',text = 'PASS').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button',text = 'PASS').click()
            self._device.delay(5)
            self._logger.debug('CTS Sensor Integration Tests successfully')               
                   
    def CTS_Sensor_Test(self,name):
        self.common_fuc(name)
#         """
#         set flight mode as true 
#         """ 
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2) 
#             if self._device(resourceId = 'android:id/switch_widget',text = 'OFF').exists:
#                 self._device(resourceId = 'android:id/switch_widget',text = 'OFF').click()
#                 self._device.delay(2) 
#                 self._logger.debug('set flight mode as on')
#                 self._device.press.back()
#         """
#         set Adaptive Brightness as false
#         """            
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2)
#             if self._device(className = 'android.widget.LinearLayout',index = 13).child(resourceId = 'android:id/switch_widget',text = 'ON').exists:
#                 self._device(className = 'android.widget.LinearLayout',index = 13).child(resourceId = 'android:id/switch_widget',text = 'ON').click() 
#                 self._device.delay(2)
#                 self._logger.debug('set Adaptive Brightness as off')
#                 self._device.press.back()
#                 self._device.delay(2)
#                 while self._device(resourceId = 'com.android.settings:id/action_button',text = 'Activate').exists:
#                     self._device(resourceId = 'com.android.settings:id/action_button',text = 'Activate').click()
#                     self._device.delay(5)
#                 
# #         """
# #         set location as off
# #         """
# #         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
# #             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
# #             self._device.delay(2)
# #             if self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'ON').exists:
# #                 self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'ON').click()
# #                 self._device.delay(2)
# #                 self._logger.debug('set location as off')
# #                 self._device.press.back()
# #                 self._device.delay(5)
#         """
#         set flight mode as true
#         """             
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2) 
#             if self._device(resourceId = 'android:id/switch_widget',text = 'ON').exists:
#                 self._device(resourceId = 'android:id/switch_widget',text = 'ON').click()
#                 self._device.delay(2) 
#                 self._logger.debug('set flight mode as Off')
#                 self._device.press.back() 
#         """
#         set Adaptive Brightness as false
#         """            
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2)
#             if self._device(className = 'android.widget.LinearLayout',index = 13).child(resourceId = 'android:id/switch_widget',text = 'OFF').exists:
#                 self._device(className = 'android.widget.LinearLayout',index = 13).child(resourceId = 'android:id/switch_widget',text = 'OFF').click() 
#                 self._device.delay(2)
#                 self._logger.debug('set Adaptive Brightness as on')
#                 self._device.press.back()
#         """
#         set location as on
#         """
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2)
#             if self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'OFF').exists:
#                 self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'OFF').click()
#                 self._device.delay(2)
#                 self._logger.debug('set Adaptive Brightness as on')
#                 self._device.press.back()
#                 self._device.delay(5)
        
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(200) 
        """
        Test Complete
        """
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button',text = 'PASS').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button',text = 'PASS').click()
            self._device.delay(5)
            self._logger.debug('CTS Sensor Tests Tests successfully') 
            return True
        else:
            self._logger.debug('CTS Sensor Tests Tests fail')                   
            return False               
                   
    def CTS_Single_Sensor_Tests(self,name):
        self.common_fuc(name)
#         """
#         set flight mode as true 
#         """ 
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2) 
#             if self._device(resourceId = 'android:id/switch_widget',text = 'OFF').exists:
#                 self._device(resourceId = 'android:id/switch_widget',text = 'OFF').click()
#                 self._device.delay(2) 
#                 self._logger.debug('set flight mode as on')
#                 self._device.press.back()
#         """
#         set Adaptive Brightness as false
#         """            
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2)
#             if self._device(className = 'android.widget.LinearLayout',index = 13).child(resourceId = 'android:id/switch_widget',text = 'ON').exists:
#                 self._device(className = 'android.widget.LinearLayout',index = 13).child(resourceId = 'android:id/switch_widget',text = 'ON').click() 
#                 self._device.delay(2)
#                 self._logger.debug('set Adaptive Brightness as off')
#                 self._device.press.back()
#                 self._device.delay(2)
#         """
#         set location as off
#         """
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2)
#             if self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'ON').exists:
#                 self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'ON').click()
#                 self._device.delay(2)
#                 self._logger.debug('set location as off')
#                 self._device.press.back()
#                 self._device.delay(5)
#         
#         self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#         self._device.delay(3)
#         self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#         self._device.delay(400)
#         
#         """
#         set flight mode as true
#         """             
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2) 
#             if self._device(resourceId = 'android:id/switch_widget',text = 'ON').exists:
#                 self._device(resourceId = 'android:id/switch_widget',text = 'ON').click()
#                 self._device.delay(2) 
#                 self._logger.debug('set flight mode as Off')
#                 self._device.press.back() 
#         """
#         set Adaptive Brightness as false
#         """            
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2)
#             if self._device(className = 'android.widget.LinearLayout',index = 13).child(resourceId = 'android:id/switch_widget',text = 'OFF').exists:
#                 self._device(className = 'android.widget.LinearLayout',index = 13).child(resourceId = 'android:id/switch_widget',text = 'OFF').click() 
#                 self._device.delay(2)
#                 self._logger.debug('set Adaptive Brightness as on')
#                 self._device.press.back()
#         """
#         set location as on
#         """
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2)
#             if self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'OFF').exists:
#                 self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'OFF').click()
#                 self._device.delay(2)
#                 self._logger.debug('set Adaptive Brightness as on')
#                 self._device.press.back()
#                 self._device.delay(5)
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(450) 
        """
        Test Complete
        """
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button',text = 'PASS').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button',text = 'PASS').click()
            self._device.delay(5)
            self._logger.debug('CTS Sensor Tests Tests successfully')
            return True 
        else:
            self._logger.debug('CTS Sensor Tests Tests fail')                   
            return False  
        
    def Device_Suspend_Tests(self,name):
        self.common_fuc(name)
                
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(100) 
        """
        Test Complete
        """
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button',text = 'PASS ANYWAY').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button',text = 'PASS ANYWAY').click()
            self._device.delay(5)
            self._logger.debug('Dynamic Sensor Discovery Test successfully') 
            return True
        else:
            self._logger.debug('Dynamic Sensor Discovery Test Tests fail')                   
            return False  
                     
    def Dynamic_Sensor_Discovery_Test(self,name):
        self.common_fuc(name)
#         """
#         set flight mode as true 
#         """ 
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(3) 
#             if self._device(resourceId = 'android:id/switch_widget',text = 'OFF').exists:
#                 self._device(resourceId = 'android:id/switch_widget',text = 'OFF').click()
#                 self._device.delay(2) 
#                 self._logger.debug('set flight mode as on')
#                 self._device.press.back()
#         """
#         set Adaptive Brightness as false
#         """            
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2)
#             if self._device(className = 'android.widget.LinearLayout',index = 13).child(resourceId = 'android:id/switch_widget',text = 'ON').exists:
#                 self._device(className = 'android.widget.LinearLayout',index = 13).child(resourceId = 'android:id/switch_widget',text = 'ON').click() 
#                 self._device.delay(2)
#                 self._logger.debug('set Adaptive Brightness as off')
#                 self._device.press.back()
#                 self._device.delay(2)
# #         """
# #         set location as off
# #         """
# #         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
# #             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
# #             self._device.delay(2)
# #             if self._device(resourceId = 'android:id/switch_widget',text = 'ON').exists:
# #                 self._device(resourceId = 'android:id/switch_widget',text = 'ON').click()
# #                 self._device.delay(2)
# #                 self._logger.debug('set location as off')
# #                 self._device.press.back()
# #                 self._device.delay(5)
#         
#         self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#         self._device.delay(3)
#         self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#         self._device.delay(10)
#         
#         """
#         set flight mode as true
#         """              
#         if self._device(resourceId = 'android:id/switch_widget',text = 'ON').exists:
#             self._device(resourceId = 'android:id/switch_widget',text = 'ON').click()
#             self._device.delay(2) 
#             self._logger.debug('set flight mode as Off')
#             self._device.press.back() 
#         """
#         set Adaptive Brightness as false
#         """            
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2)
#             if self._device(className = 'android.widget.LinearLayout',index = 13).child(resourceId = 'android:id/switch_widget',text = 'OFF').exists:
#                 self._device(className = 'android.widget.LinearLayout',index = 13).child(resourceId = 'android:id/switch_widget',text = 'OFF').click() 
#                 self._device.delay(2)
#                 self._logger.debug('set Adaptive Brightness as on')
#                 self._device.press.back()
# #         """
# #         set location as on
# #         """
# # #         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
# # #             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
# # #             self._device.delay(2)
# # #             if self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'OFF').exists:
# # #                 self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'OFF').click()
# # #                 self._device.delay(2)
# # #                 self._logger.debug('set Adaptive Brightness as on')
# # #                 self._device.press.back()
# # #                 self._device.delay(5)
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(30)
        """
        Test Complete
        """
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button',text = 'PASS').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button',text = 'PASS').click()
            self._device.delay(5)
            self._logger.debug('Dynamic Sensor Discovery Test successfully') 
            return True 
        else:
            self._logger.debug('Dynamic Sensor Discovery Test fail')                   
            return False               
    
    def Sensor_Batching_Tests(self,name):
        self.common_fuc(name)
                
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(2)
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(20)
            self._logger.debug('first time') 
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(20)
            self._logger.debug('second time')
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(20) 
            self._logger.debug('third time')
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(20) 
            self._logger.debug('five time')
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(2)
            self._logger.debug('six time')
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(2)
            self._logger.debug('seven time')
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(2)
            self._logger.debug('eight time')
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(2)
            self._logger.debug('nine time')
        """
        Test Complete
        """
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button',text = 'PASS ANYWAY').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button',text = 'PASS ANYWAY').click()
            self._device.delay(5)
            self._logger.debug('Sensor Batching Tests successfully') 
            return True
        else:
            self._logger.debug('Sensor Batching Tests Tests fail')                   
            return False  
                       
    def Significant_Motion_Tests(self,name):
        self.common_fuc(name)
#         """
#         set flight mode as true 
#         """ 
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2) 
#             if self._device(resourceId = 'android:id/switch_widget',text = 'OFF').exists:
#                 self._device(resourceId = 'android:id/switch_widget',text = 'OFF').click()
#                 self._device.delay(2) 
#                 self._logger.debug('set flight mode as on')
#                 self._device.press.back()
#         """
#         set Adaptive Brightness as false
#         """            
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2)
#             while not self._device(className = 'android.widget.LinearLayout',index = 13).child(resourceId = 'android:id/switch_widget',text = 'ON').exists:
#                 self._device(resourceId = 'com.android.settings:id/content_frame').scroll.vert.forward(steps=100)
#             self._device(className = 'android.widget.LinearLayout',index = 13).child(resourceId = 'android:id/switch_widget',text = 'ON').click() 
#             self._device.delay(2)
#             self._logger.debug('set Adaptive Brightness as off')
#             self._device.press.back()
#             self._device.delay(2)
#         """
#         set location as off
#         """
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2)
#             if self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'ON').exists:
#                 self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'ON').click()
#                 self._device.delay(2)
#                 self._logger.debug('set location as off')
#                 self._device.delay(2)
#                 self._device.press.back()
#                 self._device.delay(5)
#         
#         self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#         self._device.delay(3)
#         self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#         self._device.delay(10)
#         
#         """
#         set flight mode as true
#         """             
# 
#         if self._device(resourceId = 'android:id/switch_widget',text = 'ON').exists:
#             self._device(resourceId = 'android:id/switch_widget',text = 'ON').click()
#             self._device.delay(2) 
#             self._logger.debug('set flight mode as Off')
#             self._device.press.back() 
#         """
#         set Adaptive Brightness as false
#         """            
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2)
#             if self._device(className = 'android.widget.LinearLayout',index = 13).child(resourceId = 'android:id/switch_widget',text = 'OFF').exists:
#                 self._device(className = 'android.widget.LinearLayout',index = 13).child(resourceId = 'android:id/switch_widget',text = 'OFF').click() 
#                 self._device.delay(2)
#                 self._logger.debug('set Adaptive Brightness as on')
#                 self._device.press.back()
        """
#         set location as on
#         """
#         if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
#             self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
#             self._device.delay(2)
#             if self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'OFF').exists:
#                 self._device(resourceId = 'com.android.settings:id/switch_widget',text = 'OFF').click()
#                 self._device.delay(2)
#                 self._logger.debug('set Location as on')
#                 self._device.press.back()
#                 self._device.delay(5)
        if self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/next_button',text = 'NEXT').click()
            self._device.delay(2)
        """
        Test Complete
        """
        if self._device(resourceId = 'com.android.cts.verifier:id/pass_button',text = 'PASS').exists:
            self._device(resourceId = 'com.android.cts.verifier:id/pass_button',text = 'PASS').click()
            self._device.delay(5)
            self._logger.debug('Significant Motion Tests  successfully') 
            return True
        else:
            self._logger.debug('Significant Motion Tests fail')                   
            return False       
                   
                   
                   
                   
                   
                   
                   
 