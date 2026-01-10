def addition(a,b):
    return a+b
def substraction(a,b):
    return a-b
def multiplication(a,b):
    return a*b
def divison(a,b):
    if(b==0):
        print("Division not possible")
    else:
        return a/b

n1=int(input('Enter first number for calculation: '))
n2=int(input('Enter second number for calculation: '))
choice=input("Enter '+' for addition, '-' for substration, '/' for division and '*' for multiplication: ")
for ch in choice:
    if(ch=='+'):
        print(f"The sum is {addition(n1,n2)}")
    if(ch=='-'):
        print(f"The sum is {substraction(n1,n2)}")        
    if(ch=='*'):
        print(f"The sum is {multiplication(n1,n2)}")    
    if(ch=='/'):
        print(f"The sum is {divison(n1,n2)}")
