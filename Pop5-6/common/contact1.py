# -*- coding: UTF-8 -*-
"""Contact library for scripts.

"""
from common import Common

class Contact(Common):

    """Provide common functions for scripts, such as launching activity."""
    
    def __init__(self, device, log_name):
        Common.__init__(self, device,log_name)
        self._ssid = None
        
    def stay_in_contact(self, option = ''):
        """Keep in Contact main page
        
        @param option: the option of lists_pager_header
    
        """
        if self.get_current_packagename() == self.get_app_package_from_file('Contacts'):
            maxtime = 0
            while not self._device(resourceId = 'com.android.contacts:id/lists_pager_header').exists:
                self._device.press.back()
                self._device.delay(1)
                maxtime += 1
                if maxtime > 3:
                    self._logger.debug("Can't back Contacts")
                    break
            if maxtime < 4:
                if option <> '':
                    if self._device(text = option).exists:
                        if not self._device(text = option).isSelected():
                            self._device(text = option).click()
                            self._device.delay(3)
                        return self._device(text = option).isSelected()
                    else:
                        self._logger.debug("Can't get the %s option.", option)
                        return False
                else:
                    return True

        self._device.press.home()
        self._logger.debug("Launch Contacts.")
        if self.enter_app('Contacts'):
            self._device.delay(2)
            if self.get_current_packagename() == self.get_app_package_from_file('Contacts'):  
                maxtime = 0
                while not self._device(resourceId = 'com.android.contacts:id/lists_pager_header').exists:
                    self._device.press.back()
                    self._device.delay(1)
                    maxtime += 1
                    if maxtime > 3:
                        self._logger.debug("Can't back Contacts")
                        break
                if maxtime < 4:
                    if option <> '':
                        if self._device(text = option).exists:
                            if not self._device(text = option).isSelected():
                                self._device(text = option).click()
                                self._device.delay(3)
                            return self._device(text = option).isSelected()
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
        
    def delete_a_contact(self, option, index = 0, name = None):
        """delete a contace
        
        @param option: the option of lists_pager_header
        @param index: index in contacts list, if not given a name using the index, default is the first
        @param name: contact name in list, to delete the contact if given name 
        
        @note: Make sure the contact name is unique in the list  
        
        """
        if not self.stay_in_contact(option):
            self._logger.debug("Can't launch contact " + option)
            return False
        
        if self._device(resourceId  = 'android:id/list').exists:
            if not self._device(resourceId = 'android:id/list').child(index = 2).exists:
                self._logger.debug('there is no any contact')
                return False
            self._device(resourceId  = 'android:id/list').scroll.toBeginning()
            
        if name == None:
            self._logger.debug('delete the contact index ' + str(index))
            if not self._device(resourceId = 'com.android.contacts:id/cliv_name_textview', instance = index).exists:
                self._logger.debug('Can\'t get contact index')
                return False
            name = self._device(resourceId = 'com.android.contacts:id/cliv_name_textview', instance = index).get_text()
            self._logger.debug('Delete the contact ' + name)
            self._device(resourceId = 'com.android.contacts:id/cliv_name_textview', instance = index).click()
            self._device.delay(2)
        else:
            if not self._device(resourceId = 'android:id/list').child_by_text(name, resourceId = 'com.android.contacts:id/cliv_name_textview', allow_scroll_search=True).exists:
                self._logger.debug('Can\'t get contact name')
                return False
            self._logger.debug('Delete the contact ' + name)
            self._device(resourceId = 'com.android.contacts:id/cliv_name_textview',text = name,).click()
            self._device.delay(2)
         
        if not self._device(resourceId  = 'com.android.contacts:id/menu_edit').exists:
            self._logger.debug('Menu edit is not exist.')
            return False
        self._device(resourceId  = 'com.android.contacts:id/menu_edit').click() 
        self._device.delay(2)  
            
        if not self._device(description = 'More options').exists:
            self._logger.debug('More options is not exist.')
            return False
        self._device(description = 'More options').click()    
        self._device.delay(2)
            
        if not self._device(resourceId = 'android:id/title', text = 'Delete').exists:
            self._logger.debug('Menu delete is not exist.')
            return False
        self._device(resourceId = 'android:id/title', text = 'Delete').click()    
        self._device.delay(2)
        
        if self._device(resourceId = 'android:id/button1', text='OK').exists:
            self._device(resourceId = 'android:id/button1', text='OK').click()
            self._device.delay(2)
            
        if not self._device(resourceId  = 'android:id/list').exists:
            if not self.stay_in_contact(option):
                self._logger.debug("Can't launch contact " + option)
                return False
        
        if not self._device( resourceId = 'com.android.contacts:id/cliv_name_textview', text = name).exists:
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
        
        if self._device(resourceId = 'android:id/list').exists:
                if not self._device(resourceId = 'android:id/list').child(index = 2).exists\
                    or not self._device( resourceId = 'com.android.contacts:id/cliv_name_textview').exists:
                    self._logger.debug('there is no any contact')
                    return True
        
        self._logger.debug('delete all contact')

        if not self._device(description = 'More options').exists:
            self._logger.debug('More options is not exist.')
            return False
        self._device(description = 'More options').click()    
        self._device.delay(2)
        
        if not self._device(resourceId = 'android:id/title',  textContains = 'Delete').exists:
            self._logger.debug('Menu delete is not exist.')
            return False
        self._device(resourceId = 'android:id/title',  textContains = 'Delete').click()    
        self._device.delay(2)
        
        if not self._device(resourceId = 'com.android.contacts:id/select_items').exists:
            self._logger.debug('Select items is not exist.')
            return False
        if self._device(className = 'android.widget.CheckBox',  checked = False).exists:
            self._device(resourceId = 'com.android.contacts:id/select_items').click() 
            self._device.delay(2)
            if self._device(resourceId = 'android:id/title', text = 'Select all').exists:
                self._device(resourceId = 'android:id/title', text = 'Select all').click()  
                self._device.delay(5)
        if not self._device(className = 'android.widget.CheckBox',  checked = False).exists:
            if not self._device(resourceId = 'com.android.contacts:id/menu_option', text = 'OK').exists:
                self._logger.debug('Button Done is not exist.')
                return False 
            self._device(resourceId = 'com.android.contacts:id/menu_option', text = 'OK').click()    
            self._device.delay(2)
            
        if self._device(resourceId = 'android:id/button1', text='OK').exists:
            self._device(resourceId = 'android:id/button1', text='OK').click()
            self._device.delay(2)
             
        if self._device(resourceId = 'android:id/progress').wait.gone(timeout = 300000):
            if self._device(resourceId = 'android:id/list').exists:
                if not self._device(resourceId = 'android:id/list').child(index = 2).exists\
                    or not self._device( resourceId = 'com.android.contacts:id/cliv_name_textview').exists:
                    self._logger.debug('Delete all contact successfully.')
                    return True
        self._logger.debug('Delete all contact fail.')
        return False

    def import_contacts(self, option, index = 0):
        """import a .vcf file to import
        
        @param option: the option of lists_pager_header
        @param index: the index of the .vcf file , default is the first
        
        """
        if not self.stay_in_contact(option):
            self._logger.debug("Can't launch contact " + option)
            return False
        
        self._logger.debug('Import contact')

        if not self._device(description = 'More options').exists:
            self._logger.debug('More options is not exist.')
            return False
        self._device(description = 'More options').click()    
        self._device.delay(2)
        
        if not self._device(resourceId = 'android:id/title', textContains = 'Import').exists:
            self._logger.debug('Menu delete is not exist.')
            return False
        self._device(resourceId = 'android:id/title', textContains = 'Import').click()    
        self._device.delay(4)
        
        if self._device(resourceId = 'com.android.contacts:id/accountUserName', textContains = 'storage').exists\
            and self._device(resourceId = 'com.android.contacts:id/btn_action', text = 'Next').exists:
            self._device(resourceId = 'com.android.contacts:id/accountUserName', textContains = 'storage').click()
            self._device.delay(2)
            self._device(resourceId = 'com.android.contacts:id/btn_action', text = 'Next').click()
            self._device.delay(2)
            
        if self._device(resourceId = 'com.android.contacts:id/accountUserName', text = 'Tablet').exists\
            and self._device(resourceId = 'com.android.contacts:id/btn_action', text = 'Next').exists:
            self._device(resourceId = 'com.android.contacts:id/accountUserName', text = 'Tablet').click()
            self._device.delay(2)
            self._device(resourceId = 'com.android.contacts:id/btn_action', text = 'Next').click()
            self._device.delay(2)

        if self._device(resourceId = 'android:id/button1', text='OK').exists:
            self._device(resourceId = 'android:id/button1', text='OK').click()
            self._device.delay(2)
            
        if self._device(resourceId = 'android:id/list').wait.exists(timeout = 30000):
            for i in range(3):
                if self._device.open.notification():
                    break
                self._device.delay(2)
            if self._device(textContains = 'Finished importing vCard').wait.exists(timeout = 300000):
                self._logger.debug('Import contact successfully.')
                if self._device(resourceId = 'com.android.systemui:id/dismiss_text').exists:
                    self._device(resourceId = 'com.android.systemui:id/dismiss_text').click()
                    self._device.delay(2)
                return True
        self._logger.debug('Import contact fail.')
        return False
            
    def add_a_contact(self, name, phoneNum, isSetEmail = False):
        """add a contact
        
        @param (str)name: name of contact 
        @param (str)phoneNum: phone number of contact        

        """
        self._logger.debug('create a new contact')
        if self._device(resourceId='com.android.contacts:id/floating_action_button').exists:
            self._device(resourceId='com.android.contacts:id/floating_action_button').click()
            self._device.delay(2)
            self._logger.debug("1111111111111")
#         if self._device(resourceId = 'com.android.contacts:id/right_button', text='Phone').exists:
#             self._device(resourceId = 'com.android.contacts:id/right_button', text='Phone').click()
#             self._device.delay(2)
#         if self._device(resourceId = 'android:id/text1', text='Phone').exists:
#             self._device(resourceId = 'android:id/text1', text='Phone').click()
#             self._device.delay(2)
#         if self._device(resourceId = 'android:id/text1', text='Tablet').exists:
#             self._device(resourceId = 'android:id/text1', text='Tablet').click()
#             self._device.delay(2)
#         if self._device(resourceId = 'com.android.contacts:id/right_button', text='OK').exists:
#             self._device(resourceId = 'com.android.contacts:id/right_button', text='OK').click()
#             self._device.delay(2)
#         if not self._device(resourceId = 'com.android.contacts:id/account_type', text='Tablet').exists:
#             if not self._device(resourceId = 'com.android.contacts:id/account_type').exists:
#                 self._logger.debug("Can't find the account type view")
#                 return False
#             self._device(resourceId = 'com.android.contacts:id/account_type').click()
#             self._device.delay(3)
#             if not self._device(resourceId = 'android:id/text1', text='Tablet').exists:
#                 self._logger.debug("Can't find the account type Tablet")
#                 return False
#             self._device(resourceId = 'android:id/text1', text='Tablet').click()
#             self._device.delay(2)

        if self._device(className  = 'android.widget.EditText', text='Name').exists:
            self._device(className  = 'android.widget.EditText', text='Name').click()
            self._device.delay(2)
            if not self._device(className  = 'android.widget.EditText', text='Name', focused = 'true').exists:
                self._logger.debug("Can't move the input to name")
                return False
            self._logger.debug('input contact name:'+name)
            self._device(className  = 'android.widget.EditText', text='Name').set_text(name)
            self._device.delay(3)
        else:
            self._logger.debug("Can't find the edit name view")
            return False
        
        if isSetEmail:
            clicktime = 0
            while True:
                if self._device(className='android.widget.EditText',text='Email').exists:
                    self._device(className  = 'android.widget.EditText', text='Email').click()
                    self._device.delay(2)
                    if self._device(className  = 'android.widget.EditText', text='Email', focused = 'true').exists:
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
            self._logger.debug('input email:'+ phoneNum + '@mm.com') 
            self._device(className='android.widget.EditText',text='Email').set_text(phoneNum + '@mm.com')
            self._device.delay(3)
            
        if self._device(className='android.widget.EditText',text='Phone').exists:
            self._device(className  = 'android.widget.EditText', text='Phone').click()
            self._device.delay(2)
            if not self._device(className  = 'android.widget.EditText', text='Phone', focused = 'true').exists:
                self._logger.debug("Can't move the input to Phone")
                return False
            self._logger.debug('input phone:'+ phoneNum) 
            self._device(className='android.widget.EditText',text='Phone').set_text(phoneNum)
            self._device.delay(3)
        else:
            self._logger.debug("Can't find the edit phone number view")
            return False
        
        if self._device(resourceId = 'com.android.contacts:id/save_menu_item').exists:
            self._logger.debug('Save the contact') 
            self._device(resourceId = 'com.android.contacts:id/save_menu_item').click()
            self._device.delay(5)
        else:
            self._logger.debug("Can't find the save contact view.")
            return False
        
        if self._device(resourceId = 'com.android.contacts:id/large_title', text = name).exists\
            and self._device(resourceId = 'com.android.contacts:id/header').exists:
            if self._device(resourceId = 'com.android.contacts:id/header').get_text().replace(' ','').replace('-', '').replace('(', '').replace(')', '') == phoneNum:
                if isSetEmail:
                    if self._device(resourceId = 'com.android.contacts:id/header', text = phoneNum + '@mm.com').exists:
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
        