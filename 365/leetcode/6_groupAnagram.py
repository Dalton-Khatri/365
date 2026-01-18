class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        group={}        #creating a group
        for word in strs: #seperating every word in list
            temp=[ch for ch in word]
            temp.sort() 
            label=''.join(temp) #sorting the word in ascending order

            if label not in group: #if such word dont belongs to group then creating a new key of the word
                group[label]=[]

            group[label].append(word) #adding the word to the suitable label
        
        return list(group.values()) #returning the values of the key only 
            

        