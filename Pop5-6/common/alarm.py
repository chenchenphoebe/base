
from common import Common

class Alarm(Common):

    """Provide common functions involved Alarm."""
    
    def stay_in_alarm(self):
        """Keep in Alarm main page
        
        """
        maxtime = 0
        if self.get_current_packagename() == self.get_app_package_from_file('Clock'):
            while (not self._device(className  ='android.app.ActionBar$Tab').exists)\
             and (not self._device(className  ='android.support.v7.app.ActionBar$Tab').exists):
                self._device.press.back()
                maxtime += 1
                if maxtime > 3:
                    self._logger.debug("Can't back alarm")
                    break
            if maxtime < 4:
                if self._device(description ='Alarm').exists:
                    if not self._device(description ='Alarm').isSelected():
                        self._device(description ='Alarm').click()
                        self._device.delay(2)
                    return self._device(description ='Alarm').isSelected()
        self._device.press.home()
        self._logger.debug("Launch alarm.")
        if self.enter_app('Clock'):
            self._device.delay(2)
            if self.get_current_packagename() == self.get_app_package_from_file('Clock'):
                if self._device(description ='Alarm').exists:
                    if not self._device(description ='Alarm').isSelected():
                        self._device(description ='Alarm').click()
                        self._device.delay(2)
                    return self._device(description ='Alarm').isSelected()
            else:
                self._logger.debug('Launch alarm fail')
                return False
        else:
            return False
        
    def add_alarm_without_change(self):
        """add an alarm without change.
        
        """
        self._logger.debug("Add an alarm without change.")
        if self._device(resourceId='com.android.deskclock:id/fab').exists:
            self._device(resourceId='com.android.deskclock:id/fab').click()
            self._device.delay(2)
            self._device(text='OK').click()
            self._device.delay(2)
            if self._device(resourceId='com.android.deskclock:id/onoff', checked = True).exists:
                return True
        self._logger.debug('alarm add fail!')
        return False
    
    def discheck_alarm_current_page(self):
        """disable all alarm current page displaying
        
        """
        if self._device(resourceId='com.android.deskclock:id/onoff').exists:
            for i in range(self._device(resourceId='com.android.deskclock:id/onoff').count):
                if self._device(resourceId='com.android.deskclock:id/onoff',  instance = i).isChecked():
                    self._logger.debug('Disable one alarm.')
                    self._device(resourceId='com.android.deskclock:id/onoff',  instance = i).click()
                    self._device.delay(1)
        if not self._device(resourceId='com.android.deskclock:id/onoff', checked = True).exists:
            return True
        else:
            self._logger.debug('Disable alarm fail!')
            return False
        
    def delete_alarm(self):
        '''Delete a alarm.        

        '''
        self._logger.debug('delete a alarm')
        is_last = False
        if self._device(resourceId= 'com.android.deskclock:id/alarms_list').exists \
            and self._device(resourceId= 'com.android.deskclock:id/alarm_item').exists:
            if self._device(resourceId= 'com.android.deskclock:id/alarms_list').isScrollable():
                self._device(resourceId= 'com.android.deskclock:id/alarms_list', scrollable=True).scroll.vert.toBeginning()
            if not self._device(resourceId= 'com.android.deskclock:id/alarm_item', instance = 0).child(resourceId= 'com.android.deskclock:id/delete').exists:
                self._device(resourceId= 'com.android.deskclock:id/alarm_item', instance = 0).child(index = 0).click()
                self._device.delay(2)
            
            if self._device(resourceId= 'com.android.deskclock:id/delete').exists:
                self._device(resourceId= 'com.android.deskclock:id/delete').click()
                self._device.delay(3)
                if self._device(text = 'Alarm deleted.').exists:
                    self._logger.debug("Delete the alarm succesfully")
                    return True
                else:
                    self._logger.debug("Delete the alarm fail")
                    return False
            else:
                self._logger.debug("Delete is exist")
                return False  
        elif self._device(resourceId= 'com.android.deskclock:id/alarms_recycler_view').exists \
            and self._device(resourceId= 'com.android.deskclock:id/digital_clock').exists:
            if self._device(resourceId= 'com.android.deskclock:id/alarms_recycler_view').isScrollable():
                self._device(resourceId= 'com.android.deskclock:id/alarms_recycler_view', scrollable=True).scroll.vert.toBeginning()
            if (not self._device(resourceId= 'com.android.deskclock:id/delete').exists) and \
            self._device(resourceId= 'com.android.deskclock:id/arrow', instance = 0).exists:
                self._device(resourceId= 'com.android.deskclock:id/arrow', instance = 0).click()
                self._device.delay(2)
            
            if self._device(resourceId= 'com.android.deskclock:id/delete').exists:
                self._device(resourceId= 'com.android.deskclock:id/delete').click()
                self._device.delay(3)
                if self._device(text = 'Alarm deleted').exists:
                    self._logger.debug("Delete the alarm succesfully")
                    return True
                else:
                    self._logger.debug("Delete the alarm fail")
                    return False
            else:
                self._logger.debug("Delete is exist")
                return False  
        
        else:
            self._logger.debug('None alarm exist!')
            return False