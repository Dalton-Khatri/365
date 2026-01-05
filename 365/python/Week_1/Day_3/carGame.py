command=""
started=False
while True:
    command=input("->").lower()
    if(command=="start"):
        if started:
            print("Its already on nigga")
        else:
            started=True
            print("Engine Started")
    elif(command=="stop"):
        if not started:
            print("Its already off nigga")
        else:
            started=False
            print("Engine Stopped")
    elif(command=="help"):
        print("Follow the instruction\nType start to start the engine\nType Stop to stop the engine\nType quit to quit\n")
    elif(command=="quit"):
        break
    else:
        print("Sorry I dont understand")