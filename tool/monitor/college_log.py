# 本文件夹的主运行py文件
# 监控脚本的运行
import time

from file_path import log_dir, temp_dir


now_time_exact = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# log路径
log_path = log_dir() + '\\run_log.txt'
# temp路径
temp_path = temp_dir() + '\\COM.txt'


def collect_log_mf(log):
    print(log)
    str(log)
    with open(log_path, 'a', encoding='utf8') as temp:
        temp.write(now_time_exact + '\n')
        temp.write(log + '\n')


if __name__ == "__main__":
    collect_log_mf("11223")
