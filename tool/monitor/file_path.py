import os

"""
定义文件的路径
1.配置文件的位置                               √
2.日志文件的位置和生成
3.日志文件的建立和删除
从当前路径的str从后到前获取ATS的目录的绝对路径     √
稍后重构为类
"""


def src_dir():
    return os.path.dirname(os.path.realpath(__file__))


def find_ATS_file():
    # 查找ATS文件夹的绝对路径
    src = src_dir()
    src = src.split('\\')
    temp = ''
    for i in src:
        a = str(i) + '\\'
        a = temp + a
        temp = a
        if i == 'ATS':
            return a


def tool_dir():
    # tool目录
    return os.path.dirname(src_dir())


def temp_dir():
    # 运行时产生的temp文件
    temp_path = find_ATS_file() + 'UUT\\temp\\'
    if os.path.exists(temp_path):
        pass
    else:
        print("正在创建temp文件夹")
        os.mkdir(temp_path)
    return temp_path


def log_dir():
    # 运行时产生的日志文件
    log_dir_mf = find_ATS_file() + 'UUT\\log\\'
    if os.path.exists(log_dir_mf):
        pass
    else:
        print("正在创建log文件夹")
        os.mkdir(log_dir_mf)
    return log_dir_mf


# if __name__ == '__main__':
#     b = find_ATS_file()
#     c = tool_dir()
#     d = temp_dir()
#     e = log_dir()
#     print(" ATS文件位置：" + b + '\n', "tool文件夹位置：" + c + '\n', "temp文件夹位置：" + d + '\n', "log文件夹位置：" + e + '\n')
