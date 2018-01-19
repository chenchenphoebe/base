# -*- coding: UTF-8 -*-
"""Telephony library for scripts.
"""
from common import Common


class Phone(Common):
    """Provide common functions for scripts, such as launching activity."""

    def __init__(self, device, log_name):
        Common.__init__(self, device, log_name)
        self._ssid = None

    def stay_in_call(self, option=''):
        """Keep in Call main page
    
               @param option: the option of lists_pager_header
    
        """
        if self.get_current_packagename() == self.get_app_package_from_file('Call'):
            if option == 'Call':
                if self._device(text='Return to call in progress').exists:
                    self._device(text='Return to call in progress').click()
                    self._device.delay(2)
                if self._device(resourceId='com.android.dialer:id/elapsedTime').wait.exists(timeout=10000) \
                        and self._device(resourceId='com.android.dialer:id/floating_end_call_action_button').exists:
                    self._logger.debug('In calling')
                    return True

            maxtime = 0
            while not self._device(resourceId='com.android.dialer:id/lists_pager_header').exists:
                self._device.press.back()
                self._device.delay(1)
                maxtime += 1
                if maxtime > 3:
                    self._logger.debug("Can't back Call")
                    break
            if maxtime < 4:
                if option <> '':
                    if self._device(description=option).exists:
                        if self._device(description=option).exists:
                            if not self._device(description=option).isSelected():
                                self._device(description="Speed dial").click()
                                self._device.delay(3)
                                self._device(description=option).click()
                                self._device.delay(3)
                                if self._device(description=option).isSelected():
                                    self._logger.debug("%s is Selected", option)
                                    return True
                                else:
                                    self._logger.debug("%s isn\' Selected", option)
                                    return False

                            elif self._device(description=option).isSelected():
                                self._logger.debug("%s is Selected", option)
                                return True
                    else:
                        self._logger.debug("Can't get the %s option.", option)
                        return False
                else:
                    return True

        self._logger.debug("Launch Call.")
        if self.enter_app('Call'):
            self._device.delay(2)
            if self.get_current_packagename() == self.get_app_package_from_file('Call'):
                if option == ' ':
                    if self._device(text='Return to call in progress').exists:
                        self._device(text='Return to call in progress').click()
                        self._device.delay(2)
                    if self._device(resourceId='com.android.dialer:id/elapsedTime').wait.exists(timeout=10000) \
                            and self._device(resourceId='com.android.dialer:id/floating_end_call_action_button').exists:
                        self._logger.debug('In calling')
                        return True
                maxtime = 0
                while not self._device(resourceId='com.android.dialer:id/lists_pager_header').exists:
                    self._device.press.back()
                    self._device.delay(1)
                    maxtime += 1
                    if maxtime > 3:
                        self._logger.debug("Can't back Call")
                        break
                if maxtime < 4:
                    if option <> '':
                        if self._device(description=option).exists:
                            if self._device(description=option).exists:
                                if not self._device(description=option).isSelected():
                                    self._device(description="Speed dial").click()
                                    self._device.delay(3)
                                    self._device(description=option).click()
                                    self._device.delay(3)
                                if self._device(description=option).isSelected():
                                    self._logger.debug("%s is Selected", option)
                                    return True
                                else:
                                    self._logger.debug("%s isn\' Selected", option)
                                    return False

                            elif self._device(description=option).isSelected():
                                self._logger.debug("%s is Selected", option)
                                return True
                        else:
                            self._logger.debug("Can't get the %s option.", option)
                            return False
                    else:
                        return True
            else:
                self._logger.debug('Launch Call main page fail')
                return False
        else:
            return False

    def call_from_callLog(self, option):
        if option == 'Speed dial':
            self.stay_in_call('Speed dial')
            if self._device(resourceId='com.android.dialer:id/empty_list_view').exists:
                self._logger.debug('No call log in dialer')
                return False
            elif not self._device(resourceId='com.android.dialer:id/contact_favorite_card').exists:
                self._logger.debug('No favorite contact in dialer')
                return False
            else:
                self._device(resourceId='com.android.dialer:id/contact_favorite_card').click()

        elif option == 'Recent':
            self.stay_in_call('Recent')

            """if self._device(resourceId = 'com.android.dialer:id/lists_pager_header').exists:
                if self._device(text = 'All').exists:
                    self._device(text = 'All').click()
                    self._device.delay(2)
                    if not self._device(text = 'All').isSelected():
                        self._logger.debug("Can't get the recent all option.")
                        return False"""

            if self._device(resourceId='com.android.dialer:id/emptyListViewMessage').exists:
                self._logger.debug('No call log in dialer')
                return False
            try_time = 0
            #             while not self._device(resourceId = 'com.android.dialer:id/call_back_action').exists:
            while self._device(resourceId='com.android.dialer:id/primary_action_view').exists:
                #                 if not self._device(resourceId = 'com.android.dialer:id/name').exists:
                if not self._device(resourceId='com.android.dialer:id/primary_action_view').exists:
                    self._logger.debug('No recent contact in dialer.')
                    return False
                #                 self._device(resourceId = 'com.android.dialer:id/name').click()
                self._device(resourceId='com.android.dialer:id/call_back_action').click()
                self._device.delay(2)
                try_time += 1
                if try_time > 3:
                    #                     self._logger.debug('Call back button not exist.')
                    self._logger.debug('Can\'t start call.')
                    return False
                #             try_time = 0
                #             while self._device(resourceId = 'com.android.dialer:id/call_back_action').exists:
                #                 self._device(resourceId = 'com.android.dialer:id/call_back_action').click()
                #                 self._device.delay(2)
                #                 try_time += 1
                #                 if try_time > 5:
                #                     self._logger.debug('Still in calllog. Can\'t start call' )
                #                     return False
        else:
            self._logger.debug('Call option not exist.')
            return False

        if self._device(resourceId='com.android.dialer:id/elapsedTime').wait.exists(timeout=30000) \
                and self._device(resourceId='com.android.dialer:id/floating_end_call_action_button').exists:
            self._logger.debug('In calling')
            self._device.delay(10)
            self._device(resourceId='com.android.dialer:id/floating_end_call_action_button').click()
            #            if self._device(resourceId = com.android.dialer:id/primary_action_view').wait.exists(timeout=10000):
            if self._device(resourceId='com.android.dialer:id/primary_action_view').wait.exists(
                    timeout=10000):  # edit by yale
                self._logger.debug('End call.')
                return True
            else:
                self._logger.debug('End call fail.')
                return False
        else:
            self._logger.debug('Start call fail.')
            return False

    def call_from_dailerpad(self, number):
        self.stay_in_call('Call')
        if self._device(text='Return to call in progress').exists:
            self._device(text='Return to call in progress').click()
            self._device.delay(2)
        if self._device(resourceId='com.android.dialer:id/elapsedTime').wait.exists(timeout=10000) \
                and self._device(resourceId='com.android.dialer:id/floating_end_call_action_button').exists:
            self._logger.debug('In calling')
            self._device(resourceId='com.android.dialer:id/floating_end_call_action_button').click()
            if not self._device(resourceId='com.android.dialer:id/floating_end_call_action_button').wait.exists(
                    timeout=10000):
                self._logger.debug('End call.')

        if not self._device(resourceId='com.android.dialer:id/hide_Image_view1').exists:
            self.enter_app("Call")
        self._device.delay(2)

        for i in list(number):
            self._device(description=i).click()
            self._device.delay(1)

        if self._device(resourceId='com.android.dialer:id/digits').exists:
            #             self._device(resourceId = 'com.android.dialer:id/digits').clear_text()
            #             self._device.delay(2)
            #             self._device(resourceId = 'com.android.dialer:id/digits').set_text(number)
            self._device.delay(2)
            if not self._device(resourceId='com.android.dialer:id/digits').get_text().replace(' ', '').replace('-',
                                                                                                               '').replace(
                    '(', '').replace(')', '') == number:
                self._logger.debug('Input number fail.')
                return False

            if self._device(resourceId='com.android.dialer:id/dialpad_floating_action_button').exists:
                self._device(resourceId='com.android.dialer:id/dialpad_floating_action_button').click()
            elif self._device(resourceId='com.android.dialer:id/dialpad_floating_action_button_single').exists:
                self._device(resourceId='com.android.dialer:id/dialpad_floating_action_button_single').click()
            elif self._device(description='Dial').exists:
                self._device(description='Dial').click()
            elif self._device(description='dial').exists:
                self._device(description='dial').click()
            else:
                self._logger.debug('Dialer button not exist.')
                return False

            if self._device(resourceId='com.android.dialer:id/elapsedTime').wait.exists(timeout=30000) \
                    and self._device(resourceId='com.android.dialer:id/floating_end_call_action_button').exists:
                self._logger.debug('In calling')
                return True
            else:
                self._logger.debug('Start call fail.')
                return False
        else:
            self._logger.debug('Can\'t go to DialerPad.')
            return False

    def end_call(self):

        if self._device.press_endcall():
            return True

        return False

        self.stay_in_call('call')
        if not (self._device(resourceId='com.android.dialer:id/elapsedTime').exists \
                        and self._device(resourceId='com.android.dialer:id/floating_end_call_action_button').exists):
            self._logger.debug('Not in calling')
            return False
        else:
            self._device(resourceId='com.android.dialer:id/floating_end_call_action_button').click()
            if not self._device(resourceId='com.android.dialer:id/floating_end_call_action_button').wait.exists(
                    timeout=10000):
                self._logger.debug('End call.')
                return True
