<<<<<<< HEAD
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
=======
https://leetcode-cn.com/problems/minimum-swaps-to-make-sequences-increasing/
https://leetcode-cn.com/problems/merge-k-sorted-lists/
https://leetcode-cn.com/problems/partition-to-k-equal-sum-subsets/

class Solution:

    def get_ok_list(self):
        pass

    def di(self, nums, average):
        if len(nums) == 0: return True
        if nums[0] > average:return False
        if nums[0] == average:
            return self.di(nums[1:], average)
        for i in range(nums[1:])
            if nums


    def canPartitionKSubsets(self, nums, k):
        asum = sum(nums)
        if asum%k !=0:
            return False
        average = asum//k
        self.di(nums, average)

a = Solution()
print(a.canPartitionKSubsets([4,3,2,3,5,2,1], 4))


>>>>>>> fe53b725ef925b8f1937fdfba9e4db97ef1b9bf6
