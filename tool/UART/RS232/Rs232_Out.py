# encoding=utf-8
import serial
import threading
from time import sleep
import file_path


def Get_Port():
    """
    从temp文件中获取COM Port
    """
    com_path = file_path.temp_dir() + "COM.txt"
    try:
        with open(com_path, 'r', encoding='utf8') as temp:
            com = temp.readline()
            print(com)
    except:
        print("错误！")


class Uart(object):
    def __init__(self, port):
        self.err = 0
        self.run_status = 0
        try:
            self.uart = serial.Serial(port, 115200)
            self.run_status = 1
            print("start uart success")
        except:
            print("start uart error")
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
    # uart = Uart("COM115")
    # if -1 != uart.err:
    #     uart.run()
    # while True:
    #     input_data = input("Please input:\r\n")
    #     if "quit" == input_data:
    #         uart.close()
    #         break
    #     else:
    #         uart.uart_send_data(input_data + "\n")
    #     sleep(0.1)
    # print("exit uart")
    Get_Port()
