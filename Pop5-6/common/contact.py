# -*- coding: UTF-8 -*-
"""Contact library for scripts.

"""
from common import Common
import sys
from test.test_os import resource


class Contact(Common):
    """Provide common functions for scripts, such as launching activity."""

    def __init__(self, device, log_name):
        Common.__init__(self, device, log_name)
        self._ssid = None

    def stay_in_contact(self, option=''):
        """Keep in Contact main page
        
        @param option: the option of lists_pager_header
    
        """
        if self.get_current_packagename() == self.get_app_package_from_file('Contacts'):
            maxtime = 0
            while not self._device(resourceId='com.android.dialer:id/lists_pager').exists:
                self._device.press.back()
                self._device.delay(1)
                if self._device(resourceId='android:id/message', textContains='Discard your changes').exists \
                        and self._device(resourceId='android:id/button1', textContains='OK').exists:
                    self._device(resourceId='android:id/button1', textContains='OK').click()
                    self._device.delay(2)
                maxtime += 1
                if maxtime > 3:
                    self._logger.debug("Can't back Contacts")
                    break
            if maxtime < 4:
                if option != '':
                    if self._device(description=option).exists:
                        if not self._device(description=option).isSelected():
                            self._device(description=option).click()
                            self._device.delay(3)
                            if self._device(description=option).isSelected():
                                self._logger.debug("%s is Selected1", option)
                                return True
                            else:
                                self._logger.debug("%s isn\' Selected", option)
                                return False

                        elif self._device(description=option).isSelected():
                            self._logger.debug("%s is Selected2", option)
                            return True
                    else:
                        self._logger.debug("Can't get the %s option.", option)
                        return False
                else:
                    return True

        self._logger.debug("Launch Contacts.")
        if self.enter_app('Contacts'):
            self._device.delay(2)
            if self.get_current_packagename() == self.get_app_package_from_file('Contacts'):
                maxtime = 0
                while not self._device(resourceId='com.android.dialer:id/lists_pager').exists:
                    self._device.press.back()
                    self._device.delay(1)
                    if self._device(resourceId='android:id/message', textContains='Discard your changes').exists \
                            and self._device(resourceId='android:id/button1', textContains='OK').exists:
                        self._device(resourceId='android:id/button1', textContains='OK').click()
                        self._device.delay(2)
                    maxtime += 1
                    if maxtime > 3:
                        self._logger.debug("Can't back Contacts")
                        break
                if maxtime < 4:
                    if option <> '':
                        if self._device(description=option).exists:
                            if not self._device(description=option).isSelected():
                                self._device(description="Speed dial").click()
                                self._device.delay(3)
                                self._device(description=option).click()
                                self._device.delay(3)
                                if self._device(description=option).isSelected():
                                    self._logger.debug("%s is Selected3", option)
                                    return True
                                else:
                                    self._logger.debug("%s isn\' Selected", option)
                                    return False

                            elif self._device(description=option).isSelected():
                                self._logger.debug("%s is Selected4", option)
                                return True

                        else:
                            self._logger.debug("Can't get the %s option.", option)
                            return False
                    else:
                        return True
            else:
                self._logger.debug('Launch Contacts main page fail')
                return False
        else:
            return False

    def delete_a_contact(self, option, index=0, name=None):
        """delete a contace
        
        @param option: the option of lists_pager_header
        @param index: index in contacts list, if not given a name using the index, default is the first
        @param name: contact name in list, to delete the contact if given name 
        
        @note: Make sure the contact name is unique in the list  
        
        """
        if not self.stay_in_contact(option):
            self._logger.debug("Can't launch contact " + option)
            return False

        if self._device(resourceId='com.android.dialer:id/message', textContains='No contacts').exists:
            self._logger.debug('there is no any contact')
            return False
        elif self._device(resourceId='android:id/list').exists:
            if not self._device(className='android.view.ViewGroup').child(index=3).exists:
                self._logger.debug('there is no any contact')
                return False
            self._device(resourceId='android:id/list').scroll.toBeginning()

        if name is None:
            self._logger.debug('delete the contact index ' + str(index))
            if not self._device(resourceId='com.android.contacts:id/cliv_name_textview', instance=index).exists:
                self._logger.debug('Can\'t get contact index')
                return False
            name = self._device(resourceId='com.android.contacts:id/cliv_name_textview', instance=index).get_text()
            self._logger.debug('Delete the contact ' + name)
            self._device(resourceId='com.android.contacts:id/cliv_name_textview', instance=index).click()
            self._device.delay(2)
        else:
            if not self._device(resourceId='android:id/list').child_by_text(name,
                                                                            resourceId='com.android.contacts:id/cliv_name_textview',
                                                                            allow_scroll_search=True).exists:
                self._logger.debug('Can\'t get contact name')
                return False
            self._logger.debug('Delete the contact ' + name)
            self._device(resourceId='com.android.contacts:id/cliv_name_textview', text=name, ).click()
            self._device.delay(2)

        if self._device(resourceId='com.android.packageinstaller:id/permission_allow_button').exists:
            self._device(resourceId='com.android.packageinstaller:id/permission_allow_button').click()
            self._device.delay(2)

        # if not self._device(resourceId  = 'com.android.contacts:id/menu_edit').exists:
        #             self._logger.debug('Menu edit is not exist.')
        #             return False
        #         self._device(resourceId  = 'com.android.contacts:id/menu_edit').click()
        #         self._device.delay(2)

        if not self._device(description='More options').exists:
            self._logger.debug('More options is not exist.')
            return False
        self._device(description='More options').click()
        self._device.delay(2)

        if not self._device(resourceId='android:id/title', text='Delete').exists:
            self._logger.debug('Menu delete is not exist.')
            return False
        self._device(resourceId='android:id/title', text='Delete').click()
        self._device.delay(2)

        if self._device(resourceId='android:id/button1').exists:
            self._device(resourceId='android:id/button1').click()
            self._device.delay(2)

        if not self._device(resourceId='android:id/list').exists:
            if not self.stay_in_contact(option):
                self._logger.debug("Can't launch contact " + option)
                return False

        if not self._device(resourceId='com.android.contacts:id/cliv_name_textview', text=name).exists:
            self._logger.debug("Delete the contact %s successfully ", name)
            return True
        else:
            self._logger.debug("Delete the contact %s fail ", name)
            return False

    def delete_all_contacts(self, option):
        """delete all contact.
        
        @param option: the option of lists_pager_header
        
        """
        if not self.stay_in_contact(option):
            self._logger.debug("Can't launch contact " + option)
            return False

        if self._device(resourceId='com.android.dialer:id/message', textContains='No contacts').exists:
            self._logger.debug('there is no any contact1')
            return False
        elif self._device(resourceId='android:id/list').exists:
            if not self._device(className='android.view.ViewGroup').child(index=3).exists \
                    or not self._device(resourceId='com.android.dialer:id/cliv_name_textview').exists:
                self._logger.debug('there is no any contact2')
                return False

        self._logger.debug('delete all contact')
        if not self._device(resourceId='com.android.dialer:id/cliv_name_textview').exists:
            self._logger.debug('there is no contact.')
            return False
        contacts_num = self._device(resourceId='com.android.dialer:id/cliv_name_textview').count
        self._device(resourceId='com.android.dialer:id/cliv_name_textview').long_click()
        self._device.delay(2)

        if self._device(resourceId='com.android.contacts:id/selection_count_text').exists:
            #             if self._device(className = 'android.widget.CheckBox',  checked = False).exists:
            self._device(resourceId='com.android.contacts:id/selection_count_text').click()
            self._device.delay(2)
            if self._device(resourceId='android:id/title', text='Select all').exists:
                self._device(resourceId='android:id/title', text='Select all').click()
                self._device.delay(5)
            else:
                self._device.press.back()
                self._device.delay(1)
            # if not self._device(className = 'android.widget.CheckBox',  checked = False).exists:
            if self._device(resourceId='com.android.contacts:id/selection_count_text').exists:
                if not self._device(description='More options').exists:
                    self._logger.debug('More options is not exist.')
                    return False
                self._device(description='More options').click()
                self._device.delay(2)

                if not self._device(resourceId='com.android.dialer:id/delete', text='Delete').exists:
                    self._logger.debug('Menu delete2 is not exist.')
                    return False
                    self._device(resourceId='com.android.dialer:id/delete', text='Delete').click()
                    self._device.delay(2)

                elif not self._device(resourceId='android:id/button1', text='OK').exists:
                    self._logger.debug('Button DELETE is not exist.')
                    return False
                    self._device(resourceId='android:id/button1', text='OK').click()
                    self._device.delay(2)
            else:
                self._logger.debug('Select all contacts fail.')
                return False

        elif self._device(resourceId='com.android.contacts:id/menu_select_all').exists:
            if contacts_num > 1:
                self._device(resourceId='com.android.contacts:id/menu_select_all').click()
                self._device.delay(2)
            else:
                self._logger.debug('There is only one contact left.')

            try_time = 0
            while not self._device(resourceId='com.android.contacts:id/menu_delete').exists:
                self._device(resourceId='com.android.contacts:id/cliv_name_textview').long_click()
                self._device.delay(2)
                if self._device(resourceId='com.android.contacts:id/menu_select_all').exists:
                    self._device(resourceId='com.android.contacts:id/menu_select_all').click()
                    try_time += 1
                if try_time > 3:
                    self._logger.debug('Select all contacts fail.')
                    return False

            self._device(resourceId='com.android.contacts:id/menu_delete').click()
            self._device.delay(2)
            if not self._device(resourceId='android:id/button1').exists:
                self._logger.debug('Button Confirm delete is not exist.')
                return False
            self._device(resourceId='android:id/button1').click()
            self._device.delay(2)
        # Edit by Yale
        elif self._device(resourceId='com.android.dialer:id/select_all').exists:
            self._logger.debug("Select all contacts")
            self._device(resourceId='com.android.dialer:id/select_all').click()
            self._device.delay(2)
            if self._device(resourceId='com.android.dialer:id/select_num_new', text='0').exists:
                self._logger.debug("Select all Contacts Again")
                self._device(resourceId='com.android.dialer:id/select_all').click()
                self._device.delay(2)
        if self._device(resourceId='com.android.dialer:id/delete').exists:
            self._logger.debug("Delete all contacts")
            self._device(resourceId='com.android.dialer:id/delete').click()
            self._device.delay(2)
            if not self._device(resourceId='android:id/button1', text='OK').exists:
                self._logger.debug('Button DELETE is not exist.')
                return False
            self._device(resourceId='android:id/button1', text='OK').click()
            self._device.delay(2)


        else:
            self._logger.debug('Select all is not exist.')
            return False

        if self._device(resourceId='android:id/progress').wait.gone(timeout=300000):
            if self._device(resourceId='com.android.dialer:id/message', textContains='No contacts').exists:
                self._logger.debug('Delete all contact successfully1.')
                return True
            elif self._device(resourceId='android:id/list').exists:
                if not self._device(className='android.view.ViewGroup').child(index=2).exists \
                        or not self._device(resourceId='com.android.contacts:id/cliv_name_textview').exists:
                    self._logger.debug('Delete all contact successfully2.')
                    return True
        self._logger.Warning('Delete all contact fail.')
        return False

    def import_contacts(self, option, index=0):
        """import a .vcf file to import
        
        @param option: the option of lists_pager_header
        @param index: the index of the .vcf file , default is the first
        
        """
        if not self.stay_in_contact(option):
            self._logger.debug("Can't launch contact " + option)
            return False

        self._logger.debug('Import contact')

        if self._device(resourceId='com.android.dialer:id/import_contacts_button').exists:
            self._device(resourceId='com.android.dialer:id/import_contacts_button').click()
            self._device.delay(2)

        elif self._device(description='More options').exists:
            self._device(description='More options').click()
            self._device.delay(2)

            if not self._device(resourceId='android:id/title', textContains='Import/Export').exists:
                self._logger.debug('Menu \'Import/Export\' is not exist.')
                return False
            self._device(resourceId='android:id/title', textContains='Import/Export').click()
            self._device.delay(4)
        else:
            self._logger.debug('More options button not exist.')
            return False

        if self._device(resourceId='android:id/text1', text="Phone storage").exists \
                and self._device(resourceId='com.android.contacts:id/btn_next', text='NEXT').exists:
            self._logger.debug("Copy contacts from Phone storage")
            self._device(resourceId='android:id/text1', textContains="Phone storage").click()
            self._device.delay(2)
            self._device(resourceId='com.android.contacts:id/btn_next', text='NEXT').click()
            self._device.delay(2)

        if self._device(resourceId='android:id/text1', textContains='Phone').exists \
                and self._device(resourceId='com.android.contacts:id/btn_next', text='NEXT').exists:
            self._logger.debug("Copy contacts to Phone")
            self._device(resourceId='android:id/text1', textContains='Phone').click()
            self._device.delay(2)
            self._device(resourceId='com.android.contacts:id/btn_next', text='NEXT').click()
            self._device.delay(2)
            if self._device(resourceId='android:id/message', textContains='No vCard file').exists:
                self._logger.debug("No vCard file found in storage.")
                self._device(resourceId='android:id/button1', textContains='OK').click()
                return False

        if self._device(resourceId='android:id/list').wait.exists(timeout=30000):
            for i in range(3):
                if self._device.open.notification():
                    break
                self._device.delay(2)
            if self._device(textContains='vCards imported to Phone.').wait.exists(timeout=300000):
                self._logger.debug('Import contact successfully.')

                if not self._device(resourceId='com.android.systemui:id/dismiss_text').exists:
                    self._device(resourceId='com.android.systemui:id/notification_stack_scroller').scroll(steps=50)
                    self._device.delay(2)
                    if self._device(resourceId='com.android.systemui:id/dismiss_text').exists:
                        self._device(resourceId='com.android.systemui:id/dismiss_text').click()
                        self._device.delay(2)
                else:
                    self._device(resourceId='com.android.systemui:id/dismiss_text').click()
                    self._device.delay(2)
                return True
        self._logger.debug('Import contact fail.')
        return False

    def add_a_contact(self, name, phoneNum, isSetEmail=False):
        """add a contact
        
        @param (str)name: name of contact 
        @param (str)phoneNum: phone number of contact        

        """
        self._logger.debug('create a new contact')

        if self._device(resourceId='com.android.dialer:id/floating_action_button').exists:
            self._logger.debug("click add button")
            self._device(resourceId='com.android.dialer:id/floating_action_button').click()
            self._device.delay(2)
            if self._device(resourceId='android:id/text1', textContains='Phone-only').exists:
                self._device(resourceId='android:id/text1', textContains='Phone-only').click()

        if self._device(resourceId='com.android.contacts:id/account_type', textContains='Phone-only').exists:
            self._logger.debug("No need to swich account type.")
        elif not self._device(resourceId='com.android.contacts:id/account_type', textContains='Phone-only').exists:
            if not self._device(resourceId='com.android.contacts:id/account_type').exists:
                self._logger.debug("Can't find the account type view")
                return False
            self._device(resourceId='com.android.contacts:id/account_type').click()
            self._device.delay(3)
            if not self._device(resourceId='android:id/text1', textContains='Tablet').exists:
                self._logger.debug("Can't find the account type Tablet")
                return False
            self._device(resourceId='android:id/text1', textContains='Tablet').click()
            self._device.delay(2)
        if self._device(resourceId='com.android.contacts:id/editors').child_by_text('Name',
                                                                                    allow_scroll_search=True).exists:
            self._device(className='android.widget.EditText', text='Name').click()
            self._device.delay(2)
            if not self._device(className='android.widget.EditText', text='Name', focused='true').exists:
                self._logger.debug("Can't move the input to name")
                return False
            self._logger.debug('input contact name:' + name)
            self._device(className='android.widget.EditText', text='Name').set_text(name)
            self._device.delay(3)
        else:
            self._logger.debug("Can't find the edit name view")
            return False

        if self._device(className='android.widget.EditText', text='Phone').exists:
            self._device(className='android.widget.EditText', text='Phone').click()
            self._device.delay(2)
            if not self._device(className='android.widget.EditText', text='Phone', focused='true').exists:
                self._logger.debug("Can't move the input to Phone")
                return False
            self._logger.debug('input phone:' + phoneNum)
            self._device(className='android.widget.EditText', text='Phone').set_text(phoneNum)
            self._device.delay(3)
        else:
            self._logger.debug("Can't find the edit phone number view")
            return False

        if isSetEmail:
            clicktime = 0
            while True:
                if not self._device(className='android.widget.EditText', text='Email').exists:
                    self._device.press.back()
                if self._device(className='android.widget.EditText', text='Email').exists:
                    self._device(className='android.widget.EditText', text='Email').click()
                    self._device.delay(2)
                    if self._device(className='android.widget.EditText', text='Email', focused='true').exists:
                        break
                    else:
                        clicktime += 1
                        self._logger.debug("-----------------------------------------------")
                    if clicktime > 3:
                        self._logger.debug("Can't move the input to Email")
                        return False
                else:
                    self._logger.debug("Can't find the edit email number view")
                    return False
            self._logger.debug('input email:' + phoneNum + '@mm.com')
            self._device(className='android.widget.EditText', text='Email').set_text(phoneNum + '@mm.com')
            self._device.delay(3)
        if self._device(resourceId='com.android.contacts:id/save_menu_item').exists:
            self._logger.debug('Save the contact')
            self._device(resourceId='com.android.contacts:id/save_menu_item').click()
            self._device.delay(5)
        elif self._device(resourceId='com.android.contacts:id/menu_save').exists:
            self._logger.debug('Save the contact')
            self._device(resourceId='com.android.contacts:id/menu_save').click()
            self._device.delay(5)
        else:
            self._logger.debug("Can't find the save contact view.")
            return False

        if self._device(resourceId='com.android.contacts:id/large_title', text=name).exists \
                and self._device(resourceId='com.android.contacts:id/header').exists:
            if self._device(resourceId='com.android.contacts:id/header').get_text().replace(' ', '').replace('-',
                                                                                                             '').replace(
                '(', '').replace(')', '') == phoneNum:
                if isSetEmail:
                    if self._device(resourceId='com.android.contacts:id/header', text=phoneNum + '@mm.com').exists:
                        return True
                    else:
                        self._logger.debug('Get the Email added fail!')
                        return False
                else:
                    return True
            else:
                self._logger.debug('Get the phone number added fail!')
                return False
        else:
            self._logger.debug('Creat contact fail!')
            return False

    def call_from_contacts(self, name):
        self._logger.debug('call from contacts')
        if self._device(resourceId='android:id/list').exists:
            scroll_time = 0
            while not self._device(resourceId='com.android.dialer:id/cliv_name_textview', text=name).exists:
                self._device(resourceId='android:id/list').scroll.vert.to(text=name)
                scroll_time += 1
                self._device.delay(2)
                if scroll_time > 5:
                    self._logger.debug('Contacts %s isn\'t exists.', name)
                    return False

            self._device(resourceId='com.android.dialer:id/cliv_name_textview',text=name).click()
            self._device.delay(3)

            if not self._device(descriptionContains='Call Cellular ').exists:
                self._logger.debug('The phone number isn\'t exist.')
                return False

            try_times = 0
            while self._device(descriptionContains='Call Cellular').exists:
                self._device(descriptionContains='Call Cellular').click()
                self._device.delay(3)
                try_times += 1
                if try_times > 5:
                    self._logger.debug('Still in contact. Can\'t start call')
                    return False

            if self._device(resourceId='com.android.dialer:id/elapsedTime').wait.exists(timeout=30000) \
                    and self._device(resourceId='com.android.dialer:id/floating_end_call_action_button').exists:
                self._logger.debug('In calling')
                self._device.delay(10)
                self._device(resourceId='com.android.dialer:id/floating_end_call_action_button').click()
                if self._device(descriptionContains='Call Cellular ').wait.exists(timeout=5000):
                    self._logger.debug('Back call. ')
                    self._device.press.back()
                if self._device(descriptionContains='Contacts').wait.exists(timeout=10000):
                    self._logger.debug('End call.')
                    return True
                else:
                    self._logger.debug('End call fail.')
                    return False
            else:
                self._logger.debug('Start call fail.')
                return False

                #                 self._device.screenshot(sys.path[0]+"\\PicComparison\\call.png")
                #                 self._device.dump(sys.path[0]+"\\PicComparison\\call.uix")



                #
