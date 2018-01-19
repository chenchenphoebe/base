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
        
    def stay_in_messaging(self):
        """Keep in messaging main page
        
        """
        maxtime = 0
        while not  self._device(resourceId = 'com.android.mms:id/action_compose_new').exists:
            self._device.press.back()
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
                    while not  self._device(resourceId = 'com.android.mms:id/action_compose_new').exists:
                        self._device.press.back()
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
            
#     def sms_Send(self,number,content):
#         """send a message(SMS)
#         argv: (str)number -- the telephone number you want to send
#               (str)content -- SMS content
#               
#         author: li.huang
#         """
#         if self.enter_message():
#             self._device(resourceId='com.android.mms:id/action_compose_new').click()
#             self._device.delay(2)
#             self._logger.debug('input phone number:'+number)
#             self._device(className='android.widget.MultiAutoCompleteTextView').set_text(number)
#             self._device.delay(2)
#             self._logger.debug('input sms content:'+content)
#             self._device(className='android.widget.EditText').click()
#             self._device.delay(2)
#             #self._device.click(className='android.widget.EditText')
#             self._device.shell_dos("adb -s "+self._device.get_device_serial()+" shell input text "+content)
#             self._device.delay(2)
#             self._logger.debug('send')
#             self._device(resourceId='com.android.mms:id/send_button_sms').click()
#             self._device.delay(1)
#             if (self._device(text='SENDING…').exists) and (not self._device(resourceId ='com.android.mms:id/delivered_indicator').wait.exists(timeout=10000)) and (self._device(textContains =':').wait.exists(timeout=180000)):
#                 self._logger.debug('SMS send success!!!')
#                 self._device.press.back()
#                 self._device.delay(1)
#                 self.back_to_message()
#                 return True
#         self._logger.debug('SMS send fail!!!')
#         self.back_to_message()
#         self._device.delay(1)
#         return False
#     
#     def mms_Send(self,number,content,subject,pic=None,video=None,audio=None):
#         """send a message(MMS)
#         argv: (str)number -- the telephone number you want to send
#               (str)content -- MMS content
#               (str)subject -- MMS subject
#               pic\video\audio -- attachment of the message
#               
#         author: li.huang
#         """
#         if self.enter_message():
#             self._device(resourceId='com.android.mms:id/action_compose_new').click()
#             self._device.delay(2)
#             self._logger.debug('input phone number:'+number)
#             self._device(text='To').set_text(number)
#             self._device.delay(3)
#             self._logger.debug('input sms content:'+content)
#             self._device(className='android.widget.EditText').click()
#             self._device.delay(2)
#             self._device.shell_dos("adb -s "+self._device.get_device_serial()+" shell input text "+content)
#             self._device.delay(2)
#             self._device.press.menu()
#             self._device.delay(2)
#             if self._device(text='Add subject').exists:
#                 self._device(text='Add subject').click()
#                 self._device.delay(3)
#                 self._device.press(41)
#                 self._device.press(41)
#                 self._device.press(47)
#                 self._device.delay(2)
#             if self._device(resourceId='com.android.mms:id/attach_button_sms').exists:
#                 self._device(resourceId='com.android.mms:id/attach_button_sms').click()
#                 self._device.delay(1)
#             if self._device(description ='Attach').exists:
#                 self._device(description ='Attach').click()
#                 self._device.delay(1)
#                 
#             if pic!=None: 
#                 self._logger.debug('add a picture')
#                 self._device(text='Pictures').click()
#                 self._device.delay(2)
#                 if not self._device(text='File Manager').exists:
#                     self._device(text='Recent').click()
#                     self._device.delay(1)
#                 self._device(text='File Manager').click()
#                 self._device.delay(2)
#                 self._device(text='Phone storage').click()
#                 self._device.delay(2)
#                 self._logger.debug('drag 200,600,200,300')
#                 #self._device.shell_adb('shell input swipe 200 600 200 300')
#                 self._device(scrollable=True).scroll.vert.forward(steps=10)
#                 self._device.delay(2)
#                 maxloop=0
#                 while not self._device(textContains='Attachment').exists:
#                     if maxloop>5:
#                         self._logger.debug('Can not find Attachment folder')
#                         return False
#                     #self._device.shell_adb('shell input swipe 200 600 200 300')
#                     self._device(scrollable=True).scroll.vert.forward(steps=10)
#                     self._device.delay(2)
#                     maxloop+=1
#                 self._device(textContains='Attachment').click()
#                 self._device.delay(1)
#                 self._device(textContains='jpg').click()
#                 self._device.delay(2)                 
#             if video!=None:
#                 self._logger.debug('add a video')
#                 self._device(text='Videos').click()
#                 self._device.delay(2)
#                 if not self._device(text='File Manager').exists:
#                     self._device(text='Recent').click()
#                     self._device.delay(1)
#                 self._device(text='File Manager').click()
#                 self._device.delay(2)
#                 self._device(text='Phone storage').click()
#                 self._device.delay(2)
#                 maxloop=0
#                 while not self._device(textContains='Attachment').exists:
#                     if maxloop>5:
#                         self._logger.debug('Can not find Attachment folder')
#                         return False
#                     #self._device.shell_adb('shell input swipe 100 600 200 300')
#                     self._device(scrollable=True).scroll.vert.forward(steps=10)
#                     maxloop+=1
#                 self._device(textContains='Attachment').click()                
#                 self._device.delay(1)
#                 self._device(textContains='3gp').click()
#                 self._device.delay(2)                
#             if audio!=None:
#                 self._logger.debug('add an audio')
#                 self._device(text='Audio').click()
#                 self._device.delay(1)
#                 self._device(text='External audio').click()
#                 self._device.delay(1)
#                 self._device(text='File Manager').click()
#                 self._device.delay(1)
#                 self._device(text='Just once').click()
#                 self._device.delay(1)
#                 self._device(text='Phone storage').click()
#                 maxloop=0
#                 while not self._device(textContains='Attachment').exists:
#                     if maxloop>5:
#                         self._logger.debug('Can not find Attachment folder')
#                         return False
#                     #self._device.shell_adb('shell input swipe 100 600 200 300')
#                     self._device(scrollable=True).scroll.vert.forward(steps=10)
#                     maxloop+=1
#                 self._device(textContains='Attachment').click()
#                 self._device.delay(2)
#                 self._device(textContains='3gpp').click()
#                 self._device.delay(2)                  
#             self._logger.debug('send')    
#             if self._device(text='Send').exists:            
#                 self._device(text='Send').click()
#             if self._device(text='MMS').exists:            
#                 self._device(text='MMS').click()                
#             self._device.delay(1)
#             if (self._device(text='SENDING…').exists) and (not self._device(resourceId ='com.android.mms:id/delivered_indicator').wait.exists(timeout=10000)) and (self._device(textContains =':').wait.exists(timeout=300000)):
#                 self._logger.debug('MMS send success!!!')
#                 self._device.press.back()
#                 self._device.delay(1)
#                 self.back_to_message()
#                 return True
#         self._logger.debug('MMS send fail!!!')
#         self.back_to_message()
#         self._device.delay(1)
#         return False        
#         
#     def del_AllMessage(self):
#         """delete all message in current list
#               
#         author: li.huang
#         """
#         self._logger.debug('delete all message')
#         self._device.press.menu()
#         self._device.delay(1)
#         if self._device(text='Delete all threads').exists:
#             self._device(text='Delete all threads').click()
#             self._device.delay(1)
#             self._device(text='Delete').click()
#             self._device.delay(1)
#             if self._device(text='No conversations.').exists:
#                 self._logger.debug('message delete success!')
#                 return True
#         self._logger.debug('message delete fail!')
#         return False
#    
#     def VerifyMessageReceive(self,mdevice_NO,content):
#         """verify whether the message has received
#         argv: (str)mdevice_NO -- the telephone number of the sender
#               (str)content -- MMS content
#               
#         author: li.huang
#         """
#         self._logger.debug('verify whether the message has received')
#         if self.enter_message():
#             maxloop=0
#             while True:
#                 if self._device(textContains=mdevice_NO[7:10]).exists:
#                     self._device(textContains=mdevice_NO[7:10]).click()
#                     self._device.delay(2)
#                     maxtimes=0
#                     while self._device(text='Downloading').exists:
#                         self._logger.debug('Downloading...')
#                         self._device.delay(2)
#                         if maxtimes>=180:
#                             self._logger.debug('Message download fail')
#                             break
#                         maxtimes+=1
#                     if self._device(textContains=content).exists:
#                         self._logger.debug('message receive success!!!')
#                         self.back_to_message()
#                         return True
#                     else:
#                         self._logger.debug('Content of the message received is not correct!')
#                         break
#                 if maxloop>=180:
#                     self._logger.debug('message receive fail!!!')
#                     break
#                 maxloop+=1
#                 self._device.delay(1)
#         self.back_to_message()        
#         return False
    
    def select_messaging(self,strtype):
        """select message by specified index.
        
        @param (int)index : message order in the list
        @param (str)strtype: 'Audio', 'Video', 'Photo','Text'
        
        """
        msg_order = {'Audio':0,'Video':1,'Photo':2,'Text':3}
        if self._device(resourceId = 'android:id/list').exists\
            and self._device(resourceId = 'com.android.mms:id/from', instance = msg_order[strtype]).exists:
            self._logger.debug('Click index ' + str(msg_order[strtype]))
            self._device(resourceId = 'com.android.mms:id/from', instance = msg_order[strtype]).click()
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
                    or self._device(resourceId = 'com.google.android.apps.plus:id/photo_hashtag_fragment_container').exists:
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
                elif self._device(resourceId = 'com.google.android.apps.plus:id/videoplayer').exists:
                    if self._device(resourceId = 'com.google.android.apps.plus:id/videoplayer').wait.gone(timeout = 45000):
                        self._logger.debug('Open MMS video successfully.')
                        return True
            self._logger.debug('Open MMS video fail!')
            return False
        elif strtype == 'Audio':
            if self._device(resourceId = 'com.android.mms:id/play_slideshow_button').exists:
                self._device(resourceId = 'com.android.mms:id/play_slideshow_button').click()
                self._device.delay(2)
                if self._device(resourceId = 'com.android.mms:id/audio_icon').exists:
                    if self._device(resourceId = 'com.android.mms:id/audio_icon').wait.gone(timeout = 45000):
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
        self._logger.debug("Select message option %s." %(str_option)) 
        if not self._device(resourceId='com.android.mms:id/mms_layout_view_parent', instance = instance).exists:
            self._logger.debug('Can\'t find message')
            return False       
    
        try_long_click_times = 0
        while not self._device(resourceId = 'android:id/alertTitle', text ='Message options').exists:
            self._device(resourceId='com.android.mms:id/mms_layout_view_parent').long_click.bottomright()
            self._device.delay(2)
            try_long_click_times += 1
            if try_long_click_times > 3:
                self._logger.debug('Can\'t find Message options')
                return False
                
        if not self._device(resourceId = 'android:id/title', text = str_option).exists:
            self._logger.debug('Can\'t find option ' + str_option)
            return False      
        self._device(text=str_option).click()
        self._device.delay(3)
        return True
        
    def forward_messaging(self, sendNum, timeout,  instance = 0):
        """forward a messaging.
        
        @param sendNum: Number to receive the messaging.
        @param timeout: time to wait the messaging sent
        @param instance: the messaging index displaying in the thread

        """
        if not self.selcet_messaging_option('Forward'):
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
                      
        self.stay_in_messaging()
        
#         if self._device(resourceId = 'android:id/list').getChildCount() < 4:
        if self._device(resourceId = 'android:id/list').getChildCount() < 1: # for test SMS only
            self._logger.debug('Forward messaging fail!!!')
            return False
        
        self._device(resourceId = 'android:id/list').child(index=0).click()
        self._device.delay(2)
        if self._device(resourceId ='com.android.mms:id/history').exists:
            self._device(resourceId ='com.android.mms:id/history').scroll.toEnd() 
               
        self._logger.debug('message sending...')
        maxtime=0
        while self._device(textContains ='SENDING').exists:
            if self._device(textContains = 'Sent').exists:
                self._logger.debug('message send success!')
                return True
            if maxtime > timeout:
                self._logger.debug('Message send timeout!!!')
                return False
            self._device.delay(1)
            maxtime+=1
        if self._device(textContains = 'Sent').exists:
            self._logger.debug('message send success!')
            return True
        else:
            self._logger.debug('Message send fail!!!')
            return False
            
    def get_total_thread(self):
        """Get the number of the thread in current page
        @return:  number of threads 
        """
        thread_num = 0
        if self._device(resourceId = 'android:id/list').exists:
            thread_num = self._device(resourceId = 'android:id/list').getChildCount()
            self._logger.debug("The message thread is " + str(thread_num))
        return thread_num
    
    def delete_messaging_thread(self, index=0):
        """ Long press to delete message in the message list
        
        @param (int)index :  message order in the list

        """
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
            
            try_longclickthread_times = 0
            while not self._device(resourceId = 'android:id/title', text = 'Delete thread').exists:
                self._device(resourceId = 'com.android.mms:id/from',  instance = index).long_click()
                self._logger.debug("Long click the message thread.")
                self._device.delay(3)
                try_longclickthread_times += 1
                if try_longclickthread_times > 3:
                    self._logger.debug("Can't find the delete menu.")
                    return False
            self._device(resourceId = 'android:id/title', text = 'Delete thread').click()
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
        
        