students={}

while True:
    choice = int(input("Enter '1' for adding student\nEnter '2' for viewing marks\nEnter '3' for Exit\n"))

    if(choice==1):
        name, marks=input("Enter your name and marks seperated by comma").split(",")
        name= name.strip()
        marks = int(marks)
        students[name]=marks

        with open("student.txt","a") as f:
            for name, marks in students.items():
                f.write(f"{name},{marks}\n")
        print("Data Stored !!! \n")

    elif(choice==2):
        if not students:
            print("No Data!!! \n ")
        else:
            for name in students:
               print(f"{name},{students[name]}")
    
    elif(choice==3):
        break




            