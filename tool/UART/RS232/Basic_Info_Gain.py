from Rs232_Out import Uart

# 命令定义
base_log_on = "IOT+C1+SD.SER=1,7,1024"
base_log_off = "IOT+C1+SD.SER=0,7,1024"


def base_log_switch():
    # 底层开关
    # 开启串口接收线程
    Uart.uart_recv_thread()
    # 检查底层开关是否打开


def fbt_kernel_app_info():
    # 获取FBT Kernel App info
    # 开启串口
    Uart.uart_recv_thread()


def deal_message():
    # 对原始报文进行处理
    """
    三种形式的输出
    1.原始数据
    2.只显示报文
    3.报文解析
    """
    # 开启串口
    Uart.uart_recv_thread()


if __name__ == "__main__":
    base_log_switch()
    fbt_kernel_app_info()
