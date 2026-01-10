class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        n=len(nums)  #first we calculated the length of list
        for number in nums:  #loop around the list
            i=0
            while i<n: # while loop from 1st index of list
                if(number+nums[i]==target): #checking if it matches the targert
                    if(nums.index(number)!=i): #checking if it is the same index
                        return[nums.index(number), i] #returning the output
                i+=1




        



        