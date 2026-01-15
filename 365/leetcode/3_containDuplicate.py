class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        for n in nums:
            for i in range(len(nums)):
                if(n==nums[i]):
                    if(nums.index(n)!=i):
                        return True
        return False