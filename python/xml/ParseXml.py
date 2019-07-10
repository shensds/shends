# import xml.etree.ElementTree as ET
import xml.etree.cElementTree as ET


tree = ET.parse("country.xml")    #<xml.etree.ElementTree.ElementTree object at 0x0029FD10>  
print(tree)
root = tree.getroot()
print(root)
print(root.tag, ":", root.attrib)

# 遍历xml文档的第二层
for child in root:
    # 第二层节点的标签名称和属性
    print(child.tag,":", child.attrib) 
    # 遍历xml文档的第三层
    for children in child:
        # 第三层节点的标签名称和属性
        print(children.tag, ":", children.attrib)
        
print(root[0][1].text)

# 过滤出所有neighbor标签
for neighbor in root.iter("neighbor"):
    print(neighbor.tag, ":", neighbor.attrib)
    
    
# 遍历所有的counry标签
for country in root.findall("country"):
    # 查找country标签下的第一个rank标签
    rank = country.find("rank").text
    # 获取country标签的name属性
    name = country.get("name")
    print(name, rank)
    
    
# 将所有的rank值加1,并添加属性updated为yes
for rank in root.iter("rank"):
    new_rank = int(rank.text) + 1
    rank.text = str(new_rank)  # 必须将int转为str
    rank.set("updated", "yes") # 添加属性
# 再终端显示整个xml
ET.dump(root)
# 注意 修改的内容存在内存中 尚未保存到文件中
# 保存修改后的内容
tree.write("output.xml")
    
    
for rank in root.iter("rank"):
    # attrib为属性字典
    # 删除对应的属性updated
    del rank.attrib['updated']  
ET.dump(root)
    
    

#删除子元素remove()
# 删除rank大于50的国家
for country in root.iter("country"):
    rank = int(country.find("rank").text)
    if rank > 50:
        # remove()方法 删除子元素
        root.remove(country)
ET.dump(root)
    
    
    
    
    
#添加子元素

country = root[0]
last_ele = country[len(list(country))-1]
last_ele.tail = '\n\t\t'
# 创建新的元素, tag为test_append
elem1 = ET.Element("test_append")
elem1.text = "elem 1"
country.append(elem1)

# SubElement() 其实内部调用的时append()
elem2 = ET.SubElement(country, "test_subelement")
elem2.text = "elem 2"

# extend()
elem3 = ET.Element("test_extend")
elem3.text = "elem 3"
elem4 = ET.Element("test_extend")
elem4.text = "elem 4"
country.extend([elem3, elem4])

# insert()
elem5 = ET.Element("test_insert")
elem5.text = "elem 5"
country.insert(5, elem5)

ET.dump(country)


#创建XML
import xml.etree.ElementTree as ET
def subElement(root, tag, text):
    ele = ET.SubElement(root, tag)
    ele.text = text
    ele.tail = '\n'

root = ET.Element("note")
to = root.makeelement("to", {})
to.text = "peter"
to.tail = '\n'
root.append(to)

subElement(root, "from", "marry")
subElement(root, "heading", "Reminder")
subElement(root, "body", "Don't forget the meeting!")

tree = ET.ElementTree(root)
tree.write("note.xml", encoding="utf-8", xml_declaration=True)
    
    
#缩进
import xml.etree.ElementTree as ET
from xml.dom import minidom

def subElement(root, tag, text):
    ele = ET.SubElement(root, tag)
    ele.text = text

def saveXML(root, filename, indent="\t", newl="\n", encoding="utf-8"):
    rawText = ET.tostring(root)
    dom = minidom.parseString(rawText)
    with open(filename, 'w') as f:
        dom.writexml(f, "", indent, newl, encoding)


root = ET.Element("note")
to = root.makeelement("to", {})
to.text = "peter"
root.append(to)
subElement(root, "from", "marry")
subElement(root, "heading", "Reminder")
subElement(root, "body", "Don't forget the meeting!")
# 保存xml文件
saveXML(root, "note1.xml")
    
    
    