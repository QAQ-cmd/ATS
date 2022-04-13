import Deal_xml_message_structure_test002
import time
import inout_shit
import threading
import json

a = Deal_xml_message_structure_test002.xml_cfg()
b = inout_shit.Uart("COM115")


def w_log(whayrt):
    # 把打印的东西存起来
    with open('1234.txt', 'a', encoding='utf8') as df:
        rtyu = str(whayrt) + '\n'
        df.write(rtyu)


def fin_until(untilw, untilt):
    # 把命令单元在xml里面的位置和单元体输入，输出单元的截取字典
    # 查看报文中的命令单元是什么
    untilwk = untilw['命令单元']
    # 调用xml，查看所有的命令单元值的列表
    edc = a.xml_unti_type()
    # print(edc)
    # 查看命令单元的索引值
    if untilwk in edc:
        ygh1 = edc.index(untilwk)
    # 调出命令单元的字典
    cfv = a.xml_unti_value(ygh1)
    # 命令单元的字典的key和值
    untilw1 = cfv.keys()
    untilk1 = cfv.values()
    # 做函数，把切片值做出列表
    untilv2 = []
    var = 0
    for i in untilk1:
        var += int(i)
        untilv2.append(var)
    # print(untilv2)
    # 循环把数据切片取出来
    h1 = 0
    wsdt1 = []
    for i in untilv2:
        wsdt1.append(untilt[h1:i])
        h1 = i
    fgh = dict(zip(untilw1, wsdt1))
    return fgh


def Overall():
    # 整体格式输出,第一层，输出字典
    # 整体的字典去掉Mill
    c = a.xml_structure()
    c.pop('Middle')
    c.pop('校验位')
    # 取出整体的字典
    allk = list(c.keys())
    allv = list(c.values())
    # 做函数
    allv1 = []
    var = 0
    for i in allv:
        var += int(i)
        allv1.append(var)
    # print(var)
    print(allv1)
    while True:
        # 日志时间
        ert23 = time.strftime('当前时间：' + '%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # 开启串口线程
        # b.run()
        # 接受报文数据
        r = b.uart_recv_thread()
        # 循环把数据切片取出来
        h = 0
        wsdt = []
        for i in allv1:
            wsdt.append(r[h:i])
            h = i
        # print(wsdt)
        fgh = dict(zip(allk, wsdt))
        print(json.dumps(fgh, indent=4, ensure_ascii=False))
        w_log(ert23)
        w_log(fgh)
        # 报文时间
        # print(r[48:60])
        # 休息
        time.sleep(0.01)
        mingling_until = r[var:]
        # print(mingling_until)
        edc = fin_until(fgh, mingling_until)
        print(json.dumps(edc, indent=4, ensure_ascii=False))
        w_log(edc)


if __name__ == "__main__":
    threading.Thread(target=Overall(), daemon=True).start()
    threading.Thread.join()
