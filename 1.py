from typing import List

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
        
def make_list_node(node_list):
    
    head = ListNode(node_list[0])
    n = head
    for i in node_list[1:]:
        node = ListNode(i)
        n.next = node
        n = n.next
    return head

def print_next(node):
    lists = []
    x = node
    lists.append(x.val)
    while x.next:
        x = x.next
        lists.append(x.val)
    return(lists)



class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        import heapq
        dummy = ListNode(0)
        p = dummy
        head = []
        for i in range(len(lists)):
            if lists[i] :
                heapq.heappush(head, (lists[i].val, i))
                lists[i] = lists[i].next
        while head:
            val, idx = heapq.heappop(head)
            p.next = ListNode(val)
            p = p.next
            if lists[idx]:
                heapq.heappush(head, (lists[idx].val, idx))
                lists[idx] = lists[idx].next
        return dummy.next
        
        
a = Solution()

node_list = [[1,4,5],[1,3,4],[2,6]]
lists = []
for i in node_list:
    node = make_list_node(i)
    lists.append(node)
    
x = a.mergeKLists(lists)
print(print_next(x))
