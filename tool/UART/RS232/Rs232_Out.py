# encoding=utf-8
import serial
import threading
from time import sleep
import file_path
import college_log


def Get_Port():
    """
    从temp文件中获取COM Port
    """
    com_path = file_path.temp_dir() + "COM.txt"
    try:
        with open(com_path, 'r', encoding='utf8') as temp:
            com = temp.readline()
            print(com, end='')
            return com
    except FileNotFoundError:
        college_log.collect_log_mf("打开COM文件错误！")


class Uart(object):
    """
    实例化RS232的串口
    """
    def __init__(self, port):
        self.err = 0
        self.run_status = 0
        try:
            self.uart = serial.Serial(port, 115200)
            self.run_status = 1
            college_log.collect_log_mf("连接成功!")
        except:
            college_log.collect_log_mf("连接RS232错误!")
            print("检查该端口是否被其他程序占用!")
            self.err = -1

    def uart_recv_thread(self):
        print("start uart_recv_thread")
        while True:
            try:
                data = self.uart.readline()
                data = data.decode()
                print(data)
                sleep(0.05)
            except Exception as e:
                print("Error")
                print(e)

    def run(self):
        threading.Thread(target=self.uart_recv_thread, daemon=True).start()

    def close(self):
        print("close uart")
        self.uart.close()

    def uart_send_data(self, data):
        print("pc==>uart: ", data)
        # 加回车换行
        data = data + "\n"
        self.uart.write(data.encode(encoding="ascii"))


if __name__ == "__main__":
    port = Get_Port()
    uart = Uart(port)
    if -1 != uart.err:
        uart.run()
        while True:
            input_data = input("Please input:\r\n")
            if "quit" == input_data:
                uart.close()
                break
            else:
                uart.uart_send_data(input_data + "\n")
            sleep(0.1)
    else:
        print("退出!")

