# -*- coding: UTF-8 -*-
#*****************************************************************************
# Title:        00_ctsverifier
#*****************************************************************************

from __future__ import division

import traceback

import common.common
from common.ctsverifier import Ctsverifier
from common.getconfigs import GetConfigs
from uiautomator import Device 
import time
from nose import case


logger = common.common.createlogger("MAIN") 


mdevice= common.common.connect_device("MDEVICE")
mcts=common.ctsverifier.Ctsverifier(mdevice, "M_CTS")
logger.debug("Connect devices")

def main():
    mcts.enter_app('CTS Verifier')
    mcts.Initial()
#     mcts.Always_Wake()
#     AUDIO 6 case
    mcts.Audio_Frequency_Line_Test('Audio Frequency Line Test') 
    mcts.Audio_Input_Devices_Notifications_Test('Audio Input Devices Notifications Test')
    mcts.Audio_Input_Routing_Notifications_Test('Audio Input Routing Notifications Test')
    mcts.Audio_Output_Devices_Notifications_Test('Audio Output Devices Notifications Test')
    mcts.Audio_Output_Routing_Notifications_Test('Audio Output Routing Notifications Test')
    mcts.Hifi_Ultrasound_Speaker_Test('Hifi Ultrasound Speaker Test')
#     CAR 1 case
    mcts.Car_Dock_Test('Car Dock Test') 
#     camera 7 case
    mcts.Camera_FOV_Calibration('Camera FOV Calibration')
    mcts.Camera_Flashlight('Camera Flashlight')
    mcts.Camera_ITS_Test('Camera ITS Test') 
    mcts.Camera_Intents('Camera Intents') 
    mcts.Camera_Orientation('Camera Orientation') 
    mcts.Camera_Video('Camera Video')
    mcts.Camera_Formats('Camera Formats') 
#     CLOCK 1 case
    mcts.Alarms_And_Timers_Tests('Alarms and Timers Tests')
    mcts.Screen_Lock_Test('Screen Lock Test')    
    mcts.Keyguard_Disabled_Features_Test('Keyguard Disabled Features Test')
    mcts.Redacted_Notifications_Keyguard_Disabled_Features_Test('Redacted Notifications Keyguard Disabled Features Test')
    mcts.Hardware_Software_Feature_Summary('Hardware/Software Feature Summary')
    mcts.Connectivity_Constraints('Connectivity Constraints')
    mcts.Battery_Saving_Mode_Test('Battery Saving Mode Test')
    mcts.Device_Only_Mode_Test('Device Only Mode Test')
    mcts.High_Accuracy_Mode_Test('High Accuracy Mode Test')
    mcts.Location_Mode_Off_Test('Location Mode Off Test')
    mcts.BYOD_Provisioning_tests('BYOD Provisioning tests')
    mcts.Device_Owner_Provisioning('Device Owner Provisioning')
    mcts.Projection_Cube_Test('Projection Cube Test')
    mcts.Projection_Multitouch_Test('Projection Multitouch Test')
    mcts.Projection_Offscreen_Activity('Projection Offscreen Activity')
    mcts.Projection_Scrolling_List_Test('Projection Scrolling List Test')
    mcts.Projection_Widget_Test('Projection Widget Test')
    mcts.KeyChain_Storage_Test('KeyChain Storage Test')  
    mcts.Keyguard_Password_Verification('Keyguard Password Verification')  
    mcts.Lock_Bound_Keys_Test('Lock Bound Keys Test')
    mcts.CA_Cert_Notification_Test('CA Cert Notification Test') 
    mcts.CA_Cert_Notification_on_Boot_test('CA Cert Notification on Boot test') 
    mcts.Condition_Provider_test('Condition Provider test')
    mcts.Notification_Listener_Test('Notification Listener Test') 
#     Sensor 8 case 请打开开发者模式，关闭stay awake
    mcts.CTS_Sensor_Batching_Tests('CTS Sensor Batching Tests')  #请打开开发者模式，关闭stay awake
    mcts.CTS_Sensor_Integration_Tests('CTS Sensor Integration Tests') 
    mcts.CTS_Sensor_Test('CTS Sensor Test') 
    mcts.CTS_Single_Sensor_Tests('CTS Single Sensor Tests')
    mcts.Device_Suspend_Tests('Device Suspend Tests')
    mcts.Dynamic_Sensor_Discovery_Test('Dynamic Sensor Discovery Test')  
    mcts.Sensor_Batching_Tests('Sensor Batching Tests')
    mcts.Significant_Motion_Tests('Significant Motion Tests') 

if __name__ == "__main__":
    main()

