#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import threading
import time
from ctypes import *
import operator

# Timing0, Timing1 CAN波特率
"""
CAN波特率      Timing0(BTR0)   Timing1(BTR1)
10 Kbps       0x31            0x1C
20 Kbps       0x18            0x1C
40 Kbps       0x87            0xFF
50 Kbps       0x09            0x1C
80 Kbps       0x83            0xFF
100 Kbps      0x04            0x1C
125 Kbps      0x03            0x1C
200 Kbps      0x81            0xFA
250 Kbps      0x01            0x1C
400 Kbps      0x80            0xFA
500 Kbps      0x00            0x1C
666 Kbps      0x80            0xB6
800 Kbps      0x00            0x16
1000 Kbps     0x00            0x14
33.33 Kbps    0x09            0x6F
66.66 Kbps    0x04            0x6F
83.33 Kbps    0x03            0x6F
"""

# 过滤验收码
ACC_CODE = 0x00000000

# 过滤屏蔽码
ACC_MASK = 0xFFFFFFFF

# 保留字段
RESERVED = 0

# 滤波模式 0/1=接收所有类型
FILTER = 1

# 波特率 T0
TIMING_0 = 0x00

# 波特率 T1
TIMING_1 = 0x1c

# 工作模式 0=正常工作
MODE = 0

# CAN卡类别为 USBCAN-2A, USBCAN-2C, CANalyst-II
VCI_USB_CAN_2 = 4

# CAN卡下标索引
DEV_INDEX = 0

# 通道下标索引1
CAN_INDEX_1 = 0

# 通道下标索引2
CAN_INDEX_2 = 1

# 操作成功编码 1=操作成功 0=操作失败 -1=USB-CAN设备不存在或USB掉线
STATUS_OK = 1

# 是否开启打印
PRINT_FLAG = True

# 依赖的DLL文件(存放在根目录下)
CAN_DLL_PATH = './ControlCAN.dll'

# 读取DLL文件
Can_DLL = windll.LoadLibrary(CAN_DLL_PATH)

# 发送帧ID
TRANSMIT_ID = 0x1

# 接收帧ID
RECEIVE_ID = 0x0

# 时间标识
TIME_STAMP = 0

# 是否使用时间标识
TIME_FLAG = 0

# 发送帧类型
TRANSMIT_SEND_TYPE = 1

# 接收帧类型
RECEIVE_SEND_TYPE = 0

# 是否是远程帧
REMOTE_FLAG = 0

# 是否是扩展帧
EXTERN_FLAG = 0

# 数据长度DLC
DATA_LEN = 8

# 用来接收的帧结构体数组的长度, 适配器中为每个通道设置了2000帧左右的接收缓存区
RECEIVE_LEN = 2000

# 接收保留字段
WAIT_TIME = 0

# 要发送的参数
TRANSMIT_DATA = 5

# 要发送的帧结构体数组的长度(发送的帧数量), 最大为1000, 建议设为1, 每次发送单帧, 以提高发送效率
TRANSMIT_LEN = 1


# 通道初始化参数结构
# AccCode:  过滤验收码
# AccMask:  过滤屏蔽码
# Reserved: 保留字段
# Filter:   滤波模式 0/1=接收所有类型 2=只接收标准帧 3=只接收扩展帧
# Timing0:  波特率 T0
# Timing1:  波特率 T1
# Mode:     工作模式 0=正常工作 1=仅监听模式 2=自发自收测试模式
class VCI_CAN_INIT_CONFIG(Structure):
    _fields_ = [
        ("AccCode", c_uint),
        ("AccMask", c_uint),
        ("Reserved", c_uint),
        ("Filter", c_ubyte),
        ("Timing0", c_ubyte),
        ("Timing1", c_ubyte),
        ("Mode", c_ubyte)
    ]


# CAN帧结构体
# ID:         帧ID, 32位变量, 数据格式为靠右对齐
# TimeStamp:  设备接收到某一帧的时间标识, 时间标示从CAN卡上电开始计时, 计时单位为0.1ms
# TimeFlag:   是否使用时间标识, 为1时TimeStamp有效, TimeFlag和TimeStamp只在此帧为接收帧时才有意义
# SendType:   发送帧类型 0=正常发送(发送失败会自动重发, 重发时间为4秒, 4秒内没有发出则取消) 1=单次发送(只发送一次, 发送失败不会自动重发, 总线只产生一帧数据)[二次开发, 建议1, 提高发送的响应速度]
# RemoteFlag: 是否是远程帧 0=数据帧 1=远程帧(数据段空)
# ExternFlag: 是否是扩展帧 0=标准帧(11位ID) 1=扩展帧(29位ID)
# DataLen:    数据长度DLC(<=8), 即CAN帧Data有几个字节, 约束了后面Data[8]中的有效字节
# Data:       CAN帧的数据, 由于CAN规定了最大是8个字节, 所以这里预留了8个字节的空间, 受DataLen约束, 如DataLen定义为3, 即Data[0]、Data[1]、Data[2]是有效的
# Reserved:   保留字段
class VCI_CAN_OBJ(Structure):
    _fields_ = [
        ("ID", c_uint),
        ("TimeStamp", c_uint),
        ("TimeFlag", c_ubyte),
        ("SendType", c_ubyte),
        ("RemoteFlag", c_ubyte),
        ("ExternFlag", c_ubyte),
        ("DataLen", c_ubyte),
        ("Data", c_ubyte * 8),
        ("Reserved", c_ubyte * 3)
    ]


# 打开设备, 一个设备只能打开一次
# return: 1=OK 0=ERROR
def connect():
    # VCI_USB_CAN_2: 设备类型
    # DEV_INDEX:     设备索引
    # RESERVED:      保留参数
    ret = Can_DLL.VCI_OpenDevice(VCI_USB_CAN_2, DEV_INDEX, RESERVED)
    if ret == STATUS_OK:
        print('VCI_OpenDevice: 设备开启成功')
    else:
        print('VCI_OpenDevice: 设备开启失败')
    return ret


# 初始化通道
# return: 1=OK 0=ERROR
def init(can_index):
    # 参数结构参考103行
    init_config = VCI_CAN_INIT_CONFIG(ACC_CODE, ACC_MASK, RESERVED, FILTER, TIMING_0, TIMING_1, MODE)
    # VCI_USB_CAN_2: 设备类型
    # DEV_INDEX:     设备索引
    # can_index:     CAN通道索引
    # init_config:   请求参数体
    ret = Can_DLL.VCI_InitCAN(VCI_USB_CAN_2, DEV_INDEX, can_index, byref(init_config))
    if ret == STATUS_OK:
        print('VCI_InitCAN: 通道 ' + str(can_index + 1) + ' 初始化成功')
    else:
        print('VCI_InitCAN: 通道 ' + str(can_index + 1) + ' 初始化失败')
    return ret


# 打开通道
# return: 1=OK 0=ERROR
def start(can_index):
    # VCI_USB_CAN_2: 设备类型
    # DEV_INDEX:     设备索引
    # can_index:     CAN通道索引
    ret = Can_DLL.VCI_StartCAN(VCI_USB_CAN_2, DEV_INDEX, can_index)
    if ret == STATUS_OK:
        print('VCI_StartCAN: 通道 ' + str(can_index + 1) + ' 打开成功')
    else:
        print('VCI_StartCAN: 通道 ' + str(can_index + 1) + ' 打开失败')
    return ret


# 发送数据
# return: 1=OK 0=ERROR
def transmit(can_index):
    ubyte_array_8 = c_ubyte * 8
    DATA = ubyte_array_8(TRANSMIT_DATA, TRANSMIT_DATA, TRANSMIT_DATA, TRANSMIT_DATA, TRANSMIT_DATA, TRANSMIT_DATA,
                         TRANSMIT_DATA, TRANSMIT_DATA)
    ubyte_array_3 = c_ubyte * 3
    RESERVED_3 = ubyte_array_3(RESERVED, RESERVED, RESERVED)
    # 参数结构参考122行
    can_obj = VCI_CAN_OBJ(TRANSMIT_ID, TIME_STAMP, TIME_FLAG, TRANSMIT_SEND_TYPE, REMOTE_FLAG, EXTERN_FLAG, DATA_LEN,
                          DATA, RESERVED_3)
    # VCI_USB_CAN_2: 设备类型
    # DEV_INDEX:     设备索引
    # can_index:     CAN通道索引
    # can_obj:       请求参数体
    # TRANSMIT_LEN:  发送的帧数量
    ret = Can_DLL.VCI_Transmit(VCI_USB_CAN_2, DEV_INDEX, can_index, byref(can_obj), TRANSMIT_LEN)
    if ret == STATUS_OK:
        print('VCI_Transmit: 通道 ' + str(can_index + 1) + ' 发送数据成功 ')
    else:
        print('VCI_Transmit: 通道 ' + str(can_index + 1) + ' 发送数据失败')


# 开线程
def cl_re(can_index):
    ubyte_array_8 = c_ubyte * 8
    DATA = ubyte_array_8(RESERVED, RESERVED, RESERVED, RESERVED, RESERVED, RESERVED, RESERVED, RESERVED)
    ubyte_array_3 = c_ubyte * 3
    RESERVED_3 = ubyte_array_3(RESERVED, RESERVED, RESERVED)
    # 参数结构
    can_obj = VCI_CAN_OBJ(RECEIVE_ID, TIME_STAMP, TIME_FLAG, RECEIVE_SEND_TYPE, REMOTE_FLAG, EXTERN_FLAG, DATA_LEN,
                          DATA, RESERVED_3)
    while True:
        ret = Can_DLL.VCI_Receive(VCI_USB_CAN_2, DEV_INDEX, can_index, byref(can_obj), RECEIVE_LEN, WAIT_TIME)
        print('VCI_Receive: 通道 ' + str(can_index + 1))
        # print('DataLen: ', can_obj.DataLen)
        drf = list(can_obj.Data)
        for i in range(8):
            # print('Data: ' + hex(i))
            drf[i] = hex(drf[i])
        print('ID:%x' % can_obj.ID, end='')
        print(drf)
        time.sleep(0.1)
        rty = [1, 3]
        if operator.eq(rty, drf):
            print(drf)
            drf


# 接收数据
# return: 1=OK 0=ERROR
def receive(can_index):
    ubyte_array_8 = c_ubyte * 8
    DATA = ubyte_array_8(RESERVED, RESERVED, RESERVED, RESERVED, RESERVED, RESERVED, RESERVED, RESERVED)
    ubyte_array_3 = c_ubyte * 3
    RESERVED_3 = ubyte_array_3(RESERVED, RESERVED, RESERVED)
    # 参数结构参考122行
    can_obj = VCI_CAN_OBJ(RECEIVE_ID, TIME_STAMP, TIME_FLAG, RECEIVE_SEND_TYPE, REMOTE_FLAG, EXTERN_FLAG, DATA_LEN,
                          DATA, RESERVED_3)
    # VCI_USB_CAN_2: 设备类型
    # DEV_INDEX:     设备索引
    # can_index:     CAN通道索引
    # can_obj:       请求参数体
    # RECEIVE_LEN:   用来接收帧结构体数组的长度
    # WAIT_TIME:     保留参数
    ret = Can_DLL.VCI_Receive(VCI_USB_CAN_2, DEV_INDEX, can_index, byref(can_obj), RECEIVE_LEN, WAIT_TIME)
    while ret != STATUS_OK:
        print('VCI_Receive: 通道 ' + str(can_index + 1) + ' 接收数据失败, 正在重试')
        ret = Can_DLL.VCI_Receive(VCI_USB_CAN_2, DEV_INDEX, can_index, byref(can_obj), RECEIVE_LEN, WAIT_TIME)
    else:
        print('VCI_Receive: 通道 ' + str(can_index + 1) + ' 接收数据成功')
        threading.Thread(target=cl_re(can_index), daemon=True).start()


if __name__ == '__main__':
    connect()
    # 初始化CAN1
    init(CAN_INDEX_1)
    # 启动CAN1
    start(CAN_INDEX_1)
    # 初始化CAN2
    init(CAN_INDEX_2)
    # 启动CAN2
    start(CAN_INDEX_2)
    # CAN1发送数据
    # transmit(CAN_INDEX_1)
    # CAN2接收数据
    receive(CAN_INDEX_2)
    # threading.Thread(target=receive(CAN_INDEX_2), daemon=True).start()
    threading.Thread().join()
