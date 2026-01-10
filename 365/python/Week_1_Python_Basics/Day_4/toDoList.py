tasks=[]
while True:
    print('------TO-DO LIST------\n')
    choice= input("Enter '1' to Add Task\nEnter '2' to view task\nEnter '3' to mark a task as done\nEnter '4' to exit\n")
    if(choice=="1"):
        task=input("Enter your task: ")
        tasks.append({"task":task , "done": False})
        print("Task Added! \n")

    elif(choice=="2"):
        if not tasks:
            print("No tasks to do!!! \n")
        else:
            for i, task in enumerate(tasks,1):
                status= "✓" if task["done"] else "x"
                print(f"{i}. [{status}] {task["task"]}\n")
    
    elif(choice=="3"):
        if not tasks:
            print("No tasks to do!!!\n")
        else:
            done_num=int(input("Enter your task number"))
            tasks[done_num-1]["done"]=True
            print("Mark as done!!!\n")

    elif(choice=="4"):
        print("You are out of the process\n")
        break

