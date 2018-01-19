# -*- coding: UTF-8 -*-
"""chrome library for scripts.
"""
import re
import sys
from common import Common

chrome_package = "com.android.chrome"
chrome_activity = "com.google.android.apps.chrome.Main"


class chrome(Common):
    def __init__(self, device, log_name):
        Common.__init__(self, device, log_name)
        self._ssid = None

    ''' author: yaqi.wei
        def: Check whether step into chrome success
    '''

    def save_fail_img(self):
        """Save fail screenshot to Browser Folder
        
        """
        self.save_img("chrome")

    def enter_chrome(self):
        self._device.watcher('Keep Google').when(text='KEEP GOOGLE').click(text='OK')
        if self.enter_app('Chrome'):
            """
            Click the Accept icon
            """
            while self._device(text='ACCEPT & CONTINUE').exists:
                self._device(text='ACCEPT & CONTINUE').click()
                self._device.delay(2)
                self._device(text='NO THANKS').click()
                self._device.delay(2)
                self._logger.debug('Click the Accept icon')
            if not self._device(resourceId='com.android.chrome:id/control_container').exists:
                self._device(className='android.webkit.WebView').scroll.vert.toBeginning(steps=10, max_swipes=1000)
            if self._device(resourceId='com.android.chrome:id/url_bar').exists:
                self._logger.debug('Enter Chrome success!')
                return True
            else:
                self._logger.debug('Enter Chrome fail!')
                return False
        self._logger.debug('Not find Chrome app')
        return False

    '''
        Author: yaqi.wei
        def: check web page load success
    '''

    def check_page_load(self):
        'wait 120s to load web page'
        maxtimes = 0
        while self._device(resourceId='com.android.chrome:id/progress').exists:
            maxtimes += 1
            self._logger.info('Web page loading...')
            self._device.delay(2)
            if maxtimes >= 120:
                return False
        if self._device(text='Web page not available').exists:
            self._logger.warning('No connection')
            return False
        if self._device(description='You are offline.').exists:
            self._logger.warning('No connection')
            return False
        if self._device(description='This webpage is not available').exists:
            self._logger.warning('No connection')
            return False
        self._logger.debug('Web page load success!!!')
        return True

    """ author: yaqi.wei 
        def: Enter home page,temporary function for chrome,should modified after chrome update
        argv: (url) -- website
              (webpic) -- Part web capture of the web page
    """

    def enter_homePage(self):
        self._logger.debug('Start to enter home page...')
        if not self._device(resourceId='com.android.chrome:id/toolbar').exists:
            self._device(scrollable=True).scroll.vert.toBeginning(steps=100, max_swipes=1000)
        self._device(resourceId='com.android.chrome:id/toolbar').set_text("www.baidu.com")
        self._device.delay(5)
        if self.check_page_load():
            self._logger.debug("home page load success! ")
            return True
        else:
            self._logger.debug('Connection error, home page load fail')
            return False

    ''' Author: yaqi.wei
        def: navigate to a link and click on the link, and check whether page load sucess
        argv: (website): the web page you want to navigate on 
              (webpic): Part web capture of the navigated web page
    '''

    def browse_webpage(self, website):
        self._device(className='android.widget.EditText', resourceId="com.android.chrome:id/url_bar"). \
            set_text(website)
        self._device.delay(3)
        self._device.press.enter()
        self._device.delay(5)
        if self.check_page_load():
            'Click the link on the web page'
            self._logger.debug('Click the link on home page')
            self._device(description='百度一下,你就知道').click()
            if self.check_page_load():
                self._logger.debug('Navigated web page load success!!!')
                return True
            else:
                self._logger.debug('Navigated web page load fail!!!')
                return False
        else:
            self._logger.debug('Web page load fail!!!')
            return False
        return False

    ''' Author: yaqi.wei
        def: clear history data
    '''

    def clear_data(self):
        self._logger.debug('Clear chrome data')
        self.select_menu('Settings')
        self._device.delay(1)
        self._device(text='Privacy').click.wait(timeout=2000)
        self._device.delay(1)
        self._device(resourceId='android:id/title', text='Clear browsing data').click()
        self._device.delay(2)
        self._device(resourceId='com.android.chrome:id/button_preference', text='CLEAR DATA').click()
        self._device.delay(5)
        self._device.press.back()
        self._device.delay(2)
        self._device.press.back()
        self._device.delay(2)

    '''Author: yaqi.wei
        def: check whether exit chrome success
    '''

    def exit_chrome(self):
        self.back_home()
        self._device.delay(2)
        if self._device(packageName='com.android.launcher3').exists:
            self._logger.debug('Exit chrome success!!!')
            return True
        self._logger.debug('Exit chrome fail!!!')
        return False

    def chrome_playvideo(self, website):
        if self.enter_chrome():
            if self._device(description='Search or type URL').exists:
                self._device(className='android.widget.EditText', resourceId="com.android.chrome:id/url_bar").set_text(
                    website)
                self._device.delay(3)
                self._device.press.enter()
                self._device.delay(1)
                self._logger.debug('loading...')
                maxtimes = 0
                while not self._device(description='watch?v=MVbeoSPqRs4#').exists:
                    self._device.delay(2)
                    if maxtimes >= 60:
                        self._logger.debug("chrome play video fail!")
                        return False
                    maxtimes += 1
                self._logger.debug('play video...')
                self._device(description='watch?v=MVbeoSPqRs4#').click()
                self._device.delay(30)
                self._device.press.back()
                self._device.delay(2)
                return True
        self._logger.debug("chrome play video fail!")
        return False

    '''Author: yaqi.wei    
       def: select the menu to open
       argv: (menu_text) --- text on menu
    '''

    def select_menu(self, menu_text):
        if not self._device(resourceId='com.android.chrome:id/toolbar').exists:
            self._device(scrollable=True).scroll.vert.toBeginning(steps=100, max_swipes=1000)
            self._device.delay(2)
        if self._device(resourceId='com.android.chrome:id/toolbar').exists:
            self._device(resourceId='com.android.chrome:id/menu_button').click()
        self._device.delay(3)
        self._device(text=menu_text).click()
        self._device.delay(3)
        self._logger.debug('click the %s successfully', menu_text)

    #         if self._device(text='Bookmarks').exists:
    #             self._device(text='Bookmarks').click()
    #             self._device.delay(2)

    '''Author: yaqi.wei
       def: check bookmarks whether is enough
    '''

    def check_bookmars_num(self):
        self.select_menu("Bookmarks")
        if not self._device(resourceId='com.android.chrome:id/bookmark_items_container').getChildCount() >= 5:
            self._logger.debug('Bookmarks is not enough,pls check!!!')
            return False
        self._device.press.back()
        self._device.delay(1)
        return True

    '''Author: yaqi.wei
       def: select bookmarks to open one by one
       argv: (index) --- bookmarks's index
    '''

    def select_bookmark(self, Index):
        #         self._device(className='android.widget.LinearLayout',instance = Index*2+3).click()
        #        self._device(resourceId='com.android.chrome:id/bookmarks_list_view').\
        #            child(className='android.widget.FrameLayout',index = Index).\
        #            child(className='android.view.View',index = Index).click()
        self._device(resourceId='com.android.chrome:id/bookmark_items_container').child(
            className='android.widget.FrameLayout', instance=Index).click()
        self._device.delay(2)
        if self.check_page_load():
            self._logger.debug("Bookmark %s load success!!!", str(Index + 1))
            return True
        self._logger.debug("Bookmark %s load fail!", str(Index + 1))
        return False

    '''Author: zijin.rao
       def: check whether open app success
       argv: (appname) ---app_name
    '''

    def check_open_app(self, packagename):
        if packagename == 'com.android.settings':
            if self._device(packageName='com.android.settings').exists:
                self._logger.debug("open settings..")
                return True
        if packagename == 'com.tct.soundrecorder':
            if self._device(packageName='com.tct.soundrecorder').exists:
                self._logger.debug("open soundrecorder..")
                return True
        if packagename == 'com.android.contacts':
            if self._device(packageName='com.android.contacts').exists:
                self._logger.debug("open contacts..")
                return True
        if packagename == 'com.google.android.music':
            if self._device(packageName='com.google.android.music').exists:
                self._logger.debug("open playmusic..")
                return True
        if packagename == 'com.android.chrome':
            if self._device(packageName='com.android.chrome').exists:
                self._logger.debug("open chrome..")
                return True
        if packagename == 'com.tct.camera':
            if self._device(packageName='com.tct.camera').exists:
                self._logger.debug("open camera..")
                return True
        return False

    """
    Initialize
    """

    def add_bookmarks(self, url):
        """
        get the current bookmark sum
        """
        self.select_menu('Bookmarks')
        if self._device(text='Sync your bookmarks').exists and self._device(text='No, thanks').exists:
            self._logger.debug('Will not sync the bookmarks.')
            self._device(text='No, thanks').click()
        if self._device(className='android.widget.TextView', text='Mobile bookmarks').exists:
            self._device(className='android.widget.TextView', text='Mobile bookmarks').click()
            self._device.delay(2)
        bookmark_num = self.get_total_bookmarks()
        self._logger.debug('current bookmarks num: ' + str(bookmark_num))

        """
        Add bookmark
        """

        self._logger.debug('Add the bookmark' + url)
        if self._device(resourceId='com.android.chrome:id/url_bar').exists:
            self._device(resourceId='com.android.chrome:id/url_bar').click()
            self._device.delay(2)
            self._device(className='android.widget.EditText', resourceId='com.android.chrome:id/url_bar').set_text(url)
            self._device.press.enter()
            self._device.delay(10)
            self._logger.debug('loading......')
            self._device(resourceId='com.android.chrome:id/bookmark_button').click()
            self._logger.debug('Add' + url + 'successfully')
        else:
            self._logger.debug('Add bookmark fail,not find the url bar')
        """
        judge whether the bookmark sum has increased 
        """

        self.select_menu('Bookmarks')
        bookmark_num1 = self.get_total_bookmarks()
        self._logger.debug('bookmarks num: ' + str(bookmark_num1))
        if bookmark_num1 > bookmark_num:
            self._logger.debug('Add bookmark successful')
            self._device.press.back()
            return True
        self._logger.debug('add bookmark fail!')
        self._device.press.back()
        return False

    #             if self._device(resourceId = 'com.android.chrome:id/bookmark_button').exists:
    #                 self._device(resourceId = 'com.android.chrome:id/bookmark_button').click()
    #                 self._device.delay(1)
    #                 if self._device(resourceId = 'com.android.chrome:id/menu_button').exists:
    #                     self._device(reosurceId = 'com.android.chrome:id/menu_button').click()
    #                     if self._device(resourceId = 'com.android.chrome:id/menu_item_text',text = 'Bookmarks').exists:
    #                         self._device(resourceId = 'com.android.chrome:id/menu_item_text',text = 'Bookmarks').click()
    #                         if self._device(resourceId = 'com.android.chrome:id/no_thanks',text = 'NO THANKS').exists:
    #                             self._device(resourceId = 'com.android.chrome:id/no_thanks',text = 'NO THANKS').click()

    def get_total_bookmarks(self):
        if self._device(resourceId='com.android.chrome:id/bookmark_items_container').exists:
            return self._device(resourceId='com.android.chrome:id/bookmark_items_container').getChildCount()
        else:
            return False
