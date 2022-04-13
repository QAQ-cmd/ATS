import  inout_shit
import time

def jiexi(Message_str):
    str1 = str(Message_str)
    print('0-4:',str1[:4],'5-6:',str1[4:6])
    print("VIN:",str1[6:40])
    print("version:",str1[40:42],"加密方式:",str1[42:44])
    print("数据体长度：",str1[44:48])
    print("校验位：",str1[-2:])
    print("数据体：",str1[48:-2])
    print("解析数据体中...")
    '''整个数据单元'''
    danyuan = str1[4:6]
    '''数据体'''
    shuju = str1[48:-2]
    '''数据体信息类型'''
    shuju02 = shuju[34:]
    if danyuan == "02":
        print("这是一个实时数据上报的数据包...")
        print("数据采集时间：",shuju[:12])
        print("信息流水号：",shuju[12:16])
        print("定位信息：",shuju[16:34])
        print("ODC所有信息：",shuju[34:])
        if shuju02[:2] == "01":
            print("排放控制诊断协议类型：",shuju02[:2])
            print("排放控制报警灯状态：",shuju02[2:4])
            print("排放控制故障码总数：",shuju02[4:6])
            if shuju02[4:6] != "00":
               '''把故障码总数转化为长度'''
               print("故障码不为零有故障")
               zhuanghuan = shuju02[4:6]
               guzhang_num = int(zhuanghuan,16)
               guzhang_num = guzhang_num * 4
               print("排放控制故障码总数：", shuju02[6:6+guzhang_num])
               print("故障码信息列表：",shuju02[2:36])
            else:
                print("没有故障...")
                print("排放故障诊断信息：",shuju02[8:10])
                print("车速:",shuju02[10:14])
                print("大气压力:",shuju02[14:16])
                print("净扭矩:",shuju02[16:18])
                print("摩擦扭矩:",shuju02[18:20])
                print("发动机转速：",shuju02[20:24])
                print("发动机燃料流量：",shuju02[24:28])
                print("SCR上游氮氧：",shuju02[28:32])
                print("SCR上游氮氧：",shuju02[32:36])
                print("反应剂余量：",shuju02[36:38])
                print("进气量：",shuju02[38:42])
                print("发动机冷却液温度：",shuju02[42:44])
                print("油箱液位：",shuju02[44:46])
                kuzhan = shuju02[46:]
                print("扩展数据流：",kuzhan[:2])
                print("累积里程：",kuzhan[2:10])
                print("颗粒物浓度：",kuzhan[10:14])
                print("光吸收系数：",kuzhan[14:18])
                print("DPF压差：",kuzhan[18:22])
                print("DOC进气温度：",kuzhan[22:26])
                print("ODC出气温度：",kuzhan[26:30])
                '''终端状态信息：'''
                z_tai = kuzhan[30:]
                print("终端状态信息：",z_tai[:2])
                print("终端状态信息体：",z_tai[2:])
                # print("\n",z_tai[2:14],"\n",z_tai[14:26],"\n",z_tai[26:32],"\n",z_tai[32:52],"\n",z_tai[52:58],"\n",z_tai[58:74],"\n",z_tai[74:90],"\n",z_tai[90:104],"\n",z_tai[104:110],"\n",z_tai[110:])
        else:
            print("数据体错误...\n请检查...")
    if danyuan == "01":
        print("这是一个登陆的数据包。")
    if danyuan == "06":
        print("这是一个终端校时的数据包。")





'''
vart = inout_shit.Uart("COM115")

if -1 != vart.err:
    vart.run()
    a = vart.run()
    jiexi(a)
while True:
    time.sleep(5)

'''
	
	
	
	
	
	
	
	
	