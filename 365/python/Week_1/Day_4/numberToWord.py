numbers= {
    "1": "One",
    "2": "Two",
    "3": "Three",
    "4": "Four",
    "5": "Five",
    "6": "Six",
    "7": "Seven",
    "8": "Eight",
    "9": "Nine",
    "10": "Ten"
}

in_number = input('Enter your number: ')
output = ""
for i in in_number:
    output += numbers.get(i)+" "
print(output)
