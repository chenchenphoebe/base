"""filemanager library for scripts.
"""

import re
import sys
from common import Common
PicPath = sys.path[0]+"\\PicComparison\\"

class Filemanager(Common):
   
    def __init__(self, device, log_name):
        Common.__init__(self, device,log_name)
        self._ssid = None
        
    def save_fail_img(self):
        """Save fail screenshot to Filemanager Folder
        
        """
        self.save_img("Filemanager") 
        
    def stay_in_filemanger(self):
        """Keep in Filemanager main page
    
        """
        if self.get_current_packagename() == self.get_app_package_from_file('File Manager'):
            maxtime = 0
            while not self._device(description = 'Create folder').exists:
                self._device.press.back()
                self._device.delay(1)
                maxtime += 1
                if maxtime > 3:
                    self._logger.debug("Can't back File Manager")
                    break
            if maxtime < 4:
                return True

        self._device.press.home()
        self._logger.debug("Launch File Manager.")
        if self.enter_app('File Manager'):
            self._device.delay(2)
            if self.get_current_packagename() == self.get_app_package_from_file('File Manager'):  
                maxtime = 0
                while not self._device(description = 'Create folder').exists:
                    self._device.press.back()
                    self._device.delay(1)
                    maxtime += 1
                    if maxtime > 3:
                        self._logger.debug("Can't back File Manager")
                        break
                if maxtime < 4:
                    return True                 
            
            self._logger.debug('Launch File Manager main page fail')
            return False
        else:
            return False 
    
    
    def remove_all_file(self, indicate):
        """Remove all files in sdcard by given indicate
            @param param: files indicate such as '*.png'
        
        """
        self._device.shell_adb("shell rm /sdcard/" + indicate)
        
    def scroll_find_file(self, name):
        """find the file given
        
        @param name: file or folder name
        
        """
        if self._device(resourceId = 'com.mediatek.filemanager:id/edit_adapter_name', text = name).exists:
            return True
        
        if self._device(resourceId= 'com.mediatek.filemanager:id/list_view', scrollable = 'true').exists:
            self._device(resourceId= 'com.mediatek.filemanager:id/list_view').scroll.toBeginning()
            
            if not self._device(resourceId = 'com.mediatek.filemanager:id/edit_adapter_name').exists:
                self._logger.debug("Can't get the item name")
                return False
            first_folder_name = self._device(resourceId = 'com.mediatek.filemanager:id/edit_adapter_name', instance = 0).get_text()
            
            scroll_time = 0
            while True:
                if self._device(resourceId = 'com.mediatek.filemanager:id/edit_adapter_name', text = name).exists:
                    return True
                else:
                    self._device(resourceId= 'com.mediatek.filemanager:id/list_view').scroll.vert.forward()
                    self._logger.debug("Scroll one time.")
                    scroll_time += 1
                    
                if not self._device(resourceId = 'com.mediatek.filemanager:id/edit_adapter_name').exists:
                    self._logger.debug("Can't get the item name")
                    return False
                first_folder_name_current = self._device(resourceId = 'com.mediatek.filemanager:id/edit_adapter_name', instance = 0).get_text()
                if first_folder_name == first_folder_name_current:
                    self._logger.debug("It's list bottom. Can't find the item name.")
                    return  False
                else:
                    first_folder_name = first_folder_name_current
                    
                if scroll_time > 20:
                    self._logger.debug("Too more files.Stop finding.") 
                    return False
        else:
            self._logger.debug("Can't find the item name.")
            return False
    
    
    def get_open_path(self):
        """get the current path opened
        
        """
        if self._device(resourceId = 'com.mediatek.filemanager:id/tabs_holder').exists:
            pathLenghCurrent = self._device(resourceId = 'com.mediatek.filemanager:id/tabs_holder').getChildCount()
            path_current = []
            for i in range(pathLenghCurrent):
                if i == 0:
                    path_current.append('Home')
                elif i <> (pathLenghCurrent -1):
                    path_current.append(str(self._device(resourceId = 'com.mediatek.filemanager:id/tabs_holder').child(index = i).get_text()))
#             self._logger.debug('Current path is '+ '/'.join(path_current))
            return path_current
        else:
            self._logger.debug('Can\'t located current path ')
            return ''
    
    def open_path(self, pathName):
        """Open the given path
        
            @param pathName: the path such as 'Phone storage/DCIM/Camera'
        
        """
        self._logger.debug('To open '+ pathName)
        pathName = 'Home/' + pathName
        path = pathName.split("/")
        path_current = self.get_open_path()
        
        pathlengh_open = len(path)
        pathlengh_current = len(path_current)
        
        #get the same path
        sam_lenth = 0;
        if pathlengh_current > pathlengh_open:
            com_time = pathlengh_open
        else:
            com_time = pathlengh_current
        for i in range(com_time):
            if path_current[i] == path[i]:
                sam_lenth += 1
            else:
                break

        #back to the same path
        for i in range(pathlengh_current - sam_lenth):
            self._device.press.back()
            self._device.delay(2)
            path_new = self.get_open_path() 
            if not path_current[pathlengh_current-i-2] == path_new[len(path_new) - 1]:
                self._logger.debug('Back to '+ path_current[pathlengh_current-i-2] + ' fail.')
                break

            
        click_time = pathlengh_open - sam_lenth
        for i in range(click_time):
            if self.scroll_find_file(path[sam_lenth]):
                self._device(resourceId = 'com.mediatek.filemanager:id/edit_adapter_name', text = path[sam_lenth]).click()
                self._device.delay(2)
            path_new = self.get_open_path()  
            if not path[sam_lenth] ==  path_new[len(path_new) -1]:
                self._logger.debug('Can\'t open' + path[sam_lenth + 1])
                return False
            else:
                sam_lenth += 1
        
        if self.get_open_path() == path:
            self._logger.debug('Already open '+ pathName)
            return True 
        else:
            self._logger.debug('Open '+ pathName + ' fail')
            return False    
                
    
    def add_folder(self, name):
        """creat a folder by given name
        
        @param name: folder name
        
        
        """
        self._logger.debug('To add folder ' + name)
        if not self._device(resourceId = 'com.mediatek.filemanager:id/create_folder').exists:
            self._logger.debug('Can\'t find the add button.')
            return False 
        self._device(resourceId = 'com.mediatek.filemanager:id/create_folder').click()
        self._device.delay(2)
        
        if not self._device(resourceId = 'com.mediatek.filemanager:id/edit_text').exists:
            self._logger.debug('Can\'t find the input folder name view.')
            return False
        self._device(resourceId = 'com.mediatek.filemanager:id/edit_text').set_text(name)
        self._device.delay(2)
        
        if not self._device(resourceId = 'android:id/button1', text = 'OK').exists:
            self._logger.debug('Can\'t find the OK button.')
            return False
        self._device(resourceId = 'android:id/button1', text = 'OK').click()
        self._device.delay(2)
        
        if self._device(resourceId = 'com.mediatek.filemanager:id/edit_adapter_name', text = name).exists:
            self._logger.debug('The folder ' + name + ' is added')
            return True
        elif self.scroll_find_file(name):
            self._logger.debug('The folder ' + name + ' is added')
            return True
        else:
            self._logger.debug('Can\'t find the folder ' + name)
            return False
        
    def delete_item(self, name):
        """delete the folder by given name
        
        @param name: folder name
        
        
        """
        self._logger.debug('To delete folder or file ' + name)
        if not self.scroll_find_file(name):
            self._logger.debug('Can\'t find the folder or file ' + name)
            return False
       
        self._device(resourceId = 'com.mediatek.filemanager:id/edit_adapter_name', text = name).long_click()
        self._device.delay(5)
        if not self._device(resourceId = 'com.mediatek.filemanager:id/delete').exists:
            self._logger.debug('Select the folder or file ' + name + 'fail!')
            return False
        self._device(resourceId = 'com.mediatek.filemanager:id/delete').click()
        self._device.delay(2)
        
        if self._device(resourceId = 'android:id/button1', text = 'OK').exists:
            self._device(resourceId = 'android:id/button1', text = 'OK').click()
            self._device.delay(2)
              
        if not self.scroll_find_file(name):
            self._logger.debug('The folder or file ' + name + 'is deleted')
            return True
        else:
            self._logger.debug('Delete the folder or file' + name + 'fail!')
            return False
        
    def open_file(self, type):
        """Open file by given type
        @param type: file type
        
        """
        if type == 'Picture':
            if self._device(resourceId = 'com.mediatek.filemanager:id/edit_adapter_name', textContains  = '.jpg').exists:
                self._device(resourceId = 'com.mediatek.filemanager:id/edit_adapter_name', textContains  = '.jpg', instance = 0).click()
                self._device.delay(5)
                if self.choose_first_player():
                    self._device.delay(5)
                if self._device(resourceId = 'com.tct.gallery3d:id/gl_root_view').exists\
                    or self._device(resourceId = 'com.android.gallery3d:id/gl_root_view').exists\
                    or self._device(resourceId = 'com.google.android.apps.plus:id/photo_hashtag_fragment_container').exists\
                    or self._device(resourceId = 'com.google.android.apps.photos:id/photo_hashtag_fragment_container').exists:
                    self._logger.debug('Open picture successfully.')
                    return True
                else:
                    self._logger.debug('Open picture fail!')
                    return False
            else:
                self._logger.debug('No picture file exists.')
                return False
        elif type == 'Music':
            if self._device(resourceId = 'com.mediatek.filemanager:id/edit_adapter_name', textContains  = '.mp3').exists:
                self._device(resourceId = 'com.mediatek.filemanager:id/edit_adapter_name', textContains  = '.mp3', instance = 0).click()
                self._device.delay(5)
                if self.choose_first_player():
                    self._device.delay(5)
                    
                if self._device(resourceId = 'com.alcatel.music5:id/progress').exists\
                    or self._device(resourceId = 'com.google.android.music:id/progress').exists:
                    self._logger.debug('Play music successfully.')
                    self._device.delay(10)
                    return True
                else:
                    self._logger.debug('Play music fail!')
                    return False
            else:
                self._logger.debug('No music file exists.')
                return False
            
        elif type == 'Video':
            if self._device(resourceId = 'com.mediatek.filemanager:id/edit_adapter_name', textContains  = '.mp4').exists:
                self._device(resourceId = 'com.mediatek.filemanager:id/edit_adapter_name', textContains  = '.mp4', instance = 0).click()
                self._device.delay(5)
                if self.choose_first_player():
                    self._device.delay(5)
                    
                if self._device(resourceId = 'android:id/button2', text = 'Start over').exists:
                    self._device(resourceId = 'android:id/button2', text = 'Start over').click()
                    self._device.delay(3)
                    
                for i in range(3):
                    if self._device(resourceId = 'com.google.android.apps.plus:id/videoplayer').exists\
                      or self._device(resourceId = 'com.google.android.apps.photos:id/photos_videoplayer_videolayout').exists\
                      or self._device(resourceId = 'com.tct.gallery3d:id/surface_view').exists\
                      or self._device(resourceId = 'com.android.gallery3d:id/surface_view').exists:
                        self._logger.debug('Play video successfully.')
                        self._device.delay(10)
                        return True
                    else:
                        self._device.delay(5)
                self._logger.debug('Play video fail!')
                return False
            else:
                self._logger.debug('No video file exists.')
                return False
        else:
            self._logger.debug('Unknow file type.')
            return False
            
    def back_folder(self, path):
        """Back to filemanager folder given when switch to other apps
        @param folder_name: folder name
        
        """
        folder_names = path.split("/")
        folder_name = folder_names[len(folder_names) -1]
        for i in range(3):
            self._device.press.back()
            self._device.delay(3)
            current_path = self.get_open_path()
            if self.get_current_packagename() == self.get_app_package_from_file('File Manager')\
                and current_path[len(current_path)-1] == folder_name:
                self._logger.debug('Back ' + folder_name)
                return True
        
        self._logger.debug('Fail to back ' + folder_name)
        self.stay_in_filemanger()
        return False
    
    def copy_file(self, path_from, path_to, file_name = ''):
        """copy a file from one path to the other path
        @param path_from: file path exist
        @param path_to: file the need copy to 
                
        """
        self.open_path(path_from)
        if file_name == '':
            if self._device(resourceId = 'com.mediatek.filemanager:id/edit_adapter_name', textContains = '.').exists:
                file_name = self._device(resourceId = 'com.mediatek.filemanager:id/edit_adapter_name', textContains = '.').get_text()
            else:
                self._logger.debug("Can't find the file contain '.'")
                return  False
        if not self.scroll_find_file(file_name):
            self._logger.debug("Can't find the file")
            return  False
        
        self._device(resourceId = 'com.mediatek.filemanager:id/edit_adapter_name', text = file_name).long_click()
        self._device.delay(5)
        if not self._device(resourceId = 'com.mediatek.filemanager:id/copy').exists:
            self._logger.debug('Select the folder ' + file_name + 'fail!')
            return False

        self._device(resourceId = 'com.mediatek.filemanager:id/copy').click()
        self._device.delay(2)
        if not self._device(description = 'Create folder').exists:
            self._logger.debug("Can't back main page after click copy")
            return False
        
        self.open_path(path_to)
          
        if not self._device(resourceId = 'com.mediatek.filemanager:id/paste').exists:
            self._logger.debug("View Copy isn't exist")
            return False
        self._device(resourceId = 'com.mediatek.filemanager:id/paste').click()
        self._device.delay(3)
        
        if self.scroll_find_file(file_name):
            self._logger.debug('Copy ' + file_name + ' successfully.')
            if self.delete_item(file_name):
                return True
            else:
                return False
        else:
            self._logger.debug('Copy ' + file_name + ' fail!')
            return False
        
        
        
            
            