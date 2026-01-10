#day_8 of 365 days of coding

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        n=len(nums)
        output = [int]
        for number in nums:
            i=0
            while i<n:
                if(number+nums[i]==target):
                    if(nums.index(number)!=i):
                        return[nums.index(number), i]
                i+=1