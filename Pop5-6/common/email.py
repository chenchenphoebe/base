# -*- coding: UTF-8 -*-
"""Email library for scripts.

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

#     def email_accountSet(self,accountName,password):
#         """login email account
#         argv: (str)accountName --email account name
#               (str)password -- email account password
#               
#         author: li.huang
#         """ 
#         self._logger.debug('set email account')
#         self._device.start_activity(email_package,email_login)
#         self._device.delay(2)
#         if not self._device(text='Account setup').exists:
#             self._logger.debug('Launch Message fail')
#         else:
#             if self._device(text='Email address').exists:
#                 self._logger.debug('input account name: %s',accountName)
#                 self._device(text='Email address').set_text(accountName)
#                 self._device.delay(3)
#                 if self._device(className='android.widget.EditText',index=4).exists:
#                     self._logger.debug('input pass word: %s',password)
#                     self._device(className='android.widget.EditText',index=4).set_text(password)
#                     self._device.delay(3)
#                     self._device(text='Next').click()
#                     if self._device(text='Next').wait.exists(timeout=60000):
#                         self._device(text='Next').click()
#                     if self._device(description='Your name (displayed on outgoing messages)').wait.exists(timeout=60000):
#                         self._logger.debug('input name: Tester')
#                         self._device(description='Your name (displayed on outgoing messages)').set_text('Tester')
#                         self._device.delay(5)
#                     if self._device(text='Next').wait.exists(timeout=60000):
#                         self._device(text='Next').click()
#                         self._device.delay(2)
#                     if self._device(text=accountName).exists:
#                         self._logger.debug('email login success!!!')
#                         return True
#                     else:
#                         self._device.press.home()
#                         self._device.delay(2)
#                         self._device.start_activity(email_package,email_activity)
#                         self._device.delay(2)
#                         if self._device(text=accountName).wait.exists(timeout=60000):
#                             self._logger.debug('email login success!!!')
#                             return True
#         self._logger.debug('email login fail')           
#         return False
        
    def stay_in_email(self):
        """Keep in Email main page
        
        """
        maxtime = 0
        while not  self._device(description ='Open navigation drawer').exists:
            self._device.press.back()
            maxtime += 1
            if maxtime > 3:
                self._logger.debug("Can't back email")
                break
        if maxtime < 4:
            return True
        else:
            self._device.press.home()
            self._device.delay(2)
            self._logger.debug("Launch email.")
            if self.enter_app('Email'):
                self._device.delay(2)
                if self.get_current_packagename() == self.get_app_package_from_file('Email'):
                    self._logger.debug('Launch eamil successfully.')
                    return True
                else:
                    self._logger.debug('Launch eamil fail.')
                    return False
            else:
                return False
            
    def enter_mailbox(self,box):
        """enter the box you want  
        @param (str)box: text of the box
              
        """
        self._logger.debug('enter the box: %s',box)
        try_open_times = 0
        while not self._device(resourceId='com.android.email:id/action_bar').child(text=box).exists:
#             if self._device(resourceId='com.android.email:id/dotdotdot').exists:
            if self._device(description='Open navigation drawer').exists:
                self._device(description ='Open navigation drawer').click()
                self._device.delay(2)
                self._device(description ='Close navigation drawer').wait.exists(timeout=5000)
            if self._device(resourceId='com.android.email:id/name',text=box).exists:
                self._device(resourceId='com.android.email:id/name',text=box).click()
                self._device.delay(2)
            try_open_times += 1
            if try_open_times > 3:
                break
        if self._device(resourceId='com.android.email:id/action_bar').child(text=box).wait.exists(timeout=10000):
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
        self._device.delay(2)
        self._device(resourceId='com.android.email:id/forward').click()
        self._device.delay(2)
        if self._device(resourceId='android:id/button1').exists:
            self._device(resourceId='android:id/button1').click()
        self._device.delay(3)
        
        try_set_receiver_times = 0
        while address <> self._device(className='android.widget.MultiAutoCompleteTextView',description='To').get_text():
            self._logger.debug('Input receiver.')
            self._device(className='android.widget.MultiAutoCompleteTextView',description='To').set_text(address)
            self._device.delay(2)
            try_set_receiver_times += 1
            if try_set_receiver_times > 3:
                self._logger.debug('Input receiver fail!')
                return False
            
        if not  self._device(description='Send').exists:
            self._logger.debug('Can\'t find send button')
            return False
        self._device(description='Send').click()
        self._device.delay(2)
        self._logger.debug('email sending...')
        if self._device(resourceId='com.android.email:id/forward').exists:
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
            if box == 'Trash':
                if self._device(resourceId='com.android.email:id/empty_trash').exists:
                    self._device(resourceId='com.android.email:id/empty_trash').click()
                    self._device.delay(2)
                if self._device(resourceId='android:id/button1', text = 'Delete').exists:
                    self._device(resourceId='android:id/button1', text = 'Delete').click()
                    self._device.delay(3)
            else:
                if self._device(resourceId='com.android.email:id/conversation_list_view').child(className='android.widget.FrameLayout',instance = 0).exists:
                    if self._device(resourceId='com.android.email:id/conversation_list_view').child(resourceId = 'com.android.email:id/outbox').exists:
                        if self._device(resourceId='com.android.email:id/conversation_list_view').getChildCount() == 1:
                            return True
                        else:
                            self._device(resourceId='com.android.email:id/conversation_list_view').child(className='android.widget.FrameLayout',instance = 0).long_click()
                            self._device.delay(2)
                    else:
                        self._device(resourceId='com.android.email:id/conversation_list_view').child(className='android.widget.FrameLayout',instance = 0).long_click()
                        self._device.delay(2)
                if self._device(description='Delete').exists:
                    self._device(description='Delete').click()
                    self._device.delay(2)
                if self._device(description='Discard failed').exists:
                    self._device(description='Discard failed').click()
                    self._device.delay(2)
            if self._device(resourceId='com.android.email:id/empty_view').exists:
                break
            if maxtime>30:
                break
            maxtime+=1
        if self._device(resourceId='com.android.email:id/empty_view').exists:
            self._logger.debug('mail of the %s has delete complete',box)
            return True
        else:
            return False
    
    def select_mail(self,index):
        """Select a email
        @param index: email index in the box
        
        """
        self._logger.debug('select the mail of %s',str(index))
        self._device(className='android.widget.ListView').child(className='android.widget.FrameLayout',instance=index).click()
        self._device.delay(2)
        if self._device(description='Reply').wait.exists(timeout=10000):
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
        if self._device(resourceId='com.android.email:id/swipe_refresh_widget').exists:
            self._device(resourceId='com.android.email:id/swipe_refresh_widget').swipe.down()
        maxtime=0
        while self._device(resourceId='com.android.email:id/swipe_refresh_widget').getChildCount() == 2 \
         or self._device(resourceId='com.android.email:id/background_view').exists\
         or self._device(className='android.widget.ProgressBar').exists\
         or self._device(resourceId='com.android.email:id/loading').exists:
            self._device.delay(1)
            if maxtime>wait_time:
                self._logger.debug("load mail failed")
                return 0
            maxtime+=1
        if self._device(resourceId='com.android.email:id/error_text').exists:
            self._logger.debug("No connection or other error")
            return 1
        else:
            return 2
        
    def check_empty(self, wait_time_refrese, wait_time_empty = 0):
        """if the box is empty, stop refresh
        
        @param wait_time: time to wait for the box empty for each refresh
        
        """
        for i in range(3):
            self.refresh_emailbox(wait_time_refrese)
            if self._device(resourceId='com.android.email:id/empty_view').exists:
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
            if not self._device(resourceId='com.android.email:id/empty_view').exists:
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