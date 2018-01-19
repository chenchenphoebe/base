# -*- coding: UTF-8 -*- 

import os
import sys
import unittest

from common import Common

StorePath_Media = 'sdcard/DCIM/Camera'
gallery_package = 'com.jrdcom.filemanager'
gallery_activity = 'com.jrdcom.filemanager.activity.FileBrowserActivity'

class Camera(Common):
    def __init__(self, device, log_name):
        Common.__init__(self, device, log_name)
        self._ssid = None

    def save_fail_img(self):
        """Save fail screenshot to chrome Folder
        
        """
        self.save_img("gallery")

    def gallery_pic_del(self):
        file_number = self.get_file_num(StorePath_Media, ".jpg")
        self._device.shell_adb(" shell rm -r /storage/emulated/0/DCIM/Camera/")
        self._device.start_activity(gallery_package, gallery_activity)
        if self.get_file_num(StorePath_Media, ".jpg") < file_number:
            self._logger.debug("delete photo successfully!")
            return True
        self._logger.warning("delete photo failed!")
        return False

    def stay_in_camera(self):
        """Keep in Camera main page

        """
        if self.get_current_packagename() == self.get_app_package_from_file('Camera'):
            maxtime = 0
            while not self._device(resourceId='com.tct.tablet.camera:id/mode_overview_button').wait.exists(timeout=2000):
                self._device.press.back()
                self._device.delay(1)
                maxtime += 1
                if maxtime > 3:
                    self._logger.debug("Can't back Camera")
                    break
            if maxtime < 4:
                return True

        self._device.press.home()
        self._logger.debug("Launch Camera.")
        if self.enter_app('Camera'):
            while self._device(resourceId='com.android.packageinstaller:id/permission_message').wait.exists(
                    timeout=2000):
                self._device(text='ALLOW').click()
                self._device.delay(2)
            if self.get_current_packagename() == self.get_app_package_from_file('Camera'):
                maxtime = 0
                while not self._device(resourceId='com.tct.tablet.camera:id/mode_overview_button').wait.exists(
                        timeout=2000):
                    self._device.press.back()
                    self._device.delay(1)
                    maxtime += 1
                    if maxtime > 3:
                        self._logger.debug("Can't back Camera")
                        break
                if maxtime < 4:
                    return True

            self._logger.debug('Launch Camera main page fail')
            return False
        else:
            return False

    def open_HDR(self, status):
        """
         change HDR status
        """
        if self._device(resourceId='com.tct.tablet.camera:id/mode_item_name', text="PHOTO").exists:
            self._device(resourceId='com.tct.tablet.camera:id/mode_item_name', text="PHOTO").click()
            if status is "on":
                switch_hdr = 0
                while not self._device(resourceId='com.tct.tablet.camera:id/hdr_plus_toggle_button',
                                       description='HDR on'):
                    self._device(resourceId='com.tct.tablet.camera:id/hdr_plus_toggle_button').click()
                    switch_hdr += 1
                    if switch_hdr > 1:
                        self._logger.debug("switch the hdr fail")
                        return False
                self._logger.debug("open the hdr successfully")
                return True
            if status is "off":
                switch_hdr = 0
                while not self._device(resourceId='com.tct.tablet.camera:id/hdr_plus_toggle_button',
                                       description='HDR off'):
                    self._device(resourceId='com.tct.tablet.camera:id/hdr_plus_toggle_button').click()
                    switch_hdr += 1
                    if switch_hdr > 1:
                        self._logger.debug("switch the hdr fail")
                        return False
                self._logger.debug("close the hdr successfully")
                return True
        else:
            self._logger.debug("not in the camera application")
            return False

    def take_photo(self, mode, delay):
        """take  a photo

        """
        self._logger.debug('take %s photo', mode)
        self._device.delay(2)
        file_number = self.get_file_num(StorePath_Media, [".jpg"])
        if self._device(resourceId='com.tct.tablet.camera:id/mode_item_name', text=mode).wait.exists(timeout=2000):
            self._device(resourceId='com.tct.tablet.camera:id/mode_item_name', text=mode).click()
            self._device.delay(2)
            if self._device(resourceId='com.tct.tablet.camera:id/shutter_button').wait.exists(timeout=2000):
                self._device(resourceId='com.tct.tablet.camera:id/shutter_button').click()
                self._logger.debug("0000000000000000000000")
                if delay == '1':
                    self._device.delay(2)
                elif delay == '2':
                    self._device.delay(6)
                elif delay == '3':
                    self._device.delay(7)
                elif delay == '4':
                    self._device.delay(13)
                    self._logger.debug("1111111111111111111111111")

        else:
            self._logger.warning("Get mode button failed!")
            return False
        self._logger.debug("3333333333333")
        if self.get_file_num(StorePath_Media, [".jpg"]) == file_number + 1:
            return True
        else:
            self._logger.warning("Take picture failed!")
            return False

    def stay_in_filemanger(self):
        """Keep in Filemanager main page

        """
        if self.get_current_packagename() == self.get_app_package_from_file('Files'):
            maxtime = 0
            while not self._device(resourceId='com.jrdcom.filemanager:id/phone_name', text='Internal storage').wait.exists(timeout=2000):
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
                while not self._device(resourceId='com.jrdcom.filemanager:id/phone_name',
                                       text='Internal storage').wait.exists(timeout=2000):
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

    def delete_media_file(self, type):
        """
        clear the gallery picture
        """
        self.stay_in_filemanger()
        self._device.delay(2)
        self._device(resourceId='com.jrdcom.filemanager:id/phone_name', text='Internal storage').click()
        if self._device(className='android.widget.LinearLayout').child_by_text(type, allow_scroll_search=True, \
                                                                               resourceId='com.jrdcom.filemanager:id/edit_adapter_name').wait.exists(
            timeout=2000):
            self._device(text=type).click()
            if self._device(description='More options').wait.exists(timeout=2000):
                self._device(description="More options").click()
                if self._device(text='Select').wait.exists(timeout=2000):
                    self._device(text='Select').click()
                    if self._device(resourceId='com.jrdcom.filemanager:id/more_btn').wait.exists(timeout=2000):
                        self._device(resourceId="com.jrdcom.filemanager:id/more_btn").click()
                        if self._device(text='Select all').wait.exists(timeout=2000):
                            self._device(text='Select all').click()
                            if self._device(resourceId='com.jrdcom.filemanager:id/delete_btn').wait.exists(
                                    timeout=2000):
                                self._device(resourceId='com.jrdcom.filemanager:id/delete_btn').click()
                                if self._device(text='DELETE').wait.exists(timeout=2000):
                                    self._device(text='DELETE').click()
                                    if self._device(text='This folder is empty').wait.exists(timeout=20000):
                                        self._logger.debug("clear the %s media type file successfully", type)
                                        return True
                                    else:
                                        self._logger.debug("clear the %s media type file fail", type)
                                        return False
                                else:
                                    self._logger.debug("DELETE icon not exists")
                                    return False
                            else:
                                self._logger.debug("delete icon not exists")
                                return False
                        else:
                            self._logger.debug("Select all icon not exists")
                            return False
                    else:
                        self._logger.debug("more_btn not exists")
                        return False
                else:
                    self._logger.debug("Select icon not exists")
                    return False
            else:
                self._logger.debug("more options1 not exists")
                return False
        else:
            self._logger.debug("%s not exists", type)
            return False

    def open_flash(self, mode):
        """
        change flash mode
        """
        change_mode_time = 0
        while not self._device(description=mode).wait.exists(timeout=3000):
            self._device(resourceId='com.tct.tablet.camera:id/flash_toggle_button').click()
            change_mode_time += 1
            self._logger.debug("the change time is %d", change_mode_time)
            if change_mode_time > 7:
                self._logger.debug("change the flash mode as %s fail", mode)
                return False
        self._logger.debug("the flash mode as %s successfully", mode)
        return True

    def switch_mode(self):
        """
        switch mode
        """
        mode = ["FACE BEAUTY", "PHOTO", "BOKEH", "PANO", "VIDEO"]
        choose_time=0
        for i in mode:
            if self._device(text=i).wait.exists():
                self._device(text=i).click()
                choose_time += 1
                self._logger.debug("choose the %s mode", i)
                if choose_time == 5:
                    self._logger.debug("the current cycle complete")
                    return True
            else:
                self._logger.debug("can't find the %s mode", i)
                return False

    def take_video(self):
        """take a video

        """
        self._logger.debug('take video')
        file_number = self.get_file_num(StorePath_Media, ['.3gp', '.mp4'])
        if self._device(resourceId='com.tct.tablet.camera:id/mode_item_name', text="VIDEO").exists:
            self._device(resourceId='com.tct.tablet.camera:id/mode_item_name', text="VIDEO").click()
            # close the flash light
            while self._device(description='Flashlight on').wait.exists(timeout=2000):
                self._device(resourceId='com.tct.tablet.camera:id/flash_toggle_button').click()
            if self._device(resourceId='com.tct.tablet.camera:id/shutter_button').wait.exists(timeout=2000):
                self._device(resourceId='com.tct.tablet.camera:id/shutter_button').click()
                if self.take_photo_when_video():
                    self._logger.debug("take all photoes successfully while taking video")
                else:
                    self._logger.debug("take all photoes fail while taking video")
                    return False
                self._device.delay(150)
                self._logger.debug("recording the video successfully")
                if self._device(resourceId='com.tct.tablet.camera:id/shutter_button').wait.exists(timeout=2000):
                    self._device(resourceId='com.tct.tablet.camera:id/shutter_button').click()
                    self._logger.debug("stop recording the video")
                    self._device.delay(3)
                    return True
                else:
                    self._logger.debug("take video fail")
                    return False
        else:
            self._logger.warning("Get take video button failed!")
            return False
        if self.get_file_num(StorePath_Media, ['.3gp', '.mp4']) == file_number + 1:
            return True
        else:
            self._logger.warning("Take picture failed!")
            return False

    def get_current_camera_status(self):
        """
        get the current status
        """
        camera_info = self._device.shell_adb("shell dumpsys media.camera v -2")
        camera_info_divide = camera_info.split('\n')
        size = len(camera_info_divide)
        camera_id = []
        if size > 1:
            for index in range(size - 1):
                if camera_info_divide[index].find('Camera ID') > -1:
                    self._logger.debug(camera_info_divide[index])
                    if "Camera ID: 1" in camera_info_divide[index]:
                        self._logger.debug("the current camera status is front ")
                        return "front"
                    elif "Camera ID: 0" in camera_info_divide[index]:
                        self._logger.debug("the current camera status is back")
                        return "back"

    def take_photo_when_video(self):
        """
         take photo while taking video and judge the picture number
        """
        take_photo_times = 0
        for i in range(20):
            file_number = self.get_file_num(StorePath_Media, [".jpg"])
            if self._device(resourceId='com.tct.tablet.camera:id/video_snap_button').wait.exists(timeout=2000):
                self._device(resourceId='com.tct.tablet.camera:id/video_snap_button').click()
                self._device.delay(2)
                take_photo_times += 1
                if self.get_file_num(StorePath_Media, [".jpg"]) == file_number + 1:
                    self._logger.debug("take photo %d times successfully", take_photo_times)
                else:
                    return False
        if take_photo_times is 20:
            return True
        else:
            self._logger.debug("take photo fail while taking video")
            return False

    def open_low_loght(self, status):
        """
            change HDR status
        """
        if self._device(resourceId='com.tct.tablet.camera:id/mode_item_name', text="PHOTO").exists:
            self._device(resourceId='com.tct.tablet.camera:id/mode_item_name', text="PHOTO").click()
            if status is "on":
                switch_hdr = 0
                while not self._device(resourceId='com.tct.tablet.camera:id/lowlight_toggle_button',
                                       description='Low light on'):
                    self._device(resourceId='com.tct.tablet.camera:id/lowlight_toggle_button').click()
                    switch_hdr += 1
                    if switch_hdr > 1:
                        self._logger.debug("switch the low light mode fail")
                        return False
                self._logger.debug("open the low light mode successfully")
                return True
            if status is "off":
                switch_hdr = 0
                while not self._device(resourceId='com.tct.tablet.camera:id/lowlight_toggle_button',
                                       description='Low light off'):
                    self._device(resourceId='com.tct.tablet.camera:id/lowlight_toggle_button').click()
                    switch_hdr += 1
                    if switch_hdr > 1:
                        self._logger.debug("switch the low light fail")
                        return False
                self._logger.debug("close the low light successfully")
                return True
        else:
            self._logger.debug("not in the camera application")
            return False

    def open_filter(self):

        # close the flash light
        while self._device(description='FLASH ON').wait.exists(timeout=2000):
            self._device(resourceId='com.tct.tablet.camera:id/flash_toggle_button').click()
        filter_list = ['amaro', 'juno', 'lofi', 'title_gingham', 'title_clarendon', 'title_inkwell',
                       'title_reyes', 'title_hefe']
        take_fiter_photo = 0
        for filter in filter_list:
            if self._device(resourceId='com.tct.tablet.camera:id/camera_filters_button').wait.exists(
                    timeout=2000):
                self._device(resourceId='com.tct.tablet.camera:id/camera_filters_button').click()
                if self._device(resourceId='com.tct.tablet.camera:id/filter_labels').wait.exists(timeout=3000):
                    self._logger.debug("enter filter mode successfully")
                    if self._device(resourceId='com.tct.tablet.camera:id/filter_' + str(filter)).wait.exists(
                            timeout=2000):
                        self._device(resourceId='com.tct.tablet.camera:id/filter_' + str(filter)).click()
                        self._logger.debug("choose %s filter to take photo!!!!!!!!!!!!!!!!!!!!!!", str(filter))
                        # every filter take photos 10 times
                        cycle_time = 0
                        for i in range(10):
                            file_number = self.get_file_num(StorePath_Media, [".jpg"])
                            self._logger.debug("the file num is %d before taking photo", file_number)
                            if self._device(resourceId='com.tct.tablet.camera:id/shutter_button').wait.exists(
                                    timeout=2000):
                                self._device(resourceId='com.tct.tablet.camera:id/shutter_button').click()
                                cycle_time += 1
                                self._logger.debug("take photo %d times", cycle_time)
                                self._device.delay(10)
                                if self.get_file_num(StorePath_Media, [".jpg"]) == file_number + 1:
                                    self._logger.debug("the file num is %d after taking photo",
                                                       self.get_file_num(StorePath_Media, [".jpg"]))
                                    self._logger.debug("take fiter photo successfully")
                                else:
                                    self._logger.warning("Take picture failed!")
                                    return False
                            else:
                                self._logger.warning("Get take photo button failed!")
                                return False
                        if cycle_time is 10:
                            take_fiter_photo += 1
                            self._logger.debug("the fiter num is %s", str(take_fiter_photo))
                            self._logger.debug("take filter photo 2 times successfully")
                        else:
                            return False
        if take_fiter_photo is 8:
            self._logger.debug("choose 8 filter to take photo successfully")
            return True
        else:
            return False

    def switch_delay_mode(self):
        # swicth the delay time
        if self._device(resourceId='com.tct.tablet.camera:id/mode_item_name', text="PHOTO").exists:
            self._device(resourceId='com.tct.tablet.camera:id/mode_item_name', text="PHOTO").click()
        for i in range(10):
            switch_delay_time = 0
            for j in range(3):
                if self._device(resourceId='com.tct.tablet.camera:id/countdown_toggle_button').wait.exists(
                        timeout=2000):
                    self._device(resourceId='com.tct.tablet.camera:id/countdown_toggle_button').click()
                    switch_delay_time += 1
                    self._logger.debug("switch the delay mode %d times", switch_delay_time)
                file_number = self.get_file_num(StorePath_Media, [".jpg"])
                delay_mode = self._device(
                    resourceId='com.tct.tablet.camera:id/countdown_toggle_button').getContentDescription()
                if self._device(resourceId='com.tct.tablet.camera:id/shutter_button').wait.exists(timeout=2000):
                    self._device(resourceId='com.tct.tablet.camera:id/shutter_button').click()
                    if delay_mode is 'Countdown timer is off':
                        self._device.delay(1)
                    elif delay_mode is 'Countdown timer duration is set to 5 seconds':
                        self._device.delay(3)
                    else:
                        self._device.delay(15)
                    if self.get_file_num(StorePath_Media, [".jpg"]) == file_number + 1:
                        self._logger.debug("take %s delay photo successfully", delay_mode)
                    else:
                        self._logger.warning("Take picture failed!")
                        return False
            if switch_delay_time is 3:
                self._logger.debug("the cycle %d complete", i)
        if i is 9:
            self._logger.debug("swicth delay 10 times complete")
            return True

    def switch_camera_back_front(self):
        if self._device(descriptionContains='HDR').wait.exists(timeout=3000):
            self._logger.debug("the current status is back")
            if self._device(resourceId='com.tct.tablet.camera:id/camera_toggle_bottom_button').wait.exists(
                    timeout=2000):
                self._device(resourceId='com.tct.tablet.camera:id/camera_toggle_bottom_button').click()
                if not self._device(descriptionContains='HDR').wait.exists(timeout=3000):
                    self._logger.debug("switch tha back as front successfully")
                    self._device.delay(2)
                    return True
                else:
                    self._logger.debug("switch the back as front fail")
                    return False
        elif not self._device(descriptionContains="HDR").wait.exists(timeout=3000):
            self._logger.debug("the current status is front")
            if self._device(resourceId='com.tct.tablet.camera:id/camera_toggle_bottom_button').wait.exists(
                    timeout=2000):
                self._device(resourceId='com.tct.tablet.camera:id/camera_toggle_bottom_button').click()
                self._device.delay(2)
                if self._device(descriptionContains='HDR').wait.exists(timeout=3000):
                    self._logger.debug("switch tha front as back successfully")
                    self._device.delay(2)
                    return True
                else:
                    self._logger.debug("switch the front as back fail")
                    return False

    def switch_back_front(self, status):
        if status is "back":
            if self.get_current_camera_status() is "front":
                self._device(resourceId='com.tct.tablet.camera:id/camera_toggle_bottom_button').click()
                self._logger.debug("switch the status as back")
            self._logger.debug("the  current status is back")
            return True
        elif status is "front":
            if self.get_current_camera_status() is "back":
                self._device(resourceId='com.tct.tablet.camera:id/camera_toggle_bottom_button').click()
                self._logger.debug("switch the status as front")
            self._logger.debug("the  current status is front")
            return True

    def switch_camera_mode(self):

        if not self._device(resourceId='com.tct.tablet.camera:id/manual_settings').wait.exists(timeout=2000):
            self.back_to_home()
            self.stay_in_camera()
            if self._device(resourceId='com.tct.tablet.camera:id/mode_overview_button').wait.exists(
                    timeout=2000):
                self._device(resourceId='com.tct.tablet.camera:id/mode_overview_button').click()
                if self._device(text='Manual').wait.exists(timeout=2000):
                    self._device(text='Manual').click()
                else:
                    self._logger.debug("not exists manual")
                    return False
            else:
                self._logger.debug("overview button not exists")
                return False
        manual_sum = self._device(resourceId='com.tct.tablet.camera:id/manual_settings').getChildCount()
        self._logger.debug("the manual_sum is %d", manual_sum)
        for i in range(manual_sum):
            self._logger.debug(i)
            if self._device(resourceId='com.tct.tablet.camera:id/manual_settings') \
                    .child(className='android.widget.LinearLayout', index=i).wait.exists(timeout=2000):
                self._device(resourceId='com.tct.tablet.camera:id/manual_settings') \
                    .child(className='android.widget.LinearLayout', index=i).click()
            if i == 0 or i == 2 or i == 3:
                change_mode1 = 0
                for j in range(8):
                    file_number = self.get_file_num(StorePath_Media, [".jpg"])
                    if self._device(resourceId='com.tct.tablet.camera:id/scale_tip_layout').wait.exists(
                            timeout=2000):
                        self._device(resourceId='com.tct.tablet.camera:id/shutter_button').click()
                        change_mode1 += 1
                        self._logger.debug("take the current mode %d times", change_mode1)
                        self._device.delay(6)
                        if self.get_file_num(StorePath_Media, [".jpg"]) == file_number + 1:
                            self._logger.debug("take photo successfully")
                        else:
                            self._logger.warning("Take picture failed!")
                            return False
                        self._device(resourceId='com.tct.tablet.camera:id/manual_settings') \
                            .child(className='android.widget.LinearLayout', index=i).click()
                        if j != 8:
                            self._device.swipe(893, 1345, 716, 1357)
                            self._device.delay(1)
                if change_mode1 is 8:
                    self._logger.debug("the current mode take photo successfully")
            elif i == 1:
                change_mode2 = 0
                for j in range(12):
                    file_number = self.get_file_num(StorePath_Media, [".jpg"])
                    if self._device(resourceId='com.tct.tablet.camera:id/scale_tip_layout').wait.exists(
                            timeout=2000):
                        self._device(resourceId='com.tct.tablet.camera:id/shutter_button').click()
                        change_mode2 += 1
                        self._logger.debug("take the current mode %d times", change_mode2)
                        self._device.delay(6)
                        if self.get_file_num(StorePath_Media, [".jpg"]) == file_number + 1:
                            self._logger.debug("take photo successfully")
                        else:
                            self._logger.warning("Take picture failed!")
                            return False
                        self._device(resourceId='com.tct.tablet.camera:id/manual_settings') \
                            .child(className='android.widget.LinearLayout', index=i).click()
                        if j != 12:
                            self._device.swipe(893, 1345, 716, 1357)
                if change_mode2 is 12:
                    self._logger.debug("the current mode take photo successfully")
            elif i == 4:
                for i in range(5):
                    file_number = self.get_file_num(StorePath_Media, [".jpg"])
                    if self._device(resourceId='com.tct.tablet.camera:id/scale_tip_layout').wait.exists(
                            timeout=2000):
                        self._device(resourceId='com.tct.tablet.camera:id/shutter_button').click()
                        self._device.delay(6)
                        if self.get_file_num(StorePath_Media, [".jpg"]) == file_number + 1:
                            self._logger.debug("take photo successfully")
                            return True
                        else:
                            self._logger.warning("Take picture failed!")
                            return False
                    self._device(resourceId='com.tct.tablet.camera:id/manual_settings') \
                        .child(className='android.widget.LinearLayout', index=i).click()

    def clear_camera(self):
        self.enterSettings("Apps")
        if self._device(resourceId='com.android.settings:id/action_bar').child(text='Apps').wait.exists(timeout=3000):
            self._logger.debug("enter the Apps successfully")
            self._device.delay(2)
            if self._device(className='android.widget.ListView'). \
                    child_by_text('Camera',allow_scroll_search=True, resourceId='android:id/title').wait.exists(timeout=2000):
                self._device(text='Camera').click()
                self._device.delay(2)
                self._device(text='Storage').click()
                self._device.delay(2)
                self._device(text='CLEAR DATA').click()
                if self._device(text='Delete app data?').wait.exists(timeout=2000):
                    self._device(text='OK').click()
                return True

            else:
                self._logger.debug("Can't find Camera")
                return False

        else:
            self._logger.debug("enter the Apps fail")


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