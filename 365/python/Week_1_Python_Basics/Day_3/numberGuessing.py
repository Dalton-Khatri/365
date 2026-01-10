import random

secret_number=random.randint(1,100)
print("-----Guess The Number(1-100)---------\n")
print("You only have 5 chances to guess the number\n\n")
attempt=1
while(attempt<=5):
    your_guess= int(input("Enter your Guess: "))
    if(your_guess==secret_number):
        print("You are correct.... BINGOOooo..\n")
        break
    elif(your_guess>secret_number):
        print("Too high!!!")
    elif(your_guess<secret_number):
        print("Too low!!!")
    attempt+=1
if(attempt>5):
    print("You Failed")

