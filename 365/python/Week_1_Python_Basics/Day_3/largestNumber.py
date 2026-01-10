list = [1,2,34,67,99,101,22]
i=1
largest = list[0]
for i in list:
    if(i>largest):
        largest=i
print(f"The largest number is {largest}")