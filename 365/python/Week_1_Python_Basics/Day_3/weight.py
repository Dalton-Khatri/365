weight= int(input('Your Weight: '))
unit=input('Converting to which? L for Lbs and K for Kg: ')
if unit.lower()=="k":
    converted = weight *0.45
    print(f"Your are {converted} kilos")
else:
    converted = weight /0.45
    print(f"You are {converted} lbs")
    