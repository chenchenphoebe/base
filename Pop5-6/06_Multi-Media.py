# -*- coding: UTF-8 -*-
# *****************************************************************************
# Title:        06_Multi-Media   
# *****************************************************************************
from __future__ import division
import traceback
from uiautomator import Device
import common.common
import common.recorder2
import common.camera
import common.mix
from common.getconfigs import GetConfigs
# from common.navigation_M import Navigation
import common.navigation_L
import common.settings

logger = common.common.createlogger("MAIN")

logger.debug("Connect devices")
mdevice = common.common.connect_device("MDEVICE")
# m_brow = common.browser2.Browser(mdevice, "M_BROW")
m_cam = common.camera.Camera(mdevice, "M_CAM")
m_srec = common.recorder2.Recorder(mdevice, "M_SREC")
m_mp3 = common.mix.Music(mdevice, "M_Music")
m_nav = common.navigation_L.Navigation(mdevice, "M_MAV")
# m_nav = common.navigation_M.Navigation(mdevice, "M_MAV")
m_settings = common.settings.Settings(mdevice, 'M_SETTINGS')

cfg = GetConfigs("06_multi-media")
suc_times = 0
test_times = 0

dicttest_times = cfg.get_test_times()
for test_time in dicttest_times:
    if test_time.upper() in ('VIDEOTIMES', 'PHOTOTIMES', 'RECORDER'):
        test_times = test_times + int(dicttest_times[test_time]) * 3
    else:
        test_times += int(dicttest_times[test_time])
logger.info('Trace Total Times ' + str(test_times))

testplace = cfg.getstr("TestPlace", "TEST_PLACE", "common")


def save_fail_img():
    m_cam.save_img("Multi-Media")


def Recordvideo(key):
    global suc_times
    number = 0
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        logger.debug("Record video 10s " + str(times) + ' Times')
        #         if m_cam.stay_in_camera() and  m_cam.Switch_mode(['Video', '']):
        try:
            for loop in range(times):
                if m_cam.stay_in_camera() and m_cam.record_video(15):
                    suc_times = suc_times + 1
                    number = number + 1
                    logger.info("Trace Success Loop " + str(loop + 1))
                else:
                    save_fail_img()
        except Exception, e:
            save_fail_img()
            common.common.log_traceback(traceback.format_exc())
        logger.debug('Record video Test complete')
        return number


def PlayBackvideo(key):
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        logger.debug("Play Back video " + str(times) + ' Times')
        try:
            for loop in range(times):
                if m_cam.stay_in_camera() and m_cam.play_vedio():
                    suc_times = suc_times + 1
                    logger.info("Trace Success Loop " + str(loop + 1))
                else:
                    save_fail_img()
        except Exception, e:
            save_fail_img()
            common.common.log_traceback(traceback.format_exc())
        logger.debug('Play Back video Test complete')


def Delvideo(times):
    global suc_times
    if times:
        logger.debug("Delete video " + str(times) + ' Times')
        for loop in range(times):
            try:
                if m_cam.stay_in_camera() and m_cam.delete_media_file('Video', ['.3gp', '.mp4']):
                    suc_times = suc_times + 1
                    logger.info("Trace Success Loop " + str(loop + 1))
                else:
                    save_fail_img()
            except Exception, e:
                save_fail_img()
                common.common.log_traceback(traceback.format_exc())
        logger.debug('Delete video Test complete')


def TakePhoto(key):
    global suc_times
    global number
    number = 0
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        logger.debug("Take Photo " + str(times) + " Times")
        #         if m_cam.stay_in_camera() and  m_cam.Switch_mode(['Camera', '']):
        try:
            for loop in range(times):
                if m_cam.stay_in_camera() and m_cam.take_photo():
                    logger.info("Trace Success Loop " + str(loop + 1))
                    suc_times = suc_times + 1
                    number = number + 1
                else:
                    save_fail_img()
        except Exception, e:
            save_fail_img()
            common.common.log_traceback(traceback.format_exc())
        logger.debug('Take Photo Test complete')
        return number


def OpenPhoto(key):
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        logger.debug("Open Photo " + str(times) + " Times")
        for loop in range(times):
            try:
                if m_cam.stay_in_camera() and m_cam.enter_preview('Photo'):
                    logger.info("Trace Success Loop " + str(loop + 1))
                    suc_times = suc_times + 1
                else:
                    logger.warning("Cannot not preview picture")
                    save_fail_img()
            except Exception, e:
                save_fail_img()
                common.common.log_traceback(traceback.format_exc())
                m_cam.stay_in_camera()
        logger.debug('Open Photo Test complete')


def DelPhoto(times):
    global suc_times
    if times:
        logger.debug("Delete Photo " + str(times) + " Times")
        for loop in range(times):
            try:
                if m_cam.stay_in_camera() and m_cam.delete_media_file('Photo', ['.jpg']):
                    suc_times = suc_times + 1
                    logger.info("Trace Success Loop " + str(loop + 1))
                else:
                    save_fail_img()
            except Exception, e:
                save_fail_img()
                common.common.log_traceback(traceback.format_exc())
        logger.debug('Delete Photo Test complete')


def RecordAudio(key):
    global suc_times
    number = 0
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        logger.debug("Record Audio 5s " + str(times) + ' Times')
        for loop in range(times):
            try:
                if m_srec.stay_in_recorder() and m_srec.enter_file_list(False) and m_srec.record_audio(record_time=20):
                    suc_times = suc_times + 1
                    number += 1
                    logger.info("Trace Success Loop " + str(loop + 1))
                else:
                    save_fail_img()
            except Exception, e:
                save_fail_img()
                common.common.log_traceback(traceback.format_exc())
        logger.debug('Record Audio Test complete')
        return number


def PlayBackAudio(key):
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        logger.debug("Play Back Audio " + str(times) + ' Times')
        try:
            for loop in range(times):
                if m_srec.stay_in_recorder() and m_srec.enter_file_list(True) and m_srec.select_audio_play(loop):
                    logger.info("Trace Success Loop " + str(loop + 1))
                    suc_times = suc_times + 1
                else:
                    save_fail_img()
        except Exception, e:
            save_fail_img()
            common.common.log_traceback(traceback.format_exc())
        logger.debug('Play Back Audio Test complete')


def DelAudio(times):
    global suc_times
    if times:
        logger.debug("Delete Audio " + str(times) + ' Times')
        try:
            for loop in range(times):
                if m_srec.stay_in_recorder() and m_srec.enter_file_list(True) and m_srec.delete_audio():
                    suc_times = suc_times + 1
                    logger.info("Trace Success Loop " + str(loop + 1))
                else:
                    save_fail_img()
        except Exception, e:
            save_fail_img()
            common.common.log_traceback(traceback.format_exc())
        logger.debug('Delete Audio Test complete')


def Streaming(key):
    global suc_times
    if testplace == 'US':
        STREAMADDRESS = "http://www.youtube.com/watch?v=MVbeoSPqRs4"
    else:
        STREAMADDRESS = 'rtsp://stream.tcl-ta.com/mp4/mp4/128_96/mp4_128_96_v50_10.mp4'
    # STREAMADDRESS = 'rtsp://60.12.220.48:554/1.3gp'
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        logger.debug("Play Streaming " + str(times) + " Times")
        for loop in range(times):
            try:
                if m_brow.browser_streaming(STREAMADDRESS, waittime=30):
                    logger.info("Trace Success Loop " + str(loop + 1))
                    suc_times = suc_times + 1
                else:
                    save_fail_img()
            except Exception, e:
                save_fail_img()
                common.common.log_traceback(traceback.format_exc())
        m_brow.exit_browser()
        logger.debug('Streamings Test complete')


def OpenClosePlayer(key):
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        logger.debug("Open Close Player " + str(times) + " Times")
        for loop in range(times):
            try:
                if m_mp3.stay_in_music() and m_nav.exit_app():
                    suc_times = suc_times + 1
                    logger.info("Trace Success Loop " + str(loop + 1))
                else:
                    save_fail_img()
            except Exception, e:
                save_fail_img()
                common.common.log_traceback(traceback.format_exc())


def PlayMusic(key):
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        logger.debug("Play music " + str(times) + " Times")
        for loop in range(times):
            logger.debug(loop)
            try:
                if m_mp3.stay_in_music() and m_mp3.play_mp3(loop):
                    mdevice.delay(15)
                    suc_times = suc_times + 1
                    logger.info("Trace Success Loop " + str(loop + 1))
                else:
                    save_fail_img()
            except Exception, e:
                save_fail_img()
                common.common.log_traceback(traceback.format_exc())


def CloseMusicPlayer(key):
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        logger.debug('Close music.')
        for loop in range(times):
            try:
                if m_mp3.stay_in_music() and m_nav.exit_app():
                    suc_times = suc_times + 1
                    logger.info("Trace Success Loop " + str(loop + 1))
                else:
                    save_fail_img()
                    logger.debug("Close music fail ")
            except Exception, e:
                save_fail_img()
                common.common.log_traceback(traceback.format_exc())


def main():

    logger.debug('Start Multi-Media Test')
    mdevice.watcher("ALLOW").when(text='ALLOW').click(text='ALLOW')
    mdevice.watcher("Agree").when(text='AGREE').click(text='AGREE')
    vid_num = Recordvideo('VIDEOTIMES')
    if vid_num:
        PlayBackvideo('VIDEOTIMES')
        Delvideo(vid_num)
 
    pic_num = TakePhoto('PHOTOTIMES')
    if pic_num:
        OpenPhoto('PHOTOTIMES')
        DelPhoto(pic_num)
 
    aud_num = RecordAudio('RECORDER')
    if aud_num:
        PlayBackAudio('RECORDER')
        DelAudio(aud_num)
    OpenClosePlayer('OPENCLOSETIMES')
    PlayMusic('MUSICPLAYTIMES')
    CloseMusicPlayer('CLOSEPLAYER')

    logger.debug("Finished Multi-Media Test")
    logger.info("Success Times: %s." % suc_times)
    Rate = suc_times / test_times * 100
    if Rate < 95:
        logger.warning("Result Fail Success Rate Is " + str(Rate) + '%')
    else:
        logger.info("Result Pass Success Rate Is " + str(Rate) + '%')


if __name__ == "__main__":
    main()
    #  Scrpit End
