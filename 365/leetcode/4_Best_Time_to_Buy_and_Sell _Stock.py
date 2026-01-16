class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_price=float('inf') #initialize to infinity
        max_price=0 

        for price in prices:
            if price<min_price: 
                min_price=price 
            else:
                max_price=max(max_price, price-min_price) #for finding the max profit, from past too

        return max_price
                
                    
        