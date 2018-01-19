# -*- coding: UTF-8 -*-
"""Gmail library for scripts.

"""

from common import Common

class Email(Common):

    """Provide common functions involved email."""
    
    def __init__(self, device, log_name):
        Common.__init__(self, device,log_name)
        self._ssid = None   
        
    def save_fail_img(self):
        """Save fail screenshot to Email Folder
        
        """
        self.save_img("Email")    
        
    def stay_in_email(self):
        """Keep in Email main page
        
        """
        maxtime = 0
        while (not self._device(resourceId ='com.google.android.gm:id/search').exists) and \
            (not self._device(resourceId ='com.google.android.gm:id/actionbar_search_button').exists):
            self._device.press.back()
            maxtime += 1
            if maxtime > 3:
                self._logger.debug("Can't back gmail")
                break
        if maxtime < 4:
            return True
        else:
            self._device.press.home()
            self._device.delay(2)
            self._logger.debug("Launch gmail.")
            if self.enter_app('Gmail'):
                self._device.delay(2)
                if self.get_current_packagename() == self.get_app_package_from_file('Gmail'):
                    maxtime = 0
                    while (not self._device(resourceId ='com.google.android.gm:id/search').exists) and \
                    (not self._device(resourceId ='com.google.android.gm:id/actionbar_search_button').exists):
                        self._device.press.back()
                        maxtime += 1
                        if maxtime > 3:
                            self._logger.debug("Can't back gmail")
                            break
                    if maxtime < 4:
                        self._logger.debug('Launch gamil successfully.')
                        return True
                    else:
                        self._logger.debug('Launch gamil main page fail.')
                        return False
                else:
                    self._logger.debug('Launch gamil fail.')
                    return False
            else:
                return False
            
    def enter_mailbox(self,box):
        """enter the box you want  
        @param (str)box: text of the box
              
        """
        self._logger.debug('enter the box: %s',box)
        try_open_times = 0
        while not self._device(resourceId='com.google.android.gm:id/mail_toolbar').child(text=box).exists:
#             if self._device(resourceId='com.android.email:id/dotdotdot').exists:
            if self._device(description='Navigate up').exists:
                self._device(description ='Navigate up').click()
            elif self._device(description='Open navigation drawer').exists:
                self._device(description ='Open navigation drawer').click()
            self._device(description ='com.google.android.gm:id/account_display_name').wait.exists(timeout=5000)
            if self._device(description = 'Hide accounts').exists:
                self._device(description = 'Hide accounts').click()
                self._device.delay(2)
            if self._device(resourceId = 'android:id/list').exists:
                if self._device(resourceId = 'android:id/list').child_by_text(box, allow_scroll_search=True, resourceId='com.google.android.gm:id/name').exists:
                    self._device(resourceId='com.google.android.gm:id/name',text=box).click()
            try_open_times += 1
            if try_open_times > 3:
                break
        if self._device(resourceId='com.google.android.gm:id/mail_toolbar').child(text=box).wait.exists(timeout=10000):
            return True
        else:
            self._logger.debug('enter %s fail!',box)
            return False
            
    def forward_email(self, index, address):
        """forward a email
        @param (str)address : email address you want to send
        @param (int)index :email index
              
        """
        if not self.check_not_empty(60):
            return False

        if self._device(description='Dismiss tip').exists:
            self._device(description='Dismiss tip').click()
            self._device.delay(1)
        self._logger.debug('creat an email')
        if not self.select_mail(index):
            return False   
        if self._device(resourceId = 'com.google.android.gm:id/forward').exists:
            self._device(resourceId = 'com.google.android.gm:id/forward').click()    
        elif self._device(resourceId = 'com.google.android.gm:id/overflow').exists:
            self._device(resourceId = 'com.google.android.gm:id/overflow').click()
            self._device.delay(2) 
            if not self._device(resourceId = 'com.google.android.gm:id/title', text = 'Forward').exists:
                self._logger.debug('Menu forward not exist.')
                return False
            self._device(resourceId = 'com.google.android.gm:id/title', text = 'Forward').click()
        else:
            self._logger.debug('Foward button not exist.')
            return False     
        self._device.delay(2)

        if self._device(resourceId='android:id/button1').exists:
            self._device(resourceId='android:id/button1').click()
        self._device.delay(3)
        
#         if not self._device(className='android.widget.MultiAutoCompleteTextView',description='To').exists:
        if not self._device(resourceId='com.google.android.gm:id/to').exists:
            self._logger.debug('Address edit not exists.')
            return False
        try_set_receiver_times = 0
#         while not self._device(className='android.widget.MultiAutoCompleteTextView',description='To').get_text().upper().find(address.upper()) > -1:
        while not self._device(resourceId='com.google.android.gm:id/to').get_text().upper().find(address.upper()) > -1:
            self._logger.debug('Input receiver.') 
            self._device.press.delete()
            self._device.delay(1)
#             self._device(className='android.widget.MultiAutoCompleteTextView',description='To').set_text(address)
            self._device(resourceId='com.google.android.gm:id/to').set_text(address)
            self._device.delay(2)
            self._device.press.enter()
            self._device.delay(2)
            try_set_receiver_times += 1
            if try_set_receiver_times > 3:
                self._logger.debug('Input receiver fail!')
                return False
            
        if not self._device(description='Send').exists:
            self._logger.debug('Can\'t find send button')
            return False
        self._device(description='Send').click()
        self._device.delay(2)
        self._logger.debug('email sending...')
        if self._device(resourceId='com.google.android.gm:id/delete').exists:
            self._device(description='Navigate up').click()
            self._device.delay(10)
        
        if not self.enter_mailbox('Outbox'):
            return False
        if not self.check_empty(100, 30):
            self._logger.debug('email send fail!!!')
            return False
        else:
            if not self.enter_mailbox('Sent'):
                return False
            if self.check_not_empty(100):
                self._logger.debug('email send success!!!')
                return True
        self._logger.debug('email send fail!!!')
        return False
    
    def delete_mail(self,box):
        """delete all email of the box  
        @param (str)box: text of the box
        
        """
        self._logger.debug('delete the mail of %s',box)

        if not self.enter_mailbox(box):
            return False
        maxtime=0
        while self.check_not_empty(100):
            if self.refresh_emailbox(60) <> 2:
                return False
            if box == 'Trash' and maxtime < 3:
                if self._device(description = 'More options').exists:
                    self._device(description = 'More options').click()
                    self._device.delay(2)
                if self._device(resourceId='com.google.android.gm:id/title', text = 'Empty Trash').exists:
                    self._device(resourceId='com.google.android.gm:id/title', text = 'Empty Trash').click()
                    self._device.delay(2)
                if self._device(resourceId='com.google.android.gm:id/empty_trash_spam_action').exists:
                    self._device(resourceId='com.google.android.gm:id/empty_trash_spam_action').click()
                    self._device.delay(2)
                if self._device(resourceId='android:id/button1', text = 'Delete').exists:
                    self._device(resourceId='android:id/button1', text = 'Delete').click()
                    self._device.delay(3)
            else:
                if self._device(resourceId='com.google.android.gm:id/conversation_list_view').child(className='android.widget.FrameLayout',instance = 0).exists:
                    if self._device(resourceId='com.google.android.gm:id/conversation_list_view').child(resourceId = 'com.google.android.gm:id/outbox').exists:
                        if self._device(resourceId='com.google.android.gm:id/conversation_list_view').getChildCount() == 1:
                            return True
                        else:
                            self._device(resourceId='com.google.android.gm:id/conversation_list_view').child(className='android.widget.FrameLayout',instance = 0).long_click()
                            self._device.delay(2)
                    else:
                        self._device(resourceId='com.google.android.gm:id/conversation_list_view').child(className='android.widget.FrameLayout',instance = 0).long_click()
                        self._device.delay(2)
                if self._device(description='Delete').exists:
                    self._device(description='Delete').click()
                    self._device.delay(2)
                if self._device(description='Discard failed').exists:
                    self._device(description='Discard failed').click()
                    self._device.delay(2)
            if self._device(resourceId='com.google.android.gm:id/empty_view').exists:
                break
            if maxtime>15:
                break
            maxtime+=1
        if self._device(resourceId='com.google.android.gm:id/empty_view').exists:
            self._logger.debug('mail of the %s has delete complete',box)
            return True
        else:
            return False
    
    def select_mail(self,index):
        """Select a email
        @param index: email index in the box
        
        """
        self._logger.debug('select the mail of %s',str(index))
        self._device(resourceId = 'com.google.android.gm:id/conversation_list_view').child(className='android.widget.FrameLayout',instance=index).click()
        self._device.delay(2)
        if self._device( descriptionContains ='Reply').wait.exists(timeout=10000):
            return True
        else:
            self._logger.debug('select mail fail!')
            return False
        
    def refresh_emailbox(self, wait_time):
        """refresh the box one time
        @param wait_time: time to wait refresh finish
        @return: 0--Fail; 1--Network error; 2--Successful
        
        """
        self._logger.debug("refresh mail box")
        if self._device(resourceId='com.google.android.gm:id/swipe_refresh_widget').exists:
            self._device(resourceId='com.google.android.gm:id/swipe_refresh_widget').swipe.down()
        maxtime=0
        while self._device(resourceId='com.google.android.gm:id/swipe_refresh_widget').getChildCount() == 2 \
         or self._device(resourceId='com.google.android.gm:id/background_view').exists\
         or self._device(className='android.widget.ProgressBar').exists\
         or self._device(resourceId = 'com.google.android.gm:id/conversation_list_loading_view').exists\
         or self._device(resourceId='com.google.android.gm:id/loading').exists:
            self._device.delay(1)
            if maxtime>wait_time:
                self._logger.debug("load mail failed")
                return 0
            maxtime+=1
        if self._device(resourceId='com.google.android.gm:id/error_text').exists:
            self._logger.debug("No connection or other error")
            return 1
#         elif self._device(resourceId = 'com.google.android.gm:id/empty_text', text = 'No connection').exists:
#             self._logger.debug("No connection error")
#             return 1
        else:
            return 2
        
    def check_empty(self, wait_time_refrese, wait_time_empty = 0):
        """if the box is empty, stop refresh
        
        @param wait_time: time to wait for the box empty for each refresh
        
        """
        for i in range(3):
            self.refresh_emailbox(wait_time_refrese)
            if self._device(resourceId='com.google.android.gm:id/empty_view').exists:
                self._logger.debug('The box is empty')
                return True
            if wait_time_empty <> 0:
                self._device.delay(wait_time_empty)
        self._logger.debug('The box is not empty')
        return False
    
    def check_not_empty(self, wait_time):
        """if the box is not empty, stop refresh
        
        @param wait_time: time to wait for the box not empty for each refresh
        
        """
        for i in range(3):
            self.refresh_emailbox(wait_time)
            if not self._device(resourceId='com.google.android.gm:id/empty_view').exists:
                self._logger.debug('The box is not empty')
                return True
        self._logger.debug('The box is empty')
        return False
    
#     def test(self, address):
#         self._device(resourceId='com.android.email:id/forward').click()
#         self._device.delay(2)
#         if self._device(resourceId='android:id/button1').exists:
#             self._device(resourceId='android:id/button1').click()
#         self._device.delay(3)
#         self._device(className='android.widget.MultiAutoCompleteTextView',description='To').set_text(address)
#         self._device.delay(2)
#         self._device(description='Send').click()
#         self._device.delay(2)
#         self._logger.debug('email sending...')
#         if self._device(resourceId='com.android.email:id/forward').exists:
#             self._device.delay(10)