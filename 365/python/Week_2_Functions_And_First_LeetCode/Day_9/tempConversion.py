def c_to_f(c):
    return c * 9/5 + 32
def f_to_c(f):
    return (f - 32) * 5/9
def c_to_k(c):
    return c + 273.15
def k_to_c(k):
    return k - 273.15

temp=int(input('Enter you temperature: '))
choice=input("Enter '1' to conver C->F,\nEnter '2' to conver C->K,\nEnter '3' to conver K->F,\nEnter '4' to conver K->C,\nEnter '5' to conver F->C,\nEnter '6' to conver f->K\n")
if(choice=='1'):
    print(f'Your required temperature is {c_to_f(temp)} ')
elif(choice=='2'):
    print(f'Your required temperature is {c_to_k(temp)} ')
elif(choice=='3'):
    print(f'Your required temperature is {c_to_f(k_to_c(temp))} ')
elif(choice=='4'):
    print(f'Your required temperature is {k_to_c(temp)} ')
elif(choice=='5'):
    print(f'Your required temperature is {f_to_c(temp)} ')
elif(choice=='6'):
    print(f'Your required temperature is {c_to_k(f_to_c(temp))} ')
    