# -*- coding: UTF-8 -*-
"""Email library for scripts.

"""

from common import Common


class Email(Common):
    """Provide common functions involved email."""

    def __init__(self, device, log_name):
        Common.__init__(self, device, log_name)
        self._ssid = None

    def save_fail_img(self):
        """Save fail screenshot to Email Folder
        
        """
        self.save_img("Email")

    def stay_in_email(self):
        """Keep in Email main page
        
        """
        maxtime = 0
        while True:
            if self._device(packageName='com.tct.email', description='Open navigation drawer').exists \
                    or self._device(resourceId='com.tct.email:id/avatar').exists:
                break
            else:
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
                    maxtime = 0
                    while True:
                        if self._device(description='Open navigation drawer').exists \
                                or self._device(resourceId='com.tct.email:id/avatar').exists:
                            self._logger.debug('Launch eamil main page successfully.')
                            return True
                        else:
                            self._device.press.back()
                            maxtime += 1
                            if maxtime > 3:
                                self._logger.debug('Launch eamil main page fail.')
                                return False
                else:
                    self._logger.debug('Launch eamil fail.')
                    return False
            else:
                return False

    def enter_mailbox(self, box):
        """enter the box you want  
        @param (str)box: text of the box
              
        """
        self._logger.debug('enter the box: %s', box)
        try_open_times = 0
        #         while not self._device(resourceId='com.tct.email:id/action_bar').child(text=box).exists:
        while not self._device(resourceId='com.tct.email:id/mail_toolbar').child(text=box).exists:
            #             if self._device(resourceId='com.android.email:id/dotdotdot').exists:
            if self._device(description='Open navigation drawer').exists:
                self._device(description='Open navigation drawer').click()
                self._device.delay(2)
                self._device(resourceId='com.tct.email:id/avatar').wait.exists(timeout=5000)
            if self._device(resourceId='com.tct.email:id/name', text=box).exists:
                self._device(resourceId='com.tct.email:id/name', text=box).click()
                self._device.delay(2)
            try_open_times += 1
            if try_open_times > 3:
                break
        if self._device(resourceId='com.tct.email:id/mail_toolbar').child(text=box).wait.exists(timeout=10000):
            #         if self._device(resourceId='com.tct.email:id/action_bar').child(text=box).wait.exists(timeout=10000):
            return True
        else:
            self._logger.debug('enter %s fail!', box)
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
        if self._device(resourceId='com.tct.email:id/forward').exists:
            self._device(resourceId='com.tct.email:id/forward').click()
        elif self._device(resourceId='com.tct.email:id/forward_button').exists:
            self._device(resourceId='com.tct.email:id/forward_button').click()
        elif self._device(resourceId='com.tct.email:id/overflow').exists:
            self._device(resourceId='com.tct.email:id/overflow').click()
            self._device.delay(2)
            if self._device(resourceId='android:id/title', text='Forward').exists:
                self._device(resourceId='android:id/title', text='Forward').click()
        else:
            self._logger.debug('Can\'t find the forward button!')
            return False
        self._device.delay(2)
        if self._device(resourceId='android:id/button1').exists:
            self._device(resourceId='android:id/button1').click()
        self._device.delay(3)

        try_set_receiver_times = 0
        while not self._device(className='android.widget.MultiAutoCompleteTextView',
                               description='To').get_text().upper().find(address.upper()) > -1:
            self._logger.debug('Input receiver.')
            self._device(resourceId='com.tct.email:id/to').clear_text()
            self._device.delay(1)
            self._device(resourceId='com.tct.email:id/to').set_text(address)
            #             self._device(className='android.widget.MultiAutoCompleteTextView',description='To').set_text(address)
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
        if self._device(resourceId='com.tct.email:id/forward').exists \
                or self._device(resourceId='com.tct.email:id/forward_button').exists \
                or self._device(resourceId='com.tct.email:id/delete').exists:
            self._device(description='Navigate up').click()
            self._device.delay(5)

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

    def delete_mail(self, box):
        """delete all email of the box  
        @param (str)box: text of the box
        
        """
        self._logger.debug('delete the mail of %s', box)

        if not self.enter_mailbox(box):
            return False
        maxtime = 0
        while self.check_not_empty(100):
            if self.refresh_emailbox(60) <> 2:
                return False
            if box == 'Trash':
                if self._device(resourceId='com.tct.email:id/empty_trash').exists:
                    self._device(resourceId='com.tct.email:id/empty_trash').click()
                    self._device.delay(2)
                if self._device(resourceId='android:id/button1', text='DELETE').exists:
                    self._device(resourceId='android:id/button1', text='DELETE').click()
                    self._device.delay(3)
            else:
                index = 1
                if self._device(resourceId='com.tct.email:id/conversation_list_view').child(
                        className='android.widget.FrameLayout', instance=index).exists:
                    if self._device(resourceId='com.tct.email:id/conversation_list_view').child(
                            resourceId='com.tct.email:id/outbox').exists:
                        if self._device(resourceId='com.tct.email:id/conversation_list_view').getChildCount() == 1:
                            return True
                        else:
                            self._device(resourceId='com.tct.email:id/conversation_list_view').child(
                                className='android.widget.FrameLayout', instance=index).long_click()
                            self._device.delay(2)
                    else:
                        self._device(resourceId='com.tct.email:id/conversation_list_view').child(
                            className='android.widget.FrameLayout', instance=index).long_click()
                        self._device.delay(2)
                if self._device(description='Select all').exists:
                    self._device(description='Select all').click()
                    self._device.delay(2)
                if self._device(description='Delete').exists:
                    self._device(description='Delete').click()
                    self._device.delay(2)
                if self._device(description='Discard failed').exists:
                    self._device(description='Discard failed').click()
                    self._device.delay(2)
                if self._device(resourceId='android:id/button1', text='OK').exists:
                    self._device(resourceId='android:id/button1', text='OK').click()
                    self._device.delay(2)
            if self._device(resourceId='com.tct.email:id/empty_text').exists:
                break
            if maxtime > 30:
                break
            maxtime += 1
        if self._device(resourceId='com.tct.email:id/empty_text').exists:
            self._logger.debug('mail of the %s has delete complete', box)
            return True
        else:
            return False

    def select_mail(self, index):
        """Select a email
        @param index: email index in the box
        
        """
        self._logger.debug('select the mail of %s', str(index))

        try_time = 0
        while True:
            item_count = self._device(className='android.widget.ListView').getChildCount()
            if item_count == 0:
                self.refresh_emailbox(30)
                try_time += 1
            else:
                if item_count == 1 and index == 1:
                    self._logger.debug('Only one email in, choose this one.')
                    index = 0
                self._device(className='android.widget.ListView').child(className='android.widget.FrameLayout',
                                                                        instance=index).click()
                self._device.delay(2)
                break

            if try_time > 3:
                self._logger.debug('Can\'t get the mail items.')
                return False

        if not self._device(description='Delete').wait.exists(timeout=3000):
            self._device(resourceId='com.tct.email:id/conversation_pager').swipe.down()
            self._device.delay(2)
            self._device(resourceId='com.tct.email:id/conversation_pager').swipe.right()
            self._device.delay(2)

        if self._device(description='Delete').wait.exists(timeout=3000):
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
        if self._device(resourceId='com.tct.email:id/swipe_refresh_widget').exists:
            #             self._device(resourceId='com.tct.email:id/swipe_refresh_widget').swipe.down()
            self._device.swipe(924, 267, 924, 800, steps=5)
        maxtime = 0
        while self._device(resourceId='com.tct.email:id/swipe_refresh_widget').getChildCount() == 2 \
                or self._device(resourceId='com.tct.email:id/background_view').exists \
                or self._device(className='android.widget.ProgressBar').exists \
                or self._device(resourceId='com.tct.email:id/loading').exists:
            self._device.delay(1)
            if maxtime > wait_time:
                self._logger.debug("load mail failed")
                return 0
            maxtime += 1
        if self._device(resourceId='com.tct.email:id/error_text').exists:
            self._logger.debug("No connection or other error")
            return 1
        else:
            return 2

    def check_empty(self, wait_time_refrese, wait_time_empty=0):
        """if the box is empty, stop refresh
        
        @param wait_time: time to wait for the box empty for each refresh
        
        """
        for i in range(3):
            self.refresh_emailbox(wait_time_refrese)
            if self._device(resourceId='com.tct.email:id/empty_view').exists:
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
            if not self._device(resourceId='com.tct.email:id/empty_view').exists:
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
