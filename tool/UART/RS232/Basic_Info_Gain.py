from Rs232_Out import Uart

# 命令定义
base_log_on = "IOT+C1+SD.SER=1,7,1024"
base_log_off = "IOT+C1+SD.SER=0,7,1024"


class Rs232_Info_Gain:
    open_RS232 = Uart.uart_recv_thread()
    close_RS232 = Uart.close()

    def base_log_switch(self):
        # 底层开关
        # 检查底层开关是否打开，判断依据是底层IOT指令的首位为不为0
        while True:
            data_12 = self.open_RS232
            data_oline = self.qv(data_12)
            print(data_oline)
            # self.close_RS232

    def fbt_kernel_app_info(self):
        """
        获取FBT Kernel App info
        开启串口
        """

    def qv(self):
        data1 = self.open_RS232
        data1 = str(data1)
        if len(data1) > 20:
            # print(data1.split()[0])
            shit01 = data1.split()[0]
            if shit01 == "b'E/socklk":
                # print(data1.split()[2])
                if data1.split()[2] != "prop":
                    return data1.split()[2]

    # def deal_message(self):
        """
        对原始报文进行处理
        三种形式的输出
        1.原始数据
        2.只显示报文
        3.报文解析
        """
        print("ok")


if __name__ == "__main__":
    Rs232_Info_Gain.base_log_switch()
