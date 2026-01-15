class Solution:
    def isAnagram(self, s: str, t: str) -> bool:

        #changed the string to list
        s_list=[ch for ch in s] 
        t_list=[ch for ch in t] 

        #sorted in ascending order
        s_list.sort() 
        t_list.sort()

        return s_list==t_list #returned after comparing
