"""filemanager library for scripts.
"""
import re
import sys
from common import Common
from test.test_os import resource

PicPath = sys.path[0] + "\\PicComparison\\"


class Filemanager(Common):
    def __init__(self, device, log_name):
        Common.__init__(self, device, log_name)
        self._ssid = None

    def save_fail_img(self):
        """Save fail screenshot to Filemanager Folder
        
        """
        self.save_img("Filemanager")

    def stay_in_filemanger(self):
        """Keep in Filemanager main page
    
        """
        if self.get_current_packagename() == self.get_app_package_from_file('Files'):
            maxtime = 0
            while not self._device(resourceId='com.jrdcom.filemanager:id/path_text').exists:
                self._device.press.back()
                self._device.delay(1)
                maxtime += 1
                if maxtime > 3:
                    self._logger.debug("Can't back Files")
                    break
            if maxtime < 4:
                return True

        self._logger.debug("Launch Files.")
        if self.enter_app('Files'):
            self._device.delay(2)
            if not self.get_current_packagename() == self.get_app_package_from_file('Files'):
                self._device.press.back()
            if self.get_current_packagename() == self.get_app_package_from_file('Files'):
                maxtime = 0
                while not self._device(resourceId='com.jrdcom.filemanager:id/path_text').exists:
                    self._device.press.back()
                    self._device.delay(1)
                    maxtime += 1
                    if maxtime > 3:
                        self._logger.debug("Can't back Files")
                        break
                if maxtime < 4:
                    return True

            self._logger.debug('Launch Files main page fail')
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
        if self._device(resourceId='com.jrdcom.filemanager:id/edit_adapter_name', text=name).exists:
            return True

        if name == 'Phone' or name == 'Internal storage':
            if self._device(resourceId='com.jrdcom.filemanager:id/phone_name', text=name).exists:
                return True

        if self._device(resourceId='com.jrdcom.filemanager:id/list_view', scrollable='true').exists:
            self._device(resourceId='com.jrdcom.filemanager:id/list_view').scroll.toBeginning()

            if not self._device(resourceId='com.jrdcom.filemanager:id/edit_adapter_name').exists:
                self._logger.debug("Can't get the item name1")
                return False
            first_folder_name = self._device(resourceId='com.jrdcom.filemanager:id/edit_adapter_name',
                                             instance=0).get_text()

            scroll_time = 0
            while True:
                if self._device(resourceId='com.jrdcom.filemanager:id/edit_adapter_name', text=name).exists:
                    return True
                else:
                    self._device(resourceId='com.jrdcom.filemanager:id/list_view').scroll.vert.forward()
                    self._logger.debug("Scroll one time.")
                    scroll_time += 1

                if not self._device(resourceId='com.jrdcom.filemanager:id/edit_adapter_name').exists:
                    self._logger.debug("Can't get the item name1")
                    return False
                first_folder_name_current = self._device(resourceId='com.jrdcom.filemanager:id/edit_adapter_name',
                                                         instance=0).get_text()
                if first_folder_name == first_folder_name_current:
                    self._logger.debug("It's list bottom. Can't find the item name1.")
                    return False
                else:
                    first_folder_name = first_folder_name_current

                if scroll_time > 20:
                    self._logger.debug("Too more files.Stop finding.")
                    return False
        else:
            self._logger.debug("Can't find the item name2.")
            return False

    def get_open_path(self):
        """get the current path opened
        
        """
        if self.get_current_packagename() == self.get_app_package_from_file('Files'):

            if self._device(resourceId='com.jrdcom.filemanager:id/phone_name', text='Internal storage').exists \
                    or self._device(resourceId='com.jrdcom.filemanager:id/phone_name', text='SD').exists:
                path_current = []
                path_current.append('HOME')
                self._logger.debug('Current path is %s', path_current)
                return ['HOME']

            elif self._device(resourceId='com.jrdcom.filemanager:id/path_text', text='Internal storage').exists:
                path_current = []
                path_current.append('HOME')
                path_current.append(str(self._device(resourceId='com.jrdcom.filemanager:id/path_text').get_text()))
                self._logger.debug('Current path is %s', path_current)
                return path_current

            elif self._device(resourceId='com.jrdcom.filemanager:id/main_filebrower').child(
                    resourceId='com.jrdcom.filemanager:id/main_horizontallist_icon').exists:
                path_current = []
                path_current.append('HOME')
                path_current.append('Internal storage')
                path_current.append(str(self._device(resourceId='com.jrdcom.filemanager:id/path_text').get_text()))
                self._logger.debug('Current path is %s', path_current)
                return path_current

        else:
            self._logger.debug('Can\'t located current path ')
            return ''

    def open_path(self, pathName):
        """Open the given path
        
            @param pathName: the path such as 'PHONE/DCIM/Camera'
        
        """
        self._logger.debug('To open ' + pathName)
        pathName = 'HOME/' + pathName
        path = pathName.split("/")

        # get the current path
        path_current = self.get_open_path()
        pathlengh_open = len(path)
        pathlengh_current = len(path_current)

        # get the same path
        sam_lenth = 0
        if pathlengh_current > pathlengh_open:
            com_time = pathlengh_open
        else:
            com_time = pathlengh_current
        self._logger.debug('com_time= %s', com_time)
        for i in range(com_time):
            if path_current[i].upper() == path[i].upper():
                sam_lenth += 1
                self._logger.debug(sam_lenth)
            else:
                break

        # back to the same path
        self._logger.debug('pathlengh_current - sam_lenth= %s', pathlengh_current - sam_lenth)
        for i in range(pathlengh_current - sam_lenth):
            self._device.press.back()
            self._device.delay(2)
            path_new = self.get_open_path()
            if not path_current[pathlengh_current - i - 2].upper() == path_new[len(path_new) - 1].upper():
                self._logger.debug('Back to ' + path_current[pathlengh_current - i - 2] + ' fail.')
                break

        click_time = pathlengh_open - sam_lenth
        self._logger.debug('click_time= %s', click_time)
        for i in range(click_time):
            if path[sam_lenth] == 'Phone':
                if self._device(resourceId='com.jrdcom.filemanager:id/phone_name', text='Phone').exists:
                    self._device(resourceId='com.jrdcom.filemanager:id/phone_name', text='Phone').click()
            elif path[sam_lenth] == 'Internal storage':
                if self._device(resourceId='com.jrdcom.filemanager:id/phone_name', text='Internal storage').exists:
                    self._device(resourceId='com.jrdcom.filemanager:id/phone_name', text='Internal storage').click()
            elif self.scroll_find_file(path[sam_lenth]):
                #                 if self._device(resourceId = 'com.jrdcom.filemanager:id/list_view').child(className = 'android.widget.LinearLayout', index = 1).child(text = path[sam_lenth]).exists:
                #                     self._logger.debug('55804')
                #                     self._device(resourceId= 'com.jrdcom.filemanager:id/list_view').scroll.vert.backward()
                #                     self._device.delay(2)
                #                 if self.scroll_find_file(path[sam_lenth]):
                self._device(resourceId='com.jrdcom.filemanager:id/edit_adapter_name', text=path[sam_lenth]).click()
            self._device.delay(2)
            self._device.press.home()
            self.stay_in_filemanger()
            path_new = self.get_open_path()
            if not path[sam_lenth].upper() == path_new[len(path_new) - 1].upper():
                self._logger.debug('Can\'t open' + path[sam_lenth + 1])
                return False
            else:
                sam_lenth += 1
        # path_upper = [item.upper() for item in path ]

        if self.get_open_path() == path:
            self._logger.debug('Already open ' + pathName)
            return True
        else:
            self._logger.debug('Open ' + pathName + ' fail')
            return False

    def add_folder(self, name):
        """creat a folder by given name
        
        @param name: folder name
        
        
        """
        self._logger.debug('To add folder ' + name)

        if not self._device(resourceId='com.jrdcom.filemanager:id/more_btn').exists:
            self._logger.debug('Can\'t find the more button.')
            return False
        self._device(resourceId='com.jrdcom.filemanager:id/more_btn').click()
        self._device.delay(2)

        if not self._device(resourceId='com.jrdcom.filemanager:id/createfolder_item').exists:
            self._logger.debug('Can\'t find the createfolder_item.')
            return False
        self._device(resourceId='com.jrdcom.filemanager:id/createfolder_item').click()
        self._device.delay(2)

        if not self._device(resourceId='com.jrdcom.filemanager:id/edit_text', text='Folder name').exists:
            self._logger.debug('Can\'t find the add folder name button.')
            return False
        self._device(resourceId='com.jrdcom.filemanager:id/edit_text', text='Folder name').set_text(name)
        self._device.delay(2)

        if not self._device(resourceId='android:id/button1', text='CREATE').exists:
            self._logger.debug('Can\'t find the create button.')
            return False
        self._device(resourceId='android:id/button1', text='CREATE').click()
        self._device.delay(2)

        if self._device(resourceId='com.jrdcom.filemanager:id/edit_adapter_name', text=name).exists:
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
        self._device.delay(2)
        self._device(resourceId='com.jrdcom.filemanager:id/edit_adapter_name', text=name).long_click()
        self._device.delay(5)
        long_click_time = 0
        while not self._device(resourceId='com.jrdcom.filemanager:id/ic_selected').exists:
            self._device.press.back()
            self._device.delay(1)
            long_click_time += 1
            if long_click_time > 3:
                self._logger.debug("Can't select the folder" + name)
                break
            if long_click_time < 4:
                return True
            self._logger.debug('Select the folder or file ' + name + 'fail!')
            return False

        #         if self._device(description = 'More options').exists:
        #             self._device(description = 'More options').click()
        #             self._device.press.menu()
        if self._device(resourceId='com.jrdcom.filemanager:id/delete_btn').exists:
            self._device(resourceId='com.jrdcom.filemanager:id/delete_btn').click()
            self._device.delay(2)

        elif self._device(resourceId='com.jrdcom.filemanager:id/more_btn').exists:
            self._device(resourceId='com.jrdcom.filemanager:id/more_btn').click()
            self._device.delay(3)
            if self._device(resourceId='com.jrdcom.filemanager:id/delete_item_normal', text='Delete').exists:
                self._device(text='Delete').click()
                self._device.delay(2)
            else:
                self._logger.debug("Menu delete isn't exist")
                return False
        else:
            self._logger.debug("More options isn't exist")
            return False

        if self._device(resourceId='android:id/button1', text='DELETE').exists:
            self._device(resourceId='android:id/button1', text='DELETE').click()
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
            if self._device(resourceId='com.jrdcom.filemanager:id/edit_adapter_name', textContains='.jpg').exists:
                self._device(resourceId='com.jrdcom.filemanager:id/edit_adapter_name', textContains='.jpg',
                             instance=0).click()
                self._device.delay(2)
                while self._device(resourceId='com.android.packageinstaller:id/permission_message').exists:
                    self._device(text='ALLOW').click()
                    self._device.delay(2)

                if self.choose_first_player():
                    self._device.delay(5)
                if self._device(resourceId='com.tct.tablet.gallery3d:id/imageView').exists \
                        or self._device(
                            resourceId='com.google.android.apps.plus:id/photo_hashtag_fragment_container').exists \
                        or self._device(resourceId='com.google.android.apps.photos:id/photo_view_pager').exists:
                    self._logger.debug('Open picture successfully.')
                    return True
                else:
                    self._logger.debug('Open picture fail!')
                    return False
            else:
                self._logger.debug('No picture file exists.')
                return False
        elif type == 'Music':
            if self._device(resourceId='com.jrdcom.filemanager:id/edit_adapter_name', textContains='.mp3').exists:
                self._device(resourceId='com.jrdcom.filemanager:id/edit_adapter_name', textContains='.mp3',
                             instance=0).click()
                self._device.delay(2)
                if self.choose_first_player():
                    self._device.delay(5)

                if self._device(resourceId='com.alcatel.music5:id/preview_seek_bar').exists \
                        or self._device(resourceId='com.google.android.music:id/progress').exists:
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
            if self._device(resourceId='com.jrdcom.filemanager:id/edit_adapter_name', textContains='.mp4').exists:
                self._device(resourceId='com.jrdcom.filemanager:id/edit_adapter_name', textContains='.mp4',
                             instance=0).click()
                self._device.delay(3)
                while self._device(resourceId='com.android.packageinstaller:id/permission_message').exists:
                    self._device(text='ALLOW').click()
                    self._device.delay(2)
                if self.choose_first_player():
                    self._device.delay(5)

                if self._device(resourceId='com.tct.tablet.gallery3d:id/button_restart', text='START OVER').exists:
                    self._device(resourceId='com.tct.tablet.gallery3d:id/button_restart', text='START OVER').click()
                    self._device.delay(3)

                if self._device(resourceId='com.google.android.apps.plus:id/videoplayer').exists \
                        or self._device(
                            resourceId='com.google.android.apps.photos:id/photos_videoplayer_view_video_view_holder').exists \
                        or self._device(resourceId='com.tct.tablet.gallery3d:id/surface_view').exists:
                    self._logger.debug('Play video successfully.')
                    self._device.delay(10)
                    return True
                else:
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
        folder_name = folder_names[len(folder_names) - 1]
        for i in range(3):

            self._device.press.back()
            self._device.delay(5)
            if self._device(resourceId='com.jrdcom.filemanager:id/main_filebrower').exists:
                self._logger.debug('Back ' + folder_name)
                if folder_name == 'Movies':
                    if self._device.orientation == 'left' or self._device.orientation == 'right':
                        self._device.orientation = 'natural'
                return True

        if folder_name == 'Movies':
            if self._device.orientation == 'left' or self._device.orientation == 'right':
                self._device.orientation = 'natural'
        self._logger.debug('Fail to back ' + folder_name)
        self.stay_in_filemanger()
        return False

    def copy_file(self, path_from, path_to, file_name=''):
        """copy a file from one path to the other path
        @param path_from: file path exist
        @param path_to: file the need copy to 
                
        """
        self.open_path(path_from)
        if file_name == '':
            if self._device(resourceId='com.jrdcom.filemanager:id/edit_adapter_name', textContains='.').exists:
                file_name = self._device(resourceId='com.jrdcom.filemanager:id/edit_adapter_name',
                                         textContains='.').get_text()
            else:
                self._logger.debug("Can't find the file contain '.'")
                return False
        if not self.scroll_find_file(file_name):
            self._logger.debug("Can't find the file")
            return False

        self._device(resourceId='com.jrdcom.filemanager:id/edit_adapter_name', text=file_name).long_click()
        self._device.delay(5)
        if not self._device(resourceId='com.jrdcom.filemanager:id/ic_selected').exists:
            self._logger.debug('Select the folder ' + file_name + 'fail!')
            return False

        #         if self._device(description = 'More options').exists:
        #             self._device(description = 'More options').click()
        #             self._device.press.menu()
        if self._device(resourceId='com.jrdcom.filemanager:id/more_btn').exists:
            self._device(resourceId='com.jrdcom.filemanager:id/more_btn').click()
        else:
            self._logger.debug("More options isn't exist")
            return False
        self._device.delay(2)

        if self._device(resourceId='com.jrdcom.filemanager:id/copy_item_normal', text='Copy').exists:
            self._device(text='Copy').click()
            self._device.delay(2)
        else:
            self._logger.debug("Menu Copy isn't exist")
            return False

        if not self._device(resourceId='com.jrdcom.filemanager:id/floating_action_button').exists:
            self._logger.debug("Can't back main page after click copy")
            return False

        self.open_path(path_to)
        #         if self._device(description = 'More options').exists:
        #             self._device(description = 'More options').click()
        #             self._device.press.menu()
        if self._device(resourceId='com.jrdcom.filemanager:id/more_btn').exists:
            self._device(resourceId='com.jrdcom.filemanager:id/more_btn').click()
        else:
            self._logger.debug("More options isn't exist")
            return False
        self._device.delay(2)

        if self._device(resourceId='com.jrdcom.filemanager:id/paste_item_normal', text='Paste').exists \
                or self._device(resourceId='com.jrdcom.filemanager:id/title', text='Paste').exists \
                or self._device(resourceId='android:id/title', text='Paste').exists:
            self._device(text='Paste').click()
            self._device.delay(2)
        else:
            self._logger.debug("Menu Paste isn't exist")
            return False
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

    """
    initial
    """

    def import_contact(self, name):
        """
        import the Contacts
        """
        self.stay_in_filemanger()
        self.open_path('Internal storage')
        self._logger.debug('click the Contacts_51-100.vcf')
        if not self.scroll_find_file(name):
            self._logger.debug('Can\'t find the folder or file ' + name)
            return False
        self._device.delay(2)
        self._device(resourceId='com.jrdcom.filemanager:id/edit_adapter_name', text=name).click()
        while self._device(resourceId='com.android.packageinstaller:id/permission_message').exists:
            self._device(text='ALLOW').click()
            self._device.delay(2)
        self._device.delay(2)
        self._device.swipe(385, 3, 410, 1169)
        self._device.delay(2)
        if self._device(resourceId='android:id/title', text='Finished importing vCard Contacts_51-100.vcf').exists:
            self._logger.debug('Finished importing vCard Contacts_51-100.vcf successfully')
            self._device.swipe(410, 1169, 385, 3)
            return True
        else:
            self._logger.debug('import vCard Contacts_51-100.vcf successfully fail')
