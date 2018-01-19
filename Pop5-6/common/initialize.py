from common import Common


class Initialize(Common):
    """Provide common functions for scripts, such as launching activity."""

    def __init__(self, device, log_name):
        Common.__init__(self, device, log_name)
        self._ssid = None

    def save_fail_img(self):
        """Save fail screenshot to Messaging Folder
        
        """
        self.save_img("Initial")

    """
    Initial setting
    """

    def device_wakeup(self):
        self._logger.debug('Make device to make up')
        self._device.wakeup()
        self._logger.debug('the screen is on')
        return True

    def enterSettings(self, option):
        '''enter the option of settings

         @param option: the text of the settings option

        '''
        if self.enter_app('Settings'):
            if self._device(text=option).wait.exists(timeout=2000):
                self._logger.debug("enter " + option + " setting")
                self._device(text=option).click()
                self._device.delay(2)
            else:
                self._device(scrollable=True).scroll.to(text=option)
                self._logger.debug("enter " + option + " setting")
                self._device(text=option).click()
                self._device.delay(2)
            if self._device(text=option).wait.exists(timeout=1000):
                return True
        self.save_fail_img()
        return False

    def set_sleep_mode(self, mode):
        self._logger.debug('set the sleep mode to %s', mode)
        if self._device(text='Sleep').wait.exists:
            self._device(text='Sleep').click()
        if self._device(text=mode).wait.exists:
            self._device(text=mode).click()
            return True
        self._logger.debug('set the sleep mode to Never fail')
        return False

    def wakeupAunlock(self):
        self._logger.debug('make device to wake up')
        self._device.wakeup()
        self._logger.debug('unlock screen')
        if self._device(description='Unlock').wait.exists(timeout=3000):
            self._device.swipe(402, 1116, 402, 195)
            self._device.delay(2)
            return True
        else:
            self._logger.debug('unlock is already')
            return True
        self._logger.debug('unlock screen fail!')
        return False

    def Min_Brightness(self):
        if self._device(text='Brightness level').wait.exists(timeout=2000):
            self._device(text='Brightness level').click()
            if self._device(resourceId='com.android.systemui:id/slider', text='Display brightness').wait.exists(
                    timeout=2000):
                self._device.click(173, 64)

    def Min_Volume(self):
        if self._device(text='Sound').wait.exists(timeout=2000):
            self._device.click(170, 547)
            self._device.click(170, 754)
            self._device.click(170, 961)
            self._device.click(170, 1165)

    def turn_wifi_on(self):
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

    def connect_wifi(self, hotspotName, password):
        '''device connect wifi hotspot
         @param (str)hotspotName: the wifi hotspot's name 
         @param (str)password: the wifi hotspot's password
               
        '''
        if self._device(textContains='Connected').wait.exists(timeout=10000):
            self._logger.debug('wifi has connected.')
            return True
        else:
            for i in range(5):
                self.scroll_find_ap('Add network')
                self._device.delay(1)
                if self._device(text='Add network').click():
                    break;
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

    def set_sleep_mode(self, mode):
        self._logger.debug('set the sleep mode to %s', mode)
        if self._device(text='Sleep').wait.exists:
            self._device(text='Sleep').click()
        if self._device(text=mode).wait.exists:
            self._device(text=mode).click()
            return True
        self._logger.debug('set the sleep mode to Never fail')
        return False

    def enter_chrome(self):

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
            self._device.delay(30)
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

    def get_total_bookmarks(self):
        if self._device(resourceId='com.android.chrome:id/bookmark_items_container').exists:
            return self._device(resourceId='com.android.chrome:id/bookmark_items_container').getChildCount()
        else:
            return False

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
        while self._device(text='Create contact under account').exists:
            self._device(text='Tablet').click()
            self._device.delay(2)
        self.click_allow()
        self._device.delay(2)
        self._device.open.notification()
        self._device.delay(2)
        if self._device(resourceId='android:id/app_name_text', text='Contacts').exists:
            self._logger.debug('Finished importing vCard Contacts_51-100.vcf successfully')
            self._device(text='CLEAR ALL').click()
            return True
        else:
            self._logger.debug('import vCard Contacts_51-100.vcf successfully fail')
            return False

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

    def email_accountSet(self, accountName, password):
        """login Email account
        argv: accountName --email accout name
              password --email password
        author:hanbei
        """
        self._logger.debug('set email account')
        self.enter_app('Email')
        self._device.delay(2)
        if self._device(text='ALLOW').exists:
            self._device(text='ALLOW').click()
            self._device.delay(2)
        if self._device(text='Other').exists:
            self._device(text='Other').click()
            self._device.delay(2)
            self._device(text='NEXT').click()
        if self._device(resourceId='com.tct.email:id/account_email').exists:
            self._logger.debug('input the account name:%s', accountName)
            self._device(resourceId='com.tct.email:id/account_email').set_text(accountName)
            self._device.delay(2)
            self._device(text='NEXT').click()
            if self._device(text='Exchange').wait.exists(timeout=30000):
                self._device(text='Exchange').click()
                self._device.delay(2)
            if self._device(resourceId='com.tct.email:id/regular_password').exists:
                self._logger.debug('input the password:%s', password)
                self._device(resourceId='com.tct.email:id/regular_password').set_text(password)
                self._device.delay(2)
                self._device(text='NEXT').click()
                if self._device(text='Incoming server settings').wait.exists(timeout=60000):
                    self._device(resourceId='com.tct.email:id/account_username').clear_text()
                    self._device.delay(2)
                    self._device(resourceId='com.tct.email:id/account_username').set_text(
                        'tct-hq\\' + str(accountName[:12]))
                    self._device.delay(2)
                    if not self._device(resourceId='com.tct.email:id/account_server').wait.exists(timeout=2000):
                        self._device(scrollable=True).scroll.vert.to(resourceId='com.tct.email:id/account_server')
                    self._device(resourceId='com.tct.email:id/account_server').set_text('mailsz.tct.tcl.com')
                    self._device.delay(2)
                    if not self._device(resourceId='com.tct.email:id/account_security_type').wait.exists(timeout=2000):
                        self._device(scrollable=True).scroll.vert.to(resourceId='com.tct.email:id/account_security_type')
                    self._device(resourceId='com.tct.email:id/account_security_type').click()
                    self._device.delay(2)
                    self._device(textContains='Accept all certificates').click()
                    self._device(text='NEXT').click()
                    if self._device(text='Remote security administration').wait.exists(timeout=180000):
                        self._device(text='OK').click()
                        if self._device(text='Account options').wait.exists(timeout=30000):
                            self._device(resourceId='com.tct.email:id/account_check_frequency').click()
                            self._device(text='Never').click()
                            self._device.delay(2)
                            self._device(resourceId='com.tct.email:id/account_sync_window').click()
                            self._device(text='All').click()
                            self._device.delay(2)
                            self._device(text='Sync contacts from this account').click()
                            self._device.delay(2)
                            self._device(text='Sync calendar from this account').click()
                            self._device.delay(2)
                            self._device(text='NEXT').click()
                        if not self._device(resourceId='com.android.settings:id/action_button',
                                        textContains='Activate').wait.exists(timeout=30000):
                            self._device(scrollable=True).scroll.vert.to(textContains='Activate')
                        self._device(resourceId='com.android.settings:id/action_button', textContains='Activate').click()
                        self._device.delay(2)
                        self._device(text='FINISH').click()
                        if self._device(text='Inbox').wait.exists(timeout=30000):
                            self._logger.debug('Email login successfully')
                            return True
                        else:
                            self._logger.debug("Email login fail")
                            return  False
        self._logger.debug('Email login fail')
        return False

    def stay_in_messaging(self):
        """Keep in messaging main page
        
        """
        maxtime = 0
        while not self._device(resourceId='com.android.mms:id/floating_action_button').exists:
            self._device.press.back()
            if self._device(resourceId='android:id/button1').exists:
                self._device(resourceId='android:id/button1').click()
                self._device.delay(2)
            maxtime += 1
            if maxtime > 3:
                self._logger.debug("Can't back messaging")
                break
        if maxtime < 4:
            return True
        else:
            self._device.press.home()
            self._device.delay(2)
            self._logger.debug("Launch messaging.")
            if self.enter_app('Messaging'):
                self._device.delay(2)
                if self.get_current_packagename() == self.get_app_package_from_file('Messaging'):

                    maxtime = 0
                    while not self._device(resourceId='com.android.mms:id/floating_action_button').exists:
                        self._device.press.back()
                        if self._device(resourceId='android:id/button1').exists:
                            self._device(resourceId='android:id/button1').click()
                            self._device.delay(2)
                        maxtime += 1
                        if maxtime > 3:
                            self._logger.debug("Can't back messaging")
                            return False

                    self._logger.debug('Launch messaging successfully.')
                    return True

                else:
                    self._logger.debug('Launch messaging fail.')
                    return False
            else:
                return False

    def save_msg(self, content, Type, No=None):
        """
        save message draft in messaging list.
        
        author:li.huang
        """
        if self._device(description='add new message').exists:
            self._device(description='add new message').click()
            self._device.delay(2)
            if No != None:
                self._logger.debug('input phone number:' + No)
                self._device(resourceId='com.android.mms:id/recipients_editor').set_text(No)
            self._logger.debug('input msg content.')
            self._device.delay(1)
            if Type == 'Text':
                if self._device(resourceId='com.android.mms:id/embedded_text_editor').exists:
                    self._device(resourceId='com.android.mms:id/embedded_text_editor').click()
                    self._device(resourceId='com.android.mms:id/embedded_text_editor').set_text(content)
                    self._device.delay(1)
            '''
            if Type!='Text':
                self._device(resourceId='com.android.sz.mms:id/share_button').click()
                self._device.delay(1)
            '''
            if Type == 'Picture':
                self.mms_add_PictureOrVedio('Picture')
            if Type == 'Video':
                self.mms_add_PictureOrVedio('Video')
            if Type == 'Audio':
                self.mms_add_recordAudio('Audio')

            self.back_to_message()

            if self._device(textContains='Draft').wait.exists(timeout=30000):
                self._logger.debug('save msg success.')
                self._device.delay(2)
                return True
        self._logger.debug('save msg fail.')
        return False

    def send_saveMsg(self, Type, judge_flag=False):
        self._logger.debug('send the msg have been saved just now.')
        msg_order = {'Text': 0, 'Picture': 1, 'Video': 2, 'Audio': 3}
        if Type == "Text":
            self._device(resourceId="com.android.mms:id/listitem").child(textContains=msg_order[Type]).click()
            self._device.delay(2)
            if self._device(resourceId='com.android.mms:id/send_button_sms').exists:
                self._device(resourceId='com.android.mms:id/send_button_sms').click()
                self._device.delay(10)
            else:
                self._logger.debug("can't find the send button")
                return False
        else:
            self._device(resourceId="com.android.mms:id/listitem").child(textContains=msg_order[Type]).click()
            self._device.delay(2)
            if self._device(resourceId='com.android.mms:id/send_button_mms').exists:
                self._device(resourceId='com.android.mms:id/send_button_mms').click()
                self._device.delay(2)
            else:
                self._logger.debug("can't find the send button")
                return False
        if judge_flag and self.judge_msg_sent(Type):
            return True
        else:
            return False

    def mms_add_recordAudio(self, Type):
        """add a record audio to MMS attachment.
        argv: time_record -- time of record audio .
              
              
        for case 58\59 : step 1-2.1 
        """
        self._logger.debug("Begin to add the record audio to MMS .")
        if self._device(resourceId='com.android.mms:id/share_button').wait.exists(timeout=3000):
            self._logger.debug("Press the attachment icon .")
            self._device(resourceId='com.android.mms:id/share_button').click()
            self._device.delay(2)
        else:
            self._logger.debug("Can not found the attachment icon .")
            return False
        if self._device(resourceId='com.android.mms:id/record_audio').wait.exists(timeout=3000):
            self._logger.debug("Press the attachment icon .")
            self._device(resourceId='com.android.mms:id/record_audio').click()
        else:
            self._logger.debug("Can not found the attachment icon .")
            return False
        while self._device(resourceId='com.android.packageinstaller:id/permission_message').wait.exists(timeout=2000):
            self._device(resourceId='com.android.packageinstaller:id/permission_allow_button').click()
            self._device.delay(2)
        if self._device(resourceId='com.android.mms:id/record_list_enter').exists:
            self._device(resourceId='com.android.mms:id/record_list_enter').click()
            self._device.delay(2)
            if self._device(resourceId='com.android.mms:id/record_file_item', index=0).child(
                    resourceId='com.android.mms:id/select_check_box').exists:
                self._device(resourceId='com.android.mms:id/record_file_item', index=0).child(
                    resourceId='com.android.mms:id/select_check_box').click()
                self._device.delay(2)
                self._device(text='OK').click()
                self._logger.debug('Add audio attachment')
                if self._device(resourceId='com.android.messaging:id/audio_attachment_background').exists:
                    self._logger.debug('Add video attachment successfully')
                    return True
            else:
                self._logger.debug('Add Audio attachment fail')
                return False

    def mms_add_PictureOrVedio(self, Type):
        """
            add a vedio to MMS attachment.
        """
        self._logger.debug("Begin to add the vedio to MMS .")
        if self._device(resourceId='com.android.mms:id/share_button').wait.exists(timeout=3000):
            self._logger.debug("Press the attachment icon .")
            self._device(resourceId='com.android.mms:id/share_button').click()
            self._device.delay(2)
        else:
            self._logger.debug("Can not found the attachment icon .")
            return False
        if Type == 'Picture':
            if self._device(resourceId='com.android.mms:id/attach_image').exists:
                self._device(resourceId='com.android.mms:id/attach_image').click()
                while self._device(resourceId='com.android.packageinstaller:id/permission_message').wait.exists(
                        timeout=2000):
                    self._device(resourceId='com.android.packageinstaller:id/permission_allow_button').click()
                    self._device.delay(2)
                self._device.delay(2)
                if self._device(resourceId='com.android.mms:id/gridview').child(className='android.widget.FrameLayout',
                                                                                index=1).wait.exists(timeout=2000):
                    self._device(resourceId='com.android.mms:id/gridview').child(className='android.widget.FrameLayout',
                                                                                 index=1).click()
                    if self._device(text='OK').wait.exists(timeout=2000):
                        self._device(text='OK').click()
                self._device.delay(5)
                self._logger.debug('Add picture attachment')
                if self._device(resourceId='com.android.mms:id/image_content').exists:
                    self._logger.debug('Add picture attachment successfully')
                    return True
                else:
                    self._logger.debug('Add picture attachment fail')
                    return False

        if Type == 'Video':
            if self._device(resourceId='com.android.mms:id/attach_image').exists:
                self._device(resourceId='com.android.mms:id/attach_image').click()
                while self._device(resourceId='com.android.packageinstaller:id/permission_message').wait.exists(
                        timeout=2000):
                    self._device(resourceId='com.android.packageinstaller:id/permission_allow_button').click()
                    self._device.delay(2)
                self._device.delay(2)
                if self._device(resourceId='com.android.mms:id/gridview').child(className='android.widget.FrameLayout',
                                                                                index=2).wait.exists(timeout=2000):
                    self._device(resourceId='com.android.mms:id/gridview').child(className='android.widget.FrameLayout',
                                                                                 index=2).click()
                    if self._device(text='OK').wait.exists(timeout=2000):
                        self._device(text='OK').click()
                self._device.delay(5)
                self._logger.debug('Add video attachment')
                if self._device(resourceId='com.android.mms:id/video_thumbnail').exists:
                    self._logger.debug('Add video attachment successfully')
                    return True
                else:
                    self._logger.debug('Add video attachment fail')
                    return False

    def judge_msg_sent(self, Type='Text'):
        self._logger.debug('Begin to judge the Message is sent or not.')
        n = 0
        while n < 30:
            if not self._device(text='Sending...').exists and (
            not self._device(text='Message not sent. Touch to retry.').exists):
                break
            if self._device(text='Not sent. Touch to try again.').exists:
                self._device.debug('Text msg set successfully.')
            self._device.delay(2)
            n += 1
            if Type == 'Picture' or 'Video' or 'Audio':
                if not self._device(text='Sending...').exists and (
                not self._device(text='Message not sent. Touch to retry.').exists):
                    self._device.debug('%s msg set successfully', Type)
                    return True
        else:
            self._logger.debug('MSG send fail!!!')
            self.back_to_messageList()
            return False

    def back_to_messageList(self):
        """back to message list .
        
        """
        maxloop = 0
        while maxloop < 5:
            if self._device(resourceId='com.android.sz.mms:id/floating_action_button').exists and self._device(
                    text='Messaging').exists:
                self._logger.debug('Had back to message list screen.')
                break
            self._device.press.back()
            self._device.delay(2)
            maxloop += 1
        else:
            self._logger.debug('Fail to back to message list screen.')

    def back_to_message(self):
        """back to message list .
        
        author: bei.han
        """
        maxloop = 0
        while not self._device(text='Messaging').exists:
            self._device.press.back()
            self._device.delay(2)
            if maxloop > 5:
                break
            maxloop += 1

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
                    self._logger.debug("Can't back File Manager")
                    break
            if maxtime < 4:
                return True

        self._logger.debug("Launch Files.")
        if self.enter_app('Files'):
            self.click_allow()
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
                        self._logger.debug("Can't back File Manager")
                        break
                if maxtime < 4:
                    return True

            self._logger.debug('Launch File Manager main page fail')
            return False
        else:
            return False

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

    def add_browser_bookmarks(self, url):
        """
        get the current bookmark sum
        """
        self.select_browser_menu('Bookmarks/History')
        browser_bookmark_num = self.get_browser_total_bookmarks()
        self._logger.debug(str(browser_bookmark_num))

        """
        Add bookmark
        """

        self._logger.debug('Add the bookmark' + url)
        while not self._device(resourceId='com.hawk.android.browser:id/url').exists:
            self._device.press.back()
            self._device.delay(2)
        self._device(resourceId='com.hawk.android.browser:id/url').click()
        self._device.delay(2)
        self._device(className='android.widget.EditText', resourceId='com.hawk.android.browser:id/url').set_text(url)
        self._device.press.enter()
        self._device.delay(20)
        self._logger.debug('loading......')
        if self._device(resourceId='com.hawk.android.browser:id/menu_toolbar_id').exists:
            self._device(resourceId='com.hawk.android.browser:id/menu_toolbar_id').click()
            self._device.delay(3)
            self._device(text='Add Bookmark').click()
            self._device.delay(3)
            self._logger.debug('Add' + url + 'successfully')
        else:
            self._logger.debug('Not exists menu tool bar')
        """
        judge whether the bookmark sum has increased 
        """

        self.select_browser_menu('Bookmarks/History')
        bookmark_num1 = self.get_browser_total_bookmarks()
        self._logger.debug('bookmarks num: ' + str(bookmark_num1))
        if bookmark_num1 > browser_bookmark_num:
            self._logger.debug('Add bookmark successful')
            self._device.press.back()
            return True
        else:
            self._logger.debug('Add bookmark fail')
            return False

    def select_browser_menu(self, menu_text):
        if not self._device(resourceId='com.hawk.android.browser:id/taburlbar').exists:
            self._device(scrollable=True).scroll.vert.toBeginning(steps=100, max_swipes=1000)
            self._device.delay(2)
        if self._device(resourceId='com.hawk.android.browser:id/menu_toolbar_id').exists:
            self._device(resourceId='com.hawk.android.browser:id/menu_toolbar_id').click()
        self._device.delay(3)
        self._device(text=menu_text).click()
        self._device.delay(3)
        self._logger.debug('click the %s successfully', menu_text)
        if self._device(className='android.widget.ImageButton', index=1).wait.exists(timeout=2000):
            self._device(className='android.widget.ImageButton', index=1).click()
            if self._device(text='Default Bookmark').wait.exists(timeout=2000):
                self._logger.debug("enter the bookmark page successfully")
                return True
            else:
                self._logger.debug("enter the bookmark page fail")
                return False

    def get_browser_total_bookmarks(self):
        if self._device(resourceId='com.hawk.android.browser:id/bookmark_list').wait.exists(timeout=2000):
            browser_bookmark_num = self._device(resourceId='com.hawk.android.browser:id/bookmark_list').getChildCount() - 1
            self._logger.debug(browser_bookmark_num)
            return browser_bookmark_num
        else:
            self._logger.debug("Not exists added bookmark")
            return "0"
