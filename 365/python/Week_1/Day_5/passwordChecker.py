password=input("Enter your password")
length_ok= len(password)>8
has_digit= any(char.isdigit() for char in password)
has_special = any(char in '!@#$%^&*' for char in password)

score= length_ok+has_digit+has_special

if score==3:
    print("Strong Password")
elif score ==2:
    print("Medium strength")
else:
    print("Weak Password!")
