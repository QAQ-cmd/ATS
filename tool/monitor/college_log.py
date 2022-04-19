# 本文件夹的主运行py文件
# 监控脚本的运行
import time

import file_path as fp

now_time_exact = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# log路径
log_path = fp.log_dir() + '\\run_log.txt'
# temp路径
temp_path = fp.temp_dir() + '\\COM.txt'


def collect_log_mf(log):
    print(log)
    with open(log_path, 'a', encoding='utf8') as temp:
        temp.write(now_time_exact)
        temp.write(log)


if __name__ == "__main__":
    collect_log_mf()
