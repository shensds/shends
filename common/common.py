import os
def get_file_list(path):
    file_list = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            file = (os.path.join(root, name))
            file_list.append(file)