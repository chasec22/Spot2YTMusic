TEST_ACCOUNT = "UserToDelete"
TEST_PASSWORD = "12345"

def deleteAccount(items, acc, pas):
    with open("MicroserviceA/login.txt", "w") as w:
        for item in items:
            if item.strip("/n") != (acc + " " + pas):
                w.write(item)
    
    with open("MicroserviceA/info.txt", "r") as r:
        info = r.readlines()
    
    temp = []
    for item in info:
        temp.append(item.split("-"))
        
    for i in range(0, len(temp)):
        if temp[i][0] == acc:
            accInfo = info[i]
            
    with open("MicroserviceA/info.txt", "w") as w:
        for item in info:
            if item.strip("/n") != accInfo:
                w.write(item)
        

def findAccount(acc, pas):
    with open("MicroserviceA/login.txt", "r") as l:
        userPass = l.readlines()
        
    temp = []
    for item in userPass:
        temp.append(item.split(" "))
    
    users = []
    for i in range(0,len(temp)):
        users.append(temp[i][0])
        
    foun = False
    for i in range(0, len(users)):
        if users[i] == acc and temp[i][1] == pas + "\n":
            foun = True
            deleteAccount(userPass, acc, temp[i][1])
            break
            
    
            
    print(users)
    

if __name__ == "__main__":
    with open("txtFiles/accountToDelete.txt", "r") as r:
        userPass = r.readline()
        
    spli = userPass.split(" ")
    
    findAccount(spli[0], spli[1])