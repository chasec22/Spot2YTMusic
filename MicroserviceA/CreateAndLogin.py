from getpass import getpass

# Get all the current account stored in your texr file
def getCurrAccounts():
    filename = "login.txt" # Change filename to whatever your text file that holds user info is called
    accounts = []
    with open(filename) as file:
        accounts = [account.rstrip() for account in file]
        
    accountNPass = []
    for item in accounts:
        accountNPass.extend(item.split())
        
    return accountNPass

# even odd checker
def isEven(i):
    if i % 2 == 0: return True
    else: return False

# Takes the info of the new user and puts it into a txt file
def pasteToTxt(pas, user):
    filename = "login.txt" # Change filename for whatever your file is called
    file = open(filename, "a")
    file.write(user + " " + pas + "\n")
    file.close
    
# Checks to see if the user 
def checkUser(user, pas):
    accountsNPass = getCurrAccounts()
    usernames, passwords, count1, count2 = [],[],0,0
    for y in range(0,len(accountsNPass)):
        if isEven(y) == True:
            usernames.append(accountsNPass[y])
            count1 += 1
        else:
            passwords.append(accountsNPass[y])
            count2 +=1
       
    pasFoun = False     
    for x in range(0, len(usernames)):
        if usernames[x] == user:
            if passwords[x] == pas:
                pasFoun = True
        
    if pasFoun == False:
        return 102 #Error Code
    
    else:
        return 101
    
# This is the function to create an account and add it to the text file
def CreateA():
    x = False
    accountsNPass = getCurrAccounts()
    usernames, passwords, count1, count2 = [],[],0,0
    for y in range(0,len(accountsNPass)):
        if isEven(y) == True:
            usernames.append(accountsNPass[y])
            count1 += 1
        else:
            passwords.append(accountsNPass[y])
            count2 +=1
    
    print(usernames + passwords)
        
        
    while x == False:
        username = input("What would you like your username to be? No spaces, between 5-14 characters, and it cant already be in our system \n")
        x = True
        if 15 < len(username) or len(username) < 5:
            x = False
        for item in usernames:
            if item == username:
                x = False
        for item in username:
            if item == " ":
                x = False
        
        if x == False:
            print("There was an error with your input. Make sure your username is between 5-15 characters, has no spaces, and isnt already in our system \n")
        
    
    print("Succesfully created account with " + username + " as your username")
    x = False
    
    while x == False:
        print("What would you like your password to be? Make sure your username is between 5-15 charcters and has no spaces")
        password = getpass()
        x = True
        if 15 < len(password) or len(password) < 4:
            x = False
        for item in password:
            if item == " ":
                x = False
        
        if x == False:
            print("There was an error with your input. Make sure your password is between 5-14 characters and has no spaces \n")
        
    print(password)
    pasteToTxt(password, username)


# Example test function of getting info from a text file. 
def exampleFunc(user):
    with open("info.txt") as file: # Change filename to whatever your text file is called. 
        accounts = [account.rstrip() for account in file]
    
    temp = []
    for item in accounts:
        temp.append(item.split("-"))
    
    for item in temp:
        if item[0] == user:
            print(item[1])

# Example of a function that would choose 
def chooseFunc(input):
    testUser, testPword = "ChaseC", "54321"
    if input == 1:
        CreateA()
    if input == 2:
        err = checkUser(testUser, testPword)
        if err == 102:
            print("Error with your input, please try again and remember the system is case sensitive.")
        elif err == 101:
            print("success")
            exampleFunc(testUser)
            
    

if __name__ == "__main__":
    chooseFunc(2)