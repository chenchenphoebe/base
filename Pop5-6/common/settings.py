# -*- coding: UTF-8 -*-
"""Settings library for scripts.
"""
import os
from common import Common

Wifi = u'Wi\u2011Fi'


# Wifi = 'Wi-Fi'

class Settings(Common):
    """Provide common functions involved wifi,display,sound etc."""

    def __init__(self, device, log_name):
        Common.__init__(self, device, log_name)
        self._ssid = None

    def save_fail_img(self):
        """Save fail screenshot to WiFi Folder
        
        """
        self.save_img("Settings")

    def enterSettings(self, option):
        '''enter the option of settings
        
         @param option: the text of the settings option
         
        '''
        if self.enter_app('Settings'):
            if self._device(text=option).exists:
                self._logger.debug("enter " + option + " setting")
                self._device(text=option).click()
                self._device.delay(2)
            else:
                self._device(scrollable=True).scroll.vert.forward(steps=10)
                self._logger.debug("enter " + option + " setting")
                self._device(text=option).click()
                self._device.delay(2)
            if self._device(text=option).exists:
                return True
        return False

    def stayInSetting(self, option):
        """Stay in setting option page
        
        @param option: the option of settings
        
        """
        if self._device(resourceId='com.android.settings:id/action_bar').child(text=option).exists:
            return True
        else:
            for i in range(3):
                self._device.press.back()
                self._device.delay(1)
                if self._device(resourceId='com.android.settings:id/action_bar').child(text='Settings').exists:
                    if self._device(text=option).exists:
                        self._logger.debug("enter " + option + " setting")
                        self._device(text=option).click()
                        self._device.delay(2)
                        if self._device(resourceId='com.android.settings:id/action_bar').child(text=option).exists:
                            return True
            self._device.press.home()
            self.enterSettings(option)
            if self._device(resourceId='com.android.settings:id/action_bar').child(text=option).exists:
                return True
            else:
                self._logger.debug("enter " + option + " setting failed")
                return False

    def scroll_find_ap(self, name):
        """find the file given
        
        @param name: file or folder name
        
        """
        if self._device(resourceId='android:id/title', text=name).exists:
            return True

        if self._device(resourceId='com.android.settings:id/list', scrollable='true').exists:
            self._device(resourceId='com.android.settings:id/list').scroll.toBeginning()

            if not self._device(resourceId='android:id/title').exists:
                self._logger.debug("Can't get the item name1")
                return False
            first_folder_name = self._device(resourceId='android:id/title', instance=0).get_text()

            scroll_time = 0
            while True:
                if self._device(resourceId='android:id/title', text=name).exists:
                    return True
                else:
                    self._device(resourceId='com.android.settings:id/list').scroll.vert.forward()
                    self._logger.debug("Scroll one time.")
                    scroll_time += 1

                if not self._device(resourceId='android:id/title').exists:
                    self._logger.debug("Can't get the item name1")
                    return False
                first_folder_name_current = self._device(resourceId='android:id/title', instance=0).get_text()
                if first_folder_name == first_folder_name_current:
                    self._logger.debug("It's list bottom. Can't find the item name1.")
                    return False
                else:
                    first_folder_name = first_folder_name_current

                if scroll_time > 20:
                    self._logger.debug("Too more ap.Stop finding.")
                    return False
        else:
            self._logger.debug("Can't find the item name2.")
            return False

    def connect_wifi(self, hotspotName, password):
        '''device connect wifi hotspot
         @param (str)hotspotName: the wifi hotspot's name 
         @param (str)password: the wifi hotspot's password
               
        '''
        if self._device(textContains='Connected').wait.exists(timeout=10000):
            self._logger.debug('wifi has connected.')
            return True
        else:
            self.scroll_find_ap('Add network')
            self._device.delay(1)
            self._device(text='Add network').click()
            self._device.delay(2)
            self._device(resourceId='com.android.settings:id/ssid').set_text(hotspotName)
            self._device.delay(2)
            if self._device(text='Open').exists:
                self._device(text='Open').click()
                self._device.delay(2)
            elif self._device(text='None').exists:
                self._device(text='None').click()
                self._device.delay(2)
            if not self._device(text='WPA/WPA2 PSK').exists:
                self._logger.debug('WPA/WPA2 PSK is not exist.')
                return False
            self._device(text='WPA/WPA2 PSK').click()
            self._device.delay(2)
            self._device(resourceId='com.android.settings:id/password').set_text(password)
            self._device.delay(2)
            self._device(resourceId='android:id/button1').click()
            self._device.delay(2)
            self._device(scrollable=True).scroll.vert.toBeginning(steps=100, max_swipes=1000)
            if self._device(textContains="Connected").wait.exists(timeout=30000):
                # and (not self._device(textContains='problem').wait.exists(timeout=5000))and(not self._device(textContains='Saved').wait.exists(timeout=5000)):
                self._logger.debug('wifi connect success!!!')
                return True
            else:
                self._logger.debug('wifi connect fail!!!')
                return False

    def wifi_switch(self):
        """Trun on or off wifi
        
        """
        self._logger.debug('Switch wifi')
        if self._device(checked='false', className='android.widget.Switch'):
            self._device(className='android.widget.Switch').click()
            self._device.delay(3)
            if not self._device(textContains='To see available networks').wait.exists(timeout=15000):
                self._logger.debug('wifi is turned on')
                return True
            else:
                self._logger.debug('Trun on wifi fail!!!')
                return False
        if self._device(checked='true', className='android.widget.Switch'):
            self._device(className='android.widget.Switch').click()
            self._device.delay(3)
            if self._device(textContains='To see available networks').wait.exists(timeout=5000):
                self._logger.debug('wifi is turned off')
                return True
            else:
                self._logger.debug('Turn off wifi fail!!!')
                return False

        self._logger.debug('Can\'t find the wifi switch!!!')
        return False

    def wifi_open(self):
        """Turn on WiFi
        
        """
        self._logger.debug('Open wifi')
        if self._device(checked='false', className='android.widget.Switch'):
            self._device(className='android.widget.Switch').click()
            self._device.delay(2)
            if not self._device(textContains='To see available networks').wait.exists(timeout=15000):
                self._logger.debug('wifi is turned on')
                return True
            else:
                self._logger.debug('Turn on wifi fail!!!')
                return False
        elif self._device(checked='true', className='android.widget.Switch'):
            self._logger.debug('wifi already on')
            return True
        else:
            self._logger.debug('Can\'t find the wifi switch!!!')
            return False

    def wifi_close(self):
        """Turn off WiFi
        
        """
        self._logger.debug('Close wifi')
        if self._device(checked='true', className='android.widget.Switch'):
            self._device(className='android.widget.Switch').click()
            self._device.delay(2)
            if self._device(textContains='To see available networks').wait.exists(timeout=5000):
                self._logger.debug('wifi is turned off')
                return True
            else:
                self._logger.debug('Turn off wifi fail!!!')
                return False
        elif self._device(checked='false', className='android.widget.Switch'):
            self._logger.debug('wifi already off')
            return True
        else:
            self._logger.debug('Can\'t find the wifi switch!!!')
            return False

        #     def wifi_scan(self):
        #         self._logger.debug('Scan wifi')
        #         if self._device(description='More options').exists:
        #             self._device(description='More options').click()
        #             self._device.delay(1)
        #             self._device(text='Scan').click()
        #             self._device.delay(1)
        #             if self._device(className='android.widget.ListView').exists:
        #                 self._logger.debug('Scan wifi success!')
        #                 return True
        #             else:
        #                 self._logger.debug('Scan wifi fail!')
        #                 return False
        #

    def forget_all_password(self, hotspotName=None):
        """forget all the WiFi password remembered
        
        @param hotspotName: givern WiFi to forget
        
        """
        i = 0
        for i in range(10):
            if self._device(resourceId='android:id/list').child(resourceId='android:id/summary').exists:
                summary = self._device(resourceId='android:id/list').child(resourceId='android:id/summary',
                                                                           instance=0).get_text()
                for j in range(20):
                    if summary.find('Connecting') > -1 or summary.find('Authenticating') > -1:
                        self._device.delay(1)
                    else:
                        break
                if summary.find(
                        'Connected') > -1 or summary == 'Saved' or summary == 'Authentication problem' or summary.find(
                        'Connecting') > -1:
                    self._device(resourceId='android:id/list').child(resourceId='android:id/summary',
                                                                     instance=0).click()
                    self._device.delay(2)
                if self._device(text='Forget').exists:
                    self._device(text='Forget').click()
                    self._device.delay(2)
            else:
                self._logger.debug('None wifi saved')
                return True
        if i == 9:
            self._logger.debug('More than 10 wifi saved')
            if hotspotName <> None:
                return self.forget_hotspot(hotspotName)
            else:
                return False

    def forget_hotspot(self, hotspotName):
        """forget the given WiFi
        
        @param hotspotName: WiFi name
        
        """
        self._device(scrollable=True).scroll.vert.toBeginning(steps=100, max_swipes=1000)
        if not (self._device(textContains='Connected').wait.exists(timeout=2000) or self._device(
                text='Saved').wait.exists(timeout=2000) \
                        or self._device(text='Authentication problem').wait.exists(timeout=2000)):
            self._logger.debug('None wifi connect before.')
            return True
        self._logger.debug('forget hospot')
        self._logger.debug('Search hotspot-------> ' + hotspotName)
        self._device(scrollable=True).scroll.vert.toBeginning(steps=100, max_swipes=1000)
        for loop in range(3):
            maxloop = 0
            while True:
                if self._device(text=hotspotName).exists:
                    break
                if maxloop > 10:
                    break
                maxloop += 1
            if self._device(text=hotspotName).exists:
                self._device(text=hotspotName).click()
                self._device.delay(1)
                break
            elif loop == 2:
                self._logger.debug('can not find hotspot: %s', hotspotName)
                return False
            else:
                self._device(scrollable=True).scroll.vert.forward(steps=10)
        if self._device(text='Forget').exists:
            self._device(text='Forget').click()
            self._device.delay(5)
            self._device(scrollable=True).scroll.vert.toBeginning(steps=100, max_swipes=1000)
            if not self._device(textContains='Connected').wait.exists(timeout=2000):
                self._logger.debug('wifi has forgotten.')
                return True
            else:
                first_wifi = self._device(resourceId='android:id/title', instance=0).get_text()
                if first_wifi == hotspotName:
                    self._logger.debug('There is other wifi ' + first_wifi + 'connectting.')
                    return True
                else:
                    self._logger.debug('wifi ' + hotspotName + 'forget failed')
                    return False
        else:
            self._logger.debug('wifi ' + hotspotName + 'is didn\'t connected before!')
            self._device.press.back()
            if not self._device(text=Wifi).exists:
                self._device.press.back()
            return True

    def set_wifi_connect(self, device, name, password):
        """check if wifi connected, connect one if not
        
        @param device: device name
        @param name: wifi name
        @param password: wifi password
        
        """
        connect_wifi = 0
        while not self.if_wifi_connected(os.environ.get(device)):
            self._logger.debug("Connect Wi-Fi")
            if self.stayInSetting("Wi-Fi") and self.wifi_open() and self.connect_wifi(name, password):
                return True
            connect_wifi += 1
            if connect_wifi > 2:
                return False
        return True

    def set_wifi_close(self, device):
        """check if wifi connected, connect one if not
        """
        close_wifi = 0
        while self.if_wifi_connected(os.environ.get(device)):
            self._logger.debug("Close Wi-Fi")
            if self.stayInSetting("Wi-Fi") and self.wifi_close():
                return True
            if close_wifi > 2:
                return False
        return True

    def wifi_reconnect(self):
        """click the wifi switch button to turn off and turn on wifi then check if the wifi connecting again
        """
        if not (self.stayInSetting("Wi-Fi") and self.wifi_close()):
            return False
        if not (self.stayInSetting("Wi-Fi") and self.wifi_open()):
            return False
        if self._device(textContains='Connected').wait.exists(timeout=50000):
            self._logger.debug('wifi reconnected.')
            return True
        else:
            self._logger.debug('wifi reconnec fail.')
            return False

    def BT_switch(self):
        """Trun on or off BT
        
        """
        self._logger.debug('Switch BT')
        if self._device(checked='false', className='android.widget.Switch'):
            self._device(className='android.widget.Switch').click()
            self._device.delay(3)
            if self._device(textContains='Available devices').wait.exists(timeout=15000):
                self._logger.debug('BT is turned on')
                return True
            else:
                self._logger.debug('Turn on BT fail!!!')
                return False
        if self._device(checked='true', className='android.widget.Switch'):
            self._device(className='android.widget.Switch').click()
            self._device.delay(3)
            if self._device(resourceId='android:id/empty').wait.exists(timeout=5000):
                self._logger.debug('BT is turned off')
                return True
            else:
                self._logger.debug('Turn off BT fail!!!')
                return False

        self._logger.debug('Can\'t find the BT switch!!!')
        return False

    def switch_network(self, type, device):
        """switch network to specified type.
        
        @param (str)type: the type of network.
            
        """
        self._logger.debug("Switch network to %s." % (type))
        self._device.start_activity("com.android.settings", "com.android.settings.RadioInfo")
        self._device.delay(2)
        if not type in ('2G', '3G', 'LTE', 'All'):
            self._device.press.back()
            self._logger.warning("Wrong argument: %s." % (type))
            return False
        if type == '2G':
            text_type = 'GSM only'
        elif type == '3G':
            text_type = 'WCDMA only'
        elif type == 'LTE':
            text_type = 'LTE only'
        elif type == 'All':
            text_type = 'LTE/GSM/CDMA auto (PRL)'
        self._device(scrollable=True).scroll.to(text='Set preferred network type:')
        self._device.delay(2)
        self._device(resourceId='com.android.settings:id/preferredNetworkType').click()
        self._device.delay(1)
        for i in range(3):
            # self._device(scrollable=True).scroll.horiz.toBeginning(steps=100,max_swipes=1000)
            self._device(scrollable=True).scroll.vert.backward()
            self._device.delay(1)
        self._device(scrollable=True).scroll.to(text=text_type)

        self._device.delay(1)
        self._device(text=text_type).click()
        self._device.delay(5)
        self._device.press.back()
        self._device.delay(1)
        for i in range(60):
            if self.if_data_connected(device):
                return True
            else:
                self._device.delay(5)
        return False
