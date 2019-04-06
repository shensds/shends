import chardet
import string
import os
path = os.path.realpath(__file__)
with open(path, 'rb') as f:
    data = f.read()
    f_charInfo=chardet.detect(data)
    print (f_charInfo)


#输出：{'encoding': 'GB2312', 'language': 'Chinese', 'confidence': 0.99}