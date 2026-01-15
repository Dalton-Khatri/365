numbers=[1,2,3,4,5,6,7,8,9,10]
strings=["Dalton", "Khatri", "Bouddhha","123"]
multiplier= 10
def square_all(numbers):
    return list(map(lambda x: x**2,numbers))

def to_uppercase(strings):
    return list(map(lambda str:str.upper(),strings))

def multiply_by(numbers, multiplier):
    return list(map(lambda x:x*multiplier, numbers))

print(f"The list of squares: {square_all(numbers)}\n")
print(f"The strings in uppercase: {to_uppercase(strings)}\n")
print(f"The list of numbers multiplied are: {multiply_by(numbers,multiplier)}")
