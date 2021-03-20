>>> a = 'aabbccddeeff'
>>> a_bytes = bytes.fromhex(a)
>>> print(a_bytes)
b'\xaa\xbb\xcc\xdd\xee\xff'
>>> aa = a_bytes.hex()
>>> print(aa)
aabbccddeeff
>>>
————————————————
版权声明：本文为CSDN博主「wowocpp」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/wowocpp/article/details/79701739