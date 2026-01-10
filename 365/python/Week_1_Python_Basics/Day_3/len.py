name= input('Enter your name: ')
if(len(name)<3):
    print('Name must be at least 30 character')
elif(len(name)>50):
    print('The maximum limit reached, write a smaller one')
else:
    print('Name looks good!!')
