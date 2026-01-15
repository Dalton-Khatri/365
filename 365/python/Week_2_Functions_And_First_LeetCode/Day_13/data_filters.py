numbers=[]
strings =[]

def filter_positive():
    return list(filter(lambda x : x>=0,numbers))

def filter_by_length():
    return list(filter(lambda str: len(str)<10,strings))

def filter_divisible(divisor):

    return list(filter(lambda num: num % divisor==0, numbers))

total=int(input("Enter the number of element in list"))
divisor=int(input("Enter your divisor"))
for i in range(total):
    num=int(input("Enter your number: "))
    numbers.append(num)
print(f"The list of positive numbers are: {filter_positive()}\n")

total=int(input("Enter the number of element in string list: "))
for i in range(total):
    num=input("Enter your string: ")
    strings.append(num)
print(f"The list of string less than 10 are {filter_by_length()}\n")

print(f"The numbers which are divisible by {divisor} are {filter_divisible(divisor)}\n")





