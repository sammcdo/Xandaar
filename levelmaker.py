"""Make a basic level."""
import os, time, json

num = input("Enter the level number: ")

if os.path.isdir("xanlevels/"+num):
    choice = input("Do you want to overwrite this level? (yes/no) ")
    if choice == "yes":
        pass
    else:
        timenow = time.localtime()
        num += " ("+str(timenow.tm_mon)+"-"+str(timenow.tm_mday)+"-"+str(timenow.tm_year)+" "+str(timenow.tm_hour)+":"+str(timenow.tm_min)+")"
        print(num)
else:
    os.mkdir("xanlevels/"+num)

length = input("How long do you want the level to be? ")
with open("xanlevels/"+num+"/enemies.txt", 'w') as obj:
    enemies = []
    for i in range(0,12):
        enemies.extend([[0]*int(length)])
    json.dump(enemies, obj)