class Solution:
    def isValid(self, s: str) -> bool:
        stack=[] #created a stack to save and pop out
        for bra in s:
            if bra in "{[(": 
                stack.append(bra) #storing the open braces
            elif bra in "}])":
                if not stack: 
                    return False
                #checking if right bracket is closed
                elif bra=="}" and stack[-1]=="{": 
                    stack.pop()
                elif bra=="]" and stack[-1]=="[":
                    stack.pop()
                elif bra==")" and stack[-1]=="(":
                    stack.pop()
                else:
                    return False
        
        if not stack:  #at last if all stack is empty then this is valid
            return True

        return False