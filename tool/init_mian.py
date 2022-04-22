"""
一、设置初始化状态
    1.日志和文件夹重新开启建立和时间归零,pyc文件必要时也要清空
    2.serial port、can 、usb 不变
    3.原先的链路、休眠和can配置恢复测试前
"""
import college_log


def init_file():
    """
    初始化文件系统
    """
    # 清除run_log日志
    college_log.clean_log()
    college_log.collect_log_mf("文件初始化成功")
