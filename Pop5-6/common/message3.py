# -*- coding: UTF-8 -*-
"""Message library for scripts.
"""

from common import Common

class Message(Common):

    """Provide common functions for scripts, such as launching activity."""
    
    def __init__(self, device, log_name):
        Common.__init__(self, device,log_name)
        self._ssid = None
        
    def save_fail_img(self):
        """Save fail screenshot to Messaging Folder
        
        """
        self.save_img("Messaging") 
        
    def stay_in_thread(self,isEnterThread):
        if self.stay_in_messaging():
            if isEnterThread:
                if not self._device(resourceId = 'com.android.mms:id/next').exists:
                    self._logger.debug("Already open thread")
                    return True
                else:
                    self._device(resourceId = 'com.android.mms:id/next').click()
                    self._device.delay(2)
                    if not self._device(resourceId = 'com.android.mms:id/next').exists:
                        self._logger.debug("Open thread successfully.")
                        return True
                    else:
                        self._logger.debug("Open thread fail.")
                        return False
                        
            else:
                if self._device(resourceId = 'com.android.mms:id/next').exists:
                    self._logger.debug("Already open root thread")
                    return True
                else:
                    self._device.press.back()
                    self._device.delay(2)
                    if self._device(resourceId = 'com.android.mms:id/next').exists:
                        self._logger.debug("Open root thread successfully.")
                        return True
                    else:
                        self._logger.debug("Open root thread fail.")
                        return False
        else:
            return False
        
    def stay_in_messaging(self):
        """Keep in messaging main page
        
        """
        maxtime = 0
        while not self._device(resourceId = 'com.android.mms:id/floating_action_button').exists:
            self._device.press.back()
            if self._device(resourceId = 'android:id/button1').exists:
                self._device(resourceId = 'android:id/button1').click()
                self._device.delay(2)
            maxtime += 1
            if maxtime > 3:
                self._logger.debug("Can't back messaging")
                break
        if maxtime < 4:
            return True
                
        else:
            self._device.press.home()
            self._device.delay(2)
            self._logger.debug("Launch messaging.")
            if self.enter_app('Messaging'):
                self._device.delay(2)
                if self.get_current_packagename() == self.get_app_package_from_file('Messaging'):
                    
                    maxtime = 0
                    while not  self._device(resourceId = 'com.android.mms:id/floating_action_button').exists:
                        self._device.press.back()
                        if self._device(resourceId = 'android:id/button1').exists:
                            self._device(resourceId = 'android:id/button1').click()
                            self._device.delay(2)
                        maxtime += 1
                        if maxtime > 3:
                            self._logger.debug("Can't back messaging")
                            return False
                        
                    self._logger.debug('Launch messaging successfully.')
                    return True

                else:
                    self._logger.debug('Launch messaging fail.')
                    return False
            else:
                return False
    
    def select_messaging(self,strtype):
        """select message by specified index.
        
        @param (int)index : message order in the list
        @param (str)strtype: 'Audio', 'Video', 'Photo','Text'
        
        """
        msg_order = {'Audio':0,'Video':1,'Photo':2,'Text':3}
        if self._device(resourceId = 'android:id/list').exists\
            and self._device(resourceId = 'com.android.mms:id/listitem', instance = msg_order[strtype]).exists:
            self._logger.debug('Click index ' + str(msg_order[strtype]))
            self._device(resourceId = 'com.android.mms:id/listitem', instance = msg_order[strtype]).click()
            self._device.delay(2)
        if self._device(resourceId='com.android.mms:id/history').exists:
            return True
        else:
            self._logger.debug('select message fail!!!')
            return False
    
    def open_messaging(self,strtype):
        """Open a messaging exist
        
        @param (str)strtype: 'Audio', 'Video', 'Photo', 'Text'
        
        """
        if strtype == 'Photo':
            if self._device(resourceId = 'com.android.mms:id/image_view').exists:
                self._device(resourceId = 'com.android.mms:id/image_view').click()
                self._device.delay(2)
                self.choose_first_player()
                if self._device(resourceId = 'com.android.gallery3d:id/gl_root_view').exists\
                    or self._device(resourceId = 'com.tct.gallery3d:id/gl_root_view').exists\
                    or self._device(resourceId = 'com.google.android.apps.plus:id/photo_hashtag_fragment_container').exists\
                    or self._device(resourceId = 'com.google.android.apps.photos:id/photo_hashtag_fragment_container').exists:
                    self._logger.debug('Open MMS picture successfully.')
                    return True
            self._logger.debug('Open MMS picture fail!')
            return False
        elif strtype == 'Video':
            if self._device(resourceId = 'com.android.mms:id/play_slideshow_button').exists:
                self._device(resourceId = 'com.android.mms:id/play_slideshow_button').click()
                self._device.delay(2)
                self.choose_first_player()
                if self._device(resourceId = 'com.android.gallery3d:id/surface_view').exists:
                    if self._device(resourceId = 'com.android.gallery3d:id/surface_view').wait.gone(timeout = 45000):
                        self._logger.debug('Open MMS video successfully.')
                        return True
                elif self._device(resourceId = 'com.tct.gallery3d:id/surface_view').exists:
                    if self._device(resourceId = 'ccom.tct.gallery3d:id/surface_view').wait.gone(timeout = 45000):
                        self._logger.debug('Open MMS video successfully.')
                        return True
                elif self._device(resourceId = 'com.google.android.apps.photos:id/photo_hashtag_fragment_container').exists:
                    if not self._device(resourceId = 'com.google.android.apps.photos:id/photo_hashtag_fragment_container').wait.gone(timeout = 20000):
                        self._device.press.back()
                    if self._device(resourceId = 'com.android.mms:id/play_slideshow_button').exists:
                        self._logger.debug('Open MMS video successfully.')
                        return True
                elif self._device(resourceId = 'com.google.android.apps.plus:id/videoplayer').exists:
                    if self._device(resourceId = 'com.google.android.apps.plus:id/videoplayer').wait.gone(timeout = 45000):
                        self._logger.debug('Open MMS video successfully.')
                        return True
            self._logger.debug('Open MMS video fail!')
            return False
        elif strtype == 'Audio':
            if self._device(resourceId = 'com.android.mms:id/play_slideshow_button').exists:
                self._device(resourceId = 'com.android.mms:id/play_slideshow_button').click()
                self._device.delay(4)
                if self._device(resourceId = 'com.android.mms:id/audio_icon').exists:
                    if self._device(resourceId = 'com.android.mms:id/audio_icon').wait.gone(timeout = 30000):
                        self._logger.debug('Open MMS audio successfully.')
                        return True
                elif self._device(className = 'android.widget.ScrollView').exists:
                    if self._device(className = 'android.widget.ScrollView').wait.gone(timeout = 30000):
                        self._logger.debug('Open MMS audio successfully.')
                        return True
            self._logger.debug('Open MMS audio fail!')
            return False
        elif strtype == 'Text':
            if self._device(resourceId = 'com.android.mms:id/text_view').exists:
                self._logger.debug('Open SMS successfully.')
                return True
            else:
                self._logger.debug('Open SMS fail!')
                return False 
        else:
            self._logger.debug('Unknown messaging type.')
            return False 
                
                
    def selcet_messaging_option(self, str_option,  instance = 0):
        """Long click a messaging in tread screen and select the option.
        
        @param (str)str_option: option dispaly in the popup menu.
        @param instance: the messaging index displaying in the thread

        """
        self._logger.debug("Select message option %s." %(str_option[str_option.find('/')+1:])) 
        if not self._device(resourceId='com.android.mms:id/mms_layout_view_parent', instance = instance).exists:
            self._logger.debug('Can\'t find message')
            return False       
    
        try_long_click_times = 0
        while not self._device(resourceId = 'com.android.mms:id/detail').exists:
            self._device(resourceId='com.android.mms:id/mms_layout_view_parent').long_click.bottomright()
            self._device.delay(2)
            try_long_click_times += 1
            if try_long_click_times > 3:
                self._logger.debug('Can\'t find Message options')
                return False
                
        if not self._device(resourceId = str_option).exists:
            self._logger.debug('Can\'t find option ' + str_option)
            return False      
        self._device(resourceId = str_option).click()
        self._device.delay(3)
        return True
        
    def forward_messaging(self, sendNum, timeout,  instance = 0):
        """forward a messaging.
        
        @param sendNum: Number to receive the messaging.
        @param timeout: time to wait the messaging sent
        @param instance: the messaging index displaying in the thread

        """
        if not self.selcet_messaging_option('com.android.mms:id/forward'):
            return False
         
        if not self._device(resourceId = 'com.android.mms:id/recipients_editor').exists:
            self._logger.debug('Can\'t input number')
            return False       
        self._device(resourceId = 'com.android.mms:id/recipients_editor').set_text(sendNum)
        self._device.delay(2)
        
        if self._device(descriptionContains='Send').exists:
            self._device(descriptionContains='Send').click()
            self._device.delay(2) 
            
        else:
            self._logger.debug('Can\'t click send button')
            return False
                      
#         self.stay_in_messaging()
        self.stay_in_thread(True)
        
        if not self._device(resourceId ='android:id/list').exists:
            self._logger.debug('Back messaging mainpage fail!!!')
            return False
        
        listitem = self._device(resourceId = 'android:id/list').getChildCount()
        if listitem < 5:
            self._logger.debug('Forward messaging fail!!!')
            return False
        
        self._device(resourceId ='android:id/list').scroll.toBeginning()
        self._device.delay(1) 
        
#         self._device(resourceId = 'android:id/list').child(index = listitem - 5).click()

#         click_tread_time = 0
#         while True:
#             i = 0
#             for i in range(3):
#                 if self._device(resourceId = 'com.android.mms:id/listitem',  index = i).child(resourceId = 'com.android.mms:id/next').exists:         
#                     i += 1
#                 else:
#                     break
#             if i > 2:
#                 self._logger.debug('Get the thread fail!!!')
#                 return False

        if self._device(resourceId = 'com.android.mms:id/from', text = sendNum).exists:
            self._device(resourceId = 'com.android.mms:id/from', text = sendNum).click()
        elif self._device(resourceId = 'com.android.mms:id/subject', text = 'Fwd: ').exists:
            self._device(resourceId = 'com.android.mms:id/subject', text = 'Fwd: ').click()       
        elif self._device(resourceId = 'com.android.mms:id/listitem', index = 0).exists:
            self._device(resourceId = 'com.android.mms:id/listitem', index = 0).click()       
        else:
            self._logger.debug('Get the Fwd message fail!')
            return False

        self._device.delay(2)
        
        if self._device(resourceId ='com.android.mms:id/history').exists:
            self._device(resourceId ='com.android.mms:id/history').scroll.toEnd() 
        else:
            self._logger.debug('Open the Fwd message fail')
            return False
#             break
#             else:
#                 click_tread_time += 1
#                 
#             if click_tread_time > 3:
#                 self._logger.debug('Open the Fwd message fail')
#                 return False
               
        self._logger.debug('message sending...')
        maxtime=0
        while self._device(resourceId = 'com.android.mms:id/date_view', textContains ='Sending').exists:
            self._device.delay(1)
            maxtime+=1
            if maxtime > timeout:
                self._logger.debug('Message send timeout!!!')
                return False
            
        if self._device(resourceId = 'com.android.mms:id/date_view', textContains = ':').exists:
            self._logger.debug('message send success!')
            return True
        else:
            self._logger.debug('Message send fail!!!')
            return False
            
    def get_total_thread(self):
        thread_num = 0
        if self._device(resourceId = 'android:id/list').exists:
            thread_num = self._device(resourceId = 'android:id/list').getChildCount()
            self._logger.debug("The message thread is " + str(thread_num))
        return thread_num
    
    def delete_messaging_thread(self, index=0):
        ''' Long press to delete message in the message list
        
        @param (int)index :  message order in the list

        '''
        if not self.stay_in_messaging():
            return False
        
        self._logger.debug("Delete the %s message thread.", str(index+1))
        if self._device(resourceId = 'android:id/list').exists:
            self._device(resourceId = 'android:id/list').scroll.toBeginning()
            self._device.delay(2)
            thread_num = self._device(resourceId = 'android:id/list').getChildCount()
            self._logger.debug("The message thread before delete is " + str(thread_num))
            
            if index > thread_num - 1:
                self._logger.debug("The %s message thread is not exist.", str(index+1))
                return False
            
            if self._device(resourceId = 'com.android.mms:id/listitem',  index = index).child(resourceId = 'com.android.mms:id/next').exists:         
                index += 1
            
            try_longclickthread_times = 0
            while ((not self._device(resourceId = 'com.android.mms:id/delete').exists)\
                   and (self._device(resourceId = 'com.android.mms:id/from',  instance = index).exists)):
                self._device(resourceId = 'com.android.mms:id/from',  instance = index).long_click()
                self._logger.debug("Long click the message thread.")
                self._device.delay(3)
                try_longclickthread_times += 1
                if try_longclickthread_times > 3:
                    self._logger.debug("Can't find the delete menu.")
                    return False
            self._device(resourceId = 'com.android.mms:id/delete').click()
            self._device.delay(2)
            if self._device(resourceId = 'android:id/button1', text = 'Delete').exists:
                self._device(resourceId = 'android:id/button1', text = 'Delete').click()
                self._device.delay(2)
                
            thread_num_after_delete = self._device(resourceId = 'android:id/list').getChildCount()
            self._logger.debug("The message thread after delete is " + str(thread_num_after_delete))
            if thread_num_after_delete == thread_num - 1:
                self._logger.debug("Delete thread %s successfully.", str(index +1))
                return True
            else:
                self._logger.debug("Delete thread %s fail!", str(index +1))
                return False
        else:
            self._logger.debug("None messaging thread exist.")
            return False
        
        