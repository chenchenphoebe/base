"""Chrome library for scripts.
"""
import sys
from common import Common
from test.test_os import resource
from pydoc import classname

PicPath = sys.path[0] + "\\PicComparison\\"


class Browser(Common):
    def __init__(self, device, log_name):
        Common.__init__(self, device, log_name)
        self._ssid = None

    def save_fail_img(self):
        """Save fail screenshot to Browser Folder
        
        """
        self.save_img("Browser")

    def stay_in_browser(self):
        """Keep in Browser main page
        
        """
        if self.get_current_packagename() == self.get_app_package_from_file('Browser'):
            maxtime = 0
            while (not self._device(resourceId='com.hawk.android.browser:id/taburlbar').exists) \
                    and (not self._device(resourceId='com.hawk.android.browser:id/url').exists):
                self._device.press.back()
                maxtime += 1
                if maxtime > 3:
                    self._logger.debug("Can't back browser")
                    break
            if maxtime < 4:
                return True

        self._logger.debug("Launch browser.")
        if self.enter_app('Browser'):
            self.click_allow()
            self._device.delay(2)
            maxtime = 0
            while (not self._device(resourceId='com.hawk.android.browser:id/taburlbar').exists) \
                    and (not self._device(resourceId='com.hawk.android.browser:id/url').exists):
                self._device.press.back()
                maxtime += 1
                if maxtime > 3:
                    self._logger.debug("Can't back browser")
                    break
            if maxtime < 4:
                return True
            else:
                self._logger.debug('Launch browser fail')
        else:
            return False

    def enter_homepage(self):
        """enter home page
        
        """
        self._logger.debug('enter the home page')
        if self.stay_in_browser():
            if self._device(description='More options').exists:
                self._device(description='More options').click()
                self._device.delay(1)
            if self._device(text='Home').exists:
                self._device(text='Home').click()
                self._device.delay(1)
                self._logger.debug('loading...')
                return self.is_loading(300)
            else:
                return True
        else:
            return False

    def browse_webpage(self, website):
        """type a url to open the webpage
        
        @param website: the web address
              
        """
        if self.stay_in_browser():
            if self._device(resourceId='com.hawk.android.browser:id/taburlbar').exists:
                self._device(className='android.widget.EditText',
                             resourceId="com.hawk.android.browser:id/url").clear_text()
                self._device.delay(2)
                self._device(className='android.widget.EditText',
                             resourceId="com.hawk.android.browser:id/url").set_text(
                    website)
            else:
                self._logger.debug("Url editvies isn't exist!")
                return False
            self._device.delay(3)
            self._device.press.enter()
            self._device.delay(1)
            self._logger.debug('loading...')
            if self.is_loading(300):
                self._logger.debug(website + " open success!")
                return True
            else:
                self._logger.debug(website + " open fail!")
                return False
        else:
            self._logger.debug("Isn't in browser!")
            return False

    def clear_data(self):
        """clear data of browser

        """
        if self.stay_in_browser():
            self._logger.debug('Clear browser data')
            if self.select_menu('Settings'):
                if self._device(text='Clear data').wait.exists(timeout=2000):
                    self._device(text='Clear data').click()
                    self._device.delay(2)
                else:
                    self._logger.debug('clear date isn\'t exist')
                    return False

                if self._device(text='CLEAR').wait.exists(timeout=2000):
                    self._device(text='CLEAR').click()
                    return True
                else:
                    self._logger.debug("Not exists clear icon")
                    return False
        else:
            return False

    def select_menu(self, menu_text):
        """enter node of menu
        
        @param menu_text: menu item
        
        """
        self._logger.debug('enter menu: ' + menu_text)

        try_time = 0
        while not self._device(resourceId='com.hawk.android.browser:id/taburlbar').exists:
            if try_time > 3:
                self._logger.debug('Top views not exist')
                return False
            if self._device(resourceId='android:id/content').exists:
                self._device(resourceId='android:id/content').swipe.down()
                self._device.delay(2)
            try_time += 1
            self._logger.debug('000000000000000000000')
        if menu_text == 'Bookmarks/History':
            if self._device(resourceId='com.hawk.android.browser:id/menu_toolbar_id').exists:
                self._device(resourceId='com.hawk.android.browser:id/menu_toolbar_id').click()
                if not self._device(text=menu_text).wait.exists(timeout=2000):
                    self._device.swipe(168, 1451, 891, 1451)
                self._device.delay(1)
                self._device(text=menu_text).click()
                if self._device(className='android.widget.ImageButton', index=1).wait.exists(timeout=2000):
                    self._device(className='android.widget.ImageButton', index=1).click()
                    if self._device(text='Default Bookmark').wait.exists(timeout=2000):
                        self._logger.debug("enter the bookmark page successfully")
                        return True
                    else:
                        self._logger.debug("enter the bookmark page fail")
                        return False
                else:
                    self._logger.debug('Bookmarks not exist')
                    return False
            else:
                self._logger.debug("The menu toolbar not exists")
                return False

        elif menu_text == 'Settings':
            if self._device(resourceId='com.hawk.android.browser:id/menu_toolbar_id').wait.exists(timeout=2000):
                self._device(resourceId='com.hawk.android.browser:id/menu_toolbar_id').click()
                if not self._device(text=menu_text).wait.exists(timeout=2000):
                    self._device.swipe(891, 1451, 168, 1451)
                self._device.delay(2)
                self._device(text=menu_text).click()
                self._logger.debug("enter the setting")
                return True
            else:
                self._logger.debug("The menu toolbar not exists")
                return False

    def select_bookmark(self, index1):
        """click a bookmark
        
        @param index: the index of a bookmark in list
        
        """
        if self._device(resourceId='com.hawk.android.browser:id/history_common_menu').wait.exists(timeout=2000):
            self._device(resourceId='com.hawk.android.browser:id/history_common_menu').click()
            self._device.delay(2)
        else:
            if not self.select_menu("Bookmarks/History"):
                return False
        if not self._device(text='Default Bookmark').wait.exists(timeout=2000):
            self._logger.debug('In\'t in bookmarks')
            return False
        if self._device(resourceId='com.hawk.android.browser:id/bookmark_list').wait.exists(timeout=2000):
            bookmarks_num = self._device(resourceId='com.hawk.android.browser:id/bookmark_list').getChildCount() - 1
            if bookmarks_num >= 2:
                if self._device(resourceId='com.hawk.android.browser:id/parent', index=index1).wait.exists(
                        timeout=2000):
                    self._device(resourceId='com.hawk.android.browser:id/parent', index=index1).click()
                    return self.is_loading(100)
                else:
                    self._logger.debug('The %s && %s bookmark isn\'t exist', str(index1), str(index2))
                    return False
            else:
                self._logger.debug('The bookmark isn\'t exist')
                return False
        else:
            self._logger.debug('None bookmarks added')
            return False

    def is_loading(self, timeout):
        """check if the webpage loaded
        
        @param timeout: time to wait for the page loading
        
        """
        wait_time = 0
        while self._device(description='Stop page loading').exists or \
                self._device(resourceId='com.hawk.android.browser:id/progress').exists:
            self._device.delay(1)
            wait_time += 1
            if wait_time > timeout:
                self._logger.debug('Loading page timeout')
                return False
                #         if self._device.find(PicPath+'Offline.png'):
        if self._device(textContains='ERR_INTERNET_DISCONNECTED').exists \
                or self._device(descriptionContains='ERR_INTERNET_DISCONNECTED').exists:
            self._logger.debug('OffLine!!!')
            return False
        # elif self._device.find(PicPath+'NotAvailable.png'):
        elif self._device(textContains='ERR_CONNECTION_TIMED_OUT').exists \
                or self._device(descriptionContains='ERR_CONNECTION_TIMED_OUT').exists:
            self._logger.debug('The web page not available!!!')
            return False
        else:
            self._logger.debug('Page loading successfully')
            return True

    def exit_browser(self):
        press_back_times = 0
        for press_back_times in range(5):
            if self.get_current_packagename() != self.get_app_package_from_file('Launcher'):
                self._device.press.back()
                self._device.delay(2)
                while self._device(text='EXIT').wait.exists(timeout=2000):
                    self._device(text="EXIT").click()
            else:
                break
            if press_back_times > 3:
                self._device.press.home()
                break

        if self.get_current_packagename() == self.get_app_package_from_file('Launcher'):
            self._logger.debug('Exit Browser successfully.')
            return True
        else:
            self._logger.debug('Exit Browser fail.')
            return False
