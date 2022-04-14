"""
1.判断串口在不在                       √
2.返回值,写入临时文件                   √
3.如有多个选择串口，则选择串口            √
4.可以根据大频口判断终端是否进入了休眠，以及流水号命令查询IOT+S1+G17691.F1.PI.LOG.S=?是否进入休眠
"""
import serial.tools.list_ports
# 运行的位置不同相对路径不同
com_flag_path = 'UUT\\temp\\COM.txt'


def find_serial():
    port_list = list(serial.tools.list_ports.comports())
    port_list_name = []
    if len(port_list) <= 0:
        print("没有找到任何设备！")
    else:
        for each_port in port_list:
            tpe01 = str(each_port)
            if 'Serial' in tpe01:
                print(each_port)
                # each_port[0]很奇怪
                port_list_name.append(each_port[0])

    if len(port_list_name) == 0:
        print("没有找到串口")
        return 0
    '''
    else:
        print("串口列表：", port_list_name)
    '''
    return port_list_name


def set_serial_flag():
    a = find_serial()
    if len(a) != 0:
        i = input("从上面选择串口（按上下顺序输入序号即可）：")
        i = int(i) - 1
        if i < 0:
            print("错误：超出范围了，请重新输入")
            set_serial_flag()
        try:
            print("你选择了", a[i], "端口，正写入临时文件中...")
            with open(com_flag_path, 'w', encoding='utf8') as temp:
                temp.write(a[i])
        except IndexError as out_range:
            print("错误：超出范围了，请重新输入")
            set_serial_flag()
    if a == 0:
        print("检查USB是否接好，因为即使串口9针的另一端没有接t-box在PC机也是可以识别的")


if __name__ == '__main__':
    print("开始配置串口")
    set_serial_flag()
    print("配置串口成功")
