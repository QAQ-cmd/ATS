import xml.dom.minidom
from xml.dom.minidom import parse

class xml_cfg ():
    def __init__(self):
        DOMTree = xml.dom.minidom.parse("../Gb6_message_FeiDao.xml")
        # 把整个文件元素赋值给.Data，载入了根标签
        self.Data = DOMTree.documentElement
        self.unit = DOMTree.getElementsByTagName("Middle")
        self.cmd  = DOMTree.getElementsByTagName("Command_unit")
        self.Oute = DOMTree.getElementsByTagName("Outer")
        self.Tree = DOMTree

    def xml_unti_type (self):
        # 算下有多少个命令单元类型
        # 实例化
        a = self.Data
        b = self.cmd
        # 根的属性
        # if a.hasAttribute("type"):
            # print("Root element : %s" % a.getAttribute("type"))
        # 在整个文件中获得所有标签名字是Command_unit下的元素和属性,是个list
        # Datas = a.getElementsByTagName("Command_unit")
        # 把标签Command_unit其属性number列入list
        xml_tag_list = []
        for i in b:
            if i.hasAttribute("number"):
                # print("Tag: %s" % i.getAttribute("number"))
                xml_tag_list.append(i.getAttribute("number"))
        # print(xml_tag_list)
        return xml_tag_list

    def xml_structure (self):
        # 计算返回整体报文结构字典
        aa = deal_nodelist(self.Oute[0].childNodes)
        cc = self.Data
        # 取出对应标签的文本
        bb = []
        ee = {}
        for i in aa:
            # print(cc.getElementsByTagName(i)[0].childNodes[0].data)
            bb.append(cc.getElementsByTagName(i)[0].childNodes[0].data)
        ee = dict(zip(aa,bb))
        return ee

    def xml_structure_unti (self):
        # 计算返回各个命令单元的报文结构字典
        a = self.Data
        b = self.cmd
        # print(b)
        c = len(b)
        # 单元节点的获取
        list2 = []
        for i in range(c):
            list2.append(deal_nodelist(b[i].childNodes))
        return list2

    def xml_unti_value (self,wae):
        # 计算输出不同命令单元号的标签对应的值为list
        c = self.xml_structure_unti()[wae]
        d = self.Data
        f = self.xml_unti_type()[wae]
        # 取标签中的值
        # print("命令单元：",f)
        ed = []
        for i in c:
            # print(d.getElementsByTagName(i)[0].childNodes[0].data)
            ed.append(d.getElementsByTagName(i)[0].childNodes[0].data)
        ed1 = dict(zip(c,ed))
        return ed1


def deal_nodelist(nodelist):
    # 对输入的节点的标签列表进行str处理，输出标签列表
    Message_Str_List_Bef = []
    Message_Str_List_Aft = []
    for i in nodelist:
        i = str(i)
        Message_Str_List_Bef.append(i)
    # print(Message_Str_List_Bef)
    for i in Message_Str_List_Bef:
        if i.rfind("Element:") != -1:
            # print(i.split()[2:3])
            Message_Str_List_Aft.append(i.split()[2:3][0])
    # print(Message_Str_List_Aft)
    return Message_Str_List_Aft


if __name__ == "__main__":
    a = xml_cfg()
    print(a.xml_unti_type())
    a.xml_structure()
    print(a.xml_structure())
    a.xml_structure_unti()
    print(a.xml_structure_unti())
    # a.xml_unti_value(3)
    print(a.xml_unti_value(5))
    # b = len(a.xml_unti_type())
    # for j in  range(b):
    #     print(a.xml_unti_value(j))





