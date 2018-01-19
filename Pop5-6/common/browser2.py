"""Browser library for scripts.
"""
import sys
from common import Common
PicPath = sys.path[0]+"\\PicComparison\\"

class Browser(Common):   
    def __init__(self, device, log_name):
        Common.__init__(self, device,log_name)
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
            while not self._device(resourceId ='com.android.browser:id/url').exists:
                self._device.press.back()
                maxtime += 1
                if maxtime > 3:
                    self._logger.debug("Can't back browser")
                    break
            if maxtime < 4:
                return True

        self._device.press.home()
        self._logger.debug("Launch browser.")
        if self.enter_app('Browser'):
            self._device.delay(2)
            if self.get_current_packagename() == self.get_app_package_from_file('Browser'):
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
            self.select_menu('Home')
            self._logger.debug('loading...')
            return self.is_loading(300)
        else:
            return False              
        
    def browse_webpage(self,website):
        """type a url to open the webpage
        
        @param website: the web address
              
        """ 
        if self.stay_in_browser():
            if self._device(resourceId = 'com.android.browser:id/url').exists:
                self._device(resourceId = 'com.android.browser:id/url').set_text(website)
                self._device.delay(3)
                self._device.press.enter()
                self._device.delay(1)
                self._logger.debug('loading...')
                if self.is_loading(300):
                    self._logger.debug(website+" open success!")
                    return True
                else:
                    self._logger.debug(website+" open fail!")
                    return False
            else: 
                self._logger.debug("Url editvies isn't exist!")
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
                if not self._device(text = 'Privacy & security').exists:
                    self._logger.debug('Privacy & security isn\'t exist')
                    return False
                self._device(text = 'Privacy & security').click()
                self._device.delay(2)
                
                if not self._device(text = 'Clear cache').exists:
                    self._logger.debug('Clear cache isn\'t exist')
                    return False
                if self._device(text = 'Clear cache').isEnabled():
                    self._device(text = 'Clear cache').click()
                    self._device.delay(2)
                    if self._device(resourceId = 'android:id/button1', text = 'OK').exists:
                        self._device(resourceId = 'android:id/button1', text = 'OK').click()
                        self._device.delay(5)
                    if not self._device(text = 'Clear cache',  enabled = False).wait.exists(timeout=15000):
                        self._logger.debug('Clear browser data timeout')
                        return False
                
                self._device.press.back()
                self._device.delay(2)
                self._device.press.back()
                self._device.delay(2)
                self._logger.debug('Clear browser data finish')
                return True
            else:
                return False         

    def browser_streaming(self,website, waittime = 0):
        """play streaming by browser
 
        """         
        if self.stay_in_browser():
            if self._device(resourceId = 'com.android.browser:id/url').exists:
                self._device(resourceId = 'com.android.browser:id/url').set_text(website)
                self._device.delay(3)
                self._device.press.enter()
                self._device.delay(1)
                self._logger.debug('loading...')

                # choose player if needed 
                if  self._device(text='Open with').exists and self._device(resourceId ='android:id/text1', instance = 0).exists:
                    self._device(resourceId ='android:id/text1', instance = 0).click()
                    self._device.delay(1)
                    if self._device(text='Always').exists:
                        self._device(text='Always').click()
#                     if self._device(text='Just once').exists:
#                         self._device(text='Just once').click()
                        self._device.delay(3)
                elif self._device(text='Use a different app').exists and self._device(text='Always').exists:
                    self._device(text='Always').click()
#                     self._device(text='Just once').click()
                    self._device.delay(3)
                
                maxtimes=0
                while True: 
                    if self._device(resourceId = 'com.google.android.apps.plus:id/list_empty_progress').exists\
                        or self._device(className  = 'android.widget.ProgressBar').exists:
                        self._device.delay(2)
                        if maxtimes>=60:
                            self._logger.debug("browser play video loading fail!")
                            return False
                    elif self._device(resourceId = 'com.google.android.apps.plus:id/videoplayer').exists\
                        or self._device(resourceId = 'com.google.android.apps.photos:id/photos_videoplayer_videolayout').exists\
                        or self._device(resourceId = 'com.tct.gallery3d:id/surface_view').exists\
                        or self._device(resourceId = 'com.android.gallery3d:id/surface_view').exists:
                        break
                    elif self._device(resourceId = 'com.google.android.apps.plus:id/list_empty_text', text = 'Can\'t play video.').exists:
                        self._logger.debug("Can't play video.")
                        return False
                    else:
                        self._device.delay(5)
                        if maxtimes >= 4:
                            self._logger.debug("browser play video fail!")
                            return False
                    maxtimes+=1
                
                self._logger.debug('play video...')
                if waittime == 0:
                    self._device(resourceId = 'com.android.browser:id/url').wait.exists(timeout = 300000)
                else:
                    self._logger.debug('play video %s seconds', str(waittime))
                    self._device.delay(waittime)
                    
                if self._device(resourceId = 'com.google.android.apps.plus:id/videoplayer').exists\
                    or self._device(resourceId = 'com.google.android.apps.photos:id/photos_videoplayer_videolayout').exists\
                    or self._device(resourceId = 'com.tct.gallery3d:id/surface_view').exists\
                    or self._device(resourceId = 'com.android.gallery3d:id/surface_view').exists:
                    self._device.press.back()
                    self._device.delay(2)
                if self._device(resourceId = 'com.android.browser:id/url').exists:
                    self._logger.debug("Play streaming successfully.")
                    return True
                
        self._logger.debug("Play streaming")
        return False
    
    def select_menu(self, menu_text):
        """enter node of menu
        
        @param menu_text: menu item
        
        """
        self._logger.debug('enter menu: '+ menu_text)
        if not self._device(description='More options').exists:
                self._logger.debug("Can't find the more options")
                return False
        self._device(description='More options').click()
        self._device.delay(2)
        
        if not self._device(resourceId = 'android:id/title', textContains = menu_text).exists:
            self._logger.debug("Can't find the menu " + menu_text)
            return False
        self._device(resourceId = 'android:id/title', textContains = menu_text).click()
        self._device.delay(2)
        return True      
        
    def select_bookmark(self,index):
        """click a bookmark
        
        @param index: the index of a bookmark in list
        
        """
        if not self._device(resourceId='com.android.browser:id/all_btn').exists:
            self._logger.debug('Can\'t find Bookmark icon.')
            return False
        self._device(resourceId='com.android.browser:id/all_btn').click()
        self._device.delay(2)
        
        if not self._device(resourceId = 'com.android.browser:id/group_name', text = 'Local').exists:
            self._logger.debug('In\'t in bookmarks')
            return False
        if not self._device(resourceId='com.android.browser:id/thumb').exists:
            self._logger.debug('None bookmarks added')
            return False
        bookmarks_num = self._device(resourceId = 'com.android.browser:id/thumb').count
        if bookmarks_num >= index:
            self._device(resourceId = 'com.android.browser:id/thumb', instance = index).click()
            return self.is_loading(300)
        else:
            self._logger.debug('The bookmark isn\'t exist')
            return False
            
    def is_loading(self, timeout):
        """check if the webpage loaded
        
        @param timeout: time to wait for the page loading
        
        """
        wait_time = 0
        while self._device(description = 'Stop page load').exists:
            self._device.delay(1)
            wait_time += 1
            if wait_time > timeout:
                self._logger.debug('Loading page timeout')
                return False
        if not self._device(resourceId = 'com.android.browser:id/title').exists:
            self._logger.debug('Can\'t get the page title.')
            return False
        page_title = self._device(resourceId = 'com.android.browser:id/title').get_text()
        if page_title.find("Webpage not available") > -1 or page_title.find("Problem") > -1\
            or page_title.find("Error loading the web page") > -1:
            self._logger.debug('Page load fail!!!')
            return False
        else:
            self._logger.debug('Page loading successfully')
            return True
        
    def exit_browser(self):
        """Exit browser from menu
        
        """
        self._logger.debug('Exit browser')
        
        if self.get_current_packagename() <> self.get_app_package_from_file('Browser'):
            self._logger.debug('Already Exit browser')
            return True
        else:
            self.stay_in_browser()
            
        if not self.select_menu('Close'):
            self.stay_in_browser()
            self.select_menu('Exit')
        if self._device(text = 'Quit').exists:
            self._device(text = 'Quit').click()
            self._device.delay(2)
        if self.get_current_packagename() == self.get_app_package_from_file('Launcher'):
            self._logger.debug('Exit browser successfully')
            return True
        else:
            self._logger.debug('Exit browser fail')
            return False
        
        
        