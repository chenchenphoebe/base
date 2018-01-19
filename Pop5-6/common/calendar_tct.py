
import string
import re
import sys
from common import Common
from datetime import datetime,date,timedelta

class Calendar(Common):

    """Provide common functions involved Calendar."""
    
        
    def stay_in_calendar(self):
        """Keep in Calendar main page
        
        """
        maxtime = 0
        while not  self._device(description ='Today', resourceId = 'com.tct.calendar:id/action_today').exists:
            self._device.press.back()
            maxtime += 1
            if maxtime > 3:
                self._logger.debug("Can't back calendar")
                break
        if maxtime < 4:
            return True
        else:
            self._device.press.home()
            self._logger.debug("Launch calendar.")
        if self.enter_app('Calendar'):
            self._device.delay(2)
            if self.get_current_packagename() == self.get_app_package_from_file('Calendar'):
                maxtime = 0
                while not  self._device(description ='Today', resourceId = 'com.tct.calendar:id/action_today').exists:
                    self._device.press.back()
                    maxtime += 1
                    if maxtime > 3:
                        self._logger.debug("Can't launch calendar main page")
                        return False
                
                self._logger.debug('Launch calendar main page successfully.')
                return True
            else:
                self._logger.debug('Launch calendar fail')
                return False
        else:
            return False      
            
    def switch_view(self, strsort):
        """Switch to specified view.
        
        @param (str)strsort: view type
        
        """
        self.stay_in_calendar()
        if not self.check_view_type(strsort):
            self._logger.debug("Switch to %s view." % strsort)
#             if not self._device(resourceId  ='android:id/action_bar_spinner').exists:
#                 self._logger.debug('Spinner isn\'t exist')
#                 return False
#             self._device(resourceId  ='android:id/action_bar_spinner').click()
#             self._device.delay(2)
#             if not self._device(text = strsort).exists:
#                 self._logger.debug(strsort + " isn't exist")
#                 return False
            self._device(text = strsort).click()
        if self.check_view_type(strsort):
            return True
        else:
            self._logger.debug('can not enter the view of '+strsort)
            return False
        
    def check_view_type(self, strsort):
        """check view type whether same as the specified.
        
        @param (str)strsort: view type
        
        """
        if (strsort == "Day" and self._device(text="Day", selected = True).exists):
            self._logger.debug("Current view is Day")
            return True
        elif (strsort == "Week" and self._device(text="Week", selected = True).exists):
            self._logger.debug("Current view is Week")
            return True
        elif (strsort == "Month" and self._device(text="Month", selected = True).exists):
            self._logger.debug("Current view is Month")
            return True
        elif (strsort == "Agenda" and self._device(text="Agenda", selected = True).exists):
            self._logger.debug("Current view is Agenda")
            return True
        elif (strsort == "Year" and self._device(text="Year", selected = True).exists):
            self._logger.debug("Current view is Year")
            return True
        else:
            self._logger.warning("Cannot enter %s." % strsort)
            return False
     
#     def SelectMenuItem(self, stritem):
#         self._device.press(82)
#         self._device.delay(1)
#         self._device(text=stritem).click()        
#         self._device.delay(2)     
                   
    def calendar_is_added(self, strname):
        """check if task added.
        
        @param  (str)strname: task name just added.
        
        """
        self.switch_view("Agenda")
        if self._device(resourceId= 'com.tct.calendar:id/agenda_events_list').\
        child_by_text(strname, resourceId = 'com.tct.calendar:id/title', allow_scroll_search=True,).exists:
            return True
        else:
            self._logger.warning("Cannot find the caledar added.")
            return False
            
    def create_schedule(self, event_name, isSetDate, index = 1):
        """add a task
        
        @param event_name: task name
        @param isSetDate: if set to another date
        @param index: set the date the the 'index' days befor current diaplay
        
        """
        self._logger.debug('creat a new event ' + event_name)
        if self._device(resourceId ='com.tct.calendar:id/floating_action_button').exists:
            self._device(resourceId ='com.tct.calendar:id/floating_action_button').click()
            self._device.delay(2)
        else:
            self._logger.debug('Add event button isn\'t exist' )
            return False
        if self._device(text = 'Add account', resourceId ='android:id/button1').exists:
            self._logger.debug('It is should add a account before test.')
            return False
        self._logger.debug('input event name')
        self._device(className ='android.widget.EditText', resourceId = 'com.tct.calendar:id/title', instance = 0).set_text(event_name)
        self._device.delay(2)
        if isSetDate:
            self.set_start_date(index) 
        self._device(resourceId ='com.tct.calendar:id/action_done').click()
        self._device.delay(2)     
        return self.calendar_is_added(event_name)
    
    def set_start_date(self, index):
        """Set the task date dtart
        
        @param index: set the date the the 'index' days befor current diaplay
                
        """
        if not self._device(resourceId ='com.tct.calendar:id/start_date').exists:
            self._logger.debug('The setting date isn\'t exist.' )
            return False
        date_begin_text = self._device(resourceId ='com.tct.calendar:id/start_date').get_text()
        date_begin, type = self.format_date(date_begin_text)
        self._device(resourceId ='com.tct.calendar:id/start_date').click()        
        self._device.delay(2)
        if self._device(resourceId ='com.tct.calendar:id/date_picker_header').exists:
# Set the day to the next day. The from day will change to the set day when open the setting page next time after setting this time.
            date_set = self.set_date(index, date_begin)
            self._device.delay(2)
#             self._device(resourceId ='com.tct.calendar:id/done').click()
            self._device.click(int(self._device(resourceId ='com.tct.calendar:id/done').info[u'bounds'][u'left']) + 30, \
                int(self._device(resourceId ='com.tct.calendar:id/done').info[u'bounds'][u'top']) + 252)    
            self._device.delay(2)
        date_text = self._device(resourceId ='com.tct.calendar:id/start_date').get_text()
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
        
        type = 1
        ''' type 1 : Sat, 24 Jan 1970'
            type 2 : Sat, Jan 24, 1970
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
        if date_str[-8:-5] in en_to_in:      
            dt = date(int(date_str[-4:]), en_to_in[date_str[-8:-5]], int(date_str[-11:-9].lstrip()))
            type = 1
        else:
            dt = date(int(date_str[-4:]), en_to_in[date_str[5:8]], int(date_str[-8:-6].lstrip()))
            type = 2
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
            self._device.drag(240, 853, 240, 538)
            self._device.delay(2)
          
#         self._device(description = self.set_date_string(set_date)).click()
        des_date = self.set_date_string(set_date)
        self._device.click(int(self._device(description = des_date).info[u'bounds'][u'left']) + 30, \
                            int(self._device(description = des_date).info[u'bounds'][u'top']) + 252)
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

    def delete_calendar(self):
        """delete a task
                
        """
        self._logger.debug('delete calendar task')
        is_last = False
        if self._device(resourceId= 'com.tct.calendar:id/agenda_events_list').exists \
            and self._device(resourceId= 'com.tct.calendar:id/agenda_item_text_container').exists:
            if self._device(resourceId= 'com.tct.calendar:id/agenda_events_list').isScrollable():
                self._device(resourceId= 'com.tct.calendar:id/agenda_events_list', scrollable=True).scroll.vert.toBeginning()
            first_task = self._device(resourceId= 'com.tct.calendar:id/agenda_item_text_container', instance = 0).child(resourceId= 'com.tct.calendar:id/title').get_text()
            self._logger.debug("Delete task %s", first_task)  
            if self._device(resourceId= 'com.tct.calendar:id/agenda_item_text_container').count > 1:
                second_task = self._device(resourceId= 'com.tct.calendar:id/agenda_item_text_container', instance = 1).child(resourceId= 'com.tct.calendar:id/title').get_text()
                self._logger.debug("The next task is %s", second_task)
            else:
                is_last = True
            self._device(resourceId= 'com.tct.calendar:id/agenda_item_text_container', instance = 0).child(resourceId= 'com.tct.calendar:id/title').click()
            self._device.delay(2)
        else:
            self._logger.debug("There is none task")
            return False
        if  self._device(resourceId= 'com.tct.calendar:id/event_info_headline').child(resourceId= 'com.tct.calendar:id/title').exists:      
            if self._device(resourceId= 'com.tct.calendar:id/info_action_delete').exists:
                self._device(resourceId= 'com.tct.calendar:id/info_action_delete').click()
                self._device.delay(2)
                
            if self._device(resourceId= 'com.tct.calendar:id/delete').exists:
                self._device(resourceId= 'com.tct.calendar:id/delete').click()
                self._device.delay(2)
            
            if self._device(resourceId= 'android:id/button1').exists:
                self._device(resourceId= 'android:id/button1').click()
                self._device.delay(2)
        if not self._device(resourceId = 'com.tct.calendar:id/agenda_events_list').wait.exists(timeout=15000):
            self._logger.debug("Didn't back to event list.")
            return False
        if is_last:
            if not self._device(resourceId= 'com.tct.calendar:id/agenda_item_text_container').exists:
                self._logger.debug("Delete successful.")
                return True
            else:
                self._logger.debug("Delete fail.")
                return False
        else:
            if self._device(resourceId= 'com.tct.calendar:id/agenda_events_list').isScrollable():
                self._device(resourceId= 'com.tct.calendar:id/agenda_events_list', scrollable=True).scroll.vert.toBeginning()
                self._device.delay(2)
            first_task_after = self._device(resourceId= 'com.tct.calendar:id/agenda_item_text_container', instance = 0).child(resourceId= 'com.tct.calendar:id/title').get_text()
            self._logger.debug("The first task after delete is %s", first_task_after)
            if first_task <> first_task_after or first_task_after == second_task:
                self._logger.debug("Delete successful.")
                return True
            else:
                self._logger.debug("Delete fail.")
                return False