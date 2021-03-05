
# 二叉树类
class BTree(object):

    # 初始化
    def __init__(self, data=None, left=None, right=None):
        self.data = data    # 数据域
        self.left = left    # 左子树
        self.right = right  # 右子树

    # 前序遍历
    def preorder(self):
        if self.data is not None:
            print(self.data, end=' ')
        if self.left is not None:
            self.left.preorder()
        if self.right is not None:
            self.right.preorder()


    def find_by_data(self, data):
        if self.data is not None:
            if self.data == data:
                return self
        if self.left is not None:
            data_tree = self.left.find_by_data(data)
            if data_tree: return data_tree
        if self.right is not None:
            data_tree =  self.right.find_by_data(data)
            if data_tree: return data_tree
        return None

def print_tree(trees):
    new_trees = []
    for tree in trees:
        try:
            if tree.data:
                print(tree.data, end=" ")
                new_trees.append(tree.left)
                new_trees.append(tree.right)
        except:
            pass
    print("")
    if new_trees:
        print_tree(new_trees)

def make_tree(node_list, trees):
    new_trees = []
    i = 0
    for tree in trees:
        try:
            left_tree = BTree(node_list[i])
            i += 1
            right_tree = BTree(node_list[i])
            i += 1
            tree.left = left_tree
            new_trees.append(tree.left)
            tree.right = right_tree
            new_trees.append(tree.right)
        except:
            return
    node_list = node_list[i:]
    make_tree(node_list, new_trees)




def find_last_none(trees):
    new_trees = []
    for tree in trees:
        if tree.left:
            new_trees.append(tree.left)
        else:
            return tree, "left"
        if tree.right:
            new_trees.append(tree.right)
        else:
            return tree, "right"
    return find_last_none(new_trees)


def add(tree, num):
    father, flag = find_last_none([tree])
    if num >= father.data:
        x = getattr(father, flag)
        print(x)
        exit()
        # = BTree(num)
    else:
        #getattr(father, flag) = BTree(father.data)
        father.data = num
    return


def find_last(trees):
    new_trees = []
    for tree in trees:
        if tree.left:
            tree.left.father = tree
            new_trees.append(tree.left)
        if tree.right:
            tree.right.father = tree
            new_trees.append(tree.right)
    if new_trees:
        return find_last(new_trees)
    else:
        return trees[-1]




def delete(tree, data):
    data_tree = tree.find_by_data(data)
    last_tree = find_last([tree])
    data_tree.data = last_tree.data
    if data_tree.left and data_tree.data > data_tree.left.data:
        tmp = data_tree.left.data
        data_tree.left.data = data_tree.data
        data_tree.data = tmp
    if data_tree.right and data_tree.data > data_tree.right.data:
        tmp = data_tree.right.data
        data_tree.right.data = data_tree.data
        data_tree.data = tmp
    last_tree.father.right = None
    return tree

node_list = [1, 2, 3, 4, 5]
TREE = BTree(node_list[0])
make_tree(node_list[1:], [TREE])
# print_tree([TREE])
tree = TREE

add(tree, 6)
print_tree([tree])

tree = delete(tree, 3)
print_tree([tree])

tree = delete(tree, 2)
print_tree([tree])

add(tree, 2)
print_tree([tree])

'''
1
2 3
4 5 6

1
2 6
4 5

1
4 6
5

1
2 6
5 4
'''