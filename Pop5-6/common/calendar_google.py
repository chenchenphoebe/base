
import string
import re
import sys
from common import Common
from datetime import datetime,date,timedelta

class Calendar(Common):

    """Provide common functions involved Calendar."""
    
    def __init__(self, device, log_name):
        Common.__init__(self, device,log_name)
        self.calendar_name = self.get_app_package_from_file("Calendar")
        self._logger.debug("Calendar is " + self.calendar_name)
    
        
    def stay_in_calendar(self):
        """Keep in Calendar main page
        
        """
        maxtime = 0
        while not  self._device(description ='Show Calendar List and Settings drawer').exists:
            if self._device(resourceId  = self.calendar_name + ':id/button_dismiss').exists:
                self._device(resourceId  = self.calendar_name + ':id/button_dismiss').click()
                self._device.delay(2)
            self._device.press.back()
            self._device.delay(2)
            if self._device(resourceId  ='android:id/button2', text = 'Discard').exists:
                self._device(resourceId  ='android:id/button2', text = 'Discard').click()
                self._device.delay(2)
            maxtime += 1
            if maxtime > 3:
                self._logger.debug("Can't back calendar")
                break
        if maxtime < 4:
            self._logger.debug('Stay in calendar main page successfully.')
            return True
        else:
            self._device.press.home()
            self._logger.debug("Launch calendar.")
        if self.enter_app('Calendar'):
            self._device.delay(2)
            if self.get_current_packagename() == self.get_app_package_from_file('Calendar'):
                maxtime = 0
                while not  self._device(description ='Show Calendar List and Settings drawer').exists:
                    if self._device(resourceId  = self.calendar_name + ':id/button_dismiss').exists:
                        self._device(resourceId  = self.calendar_name + ':id/button_dismiss').click()
                        self._device.delay(2)
                    self._device.press.back()
                    if self._device(resourceId  ='android:id/button2', text = 'Discard').exists:
                        self._device(resourceId  ='android:id/button2', text = 'Discard').click()
                        self._device.delay(2)
                    maxtime += 1
                    if maxtime > 3:
                        self._logger.debug("Can't back calendar")
                        break
                if maxtime < 4:
                    self._logger.debug('Stay in calendar main page successfully.')
                    return True
            self._logger.debug('Stay in calendar main page fail!')
            return False
        else:
            return False      
            
#     def switch_view(self, strsort):
#         """Switch to specified view.
#         
#         @param (str)strsort: view type
#         
#         """
#         self.stay_in_calendar()
#         if not self._check_view_type(strsort):
#             self._logger.debug("Switch to %s view." % strsort)
#             if not self._device(description  ='Change view').exists:
#                 self._logger.debug('Change view isn\'t exist')
#                 return False
#             self._device(description  ='Change view').click()
#             self._device.delay(2)
#             if not self._device(text = strsort).exists:
#                 self._logger.debug(strsort + " isn't exist")
#                 return False
#             self._device(text = strsort).click()
#         if self._check_view_type(strsort):
#             return True
#         else:
#             self._logger.debug('can not enter the view of '+strsort)
#             return False
#         
#     def _check_view_type(self, strsort):
#         """check view type whether same as the specified.
#         
#         @param (str)strsort: view type
#         
#         """  
#         if self._device(resourceId  =self.calendar_name +':id/week_days_content').exists:
#             if strsort == "Day" and self._device(resourceId  =self.calendar_name +':id/week_days_content').getChildCount() == 1:
#                 self._logger.debug("Current view is Day")
#                 return True
#             if strsort == "Week" and self._device(resourceId  =self.calendar_name +':id/week_days_content').getChildCount() > 1:
#                 self._logger.debug("Current view is Week")
#                 return True
#         elif (strsort == "Month" and self._device(resourceId  =self.calendar_name +':id/month_view_bg').exists):
#             self._logger.debug("Current view is Month")
#             return True
#         elif (strsort == "Schedule" and self._device(resourceId  =self.calendar_name +':id/timely_list').exists):
#             self._logger.debug("Current view is Schedule")
#             return True
#         else:
#             self._logger.warning("Cannot enter %s." % strsort)
#             return False
       
                   
    def calendar_is_exist(self, strname):
        """check if task exist.
        
        @param  (str)strname: task name just added.
        
        """
#         self.switch_view("Schedule")
        if self._device(description = 'Change view').exists:
            self._device(description = 'Change view').click()
        elif self._device(description = 'Show Calendar List and Settings drawer').exists:
            self._device(description = 'Show Calendar List and Settings drawer').click()
        else:
            self._logger.debug("Isn't in main page")
            return False
        self._device.delay(2)
        if self._device(resourceId = 'android:id/title', text = 'Search').exists:
            self._device(resourceId = 'android:id/title', text = 'Search').click()
        elif self._device(resourceId = self.calendar_name +':id/search', text = 'Search').exists:
            self._device(resourceId = self.calendar_name +':id/search', text = 'Search').click()
        elif self._device(resourceId = self.calendar_name +':id/label', text = 'Search').exists:
            self._device(resourceId = self.calendar_name +':id/label', text = 'Search').click()
        else:
            self._logger.debug("Can't find the search menu")
            return False
        self._device.delay(2)
        if not self._device(resourceId = self.calendar_name +':id/search_edit_text', text = 'Search').exists:
            self._logger.debug("Can't find the search edit view")
            return False
        self._device(resourceId = self.calendar_name +':id/search_edit_text', text = 'Search').set_text(strname)
        self._device.delay(2)
        self._device.press.enter()
        self._device.delay(3)
        for i in range(3):
            if self._device(resourceId = self.calendar_name + ':id/swipe_refresh_layout').child(className = 'android.widget.ImageView').exists:
                self._device.press.enter()
                self._device.delay(3)
            else:
                break
        
        if self._device(resourceId = self.calendar_name +':id/no_results').exists:
            self._logger.warning("Cannot find the caledar.")
            return False
        else:
            self._logger.debug("The caledar exist.")
            return True
            
    def create_schedule(self, event_name, isSetDate, index = 1):
        """add a task
        
        @param event_name: task name
        @param isSetDate: if set to another date
        @param index: set the date the the 'index' days befor current day
        
        """
        self._logger.debug('creat a new event ' + event_name)
        if self._device(resourceId = self.calendar_name +':id/add_event_button').exists:
            self._device(resourceId = self.calendar_name +':id/add_event_button').click()
            self._device.delay(2)
        elif self._device(resourceId = self.calendar_name +':id/floating_action_button').exists:
            self._device(resourceId = self.calendar_name +':id/floating_action_button').click()
            self._device.delay(2)
        else:
            self._logger.debug('Add event button isn\'t exist' )
            return False
        
        if self._device(description = 'Event button').exists:
            self._device(description = 'Event button').click()
            self._device.delay(2)
        
        self._logger.debug('input event name')
        self._device(textContains ='Enter title', resourceId = self.calendar_name +':id/input').set_text(event_name)
        self._device.delay(2)
        if self._device(text = 'Done',  resourceId = self.calendar_name +':id/save').exists:
            self._device(text = 'Done',  resourceId = self.calendar_name +':id/save').click()
            self._device.delay(2)
        if isSetDate:
            today = self._device.shell_adb("shell date +%Y%m%d")
            self.set_start_date(index, today=today) 
        if not self._device(resourceId = self.calendar_name +':id/save').exists:
            self._logger.debug('Save event button isn\'t exist' )
            return False
        self._device(resourceId = self.calendar_name +':id/save').click()
        self._device.delay(2)     
        return self.calendar_is_exist(event_name)
    
    def set_start_date(self, index, today = ''):
        """Set the task date dtart
        
        @param index: set the date the the 'index' days befor current diaplay
                
        """
        if not self._device(resourceId = self.calendar_name +':id/start_date').exists:
            self._logger.debug('The setting date isn\'t exist.' )
            return False
        
        date_begin_text = self._device(resourceId = self.calendar_name +':id/start_date').get_text()
        date_begin, type = self.format_date(date_begin_text)
        
        index_relative = index
        if today <> '':
            self._logger.debug('Today is %s', today )
            today_date = date(int(today[:4]), int(today[4:6]), int(today[6:8]))
            index_relative = (date_begin - today_date).days + index
        self._logger.debug('Days relative is %s', str(index_relative) )
        
        self._device(resourceId = self.calendar_name +':id/start_date').click()        
        self._device.delay(2)
        if self._device(resourceId ='android:id/date_picker_header').exists:
            date_set = self.set_date(index_relative, date_begin)
            self._device.delay(2)
            if self._device(resourceId ='android:id/button1', text = 'OK').exists:
                self._device(resourceId ='android:id/button1', text = 'OK').click()
                self._device.delay(2)
            if self._device(resourceId = self.calendar_name +':id/done').exists:
                self._device(resourceId = self.calendar_name +':id/done').click()
                self._device.delay(2)
        date_text = self._device(resourceId = self.calendar_name +':id/start_date').get_text()
        self._logger.debug("Current set date is %s", date_text)
        if type == 1:      
            format_date = date_set.strftime('%d %b %Y')
        elif type == 2:
            format_date = date_set.strftime('%b %d, %Y')
            
        if date_set.day < 10 :
            if type == 1:
                format_date = format_date[1:]
            elif type == 2:
                format_date = format_date[:4] + format_date[5:]

        self._logger.debug("Need to set date is %s", format_date)      
        if str(date_text).find(format_date) > -1:
            self._logger.debug("set start date success")
            return True        
        else: 
            self._logger.warning("Set start date failed")
            return False
        
    def format_date(self, date_str):
        """format the date display to the date type
        
        @param date_str: date displaying
        
        """
        
        type = 3
        ''' type 1 : Sat, 24 Jan 1970
            type 2 : Sat, Jan 24, 1970/Saturday, Apr 4, 1970
            typr 3: unkonow
        '''
        en_to_in = {'Jan':1, 
                    'Feb':2,
                    'Mar':3,
                    'Apr':4,
                    'May':5,
                    'Jun':6,
                    'Jul':7,
                    'Aug':8,
                    'Sep':9,
                    'Oct':10,
                    'Nov':11,
                    'Dec':12,
                     }
        if date_str[date_str.index(',')+2: ][-8:-5] in en_to_in:      
            dt = date(int(date_str[-4:]), en_to_in[date_str[-8:-5]], int(date_str[-11:-9].lstrip()))
            type = 1
        elif date_str[date_str.index(',')+2: ][:3] in en_to_in:
            dt = date(int(date_str[-4:]), en_to_in[date_str[date_str.index(',')+2: ][:3]], int(date_str[-8:-6].lstrip()))
            type = 2
        else:
            self._logger.debug("Unkonw type")
        self._logger.debug("Format date to %s", dt)
        return dt, type
    
    
    def set_date(self, index, current_date):
        """Set the date 
        
        @param index: set the date the the 'index' days befor current diaplay
        @param current_date: date displaying
        
        """
        set_date = current_date + timedelta(days = index)
        self._logger.debug("Set date to %s", set_date)     
        drag_times = set_date.month - current_date.month + 12*(set_date.year - current_date.year)
        self._logger.debug("Drag %s times to  %s month", drag_times, set_date.month)      
        for i in range(drag_times):
            if index > 0:
#                 self._device.drag(400, 856, 400, 573)
                if self._device(resourceId = 'android:id/next').exists:
                    self._device(resourceId = 'android:id/next').click()
                    self._device.delay(2)
                else:
                    self._logger.debug("Next button not exists.") 
            else:
#                 self._device.drag(400, 537, 400, 856)
                if self._device(resourceId = 'android:id/prev').exists:
                    self._device(resourceId = 'android:id/prev').click()
                    self._device.delay(2)
                else:
                    self._logger.debug("Next button not exists.") 
        self._device(descriptionContains  = self.set_date_string(set_date)).click()
        return set_date
    
    def set_date_string(self, date):
        """Formate the date to the displaying
        
        @param date: date need to fromate
        
        """        
        month_to_string = {1:'January', 
                            2:'February',
                            3:'March',
                            4: 'April',
                            5: 'May',
                            6: 'June',
                            7: 'July',
                            8: 'August',
                            9: 'September',
                            10: 'October',
                            11: 'November',
                            12: 'December',
                     }
        day = ''
        if date.day < 10:
            day = '0' + str(date.day)
        else:
            day = str(date.day)
        month = month_to_string[date.month]
        year = str(date.year)
        self._logger.debug("Click %s", day +' '+ month + ' ' +year)
        return day +' '+ month + ' ' +year

    def delete_calendar(self, calendar_name):
        """delete a task
                
        """
        self._logger.debug('delete calendar task %s', calendar_name)
        if not self.calendar_is_exist(calendar_name):
            return False
        if not self._device(resourceId = self.calendar_name +':id/search_list').child(instance = 0).exists:
            self._logger.debug("Calendar list item isn't exist")
            return False
        self._device(resourceId = self.calendar_name +':id/search_list').child(instance = 0).click()
        self._device.delay(3)
        if not self._device(resourceId = self.calendar_name +':id/title', text = calendar_name).exists:
            self._logger.debug("Open wrong task")
            return False
        if not self._device(description = 'More options').exists:
            self._logger.debug("Can't find the more options icon")
            return False
        self._device(description = 'More options').click()
        self._device.delay(2)
#         if not self._device(resourceId = self.calendar_name +':id/info_action_edit_hit').exists:
#             self._logger.debug("Can't find the edit button")
#             return False
#         self._device(resourceId = self.calendar_name +':id/info_action_edit_hit').click()
#         self._device.delay(2)
        if not self._device(resourceId = 'android:id/title', text = 'Delete').exists:
            self._logger.debug("Can't find the delete menu")
            return False
        self._device(resourceId = 'android:id/title', text = 'Delete').click()
        self._device.delay(2)
#         if not self._device(resourceId = self.calendar_name +':id/delete', text = 'Delete').exists:
#             self._logger.debug("Can't find the delete view")
#             return False
#         self._device(resourceId = self.calendar_name +':id/delete', text = 'Delete').click()
#         self._device.delay(2)
        if self._device(resourceId = 'android:id/button1', text = 'OK').exists:
            self._device(resourceId = 'android:id/button1', text = 'OK').click()
            self._device.delay(2)
            
        self.stay_in_calendar()
        return not self.calendar_is_exist(calendar_name)