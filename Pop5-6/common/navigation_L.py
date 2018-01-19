# -*- coding: UTF-8 -*-
"""Menu navigation library for scripts.
"""

from common import Common

class Navigation(Common):
    
    def save_fail_img(self):
        """Save fail screenshot to Menu-Navigation Folder
        
        """
        self.save_img("Menu-Navigation")             
     
    def remove_recent_apps(self):
        """remove all the recent apps
        
        """
        self._logger.debug("Remove recent applications")
        self._device.press.recent()
        self._device.delay(3)
        if self._device(text = 'Your recent screens appear here').exists:
            self._logger.debug("There is none recent apps")
            return True
        
        if self._device(resourceId = 'com.android.systemui:id/recents_clearall_tv').exists\
            or self._device(resourceId = 'com.android.systemui:id/recents_clearall_button').exists:
            if self._device(resourceId = 'com.android.systemui:id/recents_clearall_tv').exists:
                self._device(resourceId = 'com.android.systemui:id/recents_clearall_tv').click()
            else:
                self._device(resourceId = 'com.android.systemui:id/recents_clearall_button').click()
            self._device.delay(3)
            
            wait_time = 0
            while self.get_current_packagename() <> self.get_app_package_from_file("Launcher"):
                self._device.delay(2)
                wait_time += 2
                if wait_time > 60:
                    self._logger.debug("Removed all app timeout fail.")
                    return  False
            self._device.press.recent()
            self._device.delay(3)
            if self._device(text = 'Your recent screens appear here').exists:
                self._logger.debug("Removed all app successfully.")
                self._device.press.back()
                return  True
            else:
                self._logger.debug("Removed all app fail.")
                self._device.press.back()
                return  False
                            
        else:
            for i in range(100):
                if self._device(resourceId = 'com.android.systemui:id/dismiss_task').exists:
                    self._device(resourceId = 'com.android.systemui:id/dismiss_task', instance = 0).click()
                    self._device.delay(1)
                else:
                    self._logger.debug("All %s applications have been removed.", str(i+1))
                    return True
            self._device.press.back()
            self._logger.debug("There are too much applications recently launched.")
            return False

    def get_pages_count(self):
        """get the number of the homepages
        
        """
        if self._device(resourceId = 'com.android.launcher3:id/workspace').exists:
            current_page = self._device(resourceId = 'com.android.launcher3:id/workspace').getChildCount()
            self._logger.debug("All page is " + str(current_page))
            return current_page
        else:
            self._logger.debug("It's in home page")
            return 0
        
    def is_round_pages(self):
        """check if the page can be swiped in circle
        """
        if self._device(resourceId = 'com.android.launcher3:id/page_indicator').exists:
            indicator = self._device(resourceId = 'com.android.launcher3:id/page_indicator').getChildCount()
            if self._device( descriptionContains  = 'of ' + str(indicator)).exists:
                self._logger.debug("It is circle round home pages")
                return True
            else:
                self._logger.debug("It is not circle round home pages")
                return False
        
    def get_current_page(self):
        """get the index of the current homepage displaying
        
        """
        all_page = self.get_pages_count()
        if self.is_round_pages():
            for i in range(all_page):
                if self._device(resourceId = 'com.android.launcher3:id/page_indicator',  descriptionContains = 'Home screen ' + str(i+1) + ' of '+ str(all_page)).exists:
#                 if self._device(resourceId = 'com.android.launcher3:id/page_indicator').child(index = i).child(resourceId = 'com.android.launcher3:id/active', className = 'android.widget.ImageView').exists:
                    self._logger.debug("Current page is %s", str(i+1))
                    return i+1
            self._logger.debug("Get current page fail")
            return -1               
            
        else:
            delay_check_page2 = False
            i = 0
            for i in range(all_page):
                if self._device(resourceId = 'com.android.launcher3:id/workspace').child(index=i).child(className = 'android.widget.TextView').exists:
                    if i == 0:
                        continue
                    if i == 1:
                        delay_check_page2 = True
                        continue
                    self._logger.debug("Current page is %s", str(i+1))
                    return i+1
            if self.get_current_packagename() == 'com.android.settings':
                self._logger.debug("Drag left to settings")
                return 1
            elif delay_check_page2:
                self._logger.debug("Current page is 2")
                return 2
            else:
                self._logger.debug("Get current page fail")
                return -1
            
    def goto_page(self, index):
        """goto the index of the homepage
        
        @param index: the index of the homepage
        
        """
        if self._device(resourceId = 'com.android.launcher3:id/workspace').exists:
            current_page = self.get_current_page()
            if current_page == index:
                return True
            elif  current_page > index:
                self._logger.debug("Swipe right %s times", str(current_page - index))
                for i in range(current_page - index):
                    if self._device(resourceId = 'com.android.launcher3:id/workspace').exists:
                        self._device(resourceId = 'com.android.launcher3:id/workspace').swipe.right(steps=10)
                        self._device.delay(2)
                    else:
                        self._logger.debug("Can't swipe.")
                        return False
            else:
                self._logger.debug("Swipe left %s times", str(index - current_page))
                for i in range(index - current_page):
                    if self._device(resourceId = 'com.android.launcher3:id/workspace').exists:
                        self._device(resourceId = 'com.android.launcher3:id/workspace').swipe.left(steps=10)
                        self._device.delay(2)
                    else:
                        self._logger.debug("Can't swipe.")
                        return False
            current_page = self.get_current_page()
            self._logger.debug("Current page aftet swipe is " + str(current_page))
            return current_page == index
        else:   
            self._logger.debug("It's in home page")
            return False           
    
    def click_icon(self, page, SucTimes, FailTimes):
        """launch each icon in the homepage except the bottom icons
        
        @param page: the index of the homepage
        @param SucTimes: Launch successfully times
        @param FailTimes: Launch fail times
        
        """
        count_app = 0
        count_folder = 0
        app_name = ''
        folder_name = ''
        
        if self._device(resourceId = 'com.android.launcher3:id/workspace').child(index = page).child(className = 'android.widget.TextView').exists:
            count_child = self._device(resourceId = 'com.android.launcher3:id/workspace').child(index = page).child(index = 0).getChildCount()
            for i in range(count_child):
                if self._device(resourceId = 'com.android.launcher3:id/workspace').child(index = page).child(index = 0).child(index = i, className = 'android.appwidget.AppWidgetHostView').exists:
                    continue
                widget_child_count = self._device(resourceId = 'com.android.launcher3:id/workspace').child(index = page).child(index = 0).child(index = i).getChildCount()                
                if widget_child_count > 1:
#------------------for the device only, can't get the folder openning screen-----------------------           
#                     continue
                    self._logger.debug('-------------------------')
                    if self._device(resourceId = 'com.android.launcher3:id/workspace').child(index = page).child(index = 0).child(index  = i, descriptionContains = 'Folder: ').exists:
                        folder_name = self._device(resourceId = 'com.android.launcher3:id/workspace').child(index = page).child(index = 0).child(index = i, descriptionContains = 'Folder: ').child(className = 'android.widget.TextView').get_text()
                        self._device(resourceId = 'com.android.launcher3:id/workspace').child(index = page).child(index = 0).child(index = i, descriptionContains = 'Folder: ').click()
                        self._device.delay(3)
                        if self._device(resourceId = 'com.android.launcher3:id/folder_content').exists:
                            count_folder += 1
                            folder_app_num = self._device(resourceId = 'com.android.launcher3:id/folder_content').child(index = 2).getChildCount()
                            self._logger.debug("There are %s app in the folder %s", str(folder_app_num), folder_name)
                            
                            for j in range(folder_app_num):
                                if not self._device(resourceId = 'com.android.launcher3:id/folder_content').exists:
                                    if self._device(resourceId = 'com.android.launcher3:id/workspace').child(index = page).child(index = 0).child(index = i, descriptionContains = 'Folder: ').exists:
                                            self._device(resourceId = 'com.android.launcher3:id/workspace').child(index = page).child(index = 0).child(index = i, descriptionContains = 'Folder: ').click()
                                            self._device.delay(3)
                                    else:
                                        self._logger.info("Isn't in home page")  
                                        break
                                if self._device(resourceId = 'com.android.launcher3:id/folder_content').child(className = 'android.widget.TextView',  instance = j).exists:
                                    app_name_folder = self._device(resourceId = 'com.android.launcher3:id/folder_content').child(className = 'android.widget.TextView',  instance = j).get_text()
                                    if app_name_folder=='' or self.check_black_app_from_file(app_name_folder):
                                        self._logger.debug("______" + app_name_folder + " in black list" )
                                        continue
                                    self._logger.debug("______Open " + app_name_folder + ' in folder' )
                                    self._device(resourceId = 'com.android.launcher3:id/folder_content').child(className = 'android.widget.TextView',  instance = j).click()
                                    self._device.delay(10) 
                                    SucTimes, FailTimes = self.get_check_result(app_name_folder, SucTimes, FailTimes)
                                    self.exit_app(page)
                                    if self.get_current_packagename() <> 'com.android.launcher3':
                                        self._logger.info("Exit %s fail!!!", app_name_folder)  
                                        break;
                                else:
                                    self._logger.info("Get widget instance in folder faild")  
                                    break;
                            
                            press_back_times = 0    
                            while self._device(resourceId = 'com.android.launcher3:id/folder_content').exists:
                                self._device.press.back()
                                self._device.delay(2)
                                press_back_times += 1
                                if press_back_times > 2:
                                    self._device.press.home()
                                    if self.get_current_page() <> (page+1):
                                        self.goto_page(page +1)
                            self._logger.debug('Finish scan the folder.')
                        elif self._device(resourceId = 'com.android.launcher3:id/folder_container').exists:
                            if self._device(resourceId = 'com.android.launcher3:id/folder_dock_indicator').exists:
                                all_page_in_folder = self._device(resourceId = 'com.android.launcher3:id/folder_dock_indicator').getChildCount()
                                for k in range(all_page_in_folder):
                                    if self.goto_page_in_folder(k+1):
                                        if not self._device(resourceId = 'com.android.launcher3:id/screen_content').exists:
                                            self._logger.info("Cannot get the screen_content") 
                                            break
                                        folder_app_num = self._device(resourceId = 'com.android.launcher3:id/screen_content').child(index = 0).child(index = 0).getChildCount()
                                        self._logger.debug("There are %s app in the folder %s page %s", str(folder_app_num), folder_name, str(k+1))
                                        
                                    for j in range(folder_app_num):
                                        if not self._device(resourceId = 'com.android.launcher3:id/folder_container').exists:
                                            if self._device(resourceId = 'com.android.launcher3:id/workspace').child(index = page).child(index = 0).child(index = i, descriptionContains = 'Folder: ').exists:
                                                self._device(resourceId = 'com.android.launcher3:id/workspace').child(index = page).child(index = 0).child(index = i, descriptionContains = 'Folder: ').click()
                                                self._device.delay(3)
                                            else:
                                                self._logger.info("Isn't in home page")  
                                                break
                                        if not self.goto_page_in_folder(k+1):
                                            break
                                        if self._device(resourceId = 'com.android.launcher3:id/folder_container').child(className = 'android.widget.TextView',  instance = j).exists:
                                            app_name_folder = self._device(resourceId = 'com.android.launcher3:id/folder_container').child(className = 'android.widget.TextView',  instance = j).get_text()
                                            if app_name_folder=='' or self.check_black_app_from_file(app_name_folder):
                                                self._logger.debug("______" + app_name_folder + " in black list" )
                                                continue
                                            self._logger.debug("______Open " + app_name_folder + ' in folder' )
                                            self._device(resourceId = 'com.android.launcher3:id/folder_container').child(className = 'android.widget.TextView',  instance = j).click()
                                            self._device.delay(10) 
                                            SucTimes, FailTimes = self.get_check_result(app_name_folder, SucTimes, FailTimes)
                                            self.exit_app(page)
                                            if self.get_current_packagename() <> 'com.android.launcher3':
                                                self._logger.info("Exit %s fail!!!", app_name_folder)  
                                                break;
                                        else:
                                            self._logger.debug("Get widget instance in folder faild")  
                                            break;
                                press_back_times = 0    
                                while self._device(resourceId = 'com.android.launcher3:id/folder_container').exists:
                                    self._device.press.back()
                                    self._device.delay(2)
                                    press_back_times += 1
                                    if press_back_times > 2:
                                        self._device.press.home()
                                        if self.get_current_page() <> (page+1):
                                            self.goto_page(page +1)
                                self._logger.debug('Finish scan the folder.')
                            else:
                                    folder_app_num = self._device(resourceId = 'com.android.launcher3:id/screen_content').child(index = 0).child(index = 0).getChildCount()
                                    self._logger.debug("There are %s app in the folder %s", str(folder_app_num), folder_name)
                                        
                                    for j in range(folder_app_num):
                                        if not self._device(resourceId = 'com.android.launcher3:id/folder_container').exists:
                                            if self._device(resourceId = 'com.android.launcher3:id/workspace').child(index = page).child(index = 0).child(index = i, descriptionContains = 'Folder: ').exists:
                                                self._device(resourceId = 'com.android.launcher3:id/workspace').child(index = page).child(index = 0).child(index = i, descriptionContains = 'Folder: ').click()
                                                self._device.delay(3)
                                            else:
                                                self._logger.info("Isn't in home page")  
                                                break
                                        if self._device(resourceId = 'com.android.launcher3:id/folder_container').child(className = 'android.widget.TextView',  instance = j).exists:
                                            app_name_folder = self._device(resourceId = 'com.android.launcher3:id/folder_container').child(className = 'android.widget.TextView',  instance = j).get_text()
                                            if app_name_folder=='' or self.check_black_app_from_file(app_name_folder):
                                                self._logger.debug("______" + app_name_folder + " in black list" )
                                                continue
                                            self._logger.debug("______Open " + app_name_folder + ' in folder' )
                                            self._device(resourceId = 'com.android.launcher3:id/folder_container').child(className = 'android.widget.TextView',  instance = j).click()
                                            self._device.delay(10) 
                                            SucTimes, FailTimes = self.get_check_result(app_name_folder, SucTimes, FailTimes)
                                            self.exit_app(page)
                                            if self.get_current_packagename() <> 'com.android.launcher3':
                                                self._logger.info("Exit %s fail!!!", app_name_folder)  
                                                break;
                                        else:
                                            self._logger.debug("Get widget instance in folder faild")  
                                            break;
                                    
                                    press_back_times = 0    
                                    while self._device(resourceId = 'com.android.launcher3:id/folder_container').exists:
                                        self._device.press.back()
                                        self._device.delay(2)
                                        press_back_times += 1
                                        if press_back_times > 2:
                                            self._device.press.home()
                                            if self.get_current_page() <> (page+1):
                                                self.goto_page(page +1)
                                    self._logger.debug('Finish scan the folder.')
                        else:
                            self._logger.debug("Can't get the folder")     
                else:
                    if self._device(resourceId = 'com.android.launcher3:id/workspace').child(index = page).child(index = 0).child(className = 'android.widget.TextView', instance = i).exists:
#                     if self._device(resourceId = 'com.android.launcher3:id/workspace').child(index = page).child(index = 0).child(index = i).child(className = 'android.widget.TextView').exists:
                        count_app += 1
                        app_name = self._device(resourceId = 'com.android.launcher3:id/workspace').child(index = page).child(index = 0).child(className = 'android.widget.TextView', instance = i).get_text()
#                         app_name = self._device(resourceId = 'com.android.launcher3:id/workspace').child(index = page).child(index = 0).child(index = i).child(className = 'android.widget.TextView').get_text()
                        if app_name =='' or self.check_black_app_from_file(app_name):
                            self._logger.debug("______" + app_name+ " in black list" )
                            continue
                        
                        self._logger.debug("______Open " + app_name)
                        self._device(resourceId = 'com.android.launcher3:id/workspace').child(index = page).child(index = 0).child(className = 'android.widget.TextView', instance = i).click()
#                         self._device(resourceId = 'com.android.launcher3:id/workspace').child(index = page).child(index = 0).child(index = i).child(className = 'android.widget.TextView').click()
                        self._device.delay(10)
                        SucTimes, FailTimes = self.get_check_result(app_name, SucTimes, FailTimes)
                        self.exit_app(page)
                    
                        if self.get_current_packagename() <> 'com.android.launcher3':
                            self._logger.info("Exit %s fail!!!", app_name)  
                            self.save_fail_img()
                            break;                      
                    else:
                        self._logger.debug("Can't get the app widget index " + str(i))
                        self.save_fail_img()
                        
        self._logger.debug("%s Apps and %s folder in the page ", str(count_app), str(count_folder))
                            
        self._logger.info('Success: %s times', str(SucTimes))
        self._logger.info('Fail   : %s times', str(FailTimes))
        return SucTimes, FailTimes
    
    def goto_page_in_folder(self, page):
        """Gogo the page in folder
        
        @param page: the page in folder
        
        """
        if self._device(resourceId = 'com.android.launcher3:id/folder_dock_indicator').exists:
            all_page_in_folder = self._device(resourceId = 'com.android.launcher3:id/folder_dock_indicator').getChildCount()
            self._logger.debug("All page is" + str(all_page_in_folder))
            page_current = 0
            for i in range(all_page_in_folder):
                if self._device( descriptionContains  = 'Page ' + str(i+1) + ' of ' + str(all_page_in_folder)).exists:
                    page_current = i+1
                    break
            if page > page_current:
                for i in range(page - page_current):
                    if self._device(resourceId = 'com.android.launcher3:id/folder_container').exists:
                        self._device(resourceId = 'com.android.launcher3:id/folder_container').swipe.left(steps=10)
                        self._device.delay(2)
                    else:
                        self._logger.debug("Can't swipe.")
                        return False
            elif page_current > page:
                for i in range(page_current - page):
                    if self._device(resourceId = 'com.android.launcher3:id/folder_container').exists:
                        self._device(resourceId = 'com.android.launcher3:id/folder_container').swipe.right(steps=10)
                        self._device.delay(2)
                    else:
                        self._logger.debug("Can't swipe.")
                        return False
            else:
                self._logger.debug("Already in page " + str(page))
                return True
            
            if self._device( descriptionContains  = 'Page ' + str(page) + ' of ' + str(all_page_in_folder)).exists: 
                self._logger.debug("Goto page " + str(page) + ' successfully') 
                return True
            else:
                self._logger.debug("Goto page " + str(page) + ' fail') 
                return False    
        else:
            self._logger.debug("Can't get page")
            return False     
    
    def check_open_app(self, app_name):
        """check if the app open
        
        @param app_name: app name to open
        
        """
        app_package_record = self.get_app_package_from_file(app_name)
        app_package_currect = self.get_current_packagename()
        self._logger.debug("The package recording in file is " + str(app_package_record))
        if app_package_currect is None:
            self._logger.debug("Can't get the package")
            return False
        elif app_package_currect == app_package_record:
            self._logger.debug("Open %s successfully.", app_name)
            return True
        else:
            self._logger.debug("The package current is " + app_package_currect)
            return False

    def get_check_result(self, app_name, SucTimes = 0, FailTimes = 0):
        """get the result if app open
        
        @param app_name: app name
        @param SucTimes: Launch successfully times
        @param FailTimes: Launch fail times
        
        """
        if self.check_open_app(app_name):
            SucTimes += 1
            self._logger.info("Trace Success Loop %s", SucTimes)
        else:
            FailTimes += 1
            self.save_fail_img()
        return SucTimes, FailTimes
    
    def exit_app(self, page = 1, enterApps = False):
        """exit app to homepage
        
        @param page: back to the given page
        
        """
        press_back_times = 0    
        for press_back_times in range(5):
            if self.get_current_packagename() <> self.get_app_package_from_file('Launcher'): 
                if press_back_times > 1:
                    self._device.press.back()
                    self._device.press.back()
                else:
                    self._device.press.back()
                self._device.delay(2)
                
                if self._device(resourceId = 'android:id/button1').exists:
                    self._device(resourceId = 'android:id/button1').click()
                    self._device.delay(2)
            else:
                break
        if press_back_times > 3:
            self._device.press.home()
            if enterApps:
                if self._device(description  = 'Apps').exists:
                    self._device(description  = 'Apps').click()
                    self._device.delay(2)
                    if self._device(resourceId = 'com.android.launcher3:id/apps_customize_page_indicator').exists\
                        and self.get_current_packagename() == self.get_app_package_from_file('Launcher'):
                        self._logger.debug("Back Apps successfully.")
                        return True
                self._logger.debug("Back Apps fail!")
                return False
            elif self.get_current_page() <> (page+1):
                self.goto_page(page +1)
        return self.get_current_packagename() == self.get_app_package_from_file('Launcher')
    
    def click_bottom_apps(self, isScanApps, SucTimes, FailTimes):
        """launch the bottom apps in homepage
        
        @param isScanApps: click all the icons in apps if true and not if false
        @param SucTimes: Launch successfully times
        @param FailTimes: Launch fail times
        
        """
        if self._device(resourceId = 'com.android.launcher3:id/hotseat').child(resourceId = 'com.android.launcher3:id/layout').child(className = 'android.widget.TextView').exists:
            index_bottom = 0 
            while not self._device(resourceId = 'com.android.launcher3:id/hotseat').child(resourceId = 'com.android.launcher3:id/layout').child(index = index_bottom).child(description = 'Apps').exists:
                index_bottom += 1
                if index_bottom > 1:
                    self.save_fail_img()
                    self._logger.debug("Can't find the bottom.")
                    break
            app_num = self._device(resourceId = 'com.android.launcher3:id/hotseat').child(resourceId = 'com.android.launcher3:id/layout').child(index = index_bottom).getChildCount()
            
            self._logger.debug(str(app_num) + " Apps in bottom")
            for i in range(app_num):
                app_name = self._device(resourceId = 'com.android.launcher3:id/hotseat').child(className = 'android.widget.TextView',  instance = i).get_text()
                if self.check_black_app_from_file(app_name):
                    self._logger.debug("______" + app_name+ " in black list" )
                    continue
                elif  app_name <> '': 
                    self._logger.debug("______Open " + app_name)
                    self._device(resourceId = 'com.android.launcher3:id/hotseat').child(text = app_name).click()
                    self._device.delay(10)
                    
                    SucTimes, FailTimes = self.get_check_result(app_name, SucTimes, FailTimes)
                    
                    self.exit_app()
                    if self.get_current_packagename() <> self.get_app_package_from_file('Launcher'):
                        self._logger.info("Exit %s fail!!!", app_name)  
                        break;
                else:
                    self._logger.debug("______Open Apps")
                    self._device(resourceId = 'com.android.launcher3:id/hotseat').child(description = 'Apps').click()
                    if self._device(resourceId = 'com.android.launcher3:id/apps_customize_pane_content').exists:
                        self._logger.debug("Open Apps successfully.")
                        SucTimes += 1
                        self._logger.info("Trace Success Loop %s", SucTimes)
                        
                        if isScanApps:
                            SucTimes, FailTimes = self.click_apps_icons(SucTimes, FailTimes)  
                         
                    else:
                        self._logger.debug("Open Apps fail.")
                        FailTimes += 1
                        self.save_fail_img()
                    press_back_times = 0    
                    for press_back_times in range(5):
                        if not self._device(resourceId = 'com.android.launcher3:id/hotseat').exists:
                            self._device.press.back()
                            self._device.delay(2)
                        else:
                            break
                    if press_back_times > 3:
                        self._device.press.home()
        else:
            self._logger.debug("get bootom hotseat failed")
            self.save_fail_img()
            
        self._logger.info('Success: %s times', str(SucTimes))
        self._logger.info('Fail   : %s times', str(FailTimes))
        return SucTimes, FailTimes
    
    def click_apps_icons(self, SucTimes, FailTimes):
        """Click icon in apps
        
        @param SucTimes: Launch successfully times
        @param FailTimes: Launch fail times
        
        """
        if self._device(resourceId = 'com.android.launcher3:id/apps_customize_page_indicator').exists:
            all_page = self._device(resourceId = 'com.android.launcher3:id/apps_customize_page_indicator').getChildCount()
            self._logger.debug("-------------------------click icons in Apps")
            self._logger.debug("%s pages in apps.", str(all_page))
            for i in range(all_page):
                self._logger.debug("-------------------------Test in pages %s", str(i))
                self.stay_in_apps_page(i, all_page)
                if self._device(className = 'android.widget.TextView'). exists:
                    app_count_one_page = self._device(className = 'android.widget.TextView').count
                    self._logger.debug("%s apps in page %s." , str(app_count_one_page), str(i))
                    for j in range(app_count_one_page):
                        self.stay_in_apps_page(i, all_page)
                        if self._device(className = 'android.widget.TextView', instance = j). exists: 
                            app_name = self._device(className = 'android.widget.TextView', instance = j).get_text()
                            if app_name =='' or self.check_black_app_from_file(app_name):
                                self._logger.debug("______" + app_name+ " in black list" )
                                continue
                              
                            self._logger.debug("______Open " + app_name)
                            self._device(className = 'android.widget.TextView', instance = j).click()
                            self._device.delay(10)
                            SucTimes, FailTimes = self.get_check_result(app_name, SucTimes, FailTimes)
                            self.exit_app(enterApps = True)
                          
                            if self.get_current_packagename() <> 'com.android.launcher3':
                                self._logger.info("Exit %s fail!!!", app_name)  
                                self.save_fail_img()
                                break;                      
                        else:
                            self._logger.debug("Can't get the app index " + str(j))
                            self.save_fail_img()
        self._device.press.home()
        self._device.delay(1)
        
        self._logger.info('Success: %s times', str(SucTimes))
        self._logger.info('Fail   : %s times', str(FailTimes))
        return SucTimes, FailTimes
    
    def get_page_apps(self):
        """Get the current page in apps
        
        """
        if self._device(resourceId = 'com.android.launcher3:id/apps_customize_page_indicator').exists:
            all_page = self._device(resourceId = 'com.android.launcher3:id/apps_customize_page_indicator').getChildCount()
        else:
            self._logger.debug("Get all page in apps fail")
            return -1
        
        for current_page in range(all_page):
#             if self._device(resourceId = 'com.android.launcher3:id/apps_customize_page_indicator').child(index = current_page).\
#             child(className = 'android.widget.ImageView', resourceId = 'com.android.launcher3:id/active'). exists:
            if self._device(resourceId = 'com.android.launcher3:id/apps_customize_page_indicator', descriptionContains = 'Apps page ' + str(current_page+1) + ' of ' + str(all_page)). exists:
                return current_page
            
        self._logger.debug("Get current page in apps fail")
        return -1
    
    def stay_in_apps_page(self, page, pages_count):
        """keep in page given in apps
        
        @param page: keep in the page given, begin with 0
        @param pages_count: all pages in apps 
        
        """
        if self._device(resourceId = 'com.android.launcher3:id/hotseat').child(description = 'Apps').exists:
            self._device(resourceId = 'com.android.launcher3:id/hotseat').child(description = 'Apps').click()
            self._device.delay(2)
            
        current_page = self.get_page_apps()
        if current_page == page:
            return True
        elif current_page > page:
            for i in range(current_page - page):
                self._logger.debug("_____Swipe to left one time.")
                self._device(resourceId = 'com.android.launcher3:id/apps_customize_pane_content').swipe.right(steps = 5)
                self._device.delay(2)
        else:
            for i in range(page - current_page):
                self._logger.debug("_____Swipe to right one time.")
                self._device(resourceId = 'com.android.launcher3:id/apps_customize_pane_content').swipe.left(steps = 5)
                self._device.delay(2)
                
        current_page = self.get_page_apps()
        if current_page == page:
            self._logger.debug("Go go page %s in apps successfully", page)
            return  True
        else:
            self._logger.debug("Current page in apps is %s", str(current_page))
            self._logger.debug("Go go page %s in apps fail!", page)
            return False
                                  