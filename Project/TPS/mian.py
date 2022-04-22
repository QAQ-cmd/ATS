"""
这是启动的主脚本
目录架构：
TPS 测试集 随便搞
tool 向TPS中的脚本提供python环境，can，usb，uart的接口实例化
UUT 测试过程中生成的日志和temp文件
    逻辑步骤:
        1.初始化,清空上次的run_log
        2.第一层的选项
        3.第二层的选项
"""
import college_log
import All_Port


def first_click_me():
    """
    初始化,
    """
    college_log.clean_log()
    college_log.collect_log_mf("初始化完成")
    college_log.collect_log_mf("开始配置串口")
    All_Port.set_serial_flag()
    college_log.collect_log_mf("配置串口成功")
    display_one()


def display_one():
    """
    显示界面之类的
    """
    college_log.collect_log_mf("welcome")
    print("选择功能:")
    print("1.获取基本信息  2.更换端口     3.测试 \n\r4.报文解析      5.底包升级    6.退出")
    function_one = input(">")
    function_one = int(function_one)
    if function_one in range(7):
        college_log.collect_log_mf("选择功能:"+str(function_one))
    else:
        college_log.collect_log_mf("错误,超出范围")


if __name__ == '__main__':
    first_click_me()