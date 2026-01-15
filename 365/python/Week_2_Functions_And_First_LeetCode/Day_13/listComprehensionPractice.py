num=[1,2,3,4,5,6,7,8,9]

#squares
num_1=[n*n for n in num]
print(num_1)

#even numbers
num_2=[n for n in num if n%2==0]
print(num_2)

#string operations
list = ["hello", "world", "python"]
list_1 = [string.upper() for string in list]
print(list_1)

#Number Filtering
nums=[10, -5, 3, -8, 15, -2, 7]
num_3=[n for n in nums if n>=0]
print(num_3)

#Nested Lists
matrix= [[1,2,3], [4,5,6], [7,8,9]]
list = [n for row in matrix for n in row]
print(list)