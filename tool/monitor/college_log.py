# 本文件夹的主运行py文件
# 监控脚本的运行
import time
import os

from file_path import log_dir, temp_dir

now_time_exact = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# log路径
log_path = log_dir() + 'run_log.txt'
# temp路径
temp_path = temp_dir() + 'COM.txt'


def collect_log_mf(*log):
    """
    传入未定参数，出来是个元组，用for循环搞他
    """
    temp_b = ''
    for i in log:
        str(i)
        temp_b += i
    print(temp_b)
    with open(log_path, 'a', encoding='utf8') as temp:
        temp.write(now_time_exact + '\n')
        temp.write(temp_b)
        temp.write('\n')


def clean_log():
    """
    删除两个log
    一个run_log 初始化时删除
    一个COM 删不删无所谓吧?..
    """
    os.remove(log_path)


if __name__ == "__main__":
    collect_log_mf("11223")
# else:
#     clean_log()
