import json

raw_00 = input(">")


def Deal_raw_data():
    # 去除前后空格
    raw = raw_00.strip()
    # 第一个字节解析
    head_mes = int(raw[:2], 16)
    print("首字节:", bin(head_mes)[2:])
    # 第一个剩余长度的位置
    head_mes_01 = int(raw[2:4], 16)
    # 第二个剩余长度的位置
    head_mes_02 = int(raw[4:6], 16)
    # 第三个剩余长度的位置
    head_mes_03 = int(raw[6:8], 16)
    if head_mes_01 < 128:
        print("报文长度1:",head_mes_01)
        return raw[4:]
    elif head_mes_02 < 128:
        # 此处128为校验位
        head_mes_02_l = head_mes_01 - 128
        head_mes_02_l = head_mes_02_l + int(raw[4:6], 16)*128
        print("报文长度2:", head_mes_02_l)
        # print(raw[-2*head_mes_02_l:])
        return raw[-2*head_mes_02_l:]
    elif head_mes_03 < 128:
        # 此处128为校验位
        head_mes_03_l = head_mes_02 - 128
        head_mes_03_l = head_mes_03_l + int(raw[6:8], 16)*128
        print("报文长度3:", head_mes_03_l)
        return raw[-2*head_mes_03_l:]
    else:
        # 此处128为校验位
        head_mes_04_l = head_mes_03 - 128
        head_mes_04_l = head_mes_04_l + int(raw[8:10], 16)*128
        print("报文长度4:", head_mes_04_l)
        return raw[-2*head_mes_04_l:]


def Topic_Name():
    b = Deal_raw_data()
    # print(b)
    c = int(b[2:4], 16)
    topic_name_all = b[4:2*c+4]
    # print("主题:", topic_name_all)
    print("主题解析:", ascii_conv(topic_name_all))
    flag = judge_Qos()
    if flag == 1:
        mes = b[2*c+4:]
        # print("负荷:", mes)
        try:
            mes = ascii_conv(mes)
            mes = str(mes)
            print("负荷解析:", mes)
        except:
            print("不是JSON格式或解析错误")
    else:
        dfg = b[2*c+4:]
        # print("负荷:", b[2*c+4:])
        try:
            mes = ascii_conv(dfg)
            mes = str(dfg)
            print("负荷解析2:", dfg)
        except:
            print("不是JSON格式或解析错误")

def judge_Qos():
    # 判断报文带不带报文标识符
    raw = raw_00.strip()
    head_mes = int(raw[:2], 16)
    a = bin(head_mes)[2:]
    a = a[-4:-2]
    if a == "01" or "10":
        return 1


def ascii_conv(tgy):
    ch = tgy
    rfg = ""
    for i in range(1, (len(ch) // 2)+1):
        lh = ch[2 * i - 2:2 * i]
        x = int(lh, 16)
        rfg += chr(x)
    # print(rfg)
    return rfg


if __name__ == "__main__":
	Topic_Name()
