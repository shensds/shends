'''
https://leetcode-cn.com/problems/minimum-swaps-to-make-sequences-increasing/
https://leetcode-cn.com/problems/merge-k-sorted-lists/
https://leetcode-cn.com/problems/partition-to-k-equal-sum-subsets/
'''
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


https://leetcode-cn.com/problems/minimum-size-subarray-sum/
https://leetcode-cn.com/problems/longest-substring-without-repeating-characters
https://leetcode-cn.com/problems/count-number-of-nice-subarrays/
https://leetcode-cn.com/problems/decode-ways/
https://leetcode-cn.com/problems/fruit-into-baskets/
https://leetcode-cn.com/problems/find-all-anagrams-in-a-string/solution/python-hua-dong-chuang-kou-438-zhao-dao-zi-fu-chua/
https://leetcode-cn.com/problems/binary-subarrays-with-sum/
https://leetcode-cn.com/problems/reconstruct-itinerary/

