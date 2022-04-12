import serial.tools.list_ports
"""
1.判断串口在不在
2.返回值,写入临时文件
3.如有多个选择串口，则选择串口
4.
"""


port_list = list(serial.tools.list_ports.comports())
port_list_name = []
if len(port_list) <= 0:
    print("The Serial port can't find!")
else:
    for each_port in port_list:
        print(each_port)
        # port_list_name.append(each_port[0])

# if __name__ == '__main__':
#     print(port_list_name)
