# *****************************************************************************
# Title:        10_Filemanager
# *****************************************************************************
from __future__ import division
import traceback
import common.common
from uiautomator import Device

from common.getconfigs import GetConfigs
import common.filemanager
import common.navigation_M

logger = common.common.createlogger("MAIN")

logger.debug("Connect devices")
mdevice = common.common.connect_device("MDEVICE")
m_filemanager = common.filemanager.Filemanager(mdevice, "M_FILEMANAGER")
m_nav = common.navigation_M.Navigation(mdevice, "M_MAV")

# internal_storage_name = 'PHONE'
# internal_storage_name = 'Phone storage'
internal_storage_name = 'Internal storage'

logger.debug("Get some configurations")
cfg = GetConfigs("10_filemanager")
dicttest_times = cfg.get_test_times()
test_times = 0
suc_times = 0
for TestTime in dicttest_times: test_times += int(dicttest_times[TestTime])
logger.info("Trace Total Times " + str(test_times))


def OpenCloseFilemanager(key):
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        logger.debug("Open Close Filemanager Time " + str(times))
        for loop in range(times):
            try:
                if m_filemanager.stay_in_filemanger() and m_nav.exit_app(1):
                    suc_times = suc_times + 1
                    logger.info("Trace Success Loop " + str(loop + 1))
                else:
                    m_filemanager.save_fail_img()
            except Exception, e:
                m_filemanager.save_fail_img()
                common.common.log_traceback(traceback.format_exc())


def AddAndDelFolder(key):
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        logger.debug("Open and Delete a folder %s Times." % times)
        for loop in range(times):
            try:
                folder_name = 'Folder_' + m_filemanager.random_number(5)
                logger.debug("Test Open and Delete folder " + folder_name)
                if m_filemanager.stay_in_filemanger() and m_filemanager.open_path(internal_storage_name) \
                        and m_filemanager.add_folder(folder_name) and m_filemanager.delete_item(folder_name):
                    suc_times += 1
                    logger.info("Trace Success Loop " + str(loop + 1))
                else:
                    m_filemanager.save_fail_img()
            except Exception, e:
                m_filemanager.save_fail_img()
        logger.debug("Open and Delete a folde Test Complete")


def OpenFile(key, path, type):
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        logger.debug("Open %s file %s Times." % (type, times))
        for loop in range(times):
            try:
                logger.debug("Test Open " + type + 'time ' + str(loop + 1))
                if m_filemanager.stay_in_filemanger() and m_filemanager.open_path(path) \
                        and m_filemanager.open_file(type) and m_filemanager.back_folder(path):
                    suc_times += 1
                    logger.info("Trace Success Loop " + str(loop + 1))
                else:
                    m_filemanager.save_fail_img()
            except Exception, e:
                m_filemanager.save_fail_img()

            if mdevice(resourceId='com.google.android.apps.plus:id/videoplayer').exists \
                    or mdevice(resourceId='com.tct.gallery3d:id/surface_view').exists:
                m_filemanager.back_folder(path)
        logger.debug("Open %s Test Complete", type)


def CopyFile(key, path_from, path_to, file_name=''):
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        logger.debug("Copy file %s Times." % times)
        for loop in range(times):
            try:
                logger.debug("Test copy file time " + str(loop + 1))
                if m_filemanager.stay_in_filemanger() and m_filemanager.copy_file(path_from, path_to, file_name):
                    suc_times += 1
                    logger.info("Trace Success Loop " + str(loop + 1))
                else:
                    m_filemanager.save_fail_img()
            except Exception, e:
                m_filemanager.save_fail_img()
        logger.debug("Open and Delete a folde Test Complete")


def main():

    logger.debug("Start Filemanager Test")

    m_filemanager.remove_all_file('*.png')

    OpenCloseFilemanager('Open')
    AddAndDelFolder('AddAndDelFolder')
    OpenFile('OpenPicture', internal_storage_name + '/Pictures', 'Picture')
    OpenFile('PlayMusic', internal_storage_name + '/Music', 'Music')
    OpenFile('PlayVideo', internal_storage_name + '/Movies', 'Video')
    CopyFile('CopyFile', internal_storage_name + '/Pictures', internal_storage_name)

    logger.debug("Finished Filemanager Test")
    logger.info("Success Times: %s." % suc_times)
    Rate = suc_times / test_times * 100
    if Rate < 95:
        logger.warning("Result Fail Success Rate Is " + str(Rate) + '%')
    else:
        logger.info("Result Pass Success Rate Is " + str(Rate) + '%')


if __name__ == "__main__":
    main()
    #  Scrpit End
